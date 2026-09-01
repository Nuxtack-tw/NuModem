# -*- coding: utf-8 -*-
"""把索引式的翻譯稿轉成「原文 → 譯文」的穩固形式，並算出還沒翻的差集。

為什麼要有這支：第一版翻譯稿是 index -> 譯文（i18n/raw/<lang>.[ab].json），
搭配當時那份 i18n/to-translate.json 才有意義。原文目錄一擴充，索引全部位移，
沿用舊檔就會整批錯位。改成以原文字串為鍵之後就不怕順序變動了。

流程：
    舊 to-translate.json（index -> 原文） ＋ raw/<lang>.[ab].json（index -> 譯文）
      → i18n/tr/<lang>.json（原文 -> 譯文）
    新 sources.json 的字串扣掉已翻的
      → i18n/delta-to-translate.json（index -> 原文，只含待補的）

用法：
    python tools/i18n_reindex.py
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, 'i18n')
RAW = os.path.join(I18N, 'raw')
TR = os.path.join(I18N, 'tr')


def jload(p):
    return json.loads(io.open(p, encoding='utf-8-sig').read())


def main():
    old_index = jload(os.path.join(I18N, 'to-translate.json'))     # index -> 原文
    new_strings = jload(os.path.join(I18N, 'sources.json'))['strings']
    os.makedirs(TR, exist_ok=True)

    langs = sorted({f.rsplit('.', 2)[0] for f in os.listdir(RAW) if f.endswith('.json')})
    print('舊目錄 %d 條、新目錄 %d 條、語言 %d 種\n'
          % (len(old_index), len(new_strings), len(langs)))

    covered = None
    for lang in langs:
        merged = {}
        for part in ('a', 'b'):
            p = os.path.join(RAW, '%s.%s.json' % (lang, part))
            if os.path.exists(p):
                merged.update(jload(p))
        by_text = {}
        for idx, tr in merged.items():
            src = old_index.get(str(idx))
            if src and isinstance(tr, str) and tr.strip():
                by_text[src] = tr
        io.open(os.path.join(TR, '%s.json' % lang), 'w', encoding='utf-8').write(
            json.dumps(by_text, ensure_ascii=False, indent=0))
        # 補譯批（tr2/，本來就是以原文為鍵）也要算進覆蓋率，否則會重複派翻譯
        # 掃描所有補譯批（tr2, tr3, …），不寫死清單 —— 寫死就會忘了加（踩過）
        extra = sorted((int(m.group(1)), m.group(0))
                       for m in (re.fullmatch(r'tr(\d+)', n) for n in os.listdir(I18N))
                       if m)
        for _, d in extra:
            p2 = os.path.join(I18N, d, '%s.json' % lang)
            if os.path.exists(p2):
                by_text = {**by_text, **jload(p2)}
        have = sum(1 for s in new_strings if s in by_text)
        print('%-7s 轉出 %4d 條；對新目錄覆蓋 %4d/%d，缺 %d'
              % (lang, len(by_text), have, len(new_strings), len(new_strings) - have))
        miss = {s for s in new_strings if s not in by_text}
        covered = miss if covered is None else (covered | miss)

    delta = [s for s in new_strings if s in covered]
    io.open(os.path.join(I18N, 'delta-to-translate.json'), 'w', encoding='utf-8').write(
        json.dumps({str(i): s for i, s in enumerate(delta)}, ensure_ascii=False, indent=0))
    print('\n待補翻譯（任一語言缺的聯集）%d 條 → i18n/delta-to-translate.json' % len(delta))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
