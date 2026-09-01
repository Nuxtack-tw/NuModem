# -*- coding: utf-8 -*-
"""抽出 NuModem 所有待翻譯字串，產生 i18n 來源目錄。

兩個來源合併：
  1. 資料型字串（AT_CMD_TABS／註解表／錯誤碼表）—— 由瀏覽器經 window.__AT_SRC 匯出，
     見 reports/i18n-design.md §3 的操作步驟，結果存 at_i18n_sources.json
  2. tt`...` 的骨架 key —— 只存在於程式碼裡，必須靜態抽：
     把 ${...} 換成 {0}{1}… 之後的字串就是 key（與執行期 tt() 的算法一致）

輸出 i18n/sources.json：{ "strings": [...], "counts": {...} }
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'NuModem_EG800.html')


def tt_keys(src):
    """掃出所有 tt`...`，回傳其骨架 key。

    逐字元掃描而非 regex —— 要正確跳過巢狀插值裡的反引號，
    例如 tt`外 ${cond ? `內` : ''} 尾` 只能算成一個 key。
    """
    keys = []
    i = 0
    n = len(src)
    while True:
        i = src.find('tt`', i)
        if i < 0:
            break
        # 確認 tt 是獨立識別字（前面不能是字母／數字／底線／$）
        if i > 0 and (src[i - 1].isalnum() or src[i - 1] in '_$.'):
            i += 3
            continue
        j = i + 3
        depth = 0          # ${ } 巢狀深度
        tpl = 0            # 內層 template 深度
        parts = ['']
        while j < n:
            c = src[j]

            # ⚠ 跳脫處理只能在「骨架文字」裡做。
            # 早期版本把它寫在最外層，結果插值裡的正規式 /\s+/g 的 \s
            # 被當成骨架文字累加進 key，產生 'SIM 狀態：{0}\s' 這種對不上的鍵（V26.0.60 踩過）
            if depth == 0 and tpl == 0:
                if c == '\\':
                    parts[-1] += src[j:j + 2]
                    j += 2
                    continue
                if c == '`':
                    break
                if c == '$' and src[j + 1:j + 2] == '{':
                    parts.append('')
                    depth = 1
                    j += 2
                    continue
                parts[-1] += c
                j += 1
                continue

            # ── 以下都在插值運算式（或其內層 template）裡：只做結構追蹤，不累加文字
            if c == '\\':
                j += 2
                continue
            if c in '"\'':                      # 跳過字串字面值，免得裡面的 {} 打亂深度
                q = c
                j += 1
                while j < n and src[j] != q:
                    j += 2 if src[j] == '\\' else 1
                j += 1
                continue
            if c == '/' and src[j + 1:j + 2] not in ('/', '*', ''):
                k = j - 1                        # 粗略判斷是不是正規式字面值
                while k >= 0 and src[k] in ' \t':
                    k -= 1
                if k >= 0 and src[k] in '=(,:[!&|?{;+':
                    j += 1
                    in_cls = False
                    while j < n:
                        if src[j] == '\\':
                            j += 2
                            continue
                        if src[j] == '[':
                            in_cls = True
                        elif src[j] == ']':
                            in_cls = False
                        elif src[j] == '/' and not in_cls:
                            break
                        j += 1
                    j += 1
                    continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    j += 1
                    continue
            elif c == '`':
                tpl = 0 if tpl else 1
            j += 1
        key = parts[0]
        for k in range(1, len(parts)):
            key += '{%d}' % (k - 1) + parts[k]
        # 跳脫序列還原成實際字元（與執行期 cooked 一致）
        key = key.replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'") \
                 .replace('\\`', '`').replace('\\\\', '\\')
        if key.strip():
            keys.append(key)
        i = j + 1
    return keys


def l_calls(src):
    """抽出 L('…') 形式的裸字面值。

    這類字串寫在 note 函式體裡（`m => x ? '甲' : '乙'`、`return '丙'`、字串串接），
    既不是資料表的值、也不是 tt 的骨架 —— 兩種抽取都掃不到。
    V26.0.60 就是漏了這一類，導致 en-US 出現「錯誤 563：socket 識別碼已被使用」中英夾雜。
    統一包成 L('…') 之後就能靠這個形狀可靠地抽出來。

    ⚠ **L('a' + 'b') 這種串接寫法抓不到** —— 下面的 regex 要求字串後面緊跟 ')'。
    2026-08-07 加 QLBS 註解時踩過：那段文字永遠不會進翻譯目錄，切語言就殘留中文。
    要換行請用「兩個獨立的 L() 相加」，不要在單一 L() 裡串接。
    """
    out = []
    for m in re.finditer(r"""L\(\s*'((?:[^'\\]|\\.)*)'\s*\)""", src):
        v = m.group(1)
        v = v.replace("\\'", "'").replace('\\\\', '\\')
        if v.strip():
            out.append(v)
    for m in re.finditer(r'''L\(\s*"((?:[^"\\]|\\.)*)"\s*\)''', src):
        v = m.group(1).replace('\\"', '"').replace('\\\\', '\\')
        if v.strip():
            out.append(v)
    return out


def main():
    src = io.open(HTML, encoding='utf-8').read()
    keys = tt_keys(src)
    # ⚠ 不能只看「有沒有漢字」——`context {0}：{1}；APN「{2}」` 與分隔符 `；`
    # 一個漢字都沒有，卻是道地的中文排版：日文不用「；」，RTL 語言還要改順序。
    # 只用漢字判斷會把這類整批漏掉（V26.0.60 踩過）
    cjk = re.compile('[一-鿿]|[，、。；：？！（）「」『』【】—…～]')
    keys = [k for k in keys if cjk.search(k)]
    bare = sorted({v for v in l_calls(src) if cjk.search(v)})

    data_path = os.path.join(ROOT, 'at_i18n_sources.json')
    data = {}
    if os.path.exists(data_path):
        data = json.load(io.open(data_path, encoding='utf-8'))
        if isinstance(data, str):
            data = json.loads(data)

    buckets = {
        'menu': data.get('menu', []),
        'annotation': data.get('annotation', []),
        'error': data.get('error', []),
        'fixed': data.get('fixed', []),
        'template': sorted(set(keys)),
        'bare': bare,
    }
    seen = set()
    ordered = []
    for name in ('menu', 'annotation', 'template', 'error', 'fixed', 'bare'):
        for s in buckets[name]:
            if s not in seen:
                seen.add(s)
                ordered.append(s)

    out_dir = os.path.join(ROOT, 'i18n')
    os.makedirs(out_dir, exist_ok=True)
    out = {
        'counts': {k: len(v) for k, v in buckets.items()},
        'unique': len(ordered),
        'buckets': buckets,
        'strings': ordered,
    }
    io.open(os.path.join(out_dir, 'sources.json'), 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print('各類數量：%s' % json.dumps(out['counts'], ensure_ascii=False))
    print('去重後合計 %d 條 → i18n/sources.json' % len(ordered))


if __name__ == '__main__':
    main()
