# -*- coding: utf-8 -*-
"""UPnP IGD 自動連接埠對應 —— 純標準函式庫，不需 pip install。

為什麼要有這個：NuModem 是給一般消費者用的，不能要求他們自己登入路由器設
port forwarding。多數家用路由器**出廠就開著 UPnP**，程式可以自己開口要一個埠
（BitTorrent／遊戲主機／視訊軟體都是這樣做的），使用者完全不必動手。

流程：SSDP 多播找到 IGD → 取裝置描述 XML → 找 WANIPConnection/WANPPPConnection
的 controlURL → SOAP AddPortMapping。離開時記得 DeletePortMapping 收乾淨。
"""
import re
import socket
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SSDP_ADDR = ('239.255.255.250', 1900)
ST_LIST = [
    'urn:schemas-upnp-org:device:InternetGatewayDevice:1',
    'urn:schemas-upnp-org:service:WANIPConnection:1',
    'urn:schemas-upnp-org:service:WANPPPConnection:1',
    'upnp:rootdevice',
]
SVC_TYPES = [
    'urn:schemas-upnp-org:service:WANIPConnection:1',
    'urn:schemas-upnp-org:service:WANPPPConnection:1',
]


def _local_ipv4s():
    """列出本機所有 IPv4。多網卡機器（VM／WSL／多網段）必須逐張試，
    否則 SSDP 多播會從預設路由那張送出去，找不到實際接路由器的那張。"""
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ips.append(s.getsockname()[0])       # 預設路由那張優先試
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip not in ips and not ip.startswith('127.'):
                ips.append(ip)
    except Exception:
        pass
    ips.append('0.0.0.0')                    # 最後再讓作業系統自己挑
    return ips


def _search_from(bind_ip, st, timeout):
    msg = ('M-SEARCH * HTTP/1.1\r\n'
           'HOST: %s:%d\r\n'
           'MAN: "ssdp:discover"\r\n'
           'MX: 2\r\n'
           'ST: %s\r\n\r\n' % (SSDP_ADDR[0], SSDP_ADDR[1], st))
    out = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((bind_ip, 0))
        # 指定多播的出口介面，這是多網卡環境的關鍵
        if bind_ip != '0.0.0.0':
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
                         socket.inet_aton(bind_ip))
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        s.settimeout(timeout)
        s.sendto(msg.encode(), SSDP_ADDR)
        while True:
            try:
                data, _ = s.recvfrom(65507)
            except socket.timeout:
                break
            m = re.search(rb'(?i)^LOCATION:\s*(\S+)', data, re.M)
            if m:
                url = m.group(1).decode('ascii', 'ignore')
                if url not in out:
                    out.append(url)
    except Exception:
        pass
    finally:
        s.close()
    return out


def _discover(timeout=2, verbose=False):
    """SSDP M-SEARCH，回傳所有裝置描述 XML 的 URL（去重、保序）。
    逐張網卡 × 逐種 ST 嘗試 —— 找到就停。"""
    found = []
    for ip in _local_ipv4s():
        for st in ST_LIST:
            hits = _search_from(ip, st, timeout)
            if verbose and hits:
                print('  · 從 %s 以 %s 找到 %d 筆' % (ip, st.split(':')[-2], len(hits)))
            for u in hits:
                if u not in found:
                    found.append(u)
            if found:
                return found
    return found


def _strip_ns(tag):
    return tag.split('}', 1)[-1]


def _find_service(desc_url, timeout=5):
    """從裝置描述 XML 裡挖出 WAN 連線服務的 controlURL 與 serviceType。"""
    try:
        xml = urllib.request.urlopen(desc_url, timeout=timeout).read()
    except Exception:
        return None
    try:
        root = ET.fromstring(xml)
    except Exception:
        return None
    for svc in root.iter():
        if _strip_ns(svc.tag) != 'service':
            continue
        kv = {_strip_ns(c.tag): (c.text or '') for c in svc}
        if kv.get('serviceType') in SVC_TYPES and kv.get('controlURL'):
            return {
                'type': kv['serviceType'],
                'control': urllib.parse.urljoin(desc_url, kv['controlURL']),
            }
    return None


def _soap(svc, action, body_xml, timeout=8):
    env = ('<?xml version="1.0"?>'
           '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
           's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>'
           '<u:%s xmlns:u="%s">%s</u:%s></s:Body></s:Envelope>'
           % (action, svc['type'], body_xml, action))
    req = urllib.request.Request(
        svc['control'], data=env.encode('utf-8'),
        headers={'Content-Type': 'text/xml; charset="utf-8"',
                 'SOAPAction': '"%s#%s"' % (svc['type'], action)})
    return urllib.request.urlopen(req, timeout=timeout).read()


def find_gateway():
    """找到可用的 IGD 服務；找不到回 None。"""
    for url in _discover():
        svc = _find_service(url)
        if svc:
            return svc
    return None


def external_ip(svc):
    try:
        r = _soap(svc, 'GetExternalIPAddress', '')
        m = re.search(rb'<NewExternalIPAddress>([^<]*)<', r)
        return m.group(1).decode() if m else None
    except Exception:
        return None


def add_mapping(svc, ext_port, int_ip, int_port, desc='NuModem TCP test', lease=0):
    """要求路由器把 ext_port 轉到 int_ip:int_port。成功回 True。"""
    body = ('<NewRemoteHost></NewRemoteHost>'
            '<NewExternalPort>%d</NewExternalPort>'
            '<NewProtocol>TCP</NewProtocol>'
            '<NewInternalPort>%d</NewInternalPort>'
            '<NewInternalClient>%s</NewInternalClient>'
            '<NewEnabled>1</NewEnabled>'
            '<NewPortMappingDescription>%s</NewPortMappingDescription>'
            '<NewLeaseDuration>%d</NewLeaseDuration>'
            % (ext_port, int_port, int_ip, desc, lease))
    try:
        _soap(svc, 'AddPortMapping', body)
        return True, None
    except urllib.error.HTTPError as e:
        detail = ''
        try:
            raw = e.read().decode('utf-8', 'ignore')
            m = re.search(r'<errorDescription>([^<]*)<', raw)
            code = re.search(r'<errorCode>([^<]*)<', raw)
            detail = '%s%s' % (m.group(1) if m else '',
                               '（碼 %s）' % code.group(1) if code else '')
        except Exception:
            pass
        return False, detail or ('HTTP %s' % e.code)
    except Exception as e:
        return False, repr(e)


def delete_mapping(svc, ext_port):
    body = ('<NewRemoteHost></NewRemoteHost>'
            '<NewExternalPort>%d</NewExternalPort>'
            '<NewProtocol>TCP</NewProtocol>' % ext_port)
    try:
        _soap(svc, 'DeletePortMapping', body)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print('搜尋 UPnP 閘道器…（逐張網卡嘗試）')
    from_ = _discover(verbose=True)
    svc = None
    for u in from_:
        svc = _find_service(u)
        if svc: break
    if not svc and from_:
        print('  找到 %d 個 UPnP 裝置但都不是 IGD：' % len(from_))
        for u in from_[:5]: print('   -', u)
    if not svc:
        print('❌ 找不到 —— 路由器沒開 UPnP，或被防火牆擋掉多播')
        raise SystemExit(1)
    print('✔ 找到：%s' % svc['control'])
    print('  服務型別：%s' % svc['type'])
    print('  路由器回報的外部 IP：%s' % (external_ip(svc) or '（查不到）'))
