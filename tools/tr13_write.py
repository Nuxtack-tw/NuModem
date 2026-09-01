r"""第七批補譯：P6 FTP 實測後改寫的兩條說明。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr13-source.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'i18n', 'tr13')

T = {
 'en-US': [
  "Log out of the FTP(S) server. ⚠ The OK that comes back immediately only means the command was accepted — the session is not closed until +QFTPCLOSE: 0,0 arrives. In between the state is 3 (closing), and any FTP command issued then returns +CME ERROR: 603 (server busy). Measured in the P6 run on 2026-08-07: treating that OK as \"closed\" and reopening straight away produces a run of 603s that looks exactly like a broken module",
  "(the module masks the password with *, measured in the P6 run on 2026-08-07; only the text you type when setting it is in the clear)"],
 'ja-JP': [
  "FTP(S) サーバーからログアウトします。⚠ すぐ返る OK はコマンドを受け付けた意味しかありません —— +QFTPCLOSE: 0,0 が届くまでは閉じ終わっていません。その間の状態は 3（クローズ中）で、このとき FTP コマンドを送るとすべて +CME ERROR: 603（サーバービジー）が返ります。2026-08-07 の P6 実測：その OK を「閉じた」と解釈してすぐ再 QFTPOPEN すると 603 が続き、モジュールが壊れたようにしか見えません",
  "（パスワードはモジュールが * で伏せます。2026-08-07 の P6 実測。設定時に入力した原文だけが平文です）"],
 'de-DE': [
  "Vom FTP(S)-Server abmelden. ⚠ Das sofort zurückkommende OK bedeutet nur, dass der Befehl angenommen wurde — geschlossen ist die Sitzung erst, wenn +QFTPCLOSE: 0,0 eintrifft. Dazwischen ist der Zustand 3 (wird geschlossen), und jeder dann abgesetzte FTP-Befehl liefert +CME ERROR: 603 (Server ausgelastet). Im P6-Lauf am 2026-08-07 gemessen: wer dieses OK als „geschlossen“ liest und sofort neu öffnet, bekommt eine Kette von 603ern, die exakt wie ein defektes Modul aussieht",
  "(das Modul maskiert das Passwort mit *, gemessen im P6-Lauf am 2026-08-07; nur der beim Setzen eingegebene Text steht im Klartext)"],
 'fr-FR': [
  "Se déconnecter du serveur FTP(S). ⚠ Le OK qui revient tout de suite signifie seulement que la commande a été acceptée — la session n'est fermée qu'à l'arrivée de +QFTPCLOSE: 0,0. Entre les deux, l'état est 3 (fermeture en cours) et toute commande FTP émise alors renvoie +CME ERROR: 603 (serveur occupé). Mesuré lors de la campagne P6 du 2026-08-07 : prendre ce OK pour « c'est fermé » et rouvrir aussitôt produit une série de 603 qui ressemble exactement à un module en panne",
  "(le module masque le mot de passe par des *, mesuré lors de la campagne P6 du 2026-08-07 ; seul le texte saisi au moment du réglage est en clair)"],
 'es-ES': [
  "Cerrar sesión en el servidor FTP(S). ⚠ El OK que vuelve de inmediato solo significa que se aceptó el comando: la sesión no está cerrada hasta que llega +QFTPCLOSE: 0,0. Mientras tanto el estado es 3 (cerrando), y cualquier comando FTP que lances en ese momento devuelve +CME ERROR: 603 (servidor ocupado). Medido en la tanda P6 del 2026-08-07: tomar ese OK por «ya está cerrado» y reabrir en seguida produce una ristra de 603 que parece exactamente un módulo averiado",
  "(el módulo enmascara la contraseña con *, medido en la tanda P6 del 2026-08-07; solo el texto que escribes al configurarla va en claro)"],
 'pt-PT': [
  "Terminar sessão no servidor FTP(S). ⚠ O OK que volta de imediato significa apenas que o comando foi aceite — a sessão só está fechada quando chegar +QFTPCLOSE: 0,0. Entretanto o estado é 3 (a fechar) e qualquer comando FTP emitido nessa altura devolve +CME ERROR: 603 (servidor ocupado). Medido na campanha P6 de 2026-08-07: tomar esse OK por «já fechou» e reabrir logo a seguir produz uma série de 603 que parece exatamente um módulo avariado",
  "(o módulo mascara a palavra-passe com *, medido na campanha P6 de 2026-08-07; só o texto que escreve ao configurá-la fica em claro)"],
 'it-IT': [
  "Disconnettersi dal server FTP(S). ⚠ L'OK che torna subito significa solo che il comando è stato accettato: la sessione non è chiusa finché non arriva +QFTPCLOSE: 0,0. Nel frattempo lo stato è 3 (in chiusura) e qualsiasi comando FTP inviato in quel momento restituisce +CME ERROR: 603 (server occupato). Misurato nella sessione P6 del 2026-08-07: prendere quell'OK per «chiuso» e riaprire subito produce una sfilza di 603 che sembra esattamente un modulo guasto",
  "(il modulo maschera la password con *, misurato nella sessione P6 del 2026-08-07; solo il testo digitato quando la si imposta è in chiaro)"],
 'ru-RU': [
  "Выйти с FTP(S)-сервера. ⚠ Мгновенно возвращаемое OK означает лишь то, что команда принята, — сессия закрыта только тогда, когда придёт +QFTPCLOSE: 0,0. В промежутке состояние равно 3 (закрывается), и любая FTP-команда, отданная в это время, возвращает +CME ERROR: 603 (сервер занят). Измерено в прогоне P6 от 2026-08-07: принять это OK за «закрыто» и сразу открыть заново — значит получить череду 603, которая выглядит в точности как сломанный модуль",
  "(модуль маскирует пароль звёздочками, измерено в прогоне P6 от 2026-08-07; в открытом виде идёт только текст, который вы вводите при настройке)"],
 'vi-VN': [
  "Đăng xuất khỏi máy chủ FTP(S). ⚠ Chữ OK trả về ngay chỉ có nghĩa lệnh đã được nhận — phiên chỉ thực sự đóng khi +QFTPCLOSE: 0,0 tới. Trong khoảng đó trạng thái là 3 (đang đóng), và mọi lệnh FTP gửi lúc này đều trả về +CME ERROR: 603 (máy chủ bận). Đo được trong đợt P6 ngày 2026-08-07: coi chữ OK đó là «đóng xong» rồi mở lại ngay sẽ nhận một tràng 603 trông y hệt module bị hỏng",
  "(module che mật khẩu bằng dấu *, đo được trong đợt P6 ngày 2026-08-07; chỉ đoạn bạn gõ lúc thiết lập mới là chữ thường)"],
 'id-ID': [
  "Keluar dari server FTP(S). ⚠ OK yang langsung muncul hanya berarti perintah diterima — sesi baru benar-benar tertutup saat +QFTPCLOSE: 0,0 tiba. Di sela itu statusnya 3 (sedang menutup), dan perintah FTP apa pun yang dikirim saat itu akan menjawab +CME ERROR: 603 (server sibuk). Terukur pada rangkaian P6 tanggal 2026-08-07: menganggap OK itu sebagai «sudah tertutup» lalu membuka lagi seketika menghasilkan rentetan 603 yang persis mirip modul rusak",
  "(modul menyamarkan kata sandi dengan *, terukur pada rangkaian P6 tanggal 2026-08-07; hanya teks yang Anda ketik saat menyetelnya yang terbuka)"],
 'ms-MY': [
  "Log keluar daripada pelayan FTP(S). ⚠ OK yang muncul serta-merta hanya bermakna arahan diterima — sesi hanya benar-benar tertutup apabila +QFTPCLOSE: 0,0 tiba. Dalam selang itu keadaannya ialah 3 (sedang menutup), dan sebarang arahan FTP yang dihantar ketika itu akan membalas +CME ERROR: 603 (pelayan sibuk). Diukur pada pusingan P6 pada 2026-08-07: menganggap OK itu sebagai «sudah tutup» lalu membuka semula serta-merta menghasilkan rentetan 603 yang nampak persis seperti modul rosak",
  "(modul menyamarkan kata laluan dengan *, diukur pada pusingan P6 pada 2026-08-07; hanya teks yang anda taip semasa menetapkannya sahaja yang terdedah)"],
 'th-TH': [
  "ออกจากระบบเซิร์ฟเวอร์ FTP(S) ⚠ คำว่า OK ที่ตอบมาทันทีหมายถึงรับคำสั่งไว้เท่านั้น — เซสชันจะปิดจริงก็ต่อเมื่อ +QFTPCLOSE: 0,0 มาถึง ระหว่างนั้นสถานะคือ 3 (กำลังปิด) และคำสั่ง FTP ใด ๆ ที่ส่งตอนนั้นจะตอบ +CME ERROR: 603 (เซิร์ฟเวอร์ไม่ว่าง) วัดได้ในรอบ P6 เมื่อ 2026-08-07: ถ้าเข้าใจว่า OK นั้นคือปิดเสร็จแล้วรีบเปิดใหม่ จะได้ 603 ต่อเนื่องจนดูเหมือนโมดูลพัง",
  "(โมดูลจะปิดบังรหัสผ่านด้วยเครื่องหมาย * วัดได้ในรอบ P6 เมื่อ 2026-08-07 มีเพียงข้อความที่คุณพิมพ์ตอนตั้งค่าเท่านั้นที่เป็นข้อความล้วน)"],
 'hi-IN': [
  "FTP(S) सर्वर से लॉग आउट करें। ⚠ तुरंत लौटा OK केवल इतना बताता है कि आदेश स्वीकार हुआ — सत्र तभी बंद होता है जब +QFTPCLOSE: 0,0 आ जाए। बीच में स्थिति 3 (बंद हो रहा है) रहती है, और उस समय भेजा गया कोई भी FTP आदेश +CME ERROR: 603 (सर्वर व्यस्त) लौटाता है। 2026-08-07 की P6 दौड़ में मापा गया: उस OK को «बंद हो गया» मानकर तुरंत दोबारा खोलने पर 603 की झड़ी लगती है, जो बिलकुल ख़राब मॉड्यूल जैसी दिखती है",
  "(मॉड्यूल पासवर्ड को * से ढक देता है, 2026-08-07 की P6 दौड़ में मापा गया; केवल सेट करते समय टाइप किया गया पाठ ही खुला होता है)"],
 'tr-TR': [
  "FTP(S) sunucusundan çıkış yapar. ⚠ Hemen dönen OK yalnızca komutun kabul edildiği anlamına gelir — oturum ancak +QFTPCLOSE: 0,0 geldiğinde kapanmış olur. Arada durum 3'tür (kapanıyor) ve o sırada verilen her FTP komutu +CME ERROR: 603 (sunucu meşgul) döndürür. 2026-08-07 tarihli P6 turunda ölçüldü: o OK'i «kapandı» sayıp hemen yeniden açmak, tam olarak bozuk bir modül gibi görünen bir 603 dizisi üretir",
  "(modül parolayı * ile gizler, 2026-08-07 tarihli P6 turunda ölçüldü; yalnızca ayarlarken yazdığınız metin açıktır)"],
 'ar-SA': [
  "تسجيل الخروج من خادم FTP(S). ⚠ وكلمة OK التي تعود فوراً لا تعني إلا أن الأمر قُبل —— فالجلسة لا تُغلق إلا حين يصل +QFTPCLOSE: 0,0. وفي ما بين ذلك تكون الحالة 3 (قيد الإغلاق)، وأي أمر FTP يُرسَل عندئذٍ يُردّ عليه بـ +CME ERROR: 603 (الخادم مشغول). وقد قيس ذلك في جولة P6 يوم 2026-08-07: من يعُدّ ذلك الـ OK إغلاقاً ثم يعيد الفتح فوراً يحصل على سلسلة من 603 تبدو تماماً كأن الموديل معطَّل",
  "(يُخفي الموديل كلمة المرور بعلامات *، قيس ذلك في جولة P6 يوم 2026-08-07؛ ولا يظهر بنص صريح إلا ما تكتبه أنت عند الضبط)"],
 'he-IL': [
  "התנתקות משרת ה-FTP(S). ⚠ ה-OK שחוזר מיד פירושו רק שהפקודה התקבלה — ההפעלה נסגרת רק כאשר מגיע +QFTPCLOSE: 0,0. בינתיים המצב הוא 3 (בתהליך סגירה), וכל פקודת FTP שתישלח אז תחזיר +CME ERROR: 603 (השרת עסוק). נמדד בסבב P6 ב-2026-08-07: מי שמפרש את ה-OK הזה כ«נסגר» ופותח מחדש מיד מקבל שרשרת של 603 שנראית בדיוק כמו מודול תקול",
  "(המודול מסתיר את הסיסמה בכוכביות, נמדד בסבב P6 ב-2026-08-07; רק הטקסט שאתה מקליד בעת ההגדרה גלוי)"],
 'fa-IR': [
  "خروج از کارساز FTP(S). ⚠ واژهٔ OK که بی‌درنگ برمی‌گردد تنها یعنی فرمان پذیرفته شد —— نشست تنها زمانی بسته می‌شود که +QFTPCLOSE: 0,0 برسد. در این میان وضعیت ۳ است (در حال بستن) و هر فرمان FTP که آن هنگام فرستاده شود پاسخ +CME ERROR: 603 (کارساز مشغول) می‌گیرد. در دور P6 در ۲۰۲۶-۰۸-۰۷ اندازه‌گیری شد: اگر آن OK را «بسته شد» بخوانید و بی‌درنگ دوباره باز کنید، رشته‌ای از ۶۰۳ می‌گیرید که دقیقاً شبیه ماژول خراب به نظر می‌رسد",
  "(ماژول گذرواژه را با * می‌پوشاند؛ در دور P6 در ۲۰۲۶-۰۸-۰۷ اندازه‌گیری شد. تنها متنی که هنگام تنظیم می‌نویسید آشکار است)"],
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
