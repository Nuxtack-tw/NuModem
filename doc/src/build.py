# -*- coding: utf-8 -*-
"""把 bodies/manual.<lang>.html 組裝成單檔多語說明書。

用法：
    python doc/src/build.py            # 產出到 doc/manual.html（正式位置）
    python doc/src/build.py <目錄>      # 產出到指定目錄（試作用）

產出的 manual.html 把每個語言的正文各包在
<div class="doc-lang" data-lang="xx">，同時只有一個帶 .active；
右上角一個語言選單，語言以 ?lang= → localStorage → navigator.language → zh-TW 決定。

**改內容請改 bodies/ 底下的檔案再重跑本腳本。
不要直接改產出的 doc/manual.html，下次組裝就會被蓋掉。**

與母專案（NuMonitor）的差異：
- 母專案的中文版另有獨立網站，所以它的檔案裡沒有 zh-TW；
  本專案 **zh-TW 是原始語言、必須內含**，而且是找不到語言時的退路
- 語言清單與主程式的 18 語完全一致（zh-TW ＋ 17）
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))          # 專案根目錄
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PROJ, 'doc')

# 順序即選單順序。zh-TW 擺第一，它是原始語言也是退路。
LANGS = ['zh-TW', 'en-US', 'ja-JP', 'fr-FR', 'de-DE', 'it-IT', 'es-ES', 'pt-PT',
         'tr-TR', 'ar-SA', 'he-IL', 'fa-IR', 'ru-RU', 'hi-IN', 'th-TH',
         'vi-VN', 'id-ID', 'ms-MY']

LANG_NAMES = {
    'zh-TW': '繁體中文', 'en-US': 'English', 'ja-JP': '日本語',
    'fr-FR': 'Français', 'de-DE': 'Deutsch', 'it-IT': 'Italiano',
    'es-ES': 'Español', 'pt-PT': 'Português', 'tr-TR': 'Türkçe',
    'ar-SA': 'العربية', 'he-IL': 'עברית', 'fa-IR': 'فارسی',
    'ru-RU': 'Русский', 'hi-IN': 'हिन्दी', 'th-TH': 'ไทย',
    'vi-VN': 'Tiếng Việt', 'id-ID': 'Bahasa Indonesia', 'ms-MY': 'Bahasa Melayu',
}

# 由右至左書寫的語言，套 dir="rtl"
RTL = {'ar-SA', 'he-IL', 'fa-IR'}

TITLES = {
    'zh-TW': 'NuModem EG800 {V} — 使用說明書',
    'en-US': 'NuModem EG800 {V} — User Manual',
    'ja-JP': 'NuModem EG800 {V} — ユーザーマニュアル',
    'fr-FR': "NuModem EG800 {V} — Manuel d'utilisation",
    'de-DE': 'NuModem EG800 {V} — Benutzerhandbuch',
    'it-IT': 'NuModem EG800 {V} — Manuale utente',
    'es-ES': 'NuModem EG800 {V} — Manual de usuario',
    'pt-PT': 'NuModem EG800 {V} — Manual do utilizador',
    'tr-TR': 'NuModem EG800 {V} — Kullanım Kılavuzu',
    'ar-SA': 'NuModem EG800 {V} — دليل المستخدم',
    'he-IL': 'NuModem EG800 {V} — מדריך למשתמש',
    'fa-IR': 'NuModem EG800 {V} — راهنمای کاربر',
    'ru-RU': 'NuModem EG800 {V} — Руководство пользователя',
    'hi-IN': 'NuModem EG800 {V} — उपयोगकर्ता नियमावली',
    'th-TH': 'NuModem EG800 {V} — คู่มือผู้ใช้',
    'vi-VN': 'NuModem EG800 {V} — Hướng dẫn sử dụng',
    'id-ID': 'NuModem EG800 {V} — Panduan Pengguna',
    'ms-MY': 'NuModem EG800 {V} — Panduan Pengguna',
}

# 版本號的唯一來源是主程式的 <title>，不在這裡另外維護
def read_version():
    p = os.path.join(PROJ, 'NuModem_EG800.html')
    s = io.open(p, encoding='utf-8').read(4096)
    m = re.search(r'<title>NuModem EG800 (V[\d.]+)</title>', s)
    if not m:
        raise SystemExit('!! 讀不到主程式的版本號，請確認 %s 的 <title>' % p)
    return m.group(1)


EXTRA_CSS = """
        /* ---- 單檔多語：一次只顯示一個語言區塊 ---- */
        .doc-lang { display: none; }
        .doc-lang.active { display: block; }

        .doc-langbar {
            position: fixed;
            top: 10px;
            right: 12px;
            z-index: 500;
        }

        .doc-langbar select {
            background: var(--bg-elevated);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 5px 26px 5px 10px;
            font-family: inherit;
            font-size: 0.85rem;
            cursor: pointer;
            appearance: none;
            background-image: linear-gradient(45deg, transparent 50%, var(--text-secondary) 50%),
                              linear-gradient(135deg, var(--text-secondary) 50%, transparent 50%);
            background-position: calc(100% - 14px) 52%, calc(100% - 9px) 52%;
            background-size: 5px 5px, 5px 5px;
            background-repeat: no-repeat;
        }

        .doc-langbar select:hover { border-color: var(--accent-blue); }
        .doc-langbar select:focus { outline: none; border-color: var(--accent-blue); }

        /* 尚無該語言版本時的提示條 */
        .doc-fallback-note {
            max-width: 900px;
            margin: 16px auto 0;
            padding: 10px 16px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-yellow);
            border-radius: 0 8px 8px 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        /* AT 面板那幾張是「只留幾顆按鈕」的窄裁切（實寬約 600 px）。
           預設的 width:100% 會把它們撐到整欄寬而糊掉 —— 這裡改成以實際尺寸顯示並置中。
           要新增這類窄圖，記得 figure 加 .narrow。 */
        .doc-lang figure.shot.narrow img {
            width: auto;
            max-width: min(100%, 380px);
            display: block;
            margin-inline: auto;
        }

        /* RTL 語言：整塊翻面。表格要跟著鏡像（欄序由右至左），這是阿拉伯文／希伯來文
           讀者的預期；只有程式碼與終端輸出必須維持左至右，那是 ASCII，翻面會讀不懂。 */
        .doc-lang[dir="rtl"] { text-align: right; }
        .doc-lang[dir="rtl"] pre,
        .doc-lang[dir="rtl"] code { direction: ltr; text-align: left; }
        .doc-lang[dir="rtl"] pre { unicode-bidi: isolate; }
        .doc-lang[dir="rtl"] th,
        .doc-lang[dir="rtl"] td { text-align: right; }
        .doc-lang[dir="rtl"] .doc-fallback-note { border-left: none; border-right: 4px solid var(--accent-yellow); }

        @media (max-width: 640px) {
            .doc-langbar { top: 6px; right: 6px; }
            .doc-langbar select { font-size: 0.8rem; padding: 4px 22px 4px 8px; }
        }
