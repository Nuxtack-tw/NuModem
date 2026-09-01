# -*- coding: utf-8 -*-
"""第二批補譯：下拉選項說明、placeholder、續寫按鈕、列表分隔符。

這一批是第一批漏掉的 —— 執行期匯出時沒收 params[].optionLabels 與 placeholder，
而列表分隔符「、」原本寫死在 rangeNote()/cfgNote() 的 join() 裡，
永遠不會進翻譯目錄。兩者都靠瀏覽器端的洩漏稽核抓出來，不是靜態掃描能發現的。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr8-source.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'i18n', 'tr8')

T = {
 'en-US': [
  "Send (continue)",
  "e.g. mqttgo.io",
  "Taiwan (HiNet 61.70.174.84) — fastest in our measurements: ping 190-210 ms from the module, 100/100 on the burst test, no throttling; 1883 plaintext / 8883 TLS",
  "HiveMQ public broker — 100/100 on the burst test, no throttling; ⚠ blocks ICMP (QPING answers 559) but TCP connects fine",
  "Eclipse Mosquitto — 100/100 on the burst test; ping 385-400 ms from the module; the site itself says not to use it for anything important, and topic pollution is worst here",
  "EMQX public broker — ⚠ publish rate limiting (only 40 of a 100-message burst got through); blocks ICMP; has a web dashboard for broker status",
  ", "],
 'ja-JP': [
  "送信（続き）",
  "例：mqttgo.io",
  "台湾（HiNet 61.70.174.84）—— 実測で最速：モジュールからの ping 190-210 ms、連続送信 100/100 で帯域制限なし。1883 平文／8883 TLS",
  "HiveMQ 公開ブローカー —— 連続送信 100/100 で帯域制限なし。⚠ ICMP を遮断（QPING は 559 を返す）が TCP は問題なく通る",
  "Eclipse Mosquitto —— 連続送信 100/100。モジュールからの ping 385-400 ms。公式サイト自身が重要な用途には使うなと明言しており、トピックの混線も最もひどい",
  "EMQX 公開ブローカー —— ⚠ パブリッシュに速度制限あり（100 件連続で 40 件しか通らない）。ICMP を遮断。ブローカーの状態を見られる Web ダッシュボードあり",
  "、"],
 'de-DE': [
  "Senden (Fortsetzung)",
  "z. B. mqttgo.io",
  "Taiwan (HiNet 61.70.174.84) — in unseren Messungen der schnellste: Ping 190-210 ms vom Modul, 100/100 im Burst-Test, keine Drosselung; 1883 Klartext / 8883 TLS",
  "Öffentlicher HiveMQ-Broker — 100/100 im Burst-Test, keine Drosselung; ⚠ blockiert ICMP (QPING antwortet 559), TCP verbindet aber problemlos",
  "Eclipse Mosquitto — 100/100 im Burst-Test; Ping 385-400 ms vom Modul; die Website selbst rät von wichtigen Einsätzen ab, und die Themenverschmutzung ist hier am schlimmsten",
  "Öffentlicher EMQX-Broker — ⚠ Ratenbegrenzung beim Veröffentlichen (von 100 Nachrichten kamen nur 40 durch); blockiert ICMP; bietet ein Web-Dashboard für den Broker-Status",
  ", "],
 'fr-FR': [
  "Envoyer (suite)",
  "ex. : mqttgo.io",
  "Taïwan (HiNet 61.70.174.84) — le plus rapide selon nos mesures : ping de 190-210 ms depuis le module, 100/100 au test de rafale, sans bridage ; 1883 en clair / 8883 TLS",
  "Broker public HiveMQ — 100/100 au test de rafale, sans bridage ; ⚠ bloque l'ICMP (QPING répond 559) mais le TCP passe sans problème",
  "Eclipse Mosquitto — 100/100 au test de rafale ; ping de 385-400 ms depuis le module ; le site lui-même déconseille tout usage important, et la pollution des sujets y est la pire",
  "Broker public EMQX — ⚠ limitation du débit de publication (sur 100 messages en rafale, 40 seulement sont passés) ; bloque l'ICMP ; dispose d'un tableau de bord web pour l'état du broker",
  ", "],
 'es-ES': [
  "Enviar (continuación)",
  "p. ej.: mqttgo.io",
  "Taiwán (HiNet 61.70.174.84): el más rápido en nuestras mediciones; ping de 190-210 ms desde el módulo, 100/100 en la prueba de ráfaga y sin limitación; 1883 en claro / 8883 TLS",
  "Bróker público de HiveMQ: 100/100 en la prueba de ráfaga y sin limitación; ⚠ bloquea ICMP (QPING responde 559), pero TCP conecta sin problemas",
  "Eclipse Mosquitto: 100/100 en la prueba de ráfaga; ping de 385-400 ms desde el módulo; el propio sitio advierte de no usarlo para nada importante, y aquí la contaminación de temas es la peor",
  "Bróker público de EMQX: ⚠ tiene límite de velocidad de publicación (de 100 mensajes en ráfaga solo pasaron 40); bloquea ICMP; dispone de un panel web para ver el estado del bróker",
  ", "],
 'pt-PT': [
  "Enviar (continuação)",
  "p. ex.: mqttgo.io",
  "Taiwan (HiNet 61.70.174.84) — o mais rápido nas nossas medições: ping de 190-210 ms a partir do módulo, 100/100 no teste de rajada e sem limitação; 1883 em claro / 8883 TLS",
  "Broker público HiveMQ — 100/100 no teste de rajada e sem limitação; ⚠ bloqueia ICMP (o QPING responde 559), mas o TCP liga sem problemas",
  "Eclipse Mosquitto — 100/100 no teste de rajada; ping de 385-400 ms a partir do módulo; o próprio site desaconselha usos importantes, e é aqui que a poluição de tópicos é pior",
  "Broker público EMQX — ⚠ tem limite de ritmo de publicação (de 100 mensagens em rajada só passaram 40); bloqueia ICMP; tem um painel web para ver o estado do broker",
  ", "],
 'it-IT': [
  "Invia (continua)",
  "es.: mqttgo.io",
  "Taiwan (HiNet 61.70.174.84): il più veloce nelle nostre misure; ping di 190-210 ms dal modulo, 100/100 nella prova a raffica e senza limitazioni; 1883 in chiaro / 8883 TLS",
  "Broker pubblico HiveMQ: 100/100 nella prova a raffica e senza limitazioni; ⚠ blocca ICMP (QPING risponde 559), ma il TCP si connette senza problemi",
  "Eclipse Mosquitto: 100/100 nella prova a raffica; ping di 385-400 ms dal modulo; il sito stesso sconsiglia usi importanti, e qui l'inquinamento dei topic è il peggiore",
  "Broker pubblico EMQX: ⚠ limita la velocità di pubblicazione (di 100 messaggi a raffica ne sono passati solo 40); blocca ICMP; offre una dashboard web per lo stato del broker",
  ", "],
 'ru-RU': [
  "Отправить (продолжение)",
  "например: mqttgo.io",
  "Тайвань (HiNet 61.70.174.84) — самый быстрый по нашим измерениям: пинг 190-210 мс с модуля, 100/100 в пакетном тесте, без ограничения скорости; 1883 открытым текстом / 8883 TLS",
  "Публичный брокер HiveMQ — 100/100 в пакетном тесте, без ограничения скорости; ⚠ блокирует ICMP (QPING отвечает 559), но TCP подключается нормально",
  "Eclipse Mosquitto — 100/100 в пакетном тесте; пинг 385-400 мс с модуля; сам сайт советует не использовать его для чего-то важного, и засорённость топиков здесь наибольшая",
  "Публичный брокер EMQX — ⚠ есть ограничение скорости публикации (из 100 сообщений подряд прошли лишь 40); блокирует ICMP; есть веб-панель для просмотра состояния брокера",
  ", "],
 'vi-VN': [
  "Gửi (viết tiếp)",
  "ví dụ: mqttgo.io",
  "Đài Loan (HiNet 61.70.174.84) — nhanh nhất theo đo đạc của chúng tôi: ping 190-210 ms từ module, 100/100 ở phép thử bắn dồn, không bị bóp băng thông; 1883 không mã hoá / 8883 TLS",
  "Broker công cộng HiveMQ — 100/100 ở phép thử bắn dồn, không bị bóp băng thông; ⚠ chặn ICMP (QPING trả về 559) nhưng TCP vẫn kết nối tốt",
  "Eclipse Mosquitto — 100/100 ở phép thử bắn dồn; ping 385-400 ms từ module; chính trang chủ khuyên đừng dùng cho việc quan trọng, và mức ô nhiễm topic ở đây là nặng nhất",
  "Broker công cộng EMQX — ⚠ có giới hạn tốc độ phát (bắn dồn 100 tin chỉ lọt 40); chặn ICMP; có Dashboard web để xem trạng thái broker",
  ", "],
 'id-ID': [
  "Kirim (lanjutan)",
  "mis.: mqttgo.io",
  "Taiwan (HiNet 61.70.174.84) — tercepat dalam pengukuran kami: ping 190-210 ms dari modul, 100/100 pada uji beruntun, tanpa pembatasan; 1883 polos / 8883 TLS",
  "Broker publik HiveMQ — 100/100 pada uji beruntun, tanpa pembatasan; ⚠ memblokir ICMP (QPING menjawab 559), tetapi TCP tersambung tanpa masalah",
  "Eclipse Mosquitto — 100/100 pada uji beruntun; ping 385-400 ms dari modul; situsnya sendiri menyarankan jangan dipakai untuk hal penting, dan pencemaran topik di sini paling parah",
  "Broker publik EMQX — ⚠ ada pembatasan laju penerbitan (dari 100 pesan beruntun hanya 40 yang lolos); memblokir ICMP; punya Dashboard web untuk melihat status broker",
  ", "],
 'ms-MY': [
  "Hantar (sambungan)",
  "cth.: mqttgo.io",
  "Taiwan (HiNet 61.70.174.84) — terpantas dalam ukuran kami: ping 190-210 ms dari modul, 100/100 dalam ujian rentetan, tanpa pengehadan; 1883 teks biasa / 8883 TLS",
  "Broker awam HiveMQ — 100/100 dalam ujian rentetan, tanpa pengehadan; ⚠ menyekat ICMP (QPING membalas 559), tetapi TCP menyambung tanpa masalah",
  "Eclipse Mosquitto — 100/100 dalam ujian rentetan; ping 385-400 ms dari modul; laman rasminya sendiri menasihatkan supaya jangan digunakan untuk perkara penting, dan pencemaran topik di sini paling teruk",
  "Broker awam EMQX — ⚠ ada had kadar penerbitan (daripada 100 mesej rentetan hanya 40 menembusi); menyekat ICMP; ada Dashboard web untuk melihat status broker",
  ", "],
 'th-TH': [
  "ส่ง (เขียนต่อ)",
  "เช่น mqttgo.io",
  "ไต้หวัน (HiNet 61.70.174.84) — เร็วที่สุดจากที่วัดได้: ping จากโมดูล 190-210 มิลลิวินาที ส่งรัว 100/100 ไม่จำกัดปริมาณ; 1883 แบบไม่เข้ารหัส / 8883 TLS",
  "โบรกเกอร์สาธารณะ HiveMQ — ส่งรัว 100/100 ไม่จำกัดปริมาณ; ⚠ บล็อก ICMP (QPING ตอบ 559) แต่ TCP เชื่อมต่อได้ปกติ",
  "Eclipse Mosquitto — ส่งรัว 100/100; ping จากโมดูล 385-400 มิลลิวินาที; เว็บไซต์ของตัวเองระบุว่าอย่านำไปใช้กับงานสำคัญ และการปะปนของหัวข้อที่นี่หนักที่สุด",
  "โบรกเกอร์สาธารณะ EMQX — ⚠ มีการจำกัดอัตราการเผยแพร่ (ส่งรัว 100 ข้อความผ่านเพียง 40); บล็อก ICMP; มีแดชบอร์ดเว็บให้ดูสถานะโบรกเกอร์",
  ", "],
 'hi-IN': [
  "भेजें (जारी रखें)",
  "जैसे: mqttgo.io",
  "ताइवान (HiNet 61.70.174.84) — हमारे मापन में सबसे तेज़: मॉड्यूल से पिंग 190-210 ms, बर्स्ट परीक्षण में 100/100, कोई सीमा नहीं; 1883 सादा / 8883 TLS",
  "HiveMQ सार्वजनिक ब्रोकर — बर्स्ट परीक्षण में 100/100, कोई सीमा नहीं; ⚠ ICMP रोकता है (QPING 559 लौटाता है), पर TCP बिना दिक़्क़त जुड़ता है",
  "Eclipse Mosquitto — बर्स्ट परीक्षण में 100/100; मॉड्यूल से पिंग 385-400 ms; उसकी अपनी साइट कहती है कि किसी ज़रूरी काम में इसका उपयोग न करें, और विषयों का प्रदूषण यहीं सबसे ज़्यादा है",
  "EMQX सार्वजनिक ब्रोकर — ⚠ प्रकाशन दर सीमित है (लगातार 100 संदेशों में से केवल 40 गए); ICMP रोकता है; ब्रोकर की स्थिति देखने के लिए वेब डैशबोर्ड है",
  ", "],
 'tr-TR': [
  "Gönder (devam)",
  "örn.: mqttgo.io",
  "Tayvan (HiNet 61.70.174.84) — ölçümlerimizde en hızlısı: modülden ping 190-210 ms, seri gönderim testinde 100/100, kısıtlama yok; 1883 düz metin / 8883 TLS",
  "HiveMQ genel aracısı — seri gönderim testinde 100/100, kısıtlama yok; ⚠ ICMP'yi engeller (QPING 559 döndürür) ama TCP sorunsuz bağlanır",
  "Eclipse Mosquitto — seri gönderim testinde 100/100; modülden ping 385-400 ms; sitesinin kendisi önemli işlerde kullanılmamasını söylüyor ve konu kirliliği en çok burada",
  "EMQX genel aracısı — ⚠ yayımlama hız sınırı var (arka arkaya 100 iletiden yalnızca 40'ı geçti); ICMP'yi engeller; aracının durumunu gösteren web panosu var",
  ", "],
 'ar-SA': [
  "إرسال (متابعة)",
  "مثال: mqttgo.io",
  "تايوان (HiNet 61.70.174.84) — الأسرع في قياساتنا: زمن استجابة 190-210 مللي ثانية من الوحدة، و100/100 في اختبار الدفق، وبلا تقييد للمعدل؛ المنفذ 1883 بنص صريح و8883 بتشفير TLS",
  "وسيط HiveMQ العمومي — ‏100/100 في اختبار الدفق وبلا تقييد للمعدل؛ ⚠ يحجب ICMP (يرد QPING بالرمز 559) لكن اتصال TCP يمر دون مشكلة",
  "‏Eclipse Mosquitto — ‏100/100 في اختبار الدفق؛ زمن استجابة 385-400 مللي ثانية من الوحدة؛ وموقعه نفسه ينصح بعدم استخدامه لأي غرض مهم، والتلوث في المواضيع هنا هو الأسوأ",
  "وسيط EMQX العمومي — ⚠ فيه تقييد لمعدل النشر (من 100 رسالة متتابعة لم تمر سوى 40)؛ ويحجب ICMP؛ وله لوحة تحكم على الويب لمتابعة حالة الوسيط",
  "، "],
 'he-IL': [
  "שלח (המשך)",
  "לדוגמה: mqttgo.io",
  "טייוואן (HiNet 61.70.174.84) — המהיר ביותר במדידות שלנו: פינג 190-210 מילישניות מהמודול, 100/100 במבחן הצרורות, ללא הגבלת קצב; 1883 בטקסט גלוי / 8883 ב-TLS",
  "ברוקר ציבורי של HiveMQ — 100/100 במבחן הצרורות, ללא הגבלת קצב; ⚠ חוסם ICMP (‏QPING משיב 559) אך TCP מתחבר ללא בעיה",
  "‏Eclipse Mosquitto — 100/100 במבחן הצרורות; פינג 385-400 מילישניות מהמודול; האתר עצמו ממליץ לא להשתמש בו לשום דבר חשוב, וזיהום הנושאים כאן הוא החמור ביותר",
  "ברוקר ציבורי של EMQX — ⚠ יש הגבלת קצב פרסום (מתוך 100 הודעות ברצף עברו רק 40); חוסם ICMP; יש לוח בקרה מבוסס דפדפן למצב הברוקר",
  ", "],
 'fa-IR': [
  "ارسال (ادامه)",
  "مثال: mqttgo.io",
  "تایوان (HiNet 61.70.174.84) — سریع‌ترین در اندازه‌گیری‌های ما: پینگ ۱۹۰-۲۱۰ میلی‌ثانیه از ماژول، ۱۰۰/۱۰۰ در آزمون رگباری، بدون محدودسازی نرخ؛ درگاه ۱۸۸۳ ساده و ۸۸۸۳ با TLS",
  "کارگزار عمومی HiveMQ — ‏۱۰۰/۱۰۰ در آزمون رگباری و بدون محدودسازی نرخ؛ ⚠ ‏ICMP را می‌بندد (‏QPING عدد ۵۵۹ برمی‌گرداند) ولی TCP بی‌مشکل وصل می‌شود",
  "‏Eclipse Mosquitto — ‏۱۰۰/۱۰۰ در آزمون رگباری؛ پینگ ۳۸۵-۴۰۰ میلی‌ثانیه از ماژول؛ خودِ وب‌گاهش می‌گوید برای کار مهم به‌کارش نبرید و آلودگی موضوع‌ها اینجا از همه بدتر است",
  "کارگزار عمومی EMQX — ⚠ محدودیت نرخ انتشار دارد (از ۱۰۰ پیام پشت‌سرهم تنها ۴۰ تا رد شد)؛ ‏ICMP را می‌بندد؛ داشبورد وب برای دیدن وضعیت کارگزار دارد",
  "، "],
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for lang, vals in T.items():
        assert len(vals) == len(KEYS), '%s: %d != %d' % (lang, len(vals), len(KEYS))
        json.dump(dict(zip(KEYS, vals)),
                  io.open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('  %-7s %d 條' % (lang, len(vals)))
    print('完成 %d 種語言' % len(T))


if __name__ == '__main__':
    main()
