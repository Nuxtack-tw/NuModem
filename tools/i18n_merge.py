# -*- coding: utf-8 -*-
"""把翻譯稿合併成瀏覽器要載的 js/i18n/at-<lang>.js，並在合併時把關品質。

**以原文字串為鍵**，不用索引 —— 索引式在原文目錄擴充時會整批錯位（V26.0.60 踩過）。

輸入（後者覆蓋前者）：
  i18n/tr/<lang>.json        原文 -> 譯文（由 tools/i18n_reindex.py 從第一批索引式稿轉出）
  i18n/tr-delta/<lang>.json  index -> 譯文（補譯批；索引對應 i18n/delta-to-translate.json）

會**擋下該語言、不產生輸出檔**的問題：
  · 佔位符 {0}{1}… 的個數或編號與原文不符 —— 執行期會印出錯的數值
  · 譯文為空

只警告的：
  · 缺翻（該條自動回退顯示繁中，不影響功能）
  · 譯文與原文完全相同（多半是漏譯；自動略過不寫入，反正查不到就回退）
  · AT 指令名／<尖括號參數> 在譯文中消失

用法：
    python tools/i18n_merge.py            # 全部語言
    python tools/i18n_merge.py en-US      # 指定語言
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, 'i18n')
TR = os.path.join(I18N, 'tr')


def tr_dirs():
    """所有翻譯稿目錄，依批次順序（tr, tr2, tr3, …），後者覆蓋前者。

    刻意用掃描而不是寫死清單 —— 每次補譯都新增一批，寫死就會忘了加（踩過）。
    ⚠ 只收 tr / tr<數字>：舊的 i18n/tr-delta/ 是索引式且對應已失效的目錄版本，
    讀進來會變成無聲錯譯，必須排除。
    """
    ds = []
    for name in os.listdir(I18N):
        if not os.path.isdir(os.path.join(I18N, name)):
            continue
        m = re.fullmatch(r'tr(\d*)', name)
        if m:
            ds.append((int(m.group(1) or 1), os.path.join(I18N, name)))
    return [p for _, p in sorted(ds)]
OUT = os.path.join(ROOT, 'js', 'i18n')

PLACEHOLDER = re.compile(r'\{(\d+)\}')
AT_CMD = re.compile(r'AT[+&][A-Z0-9]+|\+Q[A-Z]+|<[a-z_]+>')
CJK = re.compile('[一-鿿]')


def jload(p):
    return json.loads(io.open(p, encoding='utf-8-sig').read())


def load_lang(lang):
    """合併主批（tr/）與補譯批（tr2/），回傳「原文 -> 譯文」。兩者都以原文為鍵。

    ⚠ 舊的 i18n/tr-delta/ 是索引式且對應已失效的目錄版本，**刻意不讀** ——
    原文目錄一擴充索引就整批位移，那是無聲的錯譯，比缺翻危險得多。
    """
    out = {}
    for d in tr_dirs():
        p = os.path.join(d, '%s.json' % lang)
        if os.path.exists(p):
            for k, v in jload(p).items():
                if isinstance(v, str) and v.strip():
                    out[k] = v
    return out


def check(src_list, tr):
    good, fatal, warn = {}, [], []
    missing = 0
    for s in src_list:
        v = tr.get(s)
        if v is None:
            missing += 1
            continue
        if not isinstance(v, str) or not v.strip():
            fatal.append('譯文為空：%s' % s[:44])
            continue
        if sorted(PLACEHOLDER.findall(s)) != sorted(PLACEHOLDER.findall(v)):
            fatal.append('佔位符不符 %s → %s ｜ %s'
                         % (PLACEHOLDER.findall(s), PLACEHOLDER.findall(v), s[:40]))
            continue
        if v == s:
            if CJK.search(s):
                warn.append('疑似漏譯（與原文相同）：%s' % s[:44])
            continue          # 相同就不寫，查不到自然回退原文，省空間
        lost = [t for t in set(AT_CMD.findall(s)) if t not in v]
        if lost:
            warn.append('遺失技術符號 %s ｜ %s' % (lost[:3], s[:36]))
        good[s] = v
    if missing:
        warn.append('缺翻 %d 條（會回退顯示繁中）' % missing)
    return good, fatal, warn


def emit(lang, good):
    os.makedirs(OUT, exist_ok=True)
    js = (
        '// NuModem AT 面板翻譯 —— %s\n'
        '// 自動產生，請勿手改：改 i18n/tr/%s.json 或 i18n/tr-delta/%s.json 後重跑\n'
        '// tools/i18n_merge.py。key 是繁體中文原文；查不到的字串會自動回退顯示原文。\n'
        '(function () {\n'
        '    var A = (window.AT_I18N = window.AT_I18N || {});\n'
        '    A[%s] = %s;\n'
        '})();\n'
        % (lang, lang, lang, json.dumps(lang),
           json.dumps(good, ensure_ascii=False, indent=0))
    )
    p = os.path.join(OUT, 'at-%s.js' % lang)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(js)
    return p, len(js.encode('utf-8'))


def main():
    src_list = jload(os.path.join(I18N, 'sources.json'))['strings']
    want = sys.argv[1:]
    if not want:
        want = sorted({f[:-5] for f in os.listdir(TR)} if os.path.isdir(TR) else [])
    if not want:
        print('找不到 i18n/tr/ —— 先跑 tools/i18n_reindex.py')
        return 1

    print('原文 %d 條\n' % len(src_list))
    total = okc = 0
    for lang in want:
        tr = load_lang(lang)
        good, fatal, warn = check(src_list, tr)
        if fatal:
            print('%-7s ✗ 致命問題 %d 項：' % (lang, len(fatal)))
            for f in fatal[:5]:
                print('           %s' % f)
            continue
        p, size = emit(lang, good)
        total += size
        okc += 1
        print('%-7s ✓ %4d 條  %6.0f KB%s'
              % (lang, len(good), size / 1024,
                 ('   ⚠ %s' % warn[0]) if warn else ''))
        for w in warn[1:3]:
            print('           %s' % w)
    print('\n完成 %d 種語言，合計 %.1f MB（按需載入，一次只載一種）'
          % (okc, total / 1024 / 1024))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