"""


def langbar_html(available):
    # 只列真的組進來的語言 —— 列出沒有正文的語言，選下去會整頁空白
    opts = ['            <option value="%s">%s</option>' % (c, LANG_NAMES[c]) for c in available]
    return ('    <div class="doc-langbar">\n'
            '        <select id="docLangSelect" aria-label="Document language">\n'
            + '\n'.join(opts) + '\n'
            '        </select>\n'
            '    </div>\n')


SCRIPT = """    <script>
    (function () {
        // 文件語言：?lang= → localStorage → 瀏覽器語言 → zh-TW（原始語言，也是退路）
        var LANGS = %(langs)s;
        var TITLES = %(titles)s;
        var RTL = %(rtl)s;
        var KEY = 'numodem_doc_lang';
        var sel = document.getElementById('docLangSelect');
        var requested = new URLSearchParams(location.search).get('lang');

        function resolve(code) {
            if (!code) return null;
            if (LANGS.indexOf(code) >= 0) return code;
            var base = code.split('-')[0];
            for (var i = 0; i < LANGS.length; i++) {
                if (LANGS[i].split('-')[0] === base) return LANGS[i];
            }
            return null;
        }

        function pick() {
            var cands = [requested];
            try { cands.push(localStorage.getItem(KEY)); } catch (e) {}
            cands.push(navigator.language);
            (navigator.languages || []).forEach(function (l) { cands.push(l); });
            for (var i = 0; i < cands.length; i++) {
                var hit = resolve(cands[i]);
                if (hit) return hit;
            }
            return 'zh-TW';
        }

        function apply(lang, remember) {
            var blocks = document.querySelectorAll('.doc-lang');
            for (var i = 0; i < blocks.length; i++) {
                blocks[i].classList.toggle('active', blocks[i].dataset.lang === lang);
            }
            document.documentElement.lang = lang;
            document.documentElement.dir = RTL.indexOf(lang) >= 0 ? 'rtl' : 'ltr';
            if (TITLES[lang]) document.title = TITLES[lang];
            sel.value = lang;
            if (remember) { try { localStorage.setItem(KEY, lang); } catch (e) {} }
        }

        var active = pick();
        apply(active, false);

        // 主程式帶了語言過來、但本檔還沒有那個語言 → 說清楚為什麼看到中文
        if (requested && !resolve(requested) && active === 'zh-TW') {
            var note = document.createElement('div');
            note.className = 'doc-fallback-note';
            note.textContent = '本說明書尚未提供您的語言版本（' + requested + '），先顯示繁體中文版。';
            var host = document.querySelector('.doc-lang.active');
            if (host) host.insertBefore(note, host.firstChild);
        }

        sel.addEventListener('change', function () {
            apply(sel.value, true);
            var url = new URL(location.href);
            url.searchParams.set('lang', sel.value);
            history.replaceState(null, '', url);
            window.scrollTo(0, 0);
        });
    })();
    </script>
