# -*- coding: utf-8 -*-
"""檢查各語言正文的 HTML 結構是否與繁體中文原文一致。

翻譯 agent 最容易犯的錯是「順手改結構」——多一個標籤、少一個 id、
把 href 錨點翻成當地語言。那些錯誤組裝出來不會報錯，但導覽列會點不動、
錨點會跳到隱藏的語言區塊。這支就是在組裝前把它們攔下來。

用法：python doc/src/check.py
"""
import io
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BODIES = os.path.join(HERE, 'bodies')
BASE = 'zh-TW'


def profile(text):
    """抽出一份正文的結構指紋。只看結構，不看文字。"""
    return {
        'ids': sorted(re.findall(r'id="([\w-]+)"', text)),
        'hrefs': sorted(re.findall(r'href="#([\w-]+)"', text)),
        'imgs': sorted(re.findall(r'<img src="([^"]+)"', text)),
        'tags': Counter(t.lower() for t in re.findall(r'<(/?[a-zA-Z][\w-]*)', text)),
        'codes': sorted(re.findall(r'<code>([^<]+)</code>', text)),
    }


def main():
    base_path = os.path.join(BODIES, 'manual.%s.html' % BASE)
    if not os.path.exists(base_path):
        raise SystemExit('!! 找不到原文 %s' % base_path)
    base = profile(io.open(base_path, encoding='utf-8').read())
    print('原文 %s：%d 個 id、%d 個錨點、%d 張圖、%d 種標籤'
          % (BASE, len(base['ids']), len(base['hrefs']), len(base['imgs']), len(base['tags'])))

    files = sorted(f for f in os.listdir(BODIES)
                   if f.startswith('manual.') and f.endswith('.html')
                   and BASE not in f)
    if not files:
        print('（還沒有其他語言的正文）')
        return

    bad = 0
    for f in files:
        code = f[len('manual.'):-len('.html')]
        p = profile(io.open(os.path.join(BODIES, f), encoding='utf-8').read())
        probs = []

        if p['ids'] != base['ids']:
            miss = set(base['ids']) - set(p['ids'])
            extra = set(p['ids']) - set(base['ids'])
            probs.append('id 不符（少 %s／多 %s）' % (sorted(miss)[:4], sorted(extra)[:4]))
        if p['hrefs'] != base['hrefs']:
            miss = set(base['hrefs']) - set(p['hrefs'])
            extra = set(p['hrefs']) - set(base['hrefs'])
            probs.append('錨點不符（少 %s／多 %s）' % (sorted(miss)[:4], sorted(extra)[:4]))
        if p['imgs'] != base['imgs']:
            probs.append('圖片不符：%s' % p['imgs'])

        # 標籤數量：容許 <br> 這類與斷句相關的差異，其餘要一致
        LOOSE = {'br', 'strong', 'em', 'code'}
        for tag, n in base['tags'].items():
            if tag.lstrip('/') in LOOSE:
                continue
            if p['tags'].get(tag, 0) != n:
                probs.append('<%s> 數量 %d≠%d' % (tag, p['tags'].get(tag, 0), n))

        # 錨點一定要指到自己檔案裡存在的 id
        orphan = [h for h in set(p['hrefs']) if h not in set(p['ids'])]
        if orphan:
            probs.append('錨點指不到 id：%s' % sorted(orphan)[:5])

        if probs:
            bad += 1
            print('  ✘ %-7s %s' % (code, '；'.join(probs[:4])))
        else:
            print('  ✔ %-7s 結構一致' % code)

    print('\n%d/%d 份通過' % (len(files) - bad, len(files)))
    if bad:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
