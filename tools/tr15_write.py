r"""第九批補譯：窮舉欄位掃描後補上的 2 條，另修 tr14 第 42 條在拉丁語系少一個空格。

那 2 條之所以漏掉，是因為執行期匯出用的是「欄位白名單」，而白名單漏了
timeout / stateLabel / terminatorName。已改成窮舉所有字串屬性。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr15-source.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'i18n', 'tr15')

# 順序：['Ctrl+Z（0x1A）', '依 timeout 設定（本機出廠 60 秒）']
T = {
 'en-US': ["Ctrl+Z (0x1A)", "as set by timeout (60 s from the factory on this unit)"],
 'ja-JP': ["Ctrl+Z（0x1A）", "timeout の設定に従う（本機の出荷値は 60 秒）"],
 'de-DE': ["Strg+Z (0x1A)", "gemäß der Einstellung timeout (ab Werk 60 s auf diesem Gerät)"],
 'fr-FR': ["Ctrl+Z (0x1A)", "selon le réglage timeout (60 s d'usine sur cet appareil)"],
 'es-ES': ["Ctrl+Z (0x1A)", "según el ajuste timeout (60 s de fábrica en esta unidad)"],
 'pt-PT': ["Ctrl+Z (0x1A)", "conforme a definição timeout (60 s de fábrica nesta unidade)"],
 'it-IT': ["Ctrl+Z (0x1A)", "secondo l'impostazione timeout (60 s di fabbrica su questa unità)"],
 'ru-RU': ["Ctrl+Z (0x1A)", "по настройке timeout (с завода 60 с на этом экземпляре)"],
 'vi-VN': ["Ctrl+Z (0x1A)", "theo thiết lập timeout (máy này xuất xưởng là 60 giây)"],
 'id-ID': ["Ctrl+Z (0x1A)", "sesuai setelan timeout (60 detik dari pabrik pada unit ini)"],
 'ms-MY': ["Ctrl+Z (0x1A)", "mengikut tetapan timeout (60 saat dari kilang pada unit ini)"],
 'th-TH': ["Ctrl+Z (0x1A)", "ตามค่า timeout ที่ตั้งไว้ (เครื่องนี้ออกจากโรงงานเป็น 60 วินาที)"],
 'hi-IN': ["Ctrl+Z (0x1A)", "timeout सेटिंग के अनुसार (इस इकाई में फ़ैक्टरी से 60 सेकंड)"],
 'tr-TR': ["Ctrl+Z (0x1A)", "timeout ayarına göre (bu cihazda fabrikadan 60 sn)"],
 'ar-SA': ["Ctrl+Z ‏(0x1A)", "بحسب ضبط timeout (‏60 ثانية من المصنع في هذا الجهاز)"],
 'he-IL': ["Ctrl+Z ‏(0x1A)", "לפי ההגדרה timeout (‏60 שניות מהיצרן ביחידה הזו)"],
 'fa-IR': ["Ctrl+Z ‏(0x1A)", "بر پایهٔ تنظیم timeout (‏۶۰ ثانیه از کارخانه در این دستگاه)"],
}

# tr14 第 42 條：中文用全形「（」不需空格，拉丁語系接在數字後面要空一格
SPACE_FIX_LANGS = ['en-US', 'de-DE', 'fr-FR', 'es-ES', 'pt-PT', 'it-IT', 'ru-RU',
                   'vi-VN', 'id-ID', 'ms-MY', 'tr-TR']


def main():
    os.makedirs(OUT, exist_ok=True)
    for lang, vals in T.items():
        assert len(vals) == len(KEYS), '%s: %d != %d' % (lang, len(vals), len(KEYS))
        json.dump(dict(zip(KEYS, vals)),
                  io.open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    print('tr15：%d 種語言 × %d 條' % (len(T), len(KEYS)))

    k14 = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr14-source.json'), encoding='utf-8'))
    tail_key = next(k for k in k14 if k.startswith('（順序受'))
    n = 0
    for lang in SPACE_FIX_LANGS:
        p = os.path.join(ROOT, 'i18n', 'tr14', lang + '.json')
        d = json.load(io.open(p, encoding='utf-8'))
        v = d.get(tail_key, '')
        if v and not v.startswith(' '):
            d[tail_key] = ' ' + v
            json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            n += 1
    print('補上括號前的空格：%d 種語言' % n)


if __name__ == '__main__':
    main()
