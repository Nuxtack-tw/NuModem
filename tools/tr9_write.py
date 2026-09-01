# -*- coding: utf-8 -*-
"""第三批補譯：MQTT client ID／主題改用隨機尾碼後受影響的四條說明。

broker 那條 200 字的說明只改了一個子句，所以沿用 tr7 的譯文再替換該子句 ——
整段重譯不但浪費，也容易讓同一段話在兩批之間出現不一致的措辭。
替換失敗會直接報錯，不會默默把舊句子留著。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr9-source.json'), encoding='utf-8'))
OLD_BROKER_KEY_MARK = 'MQTT broker 的域名或 IP'
OUT = os.path.join(ROOT, 'i18n', 'tr9')

# 每個語言：(broker 說明裡要被換掉的舊子句, 新子句, client ID 說明, 訂閱主題說明, 發布主題說明)
T = {
 'en-US': (
  "Never send real data while testing, and add a random suffix to your topic.",
  "Never send real data while testing; this tool already appends a random suffix to both the topic and the client ID, and draws a new one on every reload.",
  "MQTT client identifier. The random suffix in the default value is generated when this page loads and changes on every reload — a fixed value is deliberately avoided, because on a public broker a duplicate client ID gets the earlier connection kicked off.",
  "The MQTT topic to subscribe to; wildcards are allowed (+ for one level, # for many). The default topic carries a random suffix so that you do not pick up other people's messages on a public broker — with a fixed topic your self-loopback check may receive something you did not send, which makes the check worthless.",
  "The MQTT topic to publish to. The random suffix in the default is the same one used by the Subscribe button — if you want the self-loopback check to work, do not change only one side."),
 'ja-JP': (
  "テスト中は実データを絶対に送らず、トピックにはランダムな接尾辞を付けてください。",
  "テスト中は実データを絶対に送らないでください。トピックと client ID のランダム接尾辞は本ツールが自動で付けます（再読み込みのたびに変わります）。",
  "MQTT クライアント識別子。既定値のランダム接尾辞はこのページの読み込み時に生成され、再読み込みのたびに変わります。固定値をあえて使わないのは、公開ブローカーでは client ID が重複すると先に接続していた方が切断されるためです",
  "購読する MQTT トピック。ワイルドカード（+ は 1 階層、# は複数階層）が使えます。既定のトピックにランダム接尾辞が付いているのは、公開ブローカーで他人のメッセージを拾わないためです。固定トピックにすると、自分が送っていないものを受け取ることがあり、自己ループバック検証の意味がなくなります",
  "発行先の MQTT トピック。既定のランダム接尾辞は Subscribe ボタンと同じものです。自己ループバック検証をするなら片方だけ変えないでください"),
 'de-DE': (
  "Senden Sie beim Testen niemals echte Daten und hängen Sie an Ihr Topic ein zufälliges Suffix an.",
  "Senden Sie beim Testen niemals echte Daten; ein zufälliges Suffix für Topic und Client-ID hängt dieses Werkzeug bereits selbst an und würfelt es bei jedem Neuladen neu.",
  "MQTT-Client-Kennung. Das zufällige Suffix im Vorgabewert entsteht beim Laden dieser Seite und ändert sich bei jedem Neuladen — ein fester Wert wird bewusst vermieden, denn bei einer doppelten Client-ID wirft ein öffentlicher Broker die zuerst bestehende Verbindung hinaus.",
  "Das MQTT-Topic, das abonniert werden soll; Platzhalter sind erlaubt (+ für eine Ebene, # für mehrere). Das voreingestellte Topic trägt ein zufälliges Suffix, damit Sie auf einem öffentlichen Broker keine fremden Nachrichten aufschnappen — mit einem festen Topic kann Ihre Selbstschleifen-Prüfung etwas empfangen, das Sie gar nicht gesendet haben, und ist damit wertlos.",
  "Das MQTT-Topic, in das veröffentlicht wird. Das zufällige Suffix der Vorgabe ist dasselbe wie bei der Schaltfläche Subscribe — wenn die Selbstschleifen-Prüfung funktionieren soll, ändern Sie nicht nur eine Seite."),
 'fr-FR': (
  "N'envoyez jamais de données réelles pendant les tests et ajoutez un suffixe aléatoire à votre sujet.",
  "N'envoyez jamais de données réelles pendant les tests ; cet outil ajoute déjà un suffixe aléatoire au sujet et à l'identifiant client, et en tire un nouveau à chaque rechargement.",
  "Identifiant du client MQTT. Le suffixe aléatoire de la valeur par défaut est produit au chargement de cette page et change à chaque rechargement — une valeur fixe est délibérément évitée, car sur un broker public un identifiant client en double fait éjecter la connexion établie en premier.",
  "Le sujet MQTT auquel s'abonner ; les jokers sont acceptés (+ pour un niveau, # pour plusieurs). Le sujet par défaut porte un suffixe aléatoire afin de ne pas capter les messages d'autrui sur un broker public — avec un sujet fixe, votre vérification en boucle peut recevoir quelque chose que vous n'avez pas envoyé, ce qui la rend inutile.",
  "Le sujet MQTT de publication. Le suffixe aléatoire par défaut est le même que celui du bouton Subscribe — pour que la vérification en boucle fonctionne, ne modifiez pas un seul des deux côtés."),
 'es-ES': (
  "Nunca envíes datos reales durante las pruebas y añade un sufijo aleatorio a tu tema.",
  "Nunca envíes datos reales durante las pruebas; esta herramienta ya añade un sufijo aleatorio al tema y al identificador de cliente, y genera uno nuevo en cada recarga.",
  "Identificador del cliente MQTT. El sufijo aleatorio del valor predeterminado se genera al cargar esta página y cambia en cada recarga; se evita a propósito un valor fijo, porque en un bróker público un identificador de cliente repetido hace que se expulse a la conexión que llegó primero.",
  "El tema MQTT al que suscribirse; se admiten comodines (+ para un nivel, # para varios). El tema predeterminado lleva un sufijo aleatorio para que no recojas mensajes ajenos en un bróker público: con un tema fijo tu comprobación de bucle propio puede recibir algo que no enviaste tú, y entonces no comprueba nada.",
  "El tema MQTT al que publicar. El sufijo aleatorio del valor predeterminado es el mismo que usa el botón Subscribe: si quieres que funcione la comprobación de bucle propio, no cambies solo uno de los dos lados."),
 'pt-PT': (
  "Nunca envie dados reais durante os testes e acrescente um sufixo aleatório ao seu tópico.",
  "Nunca envie dados reais durante os testes; esta ferramenta já acrescenta um sufixo aleatório ao tópico e ao identificador de cliente, e gera um novo a cada recarregamento.",
  "Identificador do cliente MQTT. O sufixo aleatório do valor predefinido é gerado ao carregar esta página e muda a cada recarregamento; evita-se de propósito um valor fixo, porque num broker público um identificador de cliente repetido faz expulsar a ligação que chegou primeiro.",
  "O tópico MQTT a subscrever; são aceites caracteres universais (+ para um nível, # para vários). O tópico predefinido leva um sufixo aleatório para não apanhar mensagens de outras pessoas num broker público — com um tópico fixo, a verificação em circuito fechado pode receber algo que não foi você a enviar, e deixa de verificar seja o que for.",
  "O tópico MQTT para onde publicar. O sufixo aleatório da predefinição é o mesmo que o botão Subscribe usa — para a verificação em circuito fechado funcionar, não altere apenas um dos lados."),
 'it-IT': (
  "Non inviare mai dati reali durante i test e aggiungi un suffisso casuale al tuo topic.",
  "Non inviare mai dati reali durante i test; questo strumento aggiunge già un suffisso casuale al topic e al client ID, e ne genera uno nuovo a ogni ricaricamento.",
  "Identificatore del client MQTT. Il suffisso casuale del valore predefinito viene generato al caricamento di questa pagina e cambia a ogni ricaricamento: un valore fisso è evitato di proposito, perché su un broker pubblico un client ID duplicato fa espellere la connessione arrivata per prima.",
  "Il topic MQTT a cui iscriversi; sono ammessi i caratteri jolly (+ per un livello, # per più livelli). Il topic predefinito porta un suffisso casuale per non raccogliere messaggi altrui su un broker pubblico: con un topic fisso la verifica ad anello può ricevere qualcosa che non hai inviato tu, e quindi non verifica nulla.",
  "Il topic MQTT su cui pubblicare. Il suffisso casuale predefinito è lo stesso usato dal pulsante Subscribe: se vuoi che la verifica ad anello funzioni, non cambiare solo uno dei due lati."),
 'ru-RU': (
  "Никогда не отправляйте реальные данные во время тестов и добавляйте к топику случайный суффикс.",
  "Никогда не отправляйте реальные данные во время тестов; случайный суффикс к топику и client ID этот инструмент добавляет сам и меняет его при каждой перезагрузке страницы.",
  "Идентификатор клиента MQTT. Случайный суффикс в значении по умолчанию создаётся при загрузке страницы и меняется при каждой перезагрузке — фиксированное значение намеренно не используется, потому что на публичном брокере при совпадении client ID выбрасывается то соединение, которое подключилось раньше.",
  "Топик MQTT для подписки; допускаются подстановочные знаки (+ — один уровень, # — несколько). У топика по умолчанию есть случайный суффикс, чтобы вы не подхватывали чужие сообщения на публичном брокере: с фиксированным топиком проверка «отправил себе — получил» может принять то, чего вы не отправляли, и потому ничего не проверяет.",
  "Топик MQTT для публикации. Случайный суффикс по умолчанию тот же, что и у кнопки Subscribe: чтобы проверка «отправил себе — получил» работала, не меняйте только одну сторону."),
 'vi-VN': (
  "Tuyệt đối không gửi dữ liệu thật khi thử nghiệm, và hãy thêm hậu tố ngẫu nhiên vào topic.",
  "Tuyệt đối không gửi dữ liệu thật khi thử nghiệm; hậu tố ngẫu nhiên cho topic và client ID đã được công cụ này tự thêm, và đổi mỗi lần tải lại trang.",
  "Định danh client MQTT. Hậu tố ngẫu nhiên trong giá trị mặc định được sinh ra lúc tải trang và đổi mỗi lần tải lại — cố ý không dùng giá trị cố định, vì trên broker công cộng hễ client ID trùng nhau thì kết nối vào trước sẽ bị đá ra.",
  "Topic MQTT cần đăng ký; dùng được ký tự đại diện (+ một tầng, # nhiều tầng). Topic mặc định có hậu tố ngẫu nhiên để bạn không nhặt phải tin của người khác trên broker công cộng — để topic cố định thì phép thử tự gửi tự nhận có thể nhận về thứ không phải bạn gửi, coi như thử vô ích.",
  "Topic MQTT để phát tin. Hậu tố ngẫu nhiên mặc định trùng với nút Subscribe — muốn phép thử tự gửi tự nhận chạy đúng thì đừng chỉ sửa một bên."),
 'id-ID': (
  "Jangan pernah mengirim data sungguhan saat pengujian, dan tambahkan akhiran acak pada topik Anda.",
  "Jangan pernah mengirim data sungguhan saat pengujian; akhiran acak untuk topik dan client ID sudah ditambahkan sendiri oleh alat ini, dan diganti setiap kali halaman dimuat ulang.",
  "Pengenal klien MQTT. Akhiran acak pada nilai bawaan dibuat saat halaman ini dimuat dan berganti setiap kali dimuat ulang — nilai tetap sengaja dihindari, sebab pada broker publik client ID yang kembar membuat koneksi yang lebih dulu tersambung ditendang keluar.",
  "Topik MQTT yang akan dilanggan; kartu bebas boleh dipakai (+ untuk satu tingkat, # untuk banyak tingkat). Topik bawaan memakai akhiran acak supaya Anda tidak memungut pesan orang lain di broker publik — dengan topik tetap, uji gema-diri bisa menerima sesuatu yang bukan Anda kirim, jadi tidak menguji apa pun.",
  "Topik MQTT tujuan penerbitan. Akhiran acak pada nilai bawaan sama dengan yang dipakai tombol Subscribe — kalau ingin uji gema-diri berjalan, jangan hanya mengubah satu sisi."),
 'ms-MY': (
  "Jangan sekali-kali menghantar data sebenar semasa ujian, dan tambahkan akhiran rawak pada topik anda.",
  "Jangan sekali-kali menghantar data sebenar semasa ujian; akhiran rawak bagi topik dan client ID sudah ditambah sendiri oleh alat ini, dan ditukar setiap kali halaman dimuat semula.",
  "Pengecam klien MQTT. Akhiran rawak pada nilai lalai dijana semasa halaman ini dimuatkan dan berubah setiap kali dimuat semula — nilai tetap sengaja dielakkan, kerana pada broker awam client ID yang sama membuatkan sambungan yang masuk dahulu ditendang keluar.",
  "Topik MQTT yang hendak dilanggan; kad liar dibenarkan (+ untuk satu aras, # untuk banyak aras). Topik lalai membawa akhiran rawak supaya anda tidak memungut mesej orang lain pada broker awam — dengan topik tetap, ujian gema sendiri boleh menerima sesuatu yang bukan anda hantar, jadi ia tidak menguji apa-apa.",
  "Topik MQTT tempat penerbitan. Akhiran rawak pada nilai lalai sama dengan yang digunakan butang Subscribe — jika mahu ujian gema sendiri berfungsi, jangan ubah satu pihak sahaja."),
 'th-TH': (
  "ห้ามส่งข้อมูลจริงระหว่างทดสอบโดยเด็ดขาด และควรเติมส่วนท้ายแบบสุ่มให้หัวข้อของคุณ",
  "ห้ามส่งข้อมูลจริงระหว่างทดสอบโดยเด็ดขาด ส่วนส่วนท้ายแบบสุ่มของหัวข้อและ client ID นั้นเครื่องมือนี้เติมให้อัตโนมัติแล้ว และจะสุ่มใหม่ทุกครั้งที่โหลดหน้าใหม่",
  "ตัวระบุไคลเอนต์ MQTT ส่วนท้ายแบบสุ่มในค่าเริ่มต้นถูกสร้างตอนโหลดหน้านี้ และเปลี่ยนทุกครั้งที่โหลดใหม่ — จงใจไม่ใช้ค่าคงที่ เพราะบนโบรกเกอร์สาธารณะถ้า client ID ซ้ำกัน ตัวที่เชื่อมต่อก่อนจะถูกเตะออก",
  "หัวข้อ MQTT ที่จะสับสไครบ์ ใช้อักขระแทนได้ (+ หนึ่งชั้น, # หลายชั้น) หัวข้อเริ่มต้นมีส่วนท้ายแบบสุ่มเพื่อไม่ให้ไปรับข้อความของคนอื่นบนโบรกเกอร์สาธารณะ — ถ้าเปลี่ยนเป็นหัวข้อคงที่ การทดสอบส่งหาตัวเองอาจได้รับสิ่งที่ไม่ได้ส่งเอง เท่ากับทดสอบเปล่า ๆ",
  "หัวข้อ MQTT ที่จะเผยแพร่ ส่วนท้ายแบบสุ่มในค่าเริ่มต้นเป็นชุดเดียวกับปุ่ม Subscribe — ถ้าจะทดสอบส่งหาตัวเอง อย่าแก้แค่ด้านเดียว"),
 'hi-IN': (
  "परीक्षण के दौरान असली डेटा कभी न भेजें, और अपने विषय में यादृच्छिक प्रत्यय जोड़ें।",
  "परीक्षण के दौरान असली डेटा कभी न भेजें; विषय और client ID का यादृच्छिक प्रत्यय यह उपकरण स्वयं जोड़ देता है, और हर बार पृष्ठ लोड होने पर नया बना देता है।",
  "MQTT क्लाइंट पहचानकर्ता। डिफ़ॉल्ट मान का यादृच्छिक प्रत्यय इस पृष्ठ के लोड होते समय बनता है और हर बार दोबारा लोड करने पर बदल जाता है — स्थिर मान जान-बूझकर नहीं रखा गया, क्योंकि सार्वजनिक ब्रोकर पर client ID दोहराने से पहले जुड़ा कनेक्शन बाहर कर दिया जाता है।",
  "जिस MQTT विषय की सदस्यता लेनी है; वाइल्डकार्ड चलते हैं (+ एक स्तर, # कई स्तर)। डिफ़ॉल्ट विषय में यादृच्छिक प्रत्यय इसलिए है कि सार्वजनिक ब्रोकर पर दूसरों के संदेश आपके पास न आएँ — स्थिर विषय रखने पर आपकी स्व-लूपबैक जाँच वह चीज़ पा सकती है जो आपने भेजी ही नहीं, यानी जाँच बेकार।",
  "जिस MQTT विषय पर प्रकाशित करना है। डिफ़ॉल्ट का यादृच्छिक प्रत्यय वही है जो Subscribe बटन उपयोग करता है — स्व-लूपबैक जाँच चलानी है तो केवल एक ही पक्ष मत बदलिए।"),
 'tr-TR': (
  "Test sırasında asla gerçek veri göndermeyin ve konunuza rastgele bir sonek ekleyin.",
  "Test sırasında asla gerçek veri göndermeyin; konuya ve client ID'ye rastgele soneki bu araç zaten kendisi ekliyor ve her yeniden yüklemede yenisini üretiyor.",
  "MQTT istemci tanımlayıcısı. Varsayılan değerdeki rastgele sonek bu sayfa yüklenirken üretilir ve her yeniden yüklemede değişir — sabit bir değer bilerek kullanılmaz, çünkü herkese açık bir aracıda aynı client ID önce kurulmuş bağlantıyı dışarı attırır.",
  "Abone olunacak MQTT konusu; joker karakterler kullanılabilir (+ tek düzey, # çok düzey). Varsayılan konu, herkese açık bir aracıda başkalarının iletilerini toplamayasınız diye rastgele sonek taşır — sabit bir konuda kendi kendine döngü denetiminiz göndermediğiniz bir şeyi alabilir ve denetim hiçbir şey doğrulamamış olur.",
  "Yayımlanacak MQTT konusu. Varsayılandaki rastgele sonek, Subscribe düğmesinin kullandığıyla aynıdır — kendi kendine döngü denetiminin çalışmasını istiyorsanız yalnızca bir tarafı değiştirmeyin."),
 'ar-SA': (
  "لا ترسل بيانات حقيقية أثناء الاختبار أبداً، وأضف لاحقة عشوائية إلى موضوعك.",
  "لا ترسل بيانات حقيقية أثناء الاختبار أبداً؛ أما اللاحقة العشوائية للموضوع ولمعرّف العميل فتضيفها هذه الأداة تلقائياً وتولّد غيرها مع كل إعادة تحميل.",
  "معرّف عميل MQTT. اللاحقة العشوائية في القيمة الافتراضية تُولَّد عند تحميل هذه الصفحة وتتغير مع كل إعادة تحميل — وقد تُجُنِّبت القيمة الثابتة عن قصد، لأن تكرار معرّف العميل على وسيط عمومي يجعل الاتصال الأسبق يُطرَد.",
  "موضوع MQTT المراد الاشتراك فيه؛ وتُقبل المحارف البديلة (+ لمستوى واحد و# لعدة مستويات). الموضوع الافتراضي يحمل لاحقة عشوائية كي لا تلتقط رسائل الآخرين على وسيط عمومي — فمع موضوع ثابت قد يستقبل فحص الحلقة الذاتية شيئاً لم ترسله أنت، فلا يعود يفحص شيئاً.",
  "موضوع MQTT الذي سيُنشَر فيه. اللاحقة العشوائية في القيمة الافتراضية هي نفسها التي يستعملها زر Subscribe — فإن أردت لفحص الحلقة الذاتية أن يعمل فلا تغيّر جانباً واحداً فقط."),
 'he-IL': (
  "אל תשלח לעולם נתונים אמיתיים בזמן בדיקות, והוסף סיומת אקראית לנושא שלך.",
  "אל תשלח לעולם נתונים אמיתיים בזמן בדיקות; סיומת אקראית לנושא ולמזהה הלקוח כבר מתווספת על ידי הכלי עצמו, ומוגרלת מחדש בכל טעינה.",
  "מזהה לקוח MQTT. הסיומת האקראית שבערך ברירת המחדל נוצרת בעת טעינת הדף ומשתנה בכל טעינה מחדש — ערך קבוע נמנע בכוונה, משום שבברוקר ציבורי מזהה לקוח כפול גורם לניתוק החיבור שהתחבר קודם.",
  "הנושא שאליו נרשמים ב-MQTT; מותרים תווים כלליים (+ לרמה אחת, # לכמה רמות). הנושא שבברירת המחדל נושא סיומת אקראית כדי שלא תקלוט הודעות של אחרים בברוקר ציבורי — עם נושא קבוע בדיקת הלולאה העצמית עלולה לקבל משהו שלא אתה שלחת, וכך אינה בודקת דבר.",
  "הנושא שאליו מפרסמים ב-MQTT. הסיומת האקראית בברירת המחדל זהה לזו של כפתור Subscribe — אם ברצונך שבדיקת הלולאה העצמית תעבוד, אל תשנה רק צד אחד."),
 'fa-IR': (
  "هنگام آزمایش هرگز دادهٔ واقعی نفرستید و به موضوع خود یک پسوند تصادفی بیفزایید.",
  "هنگام آزمایش هرگز دادهٔ واقعی نفرستید؛ پسوند تصادفیِ موضوع و شناسهٔ کارخواه را خودِ این ابزار می‌افزاید و با هر بار بارگذاری دوباره تولید می‌کند.",
  "شناسهٔ کارخواه MQTT. پسوند تصادفی در مقدار پیش‌فرض هنگام بارگذاری این صفحه ساخته می‌شود و با هر بار بارگذاری تغییر می‌کند — مقدار ثابت عمداً به کار نرفته است، چون روی کارگزار عمومی اگر شناسهٔ کارخواه تکراری باشد، اتصالی که زودتر برقرار شده بیرون انداخته می‌شود.",
  "موضوع MQTT برای اشتراک؛ نویسه‌های جایگزین مجازند (+ یک لایه، # چند لایه). موضوع پیش‌فرض پسوند تصادفی دارد تا روی کارگزار عمومی پیام دیگران را برندارید — با موضوع ثابت، آزمون بازگشت به خود ممکن است چیزی بگیرد که شما نفرستاده‌اید و در نتیجه هیچ چیز را نمی‌سنجد.",
  "موضوع MQTT برای انتشار. پسوند تصادفی پیش‌فرض همان است که دکمهٔ Subscribe به کار می‌برد — اگر می‌خواهید آزمون بازگشت به خود کار کند، تنها یک سو را تغییر ندهید."),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    broker_key = next(k for k in KEYS if OLD_BROKER_KEY_MARK in k)
    others = [k for k in KEYS if k != broker_key]
    assert len(others) == 3, '預期 3 條新說明，實得 %d' % len(others)
    for lang, (old_c, new_c, t_cid, t_sub, t_pub) in T.items():
        prev = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr7', lang + '.json'), encoding='utf-8'))
        old_broker = next(v for k, v in prev.items() if OLD_BROKER_KEY_MARK in k)
        assert old_c in old_broker, '%s：舊子句對不上，不敢盲改' % lang
        out = {broker_key: old_broker.replace(old_c, new_c, 1)}
        for k, v in zip(others, [t_cid, t_sub, t_pub]):
            out[k] = v
        json.dump(out, io.open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('  %-7s 4 條' % lang)
    print('完成 %d 種語言' % len(T))


if __name__ == '__main__':
    main()
