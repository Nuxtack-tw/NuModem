# -*- coding: utf-8 -*-
r"""把 NuModem 終端機的掃描結果丟給網路定位服務，回推位置。

QuecLocator（AT+QLBS）卡在要向 Quectel 申請 token（2026-08-07 起），
這支就是替代路線：模組只負責掃描（零數據流量），查詢由 PC 端發出。

用法：
    1. 在 NuModem 執行 AT+QWIFISCAN=15000,2,10,5,0 與 AT+QENG="servingcell"
    2. 把終端機輸出（含 +QWIFISCAN: 與 +QENG: 行）存成文字檔，或直接用剪貼簿
    3. python tools/wifi_geolocate.py scan.txt
       python tools/wifi_geolocate.py scan.txt --provider unwiredlabs --key <API金鑰>
       python tools/wifi_geolocate.py scan.txt --truth 25.0338,121.5645     # 有真值就順便算誤差

服務供應商（--provider）：
    beacondb     免金鑰（預設）。MLS 停服後的社群接棒資料庫（公有領域）。
                 2026-08-29 實測：基地台命中（誤差 632 m）、Wi-Fi 在本區無涵蓋
    unwiredlabs  需 --key。免費方案每日約 100 次查詢，註冊即用
    google       需 --key（要啟用帳單的 Geolocation API 金鑰）。Wi-Fi 資料庫最完整

誠實量測的兩個開關（都已內建，不用另外設）：
    - IP 退位一律關閉 —— 不關的話服務會拿「發查詢這台 PC 的 IP」推位置，
      測到的是 ISP 機房不是 Wi-Fi 定位
    - 本地管理位址（第一個位元組 0x02 位元為 1，如 C2:/62:/9E: 開頭）標示但仍送出，
      服務端自己會忽略；用 --strict 可在本機先剔除

⚠ 送出查詢等於把你的 AP MAC 與基地台資訊交給第三方服務。
⚠ 別把含真實座標的掃描檔提交進版控（.gitignore 已有 scan*.txt 的話除外，自行確認）。
"""
import argparse
import io
import json
import math
import re
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')   # SystemExit 訊息走 stderr，cp950 主控台會亂碼

RE_WIFI = re.compile(r'\+QWIFISCAN:\s*\([^)]*?(-?\d+)\s*,\s*"([0-9A-Fa-f:]{17})"\s*,\s*(\d+)\)')
RE_CELL = re.compile(
    r'\+QENG:\s*"servingcell","[^"]*","LTE","[A-Z]+",'
    r'(\d+),(\d+),([0-9A-Fa-f]+),\d+,\d+,\d+,\d+,\d+,([0-9A-Fa-f]+),(-?\d+)')


def is_local_admin(mac):
    """本地管理位址：第一個位元組的 0x02 位元為 1（多 SSID 虛擬 BSSID／隨機化位址）。"""
    return bool(int(mac.split(':')[0], 16) & 0x02)


def parse(text):
    wifi, seen = [], set()
    for rssi, mac, _ch in RE_WIFI.findall(text):
        mac = mac.upper()
        if mac not in seen:
            seen.add(mac)
            wifi.append({'macAddress': mac, 'signalStrength': int(rssi)})
    cell = None
    m = RE_CELL.search(text)
    if m:
        mcc, mnc, eci_hex, tac_hex, rsrp = m.groups()
        cell = {'radioType': 'lte', 'mobileCountryCode': int(mcc),
                'mobileNetworkCode': int(mnc),
                'locationAreaCode': int(tac_hex, 16),   # ⚠ QENG 給的是十六進位
                'cellId': int(eci_hex, 16),
                'signalStrength': int(rsrp)}
    return wifi, cell


def haversine(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0]); dl = math.radians(b[1] - a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))


