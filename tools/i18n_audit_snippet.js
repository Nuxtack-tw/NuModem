// NuModem 多語系稽核：找出「切到某語言後畫面上仍是中文」的字串。
//
// 為什麼需要這支：靜態抽取永遠會漏（V26.0.60 就漏了兩整類 ——
// 對照表的值、以及寫在 note 函式體裡的裸字面值）。唯一可靠的判準是
// **使用者實際看到的東西**，所以直接把整個畫面與註解引擎的輸出掃一遍。
//
// 用法：
//   1. 瀏覽器開啟 NuModem_EG800.html
//   2. 開發者工具 Console 貼上整份，執行 await auditI18n('en-US')
//   3. 回傳 { uiLeaks, anLeaks } —— 兩者都應該是空陣列
//
// 註：AT 指令原文、主機名、hex 這些本來就不翻譯，不會被誤報（它們沒有中文字元）。

window.auditI18n = async function (lang) {
    // ⚠ 日文正常就會用漢字，拿「有沒有 CJK 字元」判斷會整片誤報
    //（實測：正確譯文「SIM 状態: パスワードの入力待ちなし」被判成殘留中文）。
    // 對 ja-JP 改判「繁體專用字形」與「中文才用的標點」——
    // 下列字的日文新字體不同形（狀/状、說/説、讀/読、對/対、發/発、點/点、數/数…），
    // 出現即代表那條確實沒翻。
    // ⚠ 這張表只能放「日文新字體不同形」的字。日文照樣在用的字放進來會整片誤報 ——
    // 踩過：憶（記憶）、華（華やか）、軟（柔軟）、還（還元）、龍（龍）都是日中同形，已剔除。
    // 判準：該字的日文新字體是否另有寫法（狀→状、說→説、讀→読、對→対、發→発、點→点、數→数…）
    // ⚠「——」曾列在這裡，但日文本來就有二倍ダーシ，會把正確譯文整片誤判 —— 已移除。
    // 留下的「，；」則是日文確實不用的標點，出現即代表沒翻。
    const TRAD_ONLY = /[這麼們沒狀說讀對關發點數學實體國應與從將讓檢轉變當內經裡樣證團圖廣檔擊擴據斷歷獨產嗎藝豐雙屬鬆纖繫覽]|[，；]/;
    const CJK = (lang === 'ja-JP') ? TRAD_ONLY : /[一-鿿]/;
    const prev = window.languageManager.currentLang;
    await window.ensureAtI18n(lang);
    window.languageManager.setLanguage(lang);
    await new Promise(r => setTimeout(r, 400));

    // ── (1) 畫面上所有可見文字與 tooltip
    const uiLeaks = new Set();
    const SEL = '.cmd-group-title span, .cmd-group-desc, .cmd-btn-desc, .cmd-param-label,'
              + ' .cmd-act, .combo-item-desc, .combo-item-value, .group-desc-toggle,'
              + ' .at-tab, .term-tab, button, label, h1, h2, h3, p, span';
    document.querySelectorAll(SEL).forEach(e => {
        if (e.children.length) return;               // 只看葉節點，避免整段重複回報
        const t = (e.textContent || '').trim();
        // 語言選單本來就用各自的語言標示自己，不是漏譯
        if (e.closest('.lang-menu, .lang-dropdown, [data-lang]')) return;
        if (t && CJK.test(t)) uiLeaks.add(t.slice(0, 60));
    });
    document.querySelectorAll('[title], [placeholder], [data-tip]').forEach(e => {
        for (const a of ['title', 'placeholder', 'data-tip']) {
            const v = e.getAttribute(a);
            if (v && CJK.test(v)) uiLeaks.add('[' + a + '] ' + v.slice(0, 60));
        }
    });

    // ── (2) 註解引擎：對代表性回應行跑一遍
    // 每個指令都先 annotate(cmd,'sent') 建立上下文，回應行才會被比對到
    const m = window.serialMonitor;
    const CORPUS = [
        ['AT+CPIN?', ['+CPIN: READY', '+CPIN: SIM PIN', '+CME ERROR: 10']],
        ['AT+QPINC?', ['+QPINC: "SC",3,10']],
        ['AT+CEREG?', ['+CEREG: 2,1', '+CEREG: 0,3']],
        ['AT+CREG?', ['+CREG: 0,5']],
        ['AT+CGREG?', ['+CGREG: 0,1']],
        ['AT+COPS?', ['+COPS: 0,0,"Chunghwa",7']],
        ['AT+CFUN?', ['+CFUN: 1', '+CFUN: 4']],
        ['AT+CBC', ['+CBC: 0,80,3800']],
        ['AT+CSQ', ['+CSQ: 20,99', '+CSQ: 99,99']],
        ['AT+CGATT?', ['+CGATT: 1', '+CGATT: 0']],
        ['AT+QINISTAT', ['+QINISTAT: 7', '+QINISTAT: 0']],
        ['AT+QSIMSTAT?', ['+QSIMSTAT: 1,1']],
        ['AT+QNWINFO', ['+QNWINFO: "FDD LTE","46692","LTE BAND 3",1650']],
        ['AT+QURCCFG="urcport"', ['+QURCCFG: "urcport","uart1"', '+QURCCFG: "urcport","usbat"']],
        ['AT+IPR?', ['+IPR: 115200', '+IPR: 9600']],
        ['AT+QSCLK?', ['+QSCLK: 0', '+QSCLK: 1']],
        ['AT+CGDCONT?', ['+CGDCONT: 1,"IP","iot.1nce.net"']],
        ['AT+CEER', ['+CEER: ', '+CEER: No cause information available']],
        ['AT+QIGETERROR', ['+QIGETERROR: 0,operate successfully', '+QIGETERROR: 563,socket identity has been used']],
        ['AT+QISTATE', ['+QISTATE: 0,"TCP","3.94.7.51",4242,54321,2,1,0,0,"usbmodem"']],
        ['AT+QIRD=0,0', ['+QIRD: 12,6,6', '+QIRD: 6,6,0']],
        ['AT+QIRD=0,1500', ['+QIRD: 6', '+QIRD: 0']],
        ['AT+QISEND=0,0', ['+QISEND: 100,60,40', '+QISEND: 6,6,0']],
        ['AT+QIOPEN=1,0,"TCP","tcpbin.com",4242,0,0', ['+QIOPEN: 0,0', '+QIOPEN: 0,563']],
        ['AT+QPING=1,"8.8.8.8",4,4', ['+QPING: 0,"8.8.8.8",32,192,255', '+QPING: 569']],
        ['AT+QNTP=1,"pool.ntp.org",123', ['+QNTP: 0,"2026/08/06,12:40:04+32"']],
        ['AT+QSSLSTATE', ['+QSSLSTATE: 4,"SSL","1.2.3.4",443,1234,2,1,0,1,"uart1",1']],
        ['AT+QFTPSTAT', ['+QFTPSTAT: 0,4', '+QFTPSTAT: 0,1']],
        ['AT+QFTPOPEN="test.rebex.net",21', ['+QFTPOPEN: 0,0', '+QFTPOPEN: 604,0']],
        ['AT+QHTTPGET=80', ['+QHTTPGET: 0,200,1256', '+QHTTPGET: 701']],
        ['AT+QGPSCFG="gnssconfig"', ['+QGPSCFG: "gnssconfig",1']],
        ['AT+QGPSCFG="apflash"', ['+QGPSCFG: "apflash",1', '+QGPSCFG: "apflash",0']],
        ['AT+QAGPS?', ['+QAGPS: 0']],
        ['AT+QGPS?', ['+QGPS: 1', '+QGPS: 0']],
        ['AT+QMTCONN?', ['+QMTCONN: 0,3']],
        ['AT+QMTOPEN?', ['+QMTOPEN: 0,"broker.emqx.io",1883']],
        ['AT+QMTOPEN=0,"broker.emqx.io",1883', ['+QMTOPEN: 0,0', '+QMTOPEN: 0,3']],
        ['AT+QMTCONN=0,"numodem01"', ['+QMTCONN: 0,0,0', '+QMTCONN: 0,1,5']],
        ['AT+QMTSUB=0,1,"test/numodem",0', ['+QMTSUB: 0,1,0,0', '+QMTSUB: 0,1,1,2']],
        ['AT+QMTUNS=0,2,"test/numodem"', ['+QMTUNS: 0,2,0']],
        ['AT+QMTPUBEX=0,0,0,0,"test/numodem",5', ['+QMTPUBEX: 0,0,0']],
        ['AT+QMTDISC=0', ['+QMTDISC: 0,0']],
        ['AT+QMTCLOSE=0', ['+QMTCLOSE: 0,0']],
        ['ATO', ['CONNECT', 'NO CARRIER']],
        ['AT+QHTTPSTOP', ['+QHTTPSTOP: 0', '+QHTTPSTOP: 701']],
        ['AT+COPS=?', ['+COPS: (2,"Chunghwa","CHT","46692",7),(1,"TWM","TWM","46697",7)']],
        ['AT+QICFG=?', ['+QICFG: "tcp/keepalive",(0,1),(1-120),(25-100),(3-10)']],
        ['AT+QSSLCFG="seclevel",1', ['+QSSLCFG: "seclevel",1,2', '+QSSLCFG: "sslversion",1,4']],
        ['AT+QSSLCFG=?', ['+QSSLCFG: "seclevel",(0-5),(0-2)']],
        ['AT+QHTTPCFG?', ['+QHTTPCFG: "contenttype",4', '+QHTTPCFG: "closed/ind",1']],
        ['AT+QHTTPURL?', ['+QHTTPURL: http://www.example.com/']],
        ['AT+QFTPCFG="account"', ['+QFTPCFG: "account","demo","pw"', '+QFTPCFG: "transmode",1', '+QFTPCFG: "ssltype",1']],
        ['AT+QLBSCFG=?', ['+QLBSCFG: "asynch",(0,1)']],
        ['AT+QLBSCFG="token"', ['+QLBSCFG: "token",""', '+QLBSCFG: "token","****"']],
        ['AT+QLBSCFG="asynch"', ['+QLBSCFG: "asynch",1', '+QLBSCFG: "latOrder",0',
                                 '+QLBSCFG: "withTime",1', '+QLBSCFG: "timeUpdate",1',
                                 '+QLBSCFG: "timeout",60', '+QLBSCFG: "server","www.queclocator.com:80"']],
        ['AT+QLBS', ['+QLBS: 702', '+QLBS: 0', '+QLBS: 0,25.0336,121.5650,120', '+QLBS: 3,x']],
        ['AT&V', ['E1 Q0 V1 X4 &C1 &D2 S0:0 S3:13']],
    ];
    // 不隸屬任何指令的 URC，直接丟
    const URCS = ['RDY', '+CPIN: READY', '+QUSIM: 1', '+QIND: SMS DONE', '+QIND: PB DONE',
                  '+QIURC: "recv",0', '+QIURC: "closed",0', '+QIURC: "pdpdeact",1',
                  'SEND OK', 'SEND FAIL', 'OK', 'ERROR', '+CME ERROR: 4',
                  '+QGPSURC: 0', '+QAGPSURC: 0'];

    const anLeaks = [];
    for (const [cmd, resps] of CORPUS) {
        const c = m.annotate(cmd, 'sent');
        if (c && CJK.test(c)) anLeaks.push('→ ' + cmd + '  ⇒  ' + c.slice(0, 70));
        for (const r of resps) {
            m.annotate(cmd, 'sent');
            const a = m.annotate(r, 'received');
            if (a && CJK.test(a)) anLeaks.push('   ' + r.slice(0, 36) + '  ⇒  ' + a.slice(0, 80));
        }
    }
    for (const u of URCS) {
        const a = m.annotate(u, 'received');
        if (a && CJK.test(a)) anLeaks.push('   [URC] ' + u + '  ⇒  ' + a.slice(0, 80));
    }

    window.languageManager.setLanguage(prev);
    const res = { lang, uiLeaks: [...uiLeaks], anLeaks };
    console.log('%c[i18n audit] ' + lang + '：UI 漏 ' + res.uiLeaks.length
                + ' 處、註解漏 ' + res.anLeaks.length + ' 處',
                'font-weight:bold;color:' + (res.uiLeaks.length + res.anLeaks.length ? '#f85149' : '#39d353'));
    return res;
};
