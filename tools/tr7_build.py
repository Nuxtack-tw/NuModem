# -*- coding: utf-8 -*-
"""把 tr7 的「純陣列」譯稿轉成 i18n_merge 吃得下的「原文 → 譯文」字典。

為什麼用陣列而不是直接寫字典：這一批的原文有很多是長句（broker 說明那條 200 字），
一份字典要把原文重複 17 次，光是鍵就佔掉大半篇幅，也更容易打錯一個字導致對不上。
改成「索引對齊 i18n/tr7-source.json」之後，只要顧譯文本身。

用法：python tools/tr7_build.py            # 轉換 i18n/tr7/*.array.json
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR7 = os.path.join(ROOT, 'i18n', 'tr7')
SRC = os.path.join(ROOT, 'i18n', 'tr7-source.json')


def main():
    keys = json.load(io.open(SRC, encoding='utf-8'))
    ok = 0
    for f in sorted(os.listdir(TR7)):
        if not f.endswith('.array.json'):
            continue
        lang = f[:-len('.array.json')]
        vals = json.load(io.open(os.path.join(TR7, f), encoding='utf-8'))
        if len(vals) != len(keys):
            print('!! %s 有 %d 條，應為 %d 條 —— 跳過' % (lang, len(vals), len(keys)))
            continue
        bad = [i for i, v in enumerate(vals) if not isinstance(v, str) or not v.strip()]
        if bad:
            print('!! %s 第 %s 條是空的 —— 跳過' % (lang, bad[:5]))
            continue
        out = dict(zip(keys, vals))
        json.dump(out, io.open(os.path.join(TR7, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        ok += 1
        print('  %-7s %d 條' % (lang, len(out)))
    print('完成 %d 種語言' % ok)


if __name__ == '__main__':
    main()