"""


def build():
    version = read_version()
    head = io.open(os.path.join(HERE, 'manual.head.html'), encoding='utf-8').read()
    head = head.replace('    </style>', EXTRA_CSS + '    </style>', 1)
    head = head.replace('{LANG}', 'zh-TW').replace(
        '{TITLE}', TITLES['zh-TW'].replace('{V}', version))

    titles, parts, missing = {}, [], []
    for code in LANGS:
        path = os.path.join(HERE, 'bodies', 'manual.%s.html' % code)
        if not os.path.exists(path):
            missing.append(code)
            continue
        body = io.open(path, encoding='utf-8').read()
        # 各語言區塊同處一份文件，section id 會撞名、錨點會跳到隱藏區塊。
        # zh-TW 保留原始 id（外部連結 manual.html#faq 仍有效），其餘語言加前綴。
        if code != 'zh-TW':
            body = re.sub(r'id="([\w-]+)"', 'id="%s--\\1"' % code, body)
            body = re.sub(r'href="#([\w-]+)"', 'href="#%s--\\1"' % code, body)
        dir_attr = ' dir="rtl"' if code in RTL else ''
        parts.append('    <div class="doc-lang" data-lang="%s"%s>\n%s\n    </div>\n'
                     % (code, dir_attr, body))
        titles[code] = TITLES[code].replace('{V}', version)

    avail = [c for c in LANGS if c in titles]
    script = SCRIPT % {
        'langs': json.dumps(avail),
        'titles': json.dumps(titles, ensure_ascii=False),
        'rtl': json.dumps([c for c in avail if c in RTL]),
    }

    out = (head + '<body>\n' + langbar_html(avail) + ''.join(parts) + script + '</body>\n</html>\n')
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, 'manual.html')
    io.open(dest, 'w', encoding='utf-8', newline='\n').write(out)
    print('%s  ← %d 種語言、%d KB（版本 %s）'
          % (dest, len(avail), len(out) // 1024, version))
    if missing:
        print('尚無正文：%s' % ' '.join(missing))


if __name__ == '__main__':
    build()
