# -*- coding: utf-8 -*-
"""第六批補譯：移除流量警告、加上跳脫序列支援之後改寫的 9 條說明。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = json.load(io.open(os.path.join(ROOT, 'i18n', 'tr12-source.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'i18n', 'tr12')

T = {
 'en-US': [
  "Turn on AGNSS — cold start drops to seconds or minutes; takes effect after a reboot, written to NVRAM. Every GNSS start then downloads assistance data from the network, so an active PDP context is required",
  "Send data (two-stage: wait for >, then send the body; no Ctrl+Z). If the length is wrong or you abandon it midway, the AT port stays in data mode and swallows what you type next — send ESC (0x1B) with the raw-byte button on the Hardware page to get out",
  "The bytes actually sent. The length is counted in UTF-8 and filled into the command's <sendlen> automatically (a CJK character is 3 bytes); the limit is 1460 bytes (manual §2.2.3). Write control characters as escapes: \\n newline, \\r carriage return, \\t tab, \\0 NUL, \\xHH any byte, \\\\ a literal backslash — they are decoded only at send time, and the length is counted after decoding. ⚠ The default peer tcpbin echoes line by line, so a payload that does not end in \\n gets no echo at all (the default value already has one).",
  "Two traps: (1) the manual says CONNECT appears \"within 125 s\" — the module first has to open the connection and send the request header, so the prompt timeout must be set to 125 s and cannot reuse MQTT's 5 s; (2) {len} must equal the byte count of the body (or of header + body when requestheader=1); get it wrong and you are stuck in data mode until {input_time} expires.",
  "Emits CONNECT and enters data mode; the directory listing is printed as raw bytes, and anything you type meanwhile is treated as data.",
  "Enters data mode: anything you type meanwhile is treated as data.",
  "Enters data mode (CONNECT → raw bytes → OK). If the file is not plain text the terminal shows garbage.",
  "Whole-file download: a large file will occupy the terminal for a long time. Check the size with AT+QFTPSIZE first, and use the chunked version for large files.",
  "Writes to the remote server. After CONNECT you must send exactly len bytes as raw bytes, with no CR/LF appended. This tool cannot read binary files from disk — you can only paste plain text (control characters via \\n \\r \\xHH escapes)."],
 'ja-JP': [
  "AGNSS を有効化 —— コールドスタートが秒〜分に短縮されます。再起動後に有効、NVRAM に保存。以後 GNSS 起動のたびにネットワークから支援データを取得するため、有効な PDP context が必要です",
  "データ送信（2 段階：> を待ってから本文を送る。Ctrl+Z 不要）。長さを間違えたり途中でやめたりすると AT ポートがデータモードに留まり以降の入力を飲み込みます —— Hardware ページの生バイト送信ボタンで ESC（0x1B）を送れば抜けられます",
  "実際に送信されるバイト列。長さは UTF-8 で数えてコマンドの <sendlen> に自動で入ります（漢字 1 文字は 3 バイト）。上限は 1460 バイト（マニュアル §2.2.3）。制御文字はエスケープで書きます：\\n 改行、\\r 復帰、\\t タブ、\\0 NUL、\\xHH 任意のバイト、\\\\ バックスラッシュそのもの —— 送信直前に解釈され、長さも解釈後のバイト数で数えます。⚠ 既定の相手 tcpbin は行単位のエコーなので、末尾が \\n でない payload はまったく返ってきません（既定値には付いています）。",
  "落とし穴が 2 つ：(1) マニュアルには CONNECT が「within 125 s」で出るとあります —— モジュールが先に接続を張ってリクエストヘッダーを送るためで、プロンプト待ちのタイムアウトは 125 s にする必要があり、MQTT の 5 秒を流用できません。(2) {len} は body のバイト数（requestheader=1 なら「ヘッダー＋body」の合計）と一致していなければならず、間違えると {input_time} が切れるまでデータモードから戻れません。",
  "CONNECT を出してデータモードに入ります。ディレクトリ一覧は生バイトのまま出力され、その間に打った文字はすべてデータとして扱われます。",
  "データモードに入ります：その間に打った文字はすべてデータとして扱われます。",
  "データモードに入ります（CONNECT → 生バイト → OK）。ファイルがテキストでない場合、端末には文字化けが出ます。",
  "ファイル全体のダウンロード：大きなファイルは端末を長時間占有します。必ず AT+QFTPSIZE でサイズを確認し、大きい場合は分割版を使ってください。",
  "リモートサーバーへ書き込みます。CONNECT を受け取ったら「ちょうど len バイト」を生バイトで送る必要があり、CR/LF を付けてはいけません。本ツールはディスク上のバイナリファイルを読めないため、貼り付けられるのはテキストだけです（制御文字は \\n \\r \\xHH のエスケープで指定）。"],
 'de-DE': [
  "AGNSS einschalten — der Kaltstart sinkt auf Sekunden bis Minuten; wirksam nach einem Neustart, wird ins NVRAM geschrieben. Danach lädt jeder GNSS-Start Assistenzdaten aus dem Netz, ein aktiver PDP-Context ist also erforderlich",
  "Daten senden (zweistufig: auf > warten, dann den Rumpf senden; kein Ctrl+Z). Stimmt die Länge nicht oder brechen Sie mittendrin ab, bleibt der AT-Port im Datenmodus und verschluckt Ihre nächsten Eingaben — senden Sie ESC (0x1B) mit der Rohbyte-Schaltfläche auf der Hardware-Seite, um herauszukommen",
  "Die tatsächlich gesendeten Bytes. Die Länge wird in UTF-8 gezählt und automatisch in das <sendlen> des Befehls eingesetzt (ein CJK-Zeichen zählt 3 Bytes); die Grenze liegt bei 1460 Bytes (Handbuch §2.2.3). Steuerzeichen schreiben Sie als Escapes: \\n Zeilenumbruch, \\r Wagenrücklauf, \\t Tabulator, \\0 NUL, \\xHH beliebiges Byte, \\\\ ein echter Backslash — sie werden erst beim Senden aufgelöst, und die Länge zählt nach dem Auflösen. ⚠ Die Vorgabegegenstelle tcpbin antwortet zeilenweise, eine Nutzlast ohne abschließendes \\n bekommt also überhaupt kein Echo (im Vorgabewert ist eines enthalten).",
  "Zwei Fallen: (1) Das Handbuch sagt, CONNECT erscheine „within 125 s“ — das Modul muss erst die Verbindung aufbauen und den Anfrage-Header senden, deshalb muss das Zeitlimit für den Prompt auf 125 s stehen und darf nicht die 5 s von MQTT übernehmen; (2) {len} muss der Byteanzahl des Rumpfes entsprechen (bzw. von Header + Rumpf bei requestheader=1); ein Fehler hier lässt Sie bis zum Ablauf von {input_time} im Datenmodus feststecken.",
  "Gibt CONNECT aus und wechselt in den Datenmodus; das Verzeichnislisting erscheint als Rohbytes, und alles, was Sie währenddessen tippen, gilt als Daten.",
  "Wechselt in den Datenmodus: alles, was Sie währenddessen tippen, gilt als Daten.",
  "Wechselt in den Datenmodus (CONNECT → Rohbytes → OK). Ist die Datei kein reiner Text, zeigt das Terminal Zeichensalat.",
  "Download der ganzen Datei: eine große Datei belegt das Terminal lange. Prüfen Sie die Größe zuerst mit AT+QFTPSIZE und nehmen Sie für große Dateien die stückweise Variante.",
  "Schreibt auf den entfernten Server. Nach CONNECT müssen Sie genau len Bytes als Rohbytes senden, ohne CR/LF anzuhängen. Dieses Werkzeug kann keine Binärdateien von der Festplatte lesen — einfügen lässt sich nur reiner Text (Steuerzeichen über die Escapes \\n \\r \\xHH)."],
 'fr-FR': [
  "Activer l'AGNSS — le démarrage à froid tombe à quelques secondes ou minutes ; effectif après un redémarrage, écrit en NVRAM. Chaque démarrage GNSS télécharge ensuite des données d'assistance depuis le réseau, un contexte PDP actif est donc nécessaire",
  "Envoyer des données (en deux temps : attendre >, puis envoyer le corps ; pas de Ctrl+Z). Si la longueur est fausse ou que vous abandonnez en route, le port AT reste en mode données et avale ce que vous tapez ensuite — envoyez ESC (0x1B) avec le bouton d'octet brut de la page Hardware pour vous en sortir",
  "Les octets réellement envoyés. La longueur est comptée en UTF-8 et reportée automatiquement dans le <sendlen> de la commande (un caractère CJK vaut 3 octets) ; la limite est de 1460 octets (manuel §2.2.3). Écrivez les caractères de contrôle sous forme d'échappements : \\n saut de ligne, \\r retour chariot, \\t tabulation, \\0 NUL, \\xHH octet quelconque, \\\\ une barre oblique inverse littérale — ils ne sont décodés qu'à l'envoi, et la longueur est comptée après décodage. ⚠ Le correspondant par défaut tcpbin renvoie ligne par ligne : une charge utile qui ne se termine pas par \\n n'obtient aucun écho (la valeur par défaut en contient un).",
  "Deux pièges : (1) le manuel indique que CONNECT arrive « within 125 s » — le module doit d'abord ouvrir la connexion et envoyer l'en-tête de requête, donc le délai d'attente du prompt doit être réglé à 125 s et ne peut pas reprendre les 5 s de MQTT ; (2) {len} doit être égal au nombre d'octets du corps (ou de l'en-tête + corps si requestheader=1) ; une erreur vous bloque en mode données jusqu'à expiration de {input_time}.",
  "Émet CONNECT et passe en mode données ; la liste du répertoire s'imprime en octets bruts, et tout ce que vous tapez pendant ce temps est traité comme des données.",
  "Passe en mode données : tout ce que vous tapez pendant ce temps est traité comme des données.",
  "Passe en mode données (CONNECT → octets bruts → OK). Si le fichier n'est pas du texte brut, le terminal affiche du charabia.",
  "Téléchargement du fichier entier : un gros fichier monopolise longtemps le terminal. Vérifiez d'abord la taille avec AT+QFTPSIZE et utilisez la version par blocs pour les gros fichiers.",
  "Écrit sur le serveur distant. Après CONNECT, vous devez envoyer exactement len octets en octets bruts, sans ajouter de CR/LF. Cet outil ne peut pas lire de fichier binaire sur le disque — vous ne pouvez coller que du texte brut (caractères de contrôle via les échappements \\n \\r \\xHH)."],
 'es-ES': [
  "Activar AGNSS: el arranque en frío baja a segundos o minutos; surte efecto tras reiniciar y se escribe en la NVRAM. A partir de entonces cada arranque de GNSS descarga datos de asistencia de la red, así que hace falta un contexto PDP activo",
  "Enviar datos (en dos pasos: esperar al >, luego enviar el cuerpo; sin Ctrl+Z). Si la longitud está mal o lo abandonas a medias, el puerto AT se queda en modo datos y se traga lo que escribas después: envía ESC (0x1B) con el botón de byte en crudo de la página Hardware para salir",
  "Los bytes que se envían realmente. La longitud se cuenta en UTF-8 y se rellena sola en el <sendlen> del comando (un carácter CJK son 3 bytes); el límite es 1460 bytes (manual §2.2.3). Los caracteres de control se escriben como secuencias de escape: \\n salto de línea, \\r retorno de carro, \\t tabulador, \\0 NUL, \\xHH cualquier byte, \\\\ una barra invertida literal; se descodifican justo al enviar, y la longitud se cuenta ya descodificada. ⚠ El extremo predeterminado tcpbin responde línea a línea, así que una carga útil que no acabe en \\n no recibe ningún eco (el valor predeterminado ya lo lleva).",
  "Dos trampas: (1) el manual dice que CONNECT aparece «within 125 s»: el módulo primero tiene que abrir la conexión y enviar la cabecera de petición, así que el tiempo de espera del prompt debe ponerse en 125 s y no vale reutilizar los 5 s de MQTT; (2) {len} tiene que ser igual al número de bytes del cuerpo (o de cabecera + cuerpo si requestheader=1); si te equivocas te quedas en modo datos hasta que venza {input_time}.",
  "Emite CONNECT y entra en modo datos; el listado del directorio se imprime como bytes en crudo, y todo lo que escribas mientras tanto se toma como datos.",
  "Entra en modo datos: todo lo que escribas mientras tanto se toma como datos.",
  "Entra en modo datos (CONNECT → bytes en crudo → OK). Si el archivo no es texto plano, el terminal muestra caracteres ilegibles.",
  "Descarga del archivo entero: un archivo grande ocupa el terminal mucho rato. Comprueba antes el tamaño con AT+QFTPSIZE y usa la versión por trozos para archivos grandes.",
  "Escribe en el servidor remoto. Tras el CONNECT hay que enviar exactamente len bytes en crudo, sin añadir CR/LF. Esta herramienta no puede leer archivos binarios del disco: solo puedes pegar texto plano (los caracteres de control, con los escapes \\n \\r \\xHH)."],
 'pt-PT': [
  "Ativar o AGNSS — o arranque a frio desce para segundos ou minutos; só produz efeito após reiniciar e fica gravado na NVRAM. A partir daí cada arranque do GNSS descarrega dados de assistência da rede, pelo que é preciso um contexto PDP ativo",
  "Enviar dados (em duas fases: esperar pelo >, depois enviar o corpo; sem Ctrl+Z). Se o comprimento estiver errado ou desistir a meio, a porta AT fica em modo de dados e engole o que escrever a seguir — envie ESC (0x1B) com o botão de byte em bruto da página Hardware para sair",
  "Os bytes efetivamente enviados. O comprimento é contado em UTF-8 e preenchido automaticamente no <sendlen> do comando (um carácter CJK conta 3 bytes); o limite é 1460 bytes (manual §2.2.3). Os caracteres de controlo escrevem-se como sequências de escape: \\n mudança de linha, \\r retorno, \\t tabulação, \\0 NUL, \\xHH qualquer byte, \\\\ uma barra invertida literal — só são descodificados no momento do envio, e o comprimento é contado já descodificado. ⚠ O destino predefinido tcpbin responde linha a linha, portanto uma carga útil que não termine em \\n não recebe eco nenhum (o valor predefinido já traz um).",
  "Duas armadilhas: (1) o manual diz que o CONNECT aparece «within 125 s» — o módulo tem primeiro de abrir a ligação e enviar o cabeçalho do pedido, por isso o tempo limite de espera pelo prompt tem de ser 125 s e não pode reaproveitar os 5 s do MQTT; (2) {len} tem de ser igual ao número de bytes do corpo (ou de cabeçalho + corpo se requestheader=1); enganar-se deixa-o preso em modo de dados até {input_time} expirar.",
  "Emite CONNECT e entra em modo de dados; a listagem do diretório é impressa como bytes em bruto e tudo o que escrever entretanto é tratado como dados.",
  "Entra em modo de dados: tudo o que escrever entretanto é tratado como dados.",
  "Entra em modo de dados (CONNECT → bytes em bruto → OK). Se o ficheiro não for texto simples, o terminal mostra caracteres ilegíveis.",
  "Descarregamento do ficheiro inteiro: um ficheiro grande ocupa o terminal durante muito tempo. Confirme primeiro o tamanho com AT+QFTPSIZE e use a versão por blocos para ficheiros grandes.",
  "Escreve no servidor remoto. Depois do CONNECT tem de enviar exatamente len bytes em bruto, sem acrescentar CR/LF. Esta ferramenta não consegue ler ficheiros binários do disco — só pode colar texto simples (caracteres de controlo através dos escapes \\n \\r \\xHH)."],
 'it-IT': [
  "Attiva l'AGNSS: l'avvio a freddo scende a secondi o minuti; ha effetto dopo un riavvio ed è scritto in NVRAM. Da quel momento ogni avvio del GNSS scarica dati di assistenza dalla rete, perciò serve un contesto PDP attivo",
  "Invia dati (in due fasi: attendere >, poi inviare il corpo; niente Ctrl+Z). Se la lunghezza è sbagliata o abbandoni a metà, la porta AT resta in modalità dati e ingoia ciò che digiti dopo: manda ESC (0x1B) con il pulsante byte grezzo della pagina Hardware per uscirne",
  "I byte realmente inviati. La lunghezza è contata in UTF-8 e inserita automaticamente nel <sendlen> del comando (un carattere CJK vale 3 byte); il limite è 1460 byte (manuale §2.2.3). I caratteri di controllo si scrivono come sequenze di escape: \\n a capo, \\r ritorno carrello, \\t tabulazione, \\0 NUL, \\xHH un byte qualsiasi, \\\\ una barra rovesciata letterale: vengono decodificati solo all'invio e la lunghezza si conta dopo la decodifica. ⚠ Il destinatario predefinito tcpbin risponde riga per riga, quindi un payload che non finisce con \\n non riceve alcun eco (il valore predefinito ce l'ha già).",
  "Due trappole: (1) il manuale dice che CONNECT arriva «within 125 s»: il modulo deve prima aprire la connessione e inviare l'header della richiesta, quindi il timeout di attesa del prompt va portato a 125 s e non si possono riusare i 5 s di MQTT; (2) {len} deve essere uguale al numero di byte del corpo (o di header + corpo se requestheader=1); sbagliarlo ti lascia bloccato in modalità dati finché non scade {input_time}.",
  "Emette CONNECT ed entra in modalità dati; l'elenco della directory viene stampato come byte grezzi e tutto ciò che digiti nel frattempo è trattato come dati.",
  "Entra in modalità dati: tutto ciò che digiti nel frattempo è trattato come dati.",
  "Entra in modalità dati (CONNECT → byte grezzi → OK). Se il file non è testo semplice il terminale mostra caratteri illeggibili.",
  "Scaricamento dell'intero file: un file grande occupa il terminale a lungo. Controlla prima la dimensione con AT+QFTPSIZE e per i file grandi usa la versione a blocchi.",
  "Scrive sul server remoto. Dopo il CONNECT devi inviare esattamente len byte come byte grezzi, senza aggiungere CR/LF. Questo strumento non può leggere file binari dal disco: si può solo incollare testo semplice (i caratteri di controllo con gli escape \\n \\r \\xHH)."],
 'ru-RU': [
  "Включить AGNSS — холодный старт сокращается до секунд или минут; действует после перезагрузки, записывается в NVRAM. После этого каждый запуск GNSS скачивает вспомогательные данные из сети, поэтому нужен активный контекст PDP",
  "Отправить данные (в два этапа: дождаться >, затем отправить тело; Ctrl+Z не нужен). Если длина указана неверно или вы бросили на полпути, AT-порт останется в режиме данных и будет проглатывать всё, что вы наберёте дальше, — отправьте ESC (0x1B) кнопкой сырого байта на странице Hardware, чтобы выйти",
  "Байты, которые действительно уходят. Длина считается в UTF-8 и сама подставляется в <sendlen> команды (иероглиф — 3 байта); предел 1460 байт (руководство §2.2.3). Управляющие символы пишутся escape-последовательностями: \\n перевод строки, \\r возврат каретки, \\t табуляция, \\0 NUL, \\xHH произвольный байт, \\\\ сама обратная косая черта — они раскрываются только при отправке, и длина считается уже после раскрытия. ⚠ Адресат по умолчанию tcpbin отвечает построчно, поэтому полезная нагрузка, не оканчивающаяся на \\n, не получит эха вовсе (в значении по умолчанию он уже есть).",
  "Две ловушки: (1) в руководстве сказано, что CONNECT появляется «within 125 s» — модулю нужно сперва установить соединение и отправить заголовок запроса, поэтому тайм-аут ожидания приглашения надо ставить в 125 с, а не брать 5 с от MQTT; (2) {len} должно равняться числу байт тела (или заголовка + тела при requestheader=1); ошибка запирает вас в режиме данных до истечения {input_time}.",
  "Выдаёт CONNECT и переходит в режим данных; список каталога печатается сырыми байтами, а всё, что вы наберёте в это время, считается данными.",
  "Переходит в режим данных: всё, что вы наберёте в это время, считается данными.",
  "Переходит в режим данных (CONNECT → сырые байты → OK). Если файл не текстовый, в терминале будет мусор.",
  "Скачивание файла целиком: большой файл надолго займёт терминал. Сначала проверьте размер командой AT+QFTPSIZE, а для больших файлов используйте вариант с разбиением.",
  "Пишет на удалённый сервер. После CONNECT нужно отправить ровно len байт сырыми байтами, без добавления CR/LF. Этот инструмент не умеет читать двоичные файлы с диска — вставить можно только обычный текст (управляющие символы через escape-последовательности \\n \\r \\xHH)."],
 'vi-VN': [
  "Bật AGNSS — khởi động nguội rút xuống còn vài giây đến vài phút; có hiệu lực sau khi khởi động lại, ghi vào NVRAM. Từ đó mỗi lần khởi động GNSS sẽ tải dữ liệu hỗ trợ từ mạng, nên cần có PDP context đang hoạt động",
  "Gửi dữ liệu (hai bước: chờ >, rồi gửi phần thân; không cần Ctrl+Z). Nếu tính sai độ dài hoặc bỏ dở giữa chừng, cổng AT sẽ kẹt ở chế độ dữ liệu và nuốt những gì bạn gõ tiếp — gửi ESC (0x1B) bằng nút byte thô ở trang Hardware là thoát được",
  "Số byte thật sự được gửi đi. Độ dài tính theo UTF-8 và tự điền vào <sendlen> của lệnh (một chữ CJK là 3 byte); giới hạn là 1460 byte (sổ tay §2.2.3). Ký tự điều khiển viết bằng chuỗi thoát: \\n xuống dòng, \\r về đầu dòng, \\t Tab, \\0 NUL, \\xHH byte bất kỳ, \\\\ chính dấu gạch chéo ngược — chúng chỉ được giải mã ngay lúc gửi, và độ dài cũng đếm sau khi giải mã. ⚠ Đầu kia mặc định tcpbin vọng theo từng dòng, nên payload không kết thúc bằng \\n sẽ chẳng có echo nào (giá trị mặc định đã kèm sẵn).",
  "Hai cái bẫy: (1) sổ tay ghi CONNECT xuất hiện «within 125 s» — module phải mở kết nối và gửi request header trước, nên thời gian chờ dấu nhắc phải đặt 125 s, không dùng lại 5 giây của MQTT; (2) {len} phải bằng đúng số byte của phần thân (hoặc header + thân nếu requestheader=1); tính sai là kẹt ở chế độ dữ liệu cho tới khi {input_time} hết hạn.",
  "Xuất CONNECT rồi vào chế độ dữ liệu; danh sách thư mục in ra dạng byte thô, và mọi ký tự bạn gõ trong lúc đó đều bị coi là dữ liệu.",
  "Vào chế độ dữ liệu: mọi ký tự bạn gõ trong lúc đó đều bị coi là dữ liệu.",
  "Vào chế độ dữ liệu (CONNECT → byte thô → OK). Nếu tệp không phải văn bản thuần, terminal sẽ hiện ký tự lỗi.",
  "Tải nguyên tệp: tệp lớn sẽ chiếm terminal rất lâu. Hãy dùng AT+QFTPSIZE kiểm tra kích thước trước, tệp lớn thì chuyển sang bản chia khối.",
  "Ghi lên máy chủ từ xa. Sau CONNECT phải gửi đúng len byte ở dạng byte thô, không được thêm CR/LF. Công cụ này không đọc được tệp nhị phân từ đĩa — chỉ dán được văn bản thuần (ký tự điều khiển dùng chuỗi thoát \\n \\r \\xHH)."],
 'id-ID': [
  "Nyalakan AGNSS — mulai dingin turun ke hitungan detik sampai menit; berlaku setelah dimulai ulang dan ditulis ke NVRAM. Sesudah itu setiap kali GNSS dinyalakan akan mengunduh data bantuan dari jaringan, jadi perlu PDP context yang aktif",
  "Kirim data (dua tahap: tunggu >, lalu kirim badannya; tanpa Ctrl+Z). Kalau panjangnya salah atau Anda batalkan di tengah jalan, port AT tetap di mode data dan menelan apa pun yang Anda ketik berikutnya — kirim ESC (0x1B) dengan tombol byte mentah di halaman Hardware untuk keluar",
  "Byte yang benar-benar dikirim. Panjangnya dihitung dalam UTF-8 dan diisikan sendiri ke <sendlen> perintah (satu aksara CJK dihitung 3 byte); batasnya 1460 byte (manual §2.2.3). Karakter kendali ditulis sebagai urutan escape: \\n baris baru, \\r kembali ke awal baris, \\t Tab, \\0 NUL, \\xHH byte apa saja, \\\\ garis miring terbalik itu sendiri — semuanya baru diterjemahkan saat pengiriman, dan panjangnya dihitung setelah diterjemahkan. ⚠ Lawan bicara bawaan tcpbin menggemakan baris per baris, jadi payload yang tidak diakhiri \\n sama sekali tidak akan digemakan (nilai bawaan sudah memakainya).",
  "Dua jebakan: (1) manual menyebut CONNECT muncul «within 125 s» — modul harus membuka koneksi dan mengirim request header dulu, jadi batas waktu menunggu prompt harus disetel 125 s, tidak bisa memakai 5 detik milik MQTT; (2) {len} harus sama dengan jumlah byte badan pesan (atau header + badan bila requestheader=1); salah hitung membuat Anda terjebak di mode data sampai {input_time} habis.",
  "Mengeluarkan CONNECT lalu masuk mode data; daftar direktori dicetak sebagai byte mentah, dan apa pun yang Anda ketik sementara itu dianggap data.",
  "Masuk mode data: apa pun yang Anda ketik sementara itu dianggap data.",
  "Masuk mode data (CONNECT → byte mentah → OK). Kalau berkasnya bukan teks polos, terminal akan menampilkan karakter kacau.",
  "Unduh seluruh berkas: berkas besar akan menyita terminal lama sekali. Periksa dulu ukurannya dengan AT+QFTPSIZE, dan untuk berkas besar pakai versi berpotongan.",
  "Menulis ke server jarak jauh. Setelah CONNECT Anda harus mengirim tepat len byte sebagai byte mentah, tanpa menambahkan CR/LF. Alat ini tidak bisa membaca berkas biner dari cakram — yang bisa ditempel hanya teks polos (karakter kendali lewat escape \\n \\r \\xHH)."],
 'ms-MY': [
  "Hidupkan AGNSS — permulaan sejuk turun kepada beberapa saat hingga minit; berkuat kuasa selepas dimulakan semula dan ditulis ke NVRAM. Selepas itu setiap kali GNSS dihidupkan ia akan memuat turun data bantuan daripada rangkaian, jadi PDP context yang aktif diperlukan",
  "Hantar data (dua peringkat: tunggu >, kemudian hantar badannya; tanpa Ctrl+Z). Jika panjangnya salah atau anda batalkan di pertengahan, port AT kekal dalam mod data dan menelan apa sahaja yang anda taip selepas itu — hantar ESC (0x1B) dengan butang bait mentah pada halaman Hardware untuk keluar",
  "Bait yang benar-benar dihantar. Panjangnya dikira dalam UTF-8 dan diisi sendiri ke dalam <sendlen> arahan (satu aksara CJK dikira 3 bait); hadnya 1460 bait (manual §2.2.3). Aksara kawalan ditulis sebagai jujukan pelarian: \\n baris baharu, \\r kembali ke awal baris, \\t Tab, \\0 NUL, \\xHH sebarang bait, \\\\ garis condong ke belakang itu sendiri — semuanya hanya dinyahkod semasa penghantaran, dan panjangnya dikira selepas dinyahkod. ⚠ Pihak lalai tcpbin menggemakan baris demi baris, jadi muatan yang tidak berakhir dengan \\n langsung tidak akan digemakan (nilai lalai sudah membawanya).",
  "Dua perangkap: (1) manual menyatakan CONNECT muncul «within 125 s» — modul perlu membuka sambungan dan menghantar request header dahulu, jadi had masa menunggu gesaan mesti ditetapkan 125 s dan tidak boleh menggunakan 5 saat milik MQTT; (2) {len} mesti sama dengan bilangan bait badan mesej (atau pengepala + badan jika requestheader=1); tersilap kira menyebabkan anda terperangkap dalam mod data sehingga {input_time} tamat.",
  "Mengeluarkan CONNECT dan masuk mod data; senarai direktori dicetak sebagai bait mentah, dan apa sahaja yang anda taip ketika itu dianggap data.",
  "Masuk mod data: apa sahaja yang anda taip ketika itu dianggap data.",
  "Masuk mod data (CONNECT → bait mentah → OK). Jika failnya bukan teks biasa, terminal akan memaparkan aksara bercelaru.",
  "Muat turun seluruh fail: fail besar akan menduduki terminal untuk masa yang lama. Semak saiznya dahulu dengan AT+QFTPSIZE, dan bagi fail besar gunakan versi berketul.",
  "Menulis ke pelayan jauh. Selepas CONNECT anda mesti menghantar tepat len bait sebagai bait mentah, tanpa menambah CR/LF. Alat ini tidak boleh membaca fail binari daripada cakera — yang boleh ditampal hanyalah teks biasa (aksara kawalan melalui pelarian \\n \\r \\xHH)."],
 'th-TH': [
  "เปิด AGNSS — การเริ่มแบบเย็นลดเหลือระดับวินาทีถึงนาที มีผลหลังรีสตาร์ตและเขียนลง NVRAM จากนั้นทุกครั้งที่เริ่ม GNSS จะดาวน์โหลดข้อมูลช่วยเหลือจากเครือข่าย จึงต้องมี PDP context ที่เปิดใช้งานอยู่",
  "ส่งข้อมูล (สองขั้น: รอ > แล้วจึงส่งเนื้อหา ไม่ต้อง Ctrl+Z) ถ้าคำนวณความยาวผิดหรือยกเลิกกลางคัน พอร์ต AT จะค้างในโหมดข้อมูลและกลืนสิ่งที่คุณพิมพ์ต่อไป — ส่ง ESC (0x1B) ด้วยปุ่มส่งไบต์ดิบในหน้า Hardware ก็ออกได้",
  "ไบต์ที่ส่งออกไปจริง ความยาวนับแบบ UTF-8 และเติมลงใน <sendlen> ของคำสั่งให้เอง (อักษร CJK หนึ่งตัวนับ 3 ไบต์) ขีดจำกัดคือ 1460 ไบต์ (คู่มือ §2.2.3) อักขระควบคุมเขียนเป็นลำดับหลีก: \\n ขึ้นบรรทัดใหม่, \\r ปัดแคร่, \\t Tab, \\0 NUL, \\xHH ไบต์ใดก็ได้, \\\\ ตัวแบ็กสแลชเอง — ทั้งหมดจะถูกถอดรหัสตอนส่งเท่านั้น และความยาวก็นับหลังถอดรหัสแล้ว ⚠ ปลายทางเริ่มต้น tcpbin สะท้อนกลับทีละบรรทัด ดังนั้น payload ที่ไม่ลงท้ายด้วย \\n จะไม่ได้ echo เลย (ค่าเริ่มต้นใส่มาให้แล้ว)",
  "กับดักสองข้อ: (1) คู่มือเขียนว่า CONNECT จะปรากฏ «within 125 s» — เพราะโมดูลต้องสร้างการเชื่อมต่อและส่ง request header ก่อน ดังนั้นเวลารอสัญลักษณ์พร้อมต้องตั้ง 125 วินาที ใช้ 5 วินาทีแบบ MQTT ไม่ได้ (2) {len} ต้องเท่ากับจำนวนไบต์ของเนื้อหา (หรือส่วนหัว + เนื้อหา ถ้า requestheader=1) คำนวณผิดจะค้างอยู่ในโหมดข้อมูลจนกว่า {input_time} จะหมดเวลา",
  "จะส่ง CONNECT ออกมาแล้วเข้าสู่โหมดข้อมูล รายการไดเรกทอรีพิมพ์ออกมาเป็นไบต์ดิบ และทุกอักขระที่คุณพิมพ์ระหว่างนั้นจะถูกถือเป็นข้อมูล",
  "เข้าสู่โหมดข้อมูล: ทุกอักขระที่คุณพิมพ์ระหว่างนั้นจะถูกถือเป็นข้อมูล",
  "เข้าสู่โหมดข้อมูล (CONNECT → ไบต์ดิบ → OK) ถ้าไฟล์ไม่ใช่ข้อความล้วน เทอร์มินัลจะแสดงอักขระเพี้ยน",
  "ดาวน์โหลดทั้งไฟล์: ไฟล์ใหญ่จะยึดเทอร์มินัลไว้นาน ควรใช้ AT+QFTPSIZE ตรวจขนาดก่อน และไฟล์ใหญ่ให้เปลี่ยนไปใช้รุ่นแบ่งช่วง",
  "เขียนลงเซิร์ฟเวอร์ปลายทาง หลังได้ CONNECT ต้องส่งไบต์ดิบให้ครบ len ไบต์พอดี ห้ามต่อท้ายด้วย CR/LF เครื่องมือนี้อ่านไฟล์ไบนารีจากดิสก์ไม่ได้ วางได้เฉพาะข้อความล้วน (อักขระควบคุมใช้ลำดับหลีก \\n \\r \\xHH)"],
 'hi-IN': [
  "AGNSS चालू करें — ठंडा आरंभ घटकर सेकंड-मिनट के स्तर पर आ जाता है; दोबारा चालू करने पर प्रभावी होता है और NVRAM में लिखा जाता है। उसके बाद हर GNSS आरंभ पर नेटवर्क से सहायक डेटा उतरता है, इसलिए सक्रिय PDP context चाहिए",
  "डेटा भेजें (दो चरण: > की प्रतीक्षा करें, फिर मुख्य भाग भेजें; Ctrl+Z की ज़रूरत नहीं)। लंबाई ग़लत हो या आप बीच में छोड़ दें, तो AT पोर्ट डेटा मोड में अटका रहता है और आगे टाइप किया सब निगल जाता है — निकलने के लिए Hardware पृष्ठ के रॉ-बाइट बटन से ESC (0x1B) भेजें",
  "वास्तव में भेजे जाने वाले बाइट। लंबाई UTF-8 में गिनी जाती है और आदेश के <sendlen> में अपने आप भर जाती है (एक CJK अक्षर 3 बाइट); सीमा 1460 बाइट है (नियमावली §2.2.3)। नियंत्रण वर्ण एस्केप अनुक्रम से लिखें: \\n नई पंक्ति, \\r गाड़ी वापसी, \\t Tab, \\0 NUL, \\xHH कोई भी बाइट, \\\\ स्वयं बैकस्लैश — ये भेजते समय ही खोले जाते हैं, और लंबाई भी खोलने के बाद गिनी जाती है। ⚠ डिफ़ॉल्ट दूसरा छोर tcpbin पंक्ति-दर-पंक्ति लौटाता है, इसलिए जो payload \\n पर ख़त्म न हो उसका कोई एको नहीं आता (डिफ़ॉल्ट मान में पहले से है)।",
  "दो जाल: (1) नियमावली कहती है CONNECT «within 125 s» में आता है — मॉड्यूल को पहले कनेक्शन खोलकर request header भेजना होता है, इसलिए प्रॉम्प्ट की प्रतीक्षा-सीमा 125 s रखनी पड़ती है, MQTT वाले 5 सेकंड नहीं चलेंगे; (2) {len} बिलकुल body के बाइट जितना होना चाहिए (requestheader=1 हो तो «शीर्षलेख + body» का जोड़); ग़लती हुई तो {input_time} बीतने तक डेटा मोड में फँसे रहेंगे।",
  "CONNECT निकालकर डेटा मोड में चला जाता है; निर्देशिका सूची कच्चे बाइट के रूप में छपती है, और उस दौरान आप जो भी टाइप करें वह डेटा माना जाता है।",
  "डेटा मोड में चला जाता है: उस दौरान आप जो भी टाइप करें वह डेटा माना जाता है।",
  "डेटा मोड में चला जाता है (CONNECT → कच्चे बाइट → OK)। फ़ाइल सादा पाठ न हो तो टर्मिनल पर अटपटे अक्षर दिखेंगे।",
  "पूरी फ़ाइल डाउनलोड: बड़ी फ़ाइल टर्मिनल को लंबे समय तक घेरे रखेगी। पहले AT+QFTPSIZE से आकार जाँच लें, और बड़ी फ़ाइलों के लिए खंडों वाला संस्करण उपयोग करें।",
  "दूरस्थ सर्वर पर लिखता है। CONNECT मिलने के बाद ठीक len बाइट कच्चे बाइट के रूप में भेजने होंगे, CR/LF जोड़े बिना। यह उपकरण डिस्क से द्विआधारी फ़ाइल नहीं पढ़ सकता — केवल सादा पाठ चिपकाया जा सकता है (नियंत्रण वर्ण \\n \\r \\xHH एस्केप से)।"],
 'tr-TR': [
  "AGNSS'i aç — soğuk başlangıç saniyeler ya da dakikalar seviyesine iner; yeniden başlatmadan sonra etkin olur ve NVRAM'a yazılır. Bundan sonra her GNSS başlangıcı ağdan yardımcı veri indirir, dolayısıyla etkin bir PDP context gerekir",
  "Veri gönder (iki aşamalı: > işaretini bekleyin, sonra gövdeyi gönderin; Ctrl+Z gerekmez). Uzunluk yanlışsa ya da yarıda bırakırsanız AT bağlantı noktası veri kipinde kalır ve sonrasında yazdıklarınızı yutar — çıkmak için Hardware sayfasındaki ham bayt düğmesiyle ESC (0x1B) gönderin",
  "Gerçekten gönderilen baytlar. Uzunluk UTF-8 olarak sayılır ve komutun <sendlen> alanına kendiliğinden yazılır (bir CJK karakteri 3 bayttır); sınır 1460 bayttır (kılavuz §2.2.3). Denetim karakterlerini kaçış dizileriyle yazın: \\n satır sonu, \\r satır başı, \\t sekme, \\0 NUL, \\xHH herhangi bir bayt, \\\\ ters eğik çizginin kendisi — bunlar yalnızca gönderim anında çözülür ve uzunluk da çözüldükten sonra sayılır. ⚠ Varsayılan karşı taraf tcpbin satır satır yankılar, bu yüzden \\n ile bitmeyen bir yük hiç yankı almaz (varsayılan değerde zaten var).",
  "İki tuzak: (1) kılavuz CONNECT'in «within 125 s» içinde geldiğini söyler — modülün önce bağlantıyı kurup istek başlığını göndermesi gerekir, bu yüzden istem bekleme süresi 125 s olmalıdır, MQTT'nin 5 saniyesi kullanılamaz; (2) {len}, gövdenin bayt sayısına eşit olmalıdır (requestheader=1 ise «başlık + gövde» toplamına); yanlış hesaplarsanız {input_time} dolana kadar veri kipinde kalırsınız.",
  "CONNECT verip veri kipine geçer; dizin listesi ham bayt olarak basılır ve bu sırada yazdığınız her şey veri sayılır.",
  "Veri kipine geçer: bu sırada yazdığınız her şey veri sayılır.",
  "Veri kipine geçer (CONNECT → ham bayt → OK). Dosya düz metin değilse uçbirimde bozuk karakterler görünür.",
  "Dosyanın tamamını indirir: büyük bir dosya uçbirimi uzun süre meşgul eder. Önce AT+QFTPSIZE ile boyutu denetleyin, büyük dosyalar için parçalı sürümü kullanın.",
  "Uzak sunucuya yazar. CONNECT geldikten sonra tam olarak len bayt ham bayt biçiminde gönderilmelidir, CR/LF eklenmeden. Bu araç diskteki ikili dosyaları okuyamaz — yalnızca düz metin yapıştırabilirsiniz (denetim karakterleri \\n \\r \\xHH kaçışlarıyla)."],
 'ar-SA': [
  "تفعيل AGNSS —— يهبط البدء البارد إلى ثوانٍ أو دقائق؛ ولا يسري إلا بعد إعادة التشغيل ويُكتب في NVRAM. وبعدها يُنزِّل كل تشغيل لنظام GNSS بيانات مساعدة من الشبكة، فيلزم سياق PDP مفعَّل",
  "إرسال بيانات (على مرحلتين: انتظر العلامة > ثم أرسل المتن؛ ولا حاجة إلى Ctrl+Z). وإذا أخطأت في الطول أو تراجعت في المنتصف بقي منفذ AT في وضع البيانات وابتلع ما تكتبه بعد ذلك —— أرسل ESC (0x1B) بزر البايت الخام في صفحة Hardware لتخرج",
  "البايتات التي تُرسَل فعلاً. يُحسب الطول بترميز UTF-8 ويوضع تلقائياً في <sendlen> ضمن الأمر (الحرف الصيني/الياباني/الكوري يساوي 3 بايت)، والحد الأقصى 1460 بايت (الدليل §2.2.3). وتُكتب محارف التحكم بصيغة الهروب: ‏\\n سطر جديد، و\\r إرجاع، و\\t جدولة، و\\0 محرف NUL، و\\xHH أي بايت، و\\\\ الشرطة المائلة العكسية نفسها —— ولا تُفكَّك إلا لحظة الإرسال، ويُحسب الطول بعد التفكيك. ⚠ والطرف الافتراضي tcpbin يُعيد الصدى سطراً بسطر، فالحمولة التي لا تنتهي بـ \\n لا تحصل على صدى إطلاقاً (والقيمة الافتراضية تتضمنه أصلاً).",
  "مَزلقان اثنان: (1) يذكر الدليل أن CONNECT يظهر «within 125 s» —— لأن الموديل يفتح الاتصال أولاً ويرسل ترويسة الطلب، فيجب ضبط مهلة انتظار المحث على 125 ثانية ولا يصح استعمال مهلة MQTT البالغة 5 ثوانٍ؛ (2) يجب أن يساوي {len} عدد بايتات المتن (أو مجموع «الترويسة + المتن» إذا كان requestheader=1)، والخطأ فيه يبقيك حبيس وضع البيانات حتى تنقضي {input_time}.",
  "يُخرج CONNECT ويدخل وضع البيانات؛ وتُطبع قائمة الدليل بايتات خاماً، وكل ما تكتبه في تلك الأثناء يُعامَل بوصفه بيانات.",
  "يدخل وضع البيانات: وكل ما تكتبه في تلك الأثناء يُعامَل بوصفه بيانات.",
  "يدخل وضع البيانات (‏CONNECT ← بايتات خام ← OK). وإذا لم يكن الملف نصاً صِرفاً ظهرت في الطرفية محارف مشوَّشة.",
  "تنزيل الملف كاملاً: الملف الكبير يشغل الطرفية وقتاً طويلاً. تحقَّق من الحجم أولاً بالأمر AT+QFTPSIZE، واستعمل النسخة المجزَّأة للملفات الكبيرة.",
  "يكتب على الخادم البعيد. وبعد CONNECT يجب إرسال len بايت بالضبط بايتاتٍ خاماً، دون إلحاق CR/LF. ولا تستطيع هذه الأداة قراءة الملفات الثنائية من القرص —— فلا يمكن لصق سوى نص صِرف (ومحارف التحكم عبر صيغ الهروب \\n و\\r و\\xHH)."],
 'he-IL': [
  "הפעלת AGNSS — התנעה קרה יורדת לרמת שניות עד דקות; נכנס לתוקף רק לאחר הפעלה מחדש ונכתב ל-NVRAM. מכאן ואילך כל הפעלה של ה-GNSS מורידה נתוני סיוע מהרשת, ולכן נדרש הקשר PDP פעיל",
  "שליחת נתונים (בשני שלבים: להמתין ל-> ואז לשלוח את הגוף; אין צורך ב-Ctrl+Z). אם האורך שגוי או שנטשת באמצע, יציאת ה-AT נשארת במצב נתונים ובולעת את מה שתקליד לאחר מכן — שלח ESC (0x1B) בעזרת כפתור הבית הגולמי שבעמוד Hardware כדי לצאת",
  "הבתים שנשלחים בפועל. האורך נספר ב-UTF-8 ומוזן אוטומטית ל-<sendlen> של הפקודה (תו CJK שווה 3 בתים); המגבלה היא 1460 בתים (מדריך §2.2.3). תווי בקרה נכתבים כרצפי בריחה: \\n שורה חדשה, \\r חזרת גררה, \\t טאב, \\0 NUL, \\xHH בית כלשהו, \\\\ הלוכסן ההפוך עצמו — הם מפוענחים רק ברגע השליחה, והאורך נספר לאחר הפענוח. ⚠ הצד המרוחק שבברירת המחדל, tcpbin, מהדהד שורה-שורה, ולכן מטען שאינו מסתיים ב-\\n לא יקבל הד כלל (בערך ברירת המחדל כבר יש כזה).",
  "שתי מלכודות: (1) המדריך אומר ש-CONNECT מופיע «within 125 s» — המודול צריך קודם לפתוח את החיבור ולשלוח את כותרת הבקשה, ולכן פסק הזמן להמתנה לסימן חייב להיות 125 שניות ואי אפשר לאמץ את 5 השניות של MQTT; (2) ‏{len} חייב להיות שווה למספר הבתים של הגוף (או של כותרת + גוף כאשר requestheader=1); טעות כאן משאירה אותך תקוע במצב נתונים עד שיפוג {input_time}.",
  "פולט CONNECT ונכנס למצב נתונים; רשימת הספרייה מודפסת כבתים גולמיים, וכל מה שתקליד בינתיים ייחשב לנתונים.",
  "נכנס למצב נתונים: כל מה שתקליד בינתיים ייחשב לנתונים.",
  "נכנס למצב נתונים (‏CONNECT ← בתים גולמיים ← OK). אם הקובץ אינו טקסט פשוט, המסוף יציג ג'יבריש.",
  "הורדת הקובץ כולו: קובץ גדול יתפוס את המסוף לאורך זמן רב. בדוק תחילה את הגודל עם AT+QFTPSIZE, ולקבצים גדולים השתמש בגרסה המקוטעת.",
  "כותב אל השרת המרוחק. לאחר CONNECT יש לשלוח בדיוק len בתים כבתים גולמיים, בלי להוסיף CR/LF. הכלי הזה אינו יכול לקרוא קבצים בינריים מהדיסק — אפשר להדביק רק טקסט פשוט (תווי בקרה באמצעות רצפי הבריחה \\n \\r \\xHH)."],
 'fa-IR': [
  "روشن کردن AGNSS — راه‌اندازی سرد به چند ثانیه تا چند دقیقه کاهش می‌یابد؛ پس از راه‌اندازی دوباره اثر می‌کند و در NVRAM نوشته می‌شود. از آن پس هر بار که GNSS آغاز شود داده‌های کمکی را از شبکه می‌گیرد، پس بافت PDP فعال لازم است",
  "فرستادن داده (دو مرحله‌ای: منتظر > بمانید، سپس بدنه را بفرستید؛ به Ctrl+Z نیازی نیست). اگر طول را اشتباه بزنید یا میان راه رها کنید، درگاه AT در حالت داده می‌ماند و هرچه بعد بنویسید می‌بلعد — برای بیرون آمدن، ESC ‏(0x1B) را با دکمهٔ بایت خام در صفحهٔ Hardware بفرستید",
  "بایت‌هایی که واقعاً فرستاده می‌شوند. طول با UTF-8 شمرده می‌شود و خودبه‌خود در <sendlen> فرمان می‌نشیند (هر نویسهٔ CJK سه بایت است)؛ سقف ۱۴۶۰ بایت است (راهنما §2.2.3). نویسه‌های کنترلی را با دنباله‌های گریز بنویسید: \\n خط جدید، \\r بازگشت، \\t جهش، \\0 نویسهٔ NUL، \\xHH هر بایتی، \\\\ خودِ ممیز وارونه — این‌ها تنها هنگام فرستادن رمزگشایی می‌شوند و طول هم پس از رمزگشایی شمرده می‌شود. ⚠ طرف پیش‌فرض یعنی tcpbin سطر به سطر پژواک می‌دهد، پس باری که به \\n ختم نشود هیچ پژواکی نمی‌گیرد (مقدار پیش‌فرض آن را دارد).",
  "دو دام: (۱) راهنما می‌گوید CONNECT در «within 125 s» می‌آید — چون ماژول نخست باید اتصال را برقرار و سرآیند درخواست را ارسال کند، پس مهلت انتظار برای نشانه باید ۱۲۵ ثانیه باشد و نمی‌توان ۵ ثانیهٔ MQTT را به کار برد؛ (۲) ‏{len} باید برابر شمار بایت‌های بدنه باشد (یا «سرآیند + بدنه» اگر requestheader=1 باشد)؛ اشتباه در آن شما را تا پایان {input_time} در حالت داده گرفتار می‌کند.",
  "‏CONNECT را بیرون می‌دهد و به حالت داده می‌رود؛ فهرست پوشه به صورت بایت خام چاپ می‌شود و هرچه در آن میان بنویسید داده به شمار می‌آید.",
  "به حالت داده می‌رود: هرچه در آن میان بنویسید داده به شمار می‌آید.",
  "به حالت داده می‌رود (‏CONNECT ← بایت خام ← OK). اگر پرونده متن ساده نباشد، پایانه نویسه‌های درهم نشان می‌دهد.",
  "بارگیری کل پرونده: پروندهٔ بزرگ مدت زیادی پایانه را اشغال می‌کند. نخست اندازه را با AT+QFTPSIZE بررسی کنید و برای پرونده‌های بزرگ از نسخهٔ تکه‌ای استفاده کنید.",
  "روی کارساز دوردست می‌نویسد. پس از CONNECT باید دقیقاً len بایت را به صورت بایت خام بفرستید، بدون افزودن CR/LF. این ابزار نمی‌تواند پرونده‌های دودویی را از دیسک بخواند — تنها متن ساده می‌توان چسباند (نویسه‌های کنترلی با گریزهای \\n و \\r و \\xHH)."],
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
