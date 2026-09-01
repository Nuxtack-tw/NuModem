# -*- coding: utf-8 -*-
"""向路由器「請求臨時通道」的三種標準協定探測器 —— 純標準函式庫。

背景：NuModem 要給一般消費者用，不能叫他們登入路由器設 port forwarding。
業界標準做法是由程式自己向路由器要一個「有期限的」對外埠，時間到自動收回：

  1. UPnP IGD   （2001，SSDP 多播找裝置 → SOAP AddPortMapping）
  2. NAT-PMP    （Apple，RFC 6886，單播 UDP gw:5351）
  3. PCP        （RFC 6887，NAT-PMP 的後繼者，同樣 gw:5351）

為什麼 UPnP 失敗不代表沒救：UPnP 探索走**多播** 239.255.255.250:1900，
回應卻是從「路由器的 IP」單播回來 —— 來源位址跟我們送出去的目的位址不同，
Windows 防火牆的 UDP 狀態追蹤預設會把它當成**未經請求的入站封包丟掉**。
NAT-PMP／PCP 是純單播（送 gw:5351、收 gw:5351），狀態追蹤對得起來，
不會踩到這個坑。所以 UPnP 沒反應時，NAT-PMP／PCP 仍值得一試。

用法：
    python tools/nat_probe.py            # 只探測，不改任何設定
    python tools/nat_probe.py --map 5000 # 探測成功就實際要一個 5000 埠（1 小時期限）
"""
import argparse
import os
import re
import socket
import struct
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PCP_PORT = 5351          # NAT-PMP 與 PCP 共用同一個埠
NATPMP_RESULT = {
    0: '成功', 1: '不支援的版本', 2: '拒絕（功能被關閉）',
    3: '網路故障', 4: '資源不足', 5: '不支援的 opcode',
}
PCP_RESULT = {
    0: '成功', 1: '不支援的版本', 2: '沒有權限（功能被關閉）',
    3: '格式錯誤', 4: '不支援的 opcode', 5: '不支援的選項',
    6: '選項格式錯誤', 7: '對外位址不是本機', 8: '網路故障',
    9: '資源不足', 10: '不支援的協定', 11: '超過使用者配額',
    12: '無法配置指定的對外埠', 13: '位址不匹配', 14: '超出範圍',
}


# ── 找預設閘道 ──────────────────────────────────────────────
def default_gateways():
    """從 route print 撈 IPv4 預設閘道；撈不到就用各網段的 .1 猜。"""
    gws = []
    try:
        out = subprocess.run(['route', 'print', '-4'], capture_output=True,
                             timeout=10).stdout.decode('utf-8', 'ignore')
        for m in re.finditer(r'^\s*0\.0\.0\.0\s+0\.0\.0\.0\s+(\S+)\s+(\S+)',
                             out, re.M):
            gw, iface = m.group(1), m.group(2)
            if gw not in ('0.0.0.0', 'On-link') and gw not in [g[0] for g in gws]:
                gws.append((gw, iface))
    except Exception:
        pass
    if not gws:                       # 退路：每個私網網段猜 .1
        for ip in local_ipv4s():
            guess = ip.rsplit('.', 1)[0] + '.1'
            if guess != ip and guess not in [g[0] for g in gws]:
                gws.append((guess, ip))
    return gws


def local_ipv4s():
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ips.append(s.getsockname()[0])
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
    return ips