def build_request(provider, key, wifi, cell):
    if provider == 'beacondb':
        url = 'https://api.beacondb.net/v1/geolocate'
        body = {'fallbacks': {'lacf': True, 'ipf': False}}
        if wifi: body['wifiAccessPoints'] = wifi
        if cell: body['cellTowers'] = [cell]
        return url, body
    if provider == 'google':
        if not key: raise SystemExit('google 需要 --key（Geolocation API）')
        url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + key
        body = {'considerIp': False}
        if wifi: body['wifiAccessPoints'] = wifi
        if cell: body['cellTowers'] = [cell]
        return url, body
    if provider == 'unwiredlabs':
        if not key: raise SystemExit('unwiredlabs 需要 --key')
        url = 'https://us1.unwiredlabs.com/v2/process'
        body = {'token': key, 'address': 0, 'fallbacks': ['lacf']}
        if wifi:
            body['wifi'] = [{'bssid': w['macAddress'], 'signal': w['signalStrength']} for w in wifi]
        if cell:
            body['radio'] = 'lte'
            body['cells'] = [{'lac': cell['locationAreaCode'], 'cid': cell['cellId'],
                              'mcc': cell['mobileCountryCode'], 'mnc': cell['mobileNetworkCode'],
                              'signal': cell['signalStrength']}]
        return url, body
    raise SystemExit('不認識的 provider：%s' % provider)


def main():
    ap = argparse.ArgumentParser(description='NuModem 掃描結果 → 網路定位')
    ap.add_argument('scanfile', help='含 +QWIFISCAN:/+QENG: 行的文字檔（- 讀 stdin）')
    ap.add_argument('--provider', default='beacondb',
                    choices=['beacondb', 'unwiredlabs', 'google'])
    ap.add_argument('--key', default=None, help='API 金鑰（beacondb 不用）')
    ap.add_argument('--mode', default='auto', choices=['auto', 'wifi', 'cell'],
                    help='auto=都送；wifi/cell=只送其中一種（做對照實驗用）')
    ap.add_argument('--strict', action='store_true', help='本機先剔除本地管理位址')
    ap.add_argument('--truth', default=None, help='真值座標 lat,lon（有就算實際誤差）')
    a = ap.parse_args()

    text = sys.stdin.read() if a.scanfile == '-' else io.open(a.scanfile, encoding='utf-8').read()
    wifi, cell = parse(text)
    la = [w['macAddress'] for w in wifi if is_local_admin(w['macAddress'])]
    if a.strict:
        wifi = [w for w in wifi if w['macAddress'] not in la]

    print('解析：Wi-Fi %d 顆（本地管理位址 %d 顆%s）、基地台 %s'
          % (len(wifi) + (len(la) if a.strict else 0), len(la),
             '，已剔除' if a.strict and la else '', '有' if cell else '無'))
    if cell:
        print('  cell：MCC %d / MNC %d / TAC %d / ECI %d（十六進位已轉）'
              % (cell['mobileCountryCode'], cell['mobileNetworkCode'],
                 cell['locationAreaCode'], cell['cellId']))
    if a.mode == 'wifi': cell = None
    if a.mode == 'cell': wifi = []
    if not wifi and not cell:
        raise SystemExit('沒有可用素材 —— 檔案裡有 +QWIFISCAN: / +QENG: 行嗎？')

    url, body = build_request(a.provider, a.key, wifi, cell)
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json',
                                          'User-Agent': 'NuModem-EG800/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            res = json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors='replace')[:300]
        if e.code == 404:
            raise SystemExit('查無位置（404）—— 資料庫沒有這些 AP／基地台的記錄。\n%s' % detail)
        raise SystemExit('HTTP %d：%s' % (e.code, detail))

    # unwiredlabs 的回應鍵不同（lat/lon/accuracy 在頂層），錯誤也走 HTTP 200
    if a.provider == 'unwiredlabs':
        if res.get('status') == 'error':
            # 實例（2026-08-29）：免費方案回 "WiFi access not enabled" —— Wi-Fi 定位
            # 不在該帳號的方案裡；balance 是剩餘查詢額度，見報告 8-29 節
            raise SystemExit('unwiredlabs 回錯誤：%s（剩餘額度 balance=%s）'
                             % (res.get('message'), res.get('balance')))
        lat, lon, acc = res.get('lat'), res.get('lon'), res.get('accuracy')
    else:
        loc = res.get('location', {})
        lat, lon, acc = loc.get('lat'), loc.get('lng'), res.get('accuracy')
    if lat is None:
        raise SystemExit('回應解析不到座標：%s' % json.dumps(res)[:300])

    print('\n位置：%.5f, %.5f　服務回報精度 ±%.0f m' % (lat, lon, float(acc or 0)))
    print('地圖：https://www.openstreetmap.org/?mlat=%.5f&mlon=%.5f#map=17/%.5f/%.5f'
          % (lat, lon, lat, lon))
    if a.truth:
        t = tuple(float(x) for x in a.truth.split(','))
        print('與真值的實際誤差：%.0f m' % haversine((lat, lon), t))


if __name__ == '__main__':
    main()
