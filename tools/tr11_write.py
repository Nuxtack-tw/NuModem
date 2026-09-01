# -*- coding: utf-8 -*-
"""第五批補譯：SSL 頁預設對端改成 tcpbin.com:4243 後受影響的四條參數說明。

前兩條各自只在既有句子後面加了一段（tcpbin 的 15 秒逾時與逐行回聲），
所以沿用 tr/tr* 既有譯文再接上新句子；找不到舊譯文就直接報錯，不猜。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr11-source.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'i18n', 'tr11')
BATCHES = ['tr', 'tr2', 'tr3', 'tr4', 'tr5', 'tr6', 'tr7', 'tr8', 'tr9', 'tr10']

# 舊 key（用來撈既有譯文）
OLD_BUF_HOST = '遠端伺服器的域名或 IP。域名會走 DNS，解析失敗回錯誤碼 565。手冊範例用的 192.0.2.2 是文件保留位址，不是真實伺服器。'
OLD_PUSH_HOST = '遠端伺服器的域名或 IP。與 buffer 模式的差別只在最後一個參數 <access_mode>=1：收到的資料由模組直接以 URC 吐出，不必再下 AT+QSSLRECV。'

# 每語言：(接在 buffer host 後的新句, 接在 push host 後的新句, 埠說明含手冊範例, 埠說明不含手冊範例)
T = {
 'en-US': (
  " The default, tcpbin.com:4243, is a TLS echo service (verified working in the P5 run on 2026-08-07). ⚠ It idles out after only 15 seconds, so send your data promptly once connected, and it echoes line by line — a payload without a trailing newline never comes back.",
  " The default tcpbin.com:4243 likewise idles out after 15 seconds and echoes line by line.",
  "The port the server listens on. tcpbin's TLS echo is 4243, HTTPS is 443, MQTT over TLS is 8883. The manual's examples use 8010 / 8011.",
  "The port the server listens on. tcpbin's TLS echo is 4243, HTTPS is 443, MQTT over TLS is 8883."),
 'ja-JP': (
  " 既定の tcpbin.com:4243 は TLS エコーサービスです（2026-08-07 の P5 実測で動作確認済み）。⚠ アイドル 15 秒で切られるので、つないだらすぐデータを送ってください。また行単位のエコーなので、payload の末尾に改行がないと返ってきません。",
  " 既定の tcpbin.com:4243 も同じくアイドル 15 秒で切れ、行単位のエコーです。",
  "サーバーの待ち受けポート。tcpbin の TLS エコーは 4243、HTTPS は 443、MQTT over TLS は 8883。マニュアルの例では 8010／8011 を使っています。",
  "サーバーの待ち受けポート。tcpbin の TLS エコーは 4243、HTTPS は 443、MQTT over TLS は 8883。"),
 'de-DE': (
  " Die Vorgabe tcpbin.com:4243 ist ein TLS-Echodienst (im P5-Lauf am 2026-08-07 als funktionierend bestätigt). ⚠ Er trennt schon nach 15 Sekunden Leerlauf, senden Sie also zügig, sobald die Verbindung steht; außerdem antwortet er zeilenweise — ohne abschließenden Zeilenumbruch kommt die Nutzlast nie zurück.",
  " Auch die Vorgabe tcpbin.com:4243 trennt nach 15 Sekunden Leerlauf und antwortet zeilenweise.",
  "Der Port, auf dem der Server lauscht. Das TLS-Echo von tcpbin liegt auf 4243, HTTPS auf 443, MQTT over TLS auf 8883. Die Handbuchbeispiele verwenden 8010 / 8011.",
  "Der Port, auf dem der Server lauscht. Das TLS-Echo von tcpbin liegt auf 4243, HTTPS auf 443, MQTT over TLS auf 8883."),
 'fr-FR': (
  " La valeur par défaut, tcpbin.com:4243, est un service d'écho TLS (vérifié fonctionnel lors de la campagne P5 du 2026-08-07). ⚠ Il coupe au bout de 15 secondes d'inactivité seulement : envoyez vos données sans tarder une fois connecté. Il renvoie ligne par ligne — une charge utile sans saut de ligne final ne revient jamais.",
  " La valeur par défaut tcpbin.com:4243 coupe elle aussi après 15 secondes d'inactivité et renvoie ligne par ligne.",
  "Le port d'écoute du serveur. L'écho TLS de tcpbin est sur 4243, HTTPS sur 443, MQTT over TLS sur 8883. Les exemples du manuel utilisent 8010 / 8011.",
  "Le port d'écoute du serveur. L'écho TLS de tcpbin est sur 4243, HTTPS sur 443, MQTT over TLS sur 8883."),
 'es-ES': (
  " El valor predeterminado, tcpbin.com:4243, es un servicio de eco TLS (comprobado en la tanda P5 del 2026-08-07). ⚠ Corta a los 15 segundos de inactividad, así que envía los datos en cuanto conectes; además responde línea a línea: una carga útil sin salto de línea final nunca vuelve.",
  " El valor predeterminado tcpbin.com:4243 también corta a los 15 segundos de inactividad y responde línea a línea.",
  "El puerto en que escucha el servidor. El eco TLS de tcpbin está en 4243, HTTPS en 443 y MQTT over TLS en 8883. Los ejemplos del manual usan 8010 / 8011.",
  "El puerto en que escucha el servidor. El eco TLS de tcpbin está en 4243, HTTPS en 443 y MQTT over TLS en 8883."),
 'pt-PT': (
  " A predefinição, tcpbin.com:4243, é um serviço de eco TLS (confirmado a funcionar na campanha P5 de 2026-08-07). ⚠ Desliga ao fim de apenas 15 segundos de inatividade, portanto envie os dados assim que ligar; além disso responde linha a linha — uma carga útil sem mudança de linha final nunca volta.",
  " A predefinição tcpbin.com:4243 também desliga ao fim de 15 segundos de inatividade e responde linha a linha.",
  "A porta onde o servidor escuta. O eco TLS do tcpbin está na 4243, HTTPS na 443 e MQTT over TLS na 8883. Os exemplos do manual usam 8010 / 8011.",
  "A porta onde o servidor escuta. O eco TLS do tcpbin está na 4243, HTTPS na 443 e MQTT over TLS na 8883."),
 'it-IT': (
  " Il valore predefinito, tcpbin.com:4243, è un servizio di eco TLS (verificato funzionante nella sessione P5 del 2026-08-07). ⚠ Chiude dopo appena 15 secondi di inattività, quindi invia i dati appena connesso; inoltre risponde riga per riga: un payload senza newline finale non torna mai indietro.",
  " Anche il predefinito tcpbin.com:4243 chiude dopo 15 secondi di inattività e risponde riga per riga.",
  "La porta su cui il server è in ascolto. L'eco TLS di tcpbin è la 4243, HTTPS la 443, MQTT over TLS la 8883. Gli esempi del manuale usano 8010 / 8011.",
  "La porta su cui il server è in ascolto. L'eco TLS di tcpbin è la 4243, HTTPS la 443, MQTT over TLS la 8883."),
 'ru-RU': (
  " Значение по умолчанию, tcpbin.com:4243, — это TLS-эхо-сервис (работоспособность подтверждена в прогоне P5 от 2026-08-07). ⚠ Он разрывает связь всего через 15 секунд простоя, поэтому отправляйте данные сразу после подключения; кроме того, он отвечает построчно — полезная нагрузка без завершающего перевода строки не вернётся никогда.",
  " Значение по умолчанию tcpbin.com:4243 точно так же разрывает связь через 15 секунд простоя и отвечает построчно.",
  "Порт, который слушает сервер. TLS-эхо у tcpbin — 4243, HTTPS — 443, MQTT over TLS — 8883. В примерах руководства используются 8010 / 8011.",
  "Порт, который слушает сервер. TLS-эхо у tcpbin — 4243, HTTPS — 443, MQTT over TLS — 8883."),
 'vi-VN': (
  " Mặc định tcpbin.com:4243 là dịch vụ echo TLS (đã kiểm chứng chạy được trong đợt P5 ngày 2026-08-07). ⚠ Nó chỉ chờ 15 giây là ngắt, nên kết nối xong phải gửi dữ liệu ngay; ngoài ra nó vọng theo từng dòng — payload không có ký tự xuống dòng ở cuối thì sẽ không bao giờ được gửi lại.",
  " Mặc định tcpbin.com:4243 cũng ngắt sau 15 giây rảnh và cũng vọng theo từng dòng.",
  "Cổng mà máy chủ lắng nghe. Echo TLS của tcpbin là 4243, HTTPS là 443, MQTT over TLS là 8883. Ví dụ trong sổ tay dùng 8010 / 8011.",
  "Cổng mà máy chủ lắng nghe. Echo TLS của tcpbin là 4243, HTTPS là 443, MQTT over TLS là 8883."),
 'id-ID': (
  " Nilai bawaan tcpbin.com:4243 adalah layanan echo TLS (terbukti jalan pada rangkaian P5 tanggal 2026-08-07). ⚠ Ia memutus hanya setelah 15 detik menganggur, jadi begitu tersambung segeralah mengirim data; selain itu ia menggemakan baris per baris — payload tanpa baris baru di ujung tidak akan pernah dikembalikan.",
  " Nilai bawaan tcpbin.com:4243 juga memutus setelah 15 detik menganggur dan menggemakan baris per baris.",
  "Port yang didengarkan server. Echo TLS milik tcpbin ada di 4243, HTTPS di 443, MQTT over TLS di 8883. Contoh di manual memakai 8010 / 8011.",
  "Port yang didengarkan server. Echo TLS milik tcpbin ada di 4243, HTTPS di 443, MQTT over TLS di 8883."),
 'ms-MY': (
  " Nilai lalai tcpbin.com:4243 ialah perkhidmatan gema TLS (disahkan berfungsi dalam pusingan P5 pada 2026-08-07). ⚠ Ia memutuskan selepas hanya 15 saat melahu, jadi sebaik tersambung hantarlah data dengan segera; ia juga menggemakan baris demi baris — muatan tanpa baris baharu di hujung tidak akan dipulangkan.",
  " Nilai lalai tcpbin.com:4243 turut memutuskan selepas 15 saat melahu dan menggemakan baris demi baris.",
  "Port yang didengari pelayan. Gema TLS tcpbin ialah 4243, HTTPS ialah 443, MQTT over TLS ialah 8883. Contoh dalam manual menggunakan 8010 / 8011.",
  "Port yang didengari pelayan. Gema TLS tcpbin ialah 4243, HTTPS ialah 443, MQTT over TLS ialah 8883."),
 'th-TH': (
  " ค่าเริ่มต้น tcpbin.com:4243 เป็นบริการ echo แบบ TLS (ทดสอบแล้วใช้ได้ในรอบ P5 เมื่อ 2026-08-07) ⚠ มันตัดการเชื่อมต่อเมื่อว่างเพียง 15 วินาที ดังนั้นพอเชื่อมต่อได้ให้รีบส่งข้อมูล และมันสะท้อนกลับทีละบรรทัด — payload ที่ไม่มีอักขระขึ้นบรรทัดใหม่ต่อท้ายจะไม่ถูกส่งกลับ",
  " ค่าเริ่มต้น tcpbin.com:4243 ก็ตัดการเชื่อมต่อเมื่อว่าง 15 วินาทีเช่นกัน และสะท้อนกลับทีละบรรทัด",
  "พอร์ตที่เซิร์ฟเวอร์รอรับ echo แบบ TLS ของ tcpbin คือ 4243, HTTPS คือ 443, MQTT over TLS คือ 8883 ตัวอย่างในคู่มือใช้ 8010／8011",
  "พอร์ตที่เซิร์ฟเวอร์รอรับ echo แบบ TLS ของ tcpbin คือ 4243, HTTPS คือ 443, MQTT over TLS คือ 8883"),
 'hi-IN': (
  " डिफ़ॉल्ट tcpbin.com:4243 एक TLS एको सेवा है (2026-08-07 की P5 दौड़ में चलती हुई सत्यापित)। ⚠ यह मात्र 15 सेकंड निष्क्रिय रहने पर काट देती है, इसलिए जुड़ते ही डेटा भेज दीजिए; और यह पंक्ति-दर-पंक्ति लौटाती है — अंत में नई पंक्ति के बिना payload कभी वापस नहीं आता।",
  " डिफ़ॉल्ट tcpbin.com:4243 भी 15 सेकंड निष्क्रियता पर काट देती है और पंक्ति-दर-पंक्ति लौटाती है।",
  "वह पोर्ट जिस पर सर्वर सुनता है। tcpbin का TLS एको 4243 पर है, HTTPS 443 पर, MQTT over TLS 8883 पर। नियमावली के उदाहरण 8010 / 8011 का उपयोग करते हैं।",
  "वह पोर्ट जिस पर सर्वर सुनता है। tcpbin का TLS एको 4243 पर है, HTTPS 443 पर, MQTT over TLS 8883 पर।"),
 'tr-TR': (
  " Varsayılan tcpbin.com:4243 bir TLS yankı hizmetidir (2026-08-07 tarihli P5 turunda çalıştığı doğrulandı). ⚠ Yalnızca 15 saniye boşta kaldıktan sonra bağlantıyı keser, bu yüzden bağlanır bağlanmaz verinizi gönderin; ayrıca satır satır yankılar — sonunda satır sonu olmayan bir yük asla geri dönmez.",
  " Varsayılan tcpbin.com:4243 de 15 saniye boştalıktan sonra keser ve satır satır yankılar.",
  "Sunucunun dinlediği bağlantı noktası. tcpbin'in TLS yankısı 4243, HTTPS 443, MQTT over TLS 8883'tür. Kılavuzdaki örneklerde 8010 / 8011 kullanılır.",
  "Sunucunun dinlediği bağlantı noktası. tcpbin'in TLS yankısı 4243, HTTPS 443, MQTT over TLS 8883'tür."),
 'ar-SA': (
  " والقيمة الافتراضية tcpbin.com:4243 خدمةُ صدى عبر TLS (ثبت عملها في جولة P5 يوم 2026-08-07). ⚠ وهي تقطع الاتصال بعد 15 ثانية خمول فقط، فأرسل بياناتك فور الاتصال؛ كما أنها تُعيد الصدى سطراً بسطر —— فالحمولة التي لا تنتهي بسطر جديد لا تعود أبداً.",
  " والقيمة الافتراضية tcpbin.com:4243 تقطع كذلك بعد 15 ثانية خمول وتُعيد الصدى سطراً بسطر.",
  "المنفذ الذي يستمع عليه الخادم. صدى TLS في tcpbin هو 4243، وHTTPS هو 443، وMQTT over TLS هو 8883. وأمثلة الدليل تستعمل 8010 / 8011.",
  "المنفذ الذي يستمع عليه الخادم. صدى TLS في tcpbin هو 4243، وHTTPS هو 443، وMQTT over TLS هو 8883."),
 'he-IL': (
  " ברירת המחדל tcpbin.com:4243 היא שירות הד מבוסס TLS (נבדק ופעל בסבב P5 ב-2026-08-07). ⚠ הוא מנתק כבר לאחר 15 שניות של חוסר פעילות, אז שלח את הנתונים מיד עם ההתחברות; בנוסף הוא מהדהד שורה-שורה — מטען ללא ירידת שורה בסופו לא יחזור לעולם.",
  " גם ברירת המחדל tcpbin.com:4243 מנתקת לאחר 15 שניות של חוסר פעילות ומהדהדת שורה-שורה.",
  "הפורט שבו השרת מאזין. ההד המוצפן של tcpbin נמצא ב-4243, HTTPS ב-443, ו-MQTT over TLS ב-8883. הדוגמאות במדריך משתמשות ב-8010 / 8011.",
  "הפורט שבו השרת מאזין. ההד המוצפן של tcpbin נמצא ב-4243, HTTPS ב-443, ו-MQTT over TLS ב-8883."),
 'fa-IR': (
  " مقدار پیش‌فرض tcpbin.com:4243 یک سرویس پژواک روی TLS است (کارکردنش در دور P5 در ۲۰۲۶-۰۸-۰۷ وارسی شد). ⚠ تنها پس از ۱۵ ثانیه بی‌کاری قطع می‌کند، پس همین که وصل شدید داده را بفرستید؛ ضمناً سطر به سطر پژواک می‌دهد —— باری که در پایانش خط جدید نباشد هرگز بازنمی‌گردد.",
  " مقدار پیش‌فرض tcpbin.com:4243 نیز پس از ۱۵ ثانیه بی‌کاری قطع می‌کند و سطر به سطر پژواک می‌دهد.",
  "درگاهی که کارساز روی آن گوش می‌دهد. پژواک TLS در tcpbin برابر 4243، ‏HTTPS برابر 443 و MQTT over TLS برابر 8883 است. نمونه‌های راهنما از 8010 / 8011 استفاده می‌کنند.",
  "درگاهی که کارساز روی آن گوش می‌دهد. پژواک TLS در tcpbin برابر 4243، ‏HTTPS برابر 443 و MQTT over TLS برابر 8883 است."),
}


def prev_of(lang, key):
    for b in BATCHES:
        p = os.path.join(ROOT, 'i18n', b, lang + '.json')
        if os.path.exists(p):
            d = json.load(io.open(p, encoding='utf-8'))
            if d.get(key):
                return d[key]
    raise SystemExit('%s：找不到舊譯文 %s' % (lang, key[:30]))


def main():
    os.makedirs(OUT, exist_ok=True)
    k_buf = next(k for k in KEYS if k.startswith(OLD_BUF_HOST[:20]) and 'tcpbin' in k)
    k_push = next(k for k in KEYS if '<access_mode>=1' in k)
    k_port_manual = next(k for k in KEYS if '手冊範例用 8010' in k)
    k_port_plain = next(k for k in KEYS if k.startswith('伺服器的監聽埠') and '手冊範例' not in k)
    for lang, (add_buf, add_push, port_manual, port_plain) in T.items():
        out = {
            k_buf: prev_of(lang, OLD_BUF_HOST) + add_buf,
            k_push: prev_of(lang, OLD_PUSH_HOST) + add_push,
            k_port_manual: port_manual,
            k_port_plain: port_plain,
        }
        json.dump(out, io.open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('  %-7s %d 條' % (lang, len(out)))
    print('完成 %d 種語言' % len(T))


if __name__ == '__main__':
    main()
