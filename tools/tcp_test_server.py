#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NuModem P2 測試用 TCP 伺服器 —— 收 EG800K 送來的資料並原樣回送（echo）。

用途：P2「TCP socket 收發」需要一台看得見、控制得了的對端。公開 echo 服務
（tcpbin.com）雖然能用，但看不到對方實際收到什麼、也無法製造異常情境。

用法：
    python tools/tcp_test_server.py                # 預設 0.0.0.0:5000，echo 模式
    python tools/tcp_test_server.py --port 6000
    python tools/tcp_test_server.py --no-echo      # 只收不回（測單向）
    python tools/tcp_test_server.py --send-on-connect "hello\\r\\n"   # 連上就主動推
    python tools/tcp_test_server.py --drop-after 3 # 收到 3 筆後主動斷線（測 +QIURC: "closed"）

輸出每一筆資料的時間、來源、長度、ASCII 與 HEX —— 用來比對模組送出的位元組
是否與 AT+QISENDEX 的 hex 字串完全一致（P2-3／P2-4 的驗收重點）。
"""
import argparse
import datetime
import socket
import socketserver
import sys
import threading

# Windows 主控台預設 cp950，中文與特殊符號會炸；統一改 UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARGS = None
_lock = threading.Lock()
_stats = {'conns': 0, 'rx_bytes': 0, 'tx_bytes': 0, 'packets': 0}


def ts():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]


def dump(data):
    """回傳 (可讀 ASCII, HEX 字串)。控制字元以 . 代替，方便一眼看出 CR/LF。"""
    ascii_ = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)
    hex_ = ' '.join('%02X' % b for b in data)
    return ascii_, hex_


def log(msg):
    with _lock:
        print('[%s] %s' % (ts(), msg), flush=True)


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        peer = '%s:%d' % self.client_address
        with _lock:
            _stats['conns'] += 1
        log('◆ 連線建立 ← %s' % peer)

        if ARGS.send_on_connect:
            payload = ARGS.send_on_connect.encode('utf-8', 'replace') \
                .decode('unicode_escape').encode('latin-1')
            self.request.sendall(payload)
            with _lock:
                _stats['tx_bytes'] += len(payload)
            a, h = dump(payload)
            log('  → 主動推送 %d bytes | %s | %s' % (len(payload), a, h))

        count = 0
        try:
            while True:
                data = self.request.recv(4096)
                if not data:
                    break
                count += 1
                with _lock:
                    _stats['rx_bytes'] += len(data)
                    _stats['packets'] += 1
                a, h = dump(data)
                log('  ← 收到 %d bytes | %s | %s' % (len(data), a, h))

                if ARGS.echo:
                    self.request.sendall(data)
                    with _lock:
                        _stats['tx_bytes'] += len(data)
                    log('  → 回送 %d bytes（echo）' % len(data))

                if ARGS.drop_after and count >= ARGS.drop_after:
                    log('  ✂ 已收 %d 筆，主動斷線（模組端應收到 +QIURC: "closed"）' % count)
                    break
        except ConnectionResetError:
            log('  ⚠ 對端重置連線（RST）')
        except Exception as e:
            log('  ⚠ 例外：%r' % e)
        finally:
            log('◆ 連線結束 ← %s（本次 %d 筆）' % (peer, count))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def local_ips():
    """列出本機各介面的 IPv4，方便判斷同網段測試時該連哪個。"""
    ips = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ips.add(info[4][0])
    except Exception:
        pass
    try:                      # 不會真的送出封包，只是問作業系統會走哪張網卡
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return sorted(ips)


def public_ip():
    """查目前對外看到的公網 IP —— 家用寬頻的 IP 會變，每次測試前直接顯示省得手動查。"""
    import urllib.request
    for url in ('https://api.ipify.org', 'https://ifconfig.me/ip'):
        try:
            return urllib.request.urlopen(url, timeout=6).read().decode().strip()
        except Exception:
            continue
    return None


def main():
    global ARGS
    p = argparse.ArgumentParser(description='NuModem P2 測試用 TCP echo 伺服器')
    p.add_argument('--host', default='0.0.0.0', help='監聽位址（預設 0.0.0.0＝所有介面）')
    p.add_argument('--port', type=int, default=5000, help='監聽埠（預設 5000）')
    p.add_argument('--no-echo', dest='echo', action='store_false', help='只收不回送')
    p.add_argument('--send-on-connect', default='', help='連線建立就主動送出的字串（支援 \\r\\n）')
    p.add_argument('--drop-after', type=int, default=0, help='收到 N 筆後主動斷線（測 closed URC）')
    ARGS = p.parse_args()

    srv = Server((ARGS.host, ARGS.port), Handler)
    pub = public_ip()
    print('=' * 72)
    print(' NuModem P2 TCP 測試伺服器   監聽 %s:%d   echo=%s'
          % (ARGS.host, ARGS.port, '開' if ARGS.echo else '關'))
    print(' 本機 IPv4：%s' % ('、'.join(local_ips()) or '（查不到）'))
    if pub:
        print(' 目前公網 IP：%s   ← 路由器要把 %d 埠轉到本機' % (pub, ARGS.port))
        print()
        print(' 模組端指令（轉埠設好後直接複製貼上）：')
        print('   AT+QIOPEN=1,0,"TCP","%s",%d,0,0' % (pub, ARGS.port))
    else:
        print(' 公網 IP 查詢失敗（離線？）—— 手動查一次再填進 AT+QIOPEN')
    print()
    print(' 設定方式（轉埠／通道／VPS 三種）見 reports/tcp-server-setup.md')
    print(' Ctrl+C 結束')
    print('=' * 72)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print()
        log('收工。統計：連線 %d 次／封包 %d 筆／收 %d bytes／送 %d bytes'
            % (_stats['conns'], _stats['packets'], _stats['rx_bytes'], _stats['tx_bytes']))
    finally:
        srv.shutdown()


if __name__ == '__main__':
    main()
