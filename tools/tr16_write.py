r"""第十批補譯：14 條。

來源有兩類：

1. **P6 實測改寫的 FTP 密碼說明（4 條）** —— V26.0.76 之後把「手冊說密碼會明文印出」
   改成「本機韌體實測是遮成 *」，原文一改，舊譯文就對不上鍵了，等於整條沒翻。
2. **一直漏抽的短字串（10 條）** —— `at_i18n_sources.json` 是瀏覽器匯出的快照，
   而那份快照停在改動之前。2026-08-08 重新匯出並「聯集」併回（只加不減，
   避免 2026-08-07 直接覆蓋弄丟 383 條的事重演），這批才浮出來。

脈絡（翻譯時據此決定用詞，勿望文生義）：

- `' 秒'`     ：單位後綴，接在數字後面 —— `AT+QICLOSE` 的 `＝{n} 秒`（NuModem_EG800.html:4024）
- `'125 秒'`  ：按鈕上的 `timeout:` 標籤（AT+QNTP／AT+QFTPLOGIN）
- `'{0} 成功'`：HTTP 動作成功，`{0}` 是 GET／POST／READ 之類的動作名
- `'{0}成功'` ：設定類指令成功，`{0}` 是「設定 xxx」這種詞組（中文不加空格，其他語言要加）
- `'成功' / '失敗'`：對照表的值（GNSS 韌體載入結果）
- `'充電中'`  ：`CBC_STATUS['1']`，電池狀態
- `'（空）'`  ：欄位讀回是空字串時的佔位顯示（token／FTP 帳密）
- `'BSSID 上限'`：Wi-Fi 掃描參數欄位標籤（maxbssid）
- `'例：mqttgo.io'`：輸入框 placeholder
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'i18n', 'tr16')

KEYS = [
    ' 秒',
    '125 秒',
    'BSSID 上限',
    '{0} 成功',
    '{0}成功',
    '例：mqttgo.io',
    '充電中',
    '列出全部 FTP 設定子項：9 項回支援值範圍。account 那行的密碼會被模組遮成 *（2026-08-07 P6 實測），帳號則是明文',
    '失敗',
    '字串，最大 255 bytes。查詢指令讀回時密碼會被模組遮成 *（2026-08-07 P6 實測），但你在這裡輸入的原文仍是明碼',
    '成功',
    '查詢目前帳密設定；密碼會被模組遮成 *（2026-08-07 P6 實測）',
    '查詢目前設定的 FTP 帳號與密碼。⚠ 手冊寫「回應會把密碼原樣印出」，但 2026-08-07 P6 實測本機韌體是遮成 * 的 —— 以實測為準，不要因為手冊那句話就不敢查。',
    '（空）',
]

T = {
'en-US': [
    ' s',
    '125 s',
    'Max BSSIDs',
    '{0} succeeded',
    '{0} succeeded',
    'e.g. mqttgo.io',
    'Charging',
    'Lists every FTP config sub-item: 9 lines of supported value ranges. On the account line the module masks the password to * (measured 2026-08-07, P6); the username is plain text',
    'Failed',
    'String, max 255 bytes. When read back by the query command the module masks the password to * (measured 2026-08-07, P6), but what you type here is still in the clear',
    'Succeeded',
    'Query the current account settings; the module masks the password to * (measured 2026-08-07, P6)',
    'Query the FTP username and password currently set. ⚠ The manual says "the response prints the password verbatim", but the P6 test on 2026-08-07 showed this firmware masks it to * — trust the measurement, and do not avoid this query because of that sentence in the manual.',
    '(empty)',
],
'ja-JP': [
    ' 秒',
    '125 秒',
    'BSSID 上限',
    '{0} 成功',
    '{0}成功',
    '例：mqttgo.io',
    '充電中',
    'FTP 設定の全サブ項目を一覧：9 項目が対応値の範囲を返します。account の行はモジュールがパスワードを * でマスクします（2026-08-07 P6 実測）。ユーザー名は平文です',
    '失敗',
    '文字列、最大 255 バイト。クエリコマンドで読み戻すとモジュールがパスワードを * でマスクします（2026-08-07 P6 実測）が、ここに入力した内容自体は平文のままです',
    '成功',
    '現在のアカウント設定を照会します。パスワードはモジュールが * でマスクします（2026-08-07 P6 実測）',
    '現在設定されている FTP のユーザー名とパスワードを照会します。⚠ マニュアルには「応答でパスワードがそのまま出力される」とありますが、2026-08-07 の P6 実測では本機のファームウェアは * でマスクしました —— 実測を優先し、マニュアルのその一文を理由に照会をためらう必要はありません。',
    '（空）',
],
'fr-FR': [
    ' s',
    '125 s',
    'BSSID max',
    '{0} réussi',
    '{0} réussi',
    'ex. : mqttgo.io',
    'En charge',
    "Liste tous les sous-éléments de configuration FTP : 9 lignes de plages de valeurs prises en charge. Sur la ligne account, le module masque le mot de passe par * (mesuré le 2026-08-07, P6) ; le nom d'utilisateur reste en clair",
    'Échec',
    "Chaîne, 255 octets au maximum. À la relecture par la commande d'interrogation, le module masque le mot de passe par * (mesuré le 2026-08-07, P6), mais ce que vous saisissez ici reste en clair",
    'Réussi',
    "Interroge les réglages de compte actuels ; le module masque le mot de passe par * (mesuré le 2026-08-07, P6)",
    "Interroge le nom d'utilisateur et le mot de passe FTP actuellement configurés. ⚠ Le manuel indique que « la réponse affiche le mot de passe tel quel », mais le test P6 du 2026-08-07 montre que ce micrologiciel le masque par * —— fiez-vous à la mesure et n'hésitez pas à lancer cette interrogation à cause de cette phrase du manuel.",
    '(vide)',
],
'de-DE': [
    ' s',
    '125 s',
    'BSSID-Obergrenze',
    '{0} erfolgreich',
    '{0} erfolgreich',
    'z. B. mqttgo.io',
    'Wird geladen',
    'Listet alle FTP-Konfigurationsunterpunkte auf: 9 Zeilen mit unterstützten Wertebereichen. In der Zeile account maskiert das Modul das Passwort mit * (gemessen am 2026-08-07, P6); der Benutzername steht im Klartext',
    'Fehlgeschlagen',
    'Zeichenkette, maximal 255 Bytes. Beim Rücklesen über den Abfragebefehl maskiert das Modul das Passwort mit * (gemessen am 2026-08-07, P6), was Sie hier eingeben, bleibt aber im Klartext',
    'Erfolgreich',
    'Fragt die aktuellen Kontoeinstellungen ab; das Modul maskiert das Passwort mit * (gemessen am 2026-08-07, P6)',
    'Fragt den aktuell eingestellten FTP-Benutzernamen und das Passwort ab. ⚠ Das Handbuch sagt, „die Antwort gibt das Passwort unverändert aus“, doch der P6-Test vom 2026-08-07 zeigt, dass diese Firmware es mit * maskiert —— halten Sie sich an die Messung und scheuen Sie diese Abfrage nicht wegen jenes Satzes im Handbuch.',
    '(leer)',
],
'it-IT': [
    ' s',
    '125 s',
    'BSSID max',
    '{0} riuscito',
    '{0} riuscito',
    'es. mqttgo.io',
    'In carica',
    "Elenca tutte le sotto-voci di configurazione FTP: 9 righe con gli intervalli di valori supportati. Nella riga account il modulo maschera la password con * (misurato il 2026-08-07, P6); il nome utente resta in chiaro",
    'Non riuscito',
    'Stringa, massimo 255 byte. Alla rilettura tramite il comando di interrogazione il modulo maschera la password con * (misurato il 2026-08-07, P6), ma ciò che digiti qui resta in chiaro',
    'Riuscito',
    'Interroga le impostazioni account correnti; il modulo maschera la password con * (misurato il 2026-08-07, P6)',
    "Interroga il nome utente e la password FTP attualmente impostati. ⚠ Il manuale dice che «la risposta stampa la password così com'è», ma il test P6 del 2026-08-07 mostra che questo firmware la maschera con * —— fidati della misura e non evitare questa interrogazione per via di quella frase del manuale.",
    '(vuoto)',
],
'es-ES': [
    ' s',
    '125 s',
    'BSSID máx.',
    '{0} correcto',
    '{0} correcto',
    'p. ej. mqttgo.io',
    'Cargando',
    'Enumera todos los subelementos de configuración FTP: 9 líneas con los rangos de valores admitidos. En la línea account el módulo enmascara la contraseña con * (medido el 2026-08-07, P6); el nombre de usuario va en claro',
    'Fallido',
    'Cadena, máximo 255 bytes. Al releerla con el comando de consulta el módulo enmascara la contraseña con * (medido el 2026-08-07, P6), pero lo que escribes aquí sigue en claro',
    'Correcto',
    'Consulta los ajustes de cuenta actuales; el módulo enmascara la contraseña con * (medido el 2026-08-07, P6)',
    'Consulta el nombre de usuario y la contraseña FTP configurados actualmente. ⚠ El manual dice que «la respuesta imprime la contraseña tal cual», pero la prueba P6 del 2026-08-07 muestra que este firmware la enmascara con * —— hazle caso a la medición y no evites esta consulta por esa frase del manual.',
    '(vacío)',
],
'pt-PT': [
    ' s',
    '125 s',
    'BSSID máx.',
    '{0} com sucesso',
    '{0} com sucesso',
    'ex.: mqttgo.io',
    'A carregar',
    'Lista todos os subitens de configuração FTP: 9 linhas com os intervalos de valores suportados. Na linha account o módulo mascara a palavra-passe com * (medido em 2026-08-07, P6); o nome de utilizador fica em claro',
    'Falhou',
    'Cadeia, máximo 255 bytes. Ao ser relida pelo comando de consulta, o módulo mascara a palavra-passe com * (medido em 2026-08-07, P6), mas o que escreve aqui continua em claro',
    'Com sucesso',
    'Consulta as definições de conta atuais; o módulo mascara a palavra-passe com * (medido em 2026-08-07, P6)',
    'Consulta o nome de utilizador e a palavra-passe FTP atualmente definidos. ⚠ O manual diz que «a resposta imprime a palavra-passe tal como está», mas o teste P6 de 2026-08-07 mostra que este firmware a mascara com * —— confie na medição e não evite esta consulta por causa dessa frase do manual.',
    '(vazio)',
],
'tr-TR': [
    ' sn',
    '125 sn',
    'BSSID üst sınırı',
    '{0} başarılı',
    '{0} başarılı',
    'örn. mqttgo.io',
    'Şarj oluyor',
    'Tüm FTP yapılandırma alt maddelerini listeler: 9 satır desteklenen değer aralığı döner. account satırında modül parolayı * ile maskeler (2026-08-07, P6 ölçümü); kullanıcı adı açık metindir',
    'Başarısız',
    'Dizgi, en fazla 255 bayt. Sorgu komutuyla geri okunduğunda modül parolayı * ile maskeler (2026-08-07, P6 ölçümü), ancak buraya yazdığınız metin açık kalır',
    'Başarılı',
    'Geçerli hesap ayarlarını sorgular; modül parolayı * ile maskeler (2026-08-07, P6 ölçümü)',
    'Hâlihazırda ayarlı FTP kullanıcı adı ve parolasını sorgular. ⚠ Kılavuz "yanıt parolayı olduğu gibi yazdırır" diyor, ancak 2026-08-07 tarihli P6 ölçümü bu ürün yazılımının parolayı * ile maskelediğini gösterdi —— ölçümü esas alın; kılavuzdaki o cümle yüzünden bu sorguyu yapmaktan çekinmeyin.',
    '(boş)',
],
'ru-RU': [
    ' с',
    '125 с',
    'Максимум BSSID',
    '{0} выполнено',
    '{0} выполнено',
    'напр. mqttgo.io',
    'Идёт зарядка',
    'Выводит все подпункты настройки FTP: 9 строк с диапазонами поддерживаемых значений. В строке account модуль маскирует пароль символами * (измерено 2026-08-07, P6); имя пользователя выводится открыто',
    'Не выполнено',
    'Строка, не более 255 байт. При обратном чтении командой запроса модуль маскирует пароль символами * (измерено 2026-08-07, P6), но то, что вы вводите здесь, остаётся открытым текстом',
    'Выполнено',
    'Запрашивает текущие настройки учётной записи; модуль маскирует пароль символами * (измерено 2026-08-07, P6)',
    'Запрашивает заданные сейчас имя пользователя и пароль FTP. ⚠ В руководстве сказано, что «ответ печатает пароль как есть», но проверка P6 от 2026-08-07 показала: эта прошивка маскирует его символами * —— доверяйте измерению и не отказывайтесь от этого запроса из-за той фразы в руководстве.',
    '(пусто)',
],
'vi-VN': [
    ' giây',
    '125 giây',
    'Giới hạn BSSID',
    '{0} thành công',
    '{0} thành công',
    'ví dụ: mqttgo.io',
    'Đang sạc',
    'Liệt kê toàn bộ mục con cấu hình FTP: 9 dòng trả về phạm vi giá trị được hỗ trợ. Ở dòng account, mô-đun che mật khẩu thành * (đo thực tế 2026-08-07, P6); tên đăng nhập vẫn ở dạng rõ',
    'Thất bại',
    'Chuỗi, tối đa 255 byte. Khi đọc lại bằng lệnh truy vấn, mô-đun che mật khẩu thành * (đo thực tế 2026-08-07, P6), nhưng nội dung bạn nhập ở đây vẫn là văn bản rõ',
    'Thành công',
    'Truy vấn thiết lập tài khoản hiện tại; mô-đun che mật khẩu thành * (đo thực tế 2026-08-07, P6)',
    'Truy vấn tên đăng nhập và mật khẩu FTP đang được đặt. ⚠ Sổ tay ghi "phản hồi in nguyên mật khẩu", nhưng phép đo P6 ngày 2026-08-07 cho thấy firmware máy này che thành * —— hãy tin vào phép đo, đừng vì câu đó trong sổ tay mà ngại truy vấn.',
    '(trống)',
],
'id-ID': [
    ' detik',
    '125 detik',
    'Batas BSSID',
    '{0} berhasil',
    '{0} berhasil',
    'mis. mqttgo.io',
    'Sedang mengisi daya',
    'Menampilkan seluruh subitem konfigurasi FTP: 9 baris berisi rentang nilai yang didukung. Pada baris account, modul menyamarkan kata sandi menjadi * (diukur 2026-08-07, P6); nama pengguna tetap teks biasa',
    'Gagal',
    'String, maksimum 255 bita. Saat dibaca ulang oleh perintah kueri, modul menyamarkan kata sandi menjadi * (diukur 2026-08-07, P6), tetapi yang Anda ketik di sini tetap teks biasa',
    'Berhasil',
    'Menanyakan setelan akun saat ini; modul menyamarkan kata sandi menjadi * (diukur 2026-08-07, P6)',
    'Menanyakan nama pengguna dan kata sandi FTP yang sedang disetel. ⚠ Manual menyatakan "respons mencetak kata sandi apa adanya", tetapi uji P6 pada 2026-08-07 menunjukkan firmware unit ini menyamarkannya menjadi * —— percayai hasil pengukuran, jangan urung menanyakan hanya karena kalimat itu di manual.',
    '(kosong)',
],
'ms-MY': [
    ' saat',
    '125 saat',
    'Had BSSID',
    '{0} berjaya',
    '{0} berjaya',
    'cth. mqttgo.io',
    'Sedang mengecas',
    'Menyenaraikan semua subitem konfigurasi FTP: 9 baris julat nilai yang disokong. Pada baris account, modul menyamarkan kata laluan menjadi * (diukur 2026-08-07, P6); nama pengguna kekal teks biasa',
    'Gagal',
    'Rentetan, maksimum 255 bait. Apabila dibaca semula oleh perintah pertanyaan, modul menyamarkan kata laluan menjadi * (diukur 2026-08-07, P6), tetapi apa yang anda taip di sini kekal teks biasa',
    'Berjaya',
    'Menanyakan tetapan akaun semasa; modul menyamarkan kata laluan menjadi * (diukur 2026-08-07, P6)',
    'Menanyakan nama pengguna dan kata laluan FTP yang sedang ditetapkan. ⚠ Manual menyatakan "respons mencetak kata laluan sebagaimana adanya", tetapi ujian P6 pada 2026-08-07 menunjukkan perisian tegar unit ini menyamarkannya menjadi * —— percayai hasil ukuran, jangan elak pertanyaan ini kerana ayat itu dalam manual.',
    '(kosong)',
],
'th-TH': [
    ' วินาที',
    '125 วินาที',
    'จำนวน BSSID สูงสุด',
    '{0} สำเร็จ',
    '{0} สำเร็จ',
    'เช่น mqttgo.io',
    'กำลังชาร์จ',
    'แสดงรายการหัวข้อย่อยของการตั้งค่า FTP ทั้งหมด: 9 บรรทัดเป็นช่วงค่าที่รองรับ บรรทัด account โมดูลจะปิดบังรหัสผ่านเป็น * (วัดจริง 2026-08-07, P6) ส่วนชื่อผู้ใช้เป็นข้อความธรรมดา',
    'ล้มเหลว',
    'สตริง สูงสุด 255 ไบต์ เมื่ออ่านกลับด้วยคำสั่งสอบถาม โมดูลจะปิดบังรหัสผ่านเป็น * (วัดจริง 2026-08-07, P6) แต่ข้อความที่คุณพิมพ์ตรงนี้ยังเป็นข้อความธรรมดา',
    'สำเร็จ',
    'สอบถามการตั้งค่าบัญชีปัจจุบัน โมดูลจะปิดบังรหัสผ่านเป็น * (วัดจริง 2026-08-07, P6)',
    'สอบถามชื่อผู้ใช้และรหัสผ่าน FTP ที่ตั้งไว้ในขณะนี้ ⚠ คู่มือระบุว่า "การตอบกลับจะพิมพ์รหัสผ่านออกมาตรง ๆ" แต่การทดสอบ P6 เมื่อ 2026-08-07 พบว่าเฟิร์มแวร์เครื่องนี้ปิดบังเป็น * —— ให้ยึดผลวัดจริง อย่าเลี่ยงคำสั่งนี้เพราะประโยคนั้นในคู่มือ',
    '(ว่าง)',
],
'hi-IN': [
    ' सेकंड',
    '125 सेकंड',
    'BSSID की अधिकतम संख्या',
    '{0} सफल',
    '{0} सफल',
    'उदा. mqttgo.io',
    'चार्ज हो रहा है',
    'सभी FTP कॉन्फ़िगरेशन उप-मदों की सूची: 9 पंक्तियाँ समर्थित मानों की परिसीमा लौटाती हैं। account वाली पंक्ति में मॉड्यूल पासवर्ड को * से ढक देता है (2026-08-07, P6 में मापा गया); उपयोक्तानाम सादे पाठ में रहता है',
    'विफल',
    'स्ट्रिंग, अधिकतम 255 बाइट। क्वेरी कमांड से वापस पढ़ने पर मॉड्यूल पासवर्ड को * से ढक देता है (2026-08-07, P6 में मापा गया), पर आप यहाँ जो टाइप करते हैं वह सादे पाठ में ही रहता है',
    'सफल',
    'वर्तमान खाता सेटिंग्स की पूछताछ करता है; मॉड्यूल पासवर्ड को * से ढक देता है (2026-08-07, P6 में मापा गया)',
    'वर्तमान में सेट FTP उपयोक्तानाम और पासवर्ड की पूछताछ करता है। ⚠ नियमावली कहती है "प्रत्युत्तर पासवर्ड ज्यों का त्यों छाप देता है", पर 2026-08-07 के P6 परीक्षण में इस फ़र्मवेयर ने उसे * से ढका —— माप पर भरोसा करें, नियमावली के उस वाक्य के कारण यह पूछताछ करने से न कतराएँ।',
    '(खाली)',
],
'ar-SA': [
    ' ثانية',
    '125 ثانية',
    'الحد الأقصى لعدد BSSID',
    'نجح {0}',
    'نجح {0}',
    'مثال: mqttgo.io',
    'قيد الشحن',
    'يسرد جميع بنود إعداد FTP الفرعية: 9 أسطر تعيد نطاقات القيم المدعومة. في سطر account تُخفي الوحدة كلمة المرور بالرمز * (‏قياس 2026-08-07، P6)؛ أما اسم المستخدم فيظهر بنص صريح',
    'أخفق',
    'سلسلة نصية، 255 بايت كحد أقصى. عند إعادة القراءة بأمر الاستعلام تُخفي الوحدة كلمة المرور بالرمز * (‏قياس 2026-08-07، P6)، لكن ما تكتبه هنا يبقى نصًّا صريحًا',
    'نجح',
    'يستعلم عن إعدادات الحساب الحالية؛ تُخفي الوحدة كلمة المرور بالرمز * (‏قياس 2026-08-07، P6)',
    'يستعلم عن اسم مستخدم FTP وكلمة المرور المضبوطَين حاليًّا. ⚠ يقول الدليل إن «الرد يطبع كلمة المرور كما هي»، لكن اختبار P6 بتاريخ 2026-08-07 أظهر أن البرنامج الثابت في هذا الجهاز يُخفيها بالرمز * —— اعتمد على القياس، ولا تتردد في هذا الاستعلام بسبب تلك الجملة في الدليل.',
    '(فارغ)',
],
'he-IL': [
    ' שניות',
    '125 שניות',
    'מקסימום BSSID',
    '{0} הצליח',
    '{0} הצליח',
    'לדוגמה: mqttgo.io',
    'בטעינה',
    'מציג את כל תת-הפריטים של הגדרות FTP: 9 שורות של טווחי ערכים נתמכים. בשורת account המודול מסתיר את הסיסמה בכוכביות * (‏נמדד 2026-08-07, P6); שם המשתמש מוצג כטקסט גלוי',
    'נכשל',
    'מחרוזת, עד 255 בתים. בקריאה חוזרת בפקודת השאילתה המודול מסתיר את הסיסמה בכוכביות * (‏נמדד 2026-08-07, P6), אבל מה שאתה מקליד כאן נשאר טקסט גלוי',
    'הצליח',
    'שואל את הגדרות החשבון הנוכחיות; המודול מסתיר את הסיסמה בכוכביות * (‏נמדד 2026-08-07, P6)',
    'שואל את שם המשתמש והסיסמה של FTP המוגדרים כעת. ⚠ המדריך אומר ש„התשובה מדפיסה את הסיסמה כמות שהיא”, אבל בדיקת P6 מ-2026-08-07 הראתה שהקושחה כאן מסתירה אותה בכוכביות * —— סמוך על המדידה, ואל תימנע מהשאילתה הזו בגלל המשפט ההוא במדריך.',
    '(ריק)',
],
'fa-IR': [
    ' ثانیه',
    '۱۲۵ ثانیه',
    'بیشینهٔ BSSID',
    '{0} موفق بود',
    '{0} موفق بود',
    'مثال: mqttgo.io',
    'در حال شارژ',
    'همهٔ زیرموردهای پیکربندی FTP را فهرست می‌کند: ۹ سطر بازهٔ مقادیر پشتیبانی‌شده. در سطر account ماژول گذرواژه را با * می‌پوشاند (‏اندازه‌گیری 2026-08-07، P6)؛ نام کاربری به‌صورت متن آشکار می‌آید',
    'ناموفق',
    'رشته، حداکثر ۲۵۵ بایت. هنگام بازخوانی با فرمان پرس‌وجو ماژول گذرواژه را با * می‌پوشاند (‏اندازه‌گیری 2026-08-07، P6)، اما آنچه اینجا تایپ می‌کنید همچنان متن آشکار است',
    'موفق بود',
    'تنظیمات فعلی حساب را پرس‌وجو می‌کند؛ ماژول گذرواژه را با * می‌پوشاند (‏اندازه‌گیری 2026-08-07، P6)',
    'نام کاربری و گذرواژهٔ FTP تنظیم‌شدهٔ کنونی را پرس‌وجو می‌کند. ⚠ راهنما می‌گوید «پاسخ گذرواژه را عیناً چاپ می‌کند»، اما آزمون P6 در 2026-08-07 نشان داد میان‌افزار این دستگاه آن را با * می‌پوشاند —— به اندازه‌گیری تکیه کنید و به‌خاطر آن جملهٔ راهنما از این پرس‌وجو صرف‌نظر نکنید.',
    '(خالی)',
],
}


def main():
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(ROOT, 'i18n', 'tr16-source.json'), 'w', encoding='utf-8').write(
        json.dumps(KEYS, ensure_ascii=False, indent=1))

    for lang, vals in T.items():
        assert len(vals) == len(KEYS), '%s：%d 條 ≠ 原文 %d 條' % (lang, len(vals), len(KEYS))
        # 佔位符必須原封不動，否則執行期會印出錯的數值
        for k, v in zip(KEYS, vals):
            assert ('{0}' in k) == ('{0}' in v), '%s 佔位符對不上：%s' % (lang, k)
        json.dump(dict(zip(KEYS, vals)),
                  io.open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    print('tr16：%d 種語言 × %d 條 → %s' % (len(T), len(KEYS), OUT))


if __name__ == '__main__':
    main()