def src_ip_towards(gw):
    """問作業系統：要送到這個閘道，會用哪張網卡的 IP 當來源。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw, PCP_PORT))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def _udp_ask(gw, payload, timeout=2.0, tries=2):
    """單播 UDP 問一句、等回應。NAT-PMP／PCP 都是這個模式。"""
    for _ in range(tries):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        try:
            s.sendto(payload, (gw, PCP_PORT))
            data, _addr = s.recvfrom(1100)
            return data
        except socket.timeout:
            continue
        except Exception:
            return None
        finally:
            s.close()
    return None


# ── NAT-PMP（RFC 6886）────────────────────────────────────
def natpmp_external_ip(gw):
    r = _udp_ask(gw, struct.pack('!BB', 0, 0))       # 版本 0、opcode 0
    if not r or len(r) < 12:
        return None, '無回應'
    ver, op, res = struct.unpack('!BBH', r[:4])
    if op != 128:
        return None, 'opcode 非預期（%d）' % op
    if res != 0:
        return None, NATPMP_RESULT.get(res, '錯誤碼 %d' % res)
    return socket.inet_ntoa(r[8:12]), None


def natpmp_map(gw, int_port, ext_port, lifetime=3600):
    """opcode 2 = TCP。lifetime 就是「臨時」的本體 —— 秒數到了自動撤銷。"""
    req = struct.pack('!BBHHHI', 0, 2, 0, int_port, ext_port, lifetime)
    r = _udp_ask(gw, req, timeout=3.0)
    if not r or len(r) < 16:
        return None, '無回應'
    ver, op, res = struct.unpack('!BBH', r[:4])
    if res != 0:
        return None, NATPMP_RESULT.get(res, '錯誤碼 %d' % res)
    _ipport, mapped, life = struct.unpack('!HHI', r[8:16])
    return (mapped, life), None


# ── PCP（RFC 6887）─────────────────────────────────────────
def _v4mapped(ip):
    return b'\x00' * 10 + b'\xff\xff' + socket.inet_aton(ip)


def pcp_announce(gw, my_ip):
    """opcode 0 = ANNOUNCE，最輕量的「你在嗎」。"""
    req = struct.pack('!BBHI', 2, 0, 0, 0) + _v4mapped(my_ip)
    r = _udp_ask(gw, req)
    if not r or len(r) < 24:
        return None, '無回應'
    ver, op_r, _rsv, res = struct.unpack('!BBBB', r[:4])
    if not (op_r & 0x80):
        return None, '不是回應封包'
    if res != 0:
        return None, PCP_RESULT.get(res, '錯誤碼 %d' % res)
    return True, None


def pcp_map(gw, my_ip, int_port, ext_port, lifetime=3600):
    nonce = os.urandom(12)
    hdr = struct.pack('!BBHI', 2, 1, 0, lifetime) + _v4mapped(my_ip)
    body = (nonce + struct.pack('!B', 6) + b'\x00' * 3
            + struct.pack('!HH', int_port, ext_port) + _v4mapped('0.0.0.0'))
    r = _udp_ask(gw, hdr + body, timeout=3.0)
    if not r or len(r) < 60:
        return None, '無回應'
    ver, op_r, _rsv, res = struct.unpack('!BBBB', r[:4])
    if res != 0:
        return None, PCP_RESULT.get(res, '錯誤碼 %d' % res)
    life = struct.unpack('!I', r[4:8])[0]
    mapped = struct.unpack('!H', r[42:44])[0]
    ext = socket.inet_ntoa(r[56:60])
    return (mapped, ext, life), None


# ── UPnP 直連探測（繞過多播，判斷是「路由器沒開」還是「多播被擋」）──
UPNP_PORTS = [1900, 5000, 49152, 49153, 49154, 2869, 5431, 80, 8080, 1780, 1990]
UPNP_PATHS = ['/rootDesc.xml', '/description.xml', '/igd.xml', '/gatedesc.xml',
              '/DeviceDescription.xml', '/upnp/BasicDevice.xml', '/']


def upnp_direct(gw):
    """直接對閘道的常見 UPnP 埠抓裝置描述 XML。抓得到 = UPnP 有開，
    只是多播探索被防火牆吃了；完全抓不到 = 路由器根本沒開 UPnP。"""
    hits = []
    for port in UPNP_PORTS:
        s = socket.socket()
        s.settimeout(0.6)
        try:
            s.connect((gw, port))
        except Exception:
            continue
        finally:
            s.close()
        for path in UPNP_PATHS:
            url = 'http://%s:%d%s' % (gw, port, path)
            try:
                body = urllib.request.urlopen(url, timeout=3).read(20000)
            except Exception:
                continue
            if b'InternetGatewayDevice' in body:
                hits.append(url)
                break
            if b'<deviceType>' in body and b'urn:schemas-upnp-org' in body:
                hits.append(url + '（UPnP 但非 IGD）')
                break
    return hits


def main():
    p = argparse.ArgumentParser(description='NAT-PMP／PCP／UPnP 路由器臨時開埠探測')
    p.add_argument('--map', type=int, default=0,
                   help='探測成功就實際申請這個埠（1 小時期限）')
    p.add_argument('--lifetime', type=int, default=3600, help='通道期限秒數')
    a = p.parse_args()

    gws = default_gateways()
    if not gws:
        print('找不到預設閘道，無法探測。')
        return 1
    print('=' * 68)
    print(' 路由器臨時通道探測（不會改任何持久設定）')
    print('=' * 68)

    ok_any = False
    for gw, iface in gws:
        my_ip = src_ip_towards(gw) or iface
        print('\n▶ 閘道 %s（本機來源 IP %s）' % (gw, my_ip))

        ip, err = natpmp_external_ip(gw)
        if ip:
            ok_any = True
            print('  ✔ NAT-PMP 可用 —— 路由器回報對外 IP：%s' % ip)
            if a.map:
                r, e2 = natpmp_map(gw, a.map, a.map, a.lifetime)
                if r:
                    print('    ✔ 已開通 %s:%d → 本機 %d，期限 %d 秒'
                          % (ip, r[0], a.map, r[1]))
                else:
                    print('    ✘ 開埠失敗：%s' % e2)
        else:
            print('  ✘ NAT-PMP：%s' % err)

        okp, err = pcp_announce(gw, my_ip)
        if okp:
            ok_any = True
            print('  ✔ PCP 可用（ANNOUNCE 有回應）')
            if a.map:
                r, e2 = pcp_map(gw, my_ip, a.map, a.map, a.lifetime)
                if r:
                    print('    ✔ 已開通 %s:%d → 本機 %d，期限 %d 秒'
                          % (r[1], r[0], a.map, r[2]))
                else:
                    print('    ✘ 開埠失敗：%s' % e2)
        else:
            print('  ✘ PCP：%s' % err)

        hits = upnp_direct(gw)
        if hits:
            ok_any = True
            print('  ✔ UPnP 直連找到裝置描述（代表多播被防火牆擋，不是路由器沒開）：')
            for h in hits:
                print('      %s' % h)
        else:
            print('  ✘ UPnP：閘道常見埠上找不到裝置描述 → 路由器沒開 UPnP')

    print()
    if not ok_any:
        print('結論：這台路由器三種協定全不支援／全關閉，程式無法自動開埠。')
        print('      消費者情境請改走「模組主動外連公開伺服器」的方向。')
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
