import os
import json

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# Load JSON Data
with open('src/data/workspace.json', 'r', encoding='utf-8') as f:
    ws_data = json.load(f)

# Let's build the Swiss Grid Design CSS
swiss_css = '''
<style>
/* 
=====================================================
Swiss Grid & Architecture Minimalism (J-Hub v2.0)
=====================================================
*/
:root {
    --bg-color: #f5f5f7;
    --surface: #ffffff;
    --text-primary: #1d1d1f;
    --text-secondary: #86868b;
    --accent: #000000;
    --border: #e5e5ea;
    --radius: 0px; /* Brutalism: No rounded corners */
}

body {
    background-color: var(--bg-color);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
    letter-spacing: -0.3px;
    margin: 0;
    padding: 0;
}

header {
    background: var(--surface);
    border-bottom: 2px solid var(--accent);
    padding: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.mode-switch {
    display: flex;
    gap: 10px;
}

.mode-btn {
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s;
}

.mode-btn.active {
    background: var(--accent);
    color: #fff;
}

/* Swiss Typography */
h1, h2, h3 {
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 16px;
}

/* App Container */
#app-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
}

/* Hide all pages by default */
.page-view {
    display: none;
    animation: fadeIn 0.4s ease-out forwards;
}
.page-view.active {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Journal Mosaic overrides for Swiss aesthetic */
.grid-mosaic {
    gap: 4px !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.mosaic-block {
    border-radius: 0 !important;
    box-shadow: none !important;
    filter: grayscale(100%);
    transition: filter 0.3s, transform 0.3s !important;
}
.mosaic-block:hover {
    filter: grayscale(0%);
    transform: scale(1.02) !important;
    z-index: 10;
    border: 1px solid #000;
}
.mosaic-block.active {
    filter: grayscale(0%);
    border: 2px solid #000 !important;
    box-shadow: none !important;
}

/* Workspace Accordion UI */
.wa-container {
    margin-bottom: 24px;
    border: 1px solid var(--accent);
    background: var(--surface);
}
.wa-header {
    padding: 24px;
    background: #fafafc;
    border-bottom: 1px solid var(--accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    user-select: none;
}
.wa-header:hover {
    background: #f0f0f5;
}
.wa-title {
    font-size: 24px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -1px;
    margin: 0;
}
.wa-icon {
    font-size: 24px;
    font-weight: 300;
    transition: transform 0.3s;
}
.wa-container.collapsed .wa-content {
    display: none;
}
.wa-container.collapsed .wa-header {
    border-bottom: none;
}
.wa-container.collapsed .wa-icon {
    transform: rotate(180deg);
}
.wa-content {
    padding: 32px;
}

/* Workspace Tables & Typography (Readable Design) */
.workspace-card h2, .workspace-card h3 {
    font-size: 20px;
    letter-spacing: -0.5px;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 16px;
    text-transform: uppercase;
}

.card-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px; /* Global rule minimum for 50-60 age group */
    line-height: 1.6;
    margin-bottom: 24px;
}

.table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.card-table th {
    text-align: left;
    font-weight: 600;
    color: var(--text-secondary);
    padding: 12px;
    border-bottom: 1px solid #e0e0e0; /* Apple hairline border */
}

.card-table td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0; /* Apple hairline border */
    color: var(--text-primary);
}

.card-table tr:nth-child(even) td {
    background-color: #fafafc; /* Apple pure parchment/even row color */
}

.card-table tr:hover td {
    background-color: #f0f0f5;
    transition: background-color 0.2s;
}

/* Badge and specific highlighting */
.highlight-red {
    color: #e30000;
    font-weight: 600;
}
.highlight-blue {
    color: #0066cc;
    font-weight: 600;
}


/* Workspace Interior Elements (Swiss Grid Adaptation) */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    margin-bottom: 32px;
    align-items: start;
}
@media (max-width: 768px) {
    .grid-2 { grid-template-columns: 1fr; }
}

.hero {
    background: transparent;
    border-bottom: 4px solid var(--accent);
    padding: 0 0 16px 0;
    margin-bottom: 32px;
}
.hero h1 {
    font-size: 32px;
    margin: 0 0 8px 0;
    text-transform: uppercase;
    letter-spacing: -1px;
}
.hero p {
    font-size: 16px;
    color: var(--text-secondary);
    margin: 0;
}

.card {
    background: var(--surface);
    border: 1px solid var(--accent); /* Brutalism strict borders */
    padding: 24px;
    box-shadow: none;
    border-radius: 0;
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-bottom: 0 !important;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}

.tag-row {
    margin-bottom: 8px; /* Fixes overlap with report-title */
}
.chip {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    text-transform: uppercase;
    border: 1px solid var(--accent);
    background: transparent;
    color: var(--accent);
}
.chip.red {
    border-color: var(--text-primary);
    color: var(--surface);
    background: var(--text-primary); /* Swiss Grid high contrast instead of raw red */
}
.chip.blue, .chip.green {
    border-color: var(--text-secondary);
    color: var(--text-secondary);
    background: transparent;
}

ul {
    list-style-type: square; /* Swiss modernism list style */
    padding-left: 20px;
    margin: 0;
}
li {
    margin-bottom: 8px;
    font-size: 14px;
    color: var(--text-primary);
}
.highlight {
    font-weight: 700;
    background: rgba(0,0,0,0.05);
    padding: 2px 4px;
}

/* Calendar & Day Block Styling */
.day-block {
    border-bottom: 1px solid var(--accent); /* Clear separation lines between days */
    padding: 16px 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.day-block:last-child {
    border-bottom: none;
}
.day-header {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
}
.day-date {
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -1px;
}
.day-weekday {
    font-size: 14px;
    color: var(--text-secondary);
    text-transform: uppercase;
}
.event-card {
    background: #fafafc;
    border: 1px solid #e5e5ea;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.event-card.important {
    border-left: 4px solid var(--accent);
    background: var(--surface);
}
.event-name {
    font-weight: 700;
    font-size: 15px;
}
.event-note {
    font-size: 13px;
    color: var(--text-secondary);
}
.event-time {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 2px;
}

/* Login Screen */
#login-screen {
    position: fixed; inset: 0; background: var(--bg-color);
    display: flex; justify-content: center; align-items: center; z-index: 9999;
}
.login-card {
    background: var(--surface); border: 2px solid var(--accent);
    padding: 40px; width: 340px; text-align: left;
}
.login-card input {
    width: 100%; padding: 12px; margin-bottom: 16px;
    border: 1px solid var(--border); font-size: 16px; box-sizing: border-box;
}
.login-card button {
    width: 100%; padding: 16px; background: var(--accent);
    color: #fff; font-weight: bold; border: none; font-size: 16px; cursor: pointer;
}
</style>
'''

# SEC-01 FIX: auth_data.js는 더 이상 클라이언트에 주입하지 않음 (보안 취약점 제거)
# 인증은 서버 측 /api/login 엔드포인트에서만 처리
auth_data_js = '// Auth handled server-side via /api/login'

# Advanced SHA-256 Script
sha_script = '''
<script>
!function(t,n){"object"==typeof exports?module.exports=exports=n():"function"==typeof define&&define.amd?define([],n):t.CryptoJS=n()}(this,function(){return function(f){var i;if("undefined"!=typeof window&&window.crypto&&(i=window.crypto),"undefined"!=typeof self&&self.crypto&&(i=self.crypto),!(i=!(i=!(i="undefined"!=typeof globalThis&&globalThis.crypto?globalThis.crypto:i)&&"undefined"!=typeof window&&window.msCrypto?window.msCrypto:i)&&"undefined"!=typeof global&&global.crypto?global.crypto:i)&&"function"==typeof require)try{i=require("crypto")}catch(t){}var e=Object.create||function(t){return n.prototype=t,t=new n,n.prototype=null,t};function n(){}var t={},r=t.lib={},o=r.Base={extend:function(t){var n=e(this);return t&&n.mixIn(t),n.hasOwnProperty("init")&&this.init!==n.init||(n.init=function(){n.$super.init.apply(this,arguments)}),(n.init.prototype=n).$super=this,n},create:function(){var t=this.extend();return t.init.apply(t,arguments),t},init:function(){},mixIn:function(t){for(var n in t)t.hasOwnProperty(n)&&(this[n]=t[n]);t.hasOwnProperty("toString")&&(this.toString=t.toString)},clone:function(){return this.init.prototype.extend(this)}},u=r.WordArray=o.extend({init:function(t,n){t=this.words=t||[],this.sigBytes=null!=n?n:4*t.length},toString:function(t){return(t||a).stringify(this)},concat:function(t){var n=this.words,e=t.words,i=this.sigBytes,r=t.sigBytes;if(this.clamp(),i%4)for(var o=0;o<r;o++){var s=e[o>>>2]>>>24-o%4*8&255;n[i+o>>>2]|=s<<24-(i+o)%4*8}else for(var a=0;a<r;a+=4)n[i+a>>>2]=e[a>>>2];return this.sigBytes+=r,this},clamp:function(){var t=this.words,n=this.sigBytes;t[n>>>2]&=4294967295<<32-n%4*8,t.length=f.ceil(n/4)},clone:function(){var t=o.clone.call(this);return t.words=this.words.slice(0),t},random:function(t){for(var n=[],e=0;e<t;e+=4)n.push(function(){if(i){if("function"==typeof i.getRandomValues)try{return i.getRandomValues(new Uint32Array(1))[0]}catch(t){}if("function"==typeof i.randomBytes)try{return i.randomBytes(4).readInt32LE()}catch(t){}}throw new Error("Native crypto module could not be used to get secure random number.")}());return new u.init(n,t)}}),s=t.enc={},a=s.Hex={stringify:function(t){for(var n=t.words,e=t.sigBytes,i=[],r=0;r<e;r++){var o=n[r>>>2]>>>24-r%4*8&255;i.push((o>>>4).toString(16)),i.push((15&o).toString(16))}return i.join("")},parse:function(t){for(var n=t.length,e=[],i=0;i<n;i+=2)e[i>>>3]|=parseInt(t.substr(i,2),16)<<24-i%8*4;return new u.init(e,n/2)}},c=s.Latin1={stringify:function(t){for(var n=t.words,e=t.sigBytes,i=[],r=0;r<e;r++){var o=n[r>>>2]>>>24-r%4*8&255;i.push(String.fromCharCode(o))}return i.join("")},parse:function(t){for(var n=t.length,e=[],i=0;i<n;i++)e[i>>>2]|=(255&t.charCodeAt(i))<<24-i%4*8;return new u.init(e,n)}},p=s.Utf8={stringify:function(t){try{return decodeURIComponent(escape(c.stringify(t)))}catch(t){throw new Error("Malformed UTF-8 data")}},parse:function(t){return c.parse(unescape(encodeURIComponent(t)))}},d=r.BufferedBlockAlgorithm=o.extend({reset:function(){this._data=new u.init,this._nDataBytes=0},_append:function(t){"string"==typeof t&&(t=p.parse(t)),this._data.concat(t),this._nDataBytes+=t.sigBytes},_process:function(t){var n,e=this._data,i=e.words,r=e.sigBytes,o=this.blockSize,s=r/(4*o),a=(s=t?f.ceil(s):f.max((0|s)-this._minBufferSize,0))*o,r=f.min(4*a,r);if(a){for(var c=0;c<a;c+=o)this._doProcessBlock(i,c);n=i.splice(0,a),e.sigBytes-=r}return new u.init(n,r)},clone:function(){var t=o.clone.call(this);return t._data=this._data.clone(),t},_minBufferSize:0}),h=(r.Hasher=d.extend({cfg:o.extend(),init:function(t){this.cfg=this.cfg.extend(t),this.reset()},reset:function(){d.reset.call(this),this._doReset()},update:function(t){return this._append(t),this._process(),this},finalize:function(t){return t&&this._append(t),this._doFinalize()},blockSize:16,_createHelper:function(e){return function(t,n){return new e.init(n).finalize(t)}},_createHmacHelper:function(e){return function(t,n){return new h.HMAC.init(e,n).finalize(t)}}}),t.algo={});return t}(Math)});
!function(e,t){"object"==typeof exports?module.exports=exports=t(require("./core")):"function"==typeof define&&define.amd?define(["./core"],t):t(e.CryptoJS)}(this,function(s){return function(n){var e=s,t=e.lib,r=t.WordArray,o=t.Hasher,t=e.algo,i=[],_=[];!function(){function e(e){return 4294967296*(e-(0|e))|0}for(var t=2,r=0;r<64;)!function(e){for(var t=n.sqrt(e),r=2;r<=t;r++)if(!(e%r))return;return 1}(t)||(r<8&&(i[r]=e(n.pow(t,.5))),_[r]=e(n.pow(t,1/3)),r++),t++}();var p=[],t=t.SHA256=o.extend({_doReset:function(){this._hash=new r.init(i.slice(0))},_doProcessBlock:function(e,t){for(var r=this._hash.words,o=r[0],n=r[1],i=r[2],s=r[3],a=r[4],c=r[5],h=r[6],f=r[7],u=0;u<64;u++){u<16?p[u]=0|e[t+u]:(l=p[u-15],d=p[u-2],p[u]=((l<<25|l>>>7)^(l<<14|l>>>18)^l>>>3)+p[u-7]+((d<<15|d>>>17)^(d<<13|d>>>19)^d>>>10)+p[u-16]);var l=o&n^o&i^n&i,d=f+((a<<26|a>>>6)^(a<<21|a>>>11)^(a<<7|a>>>25))+(a&c^~a&h)+_[u]+p[u],f=h,h=c,c=a,a=s+d|0,s=i,i=n,n=o,o=d+(((o<<30|o>>>2)^(o<<19|o>>>13)^(o<<10|o>>>22))+l)|0}r[0]=r[0]+o|0,r[1]=r[1]+n|0,r[2]=r[2]+i|0,r[3]=r[3]+s|0,r[4]=r[4]+a|0,r[5]=r[5]+c|0,r[6]=r[6]+h|0,r[7]=r[7]+f|0},_doFinalize:function(){var e=this._data,t=e.words,r=8*this._nDataBytes,o=8*e.sigBytes;return t[o>>>5]|=128<<24-o%32,t[14+(64+o>>>9<<4)]=n.floor(r/4294967296),t[15+(64+o>>>9<<4)]=r,e.sigBytes=4*t.length,this._process(),this._hash},clone:function(){var e=o.clone.call(this);return e._hash=this._hash.clone(),e}});e.SHA256=o._createHelper(t),e.HmacSHA256=o._createHmacHelper(t)}(Math),s.SHA256});
</script>
<script>
async function sha256(message) {
    if (typeof CryptoJS !== 'undefined') {
        return CryptoJS.SHA256(message).toString();
    }
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
</script>
'''

# New JS Logic for Modes & Accordion
app_logic = '''
<script>
    // SEC-02 FIX: 서버 측 인증으로 전환 — 클라이언트에 해시 데이터 없음
    async function attemptLogin() {
        const name = document.getElementById("login-name").value.trim();
        const pass = document.getElementById("login-pass").value.trim();
        const err = document.getElementById("login-error");
        const btn = document.querySelector('.login-card button');
        
        if (!name || !pass) { err.textContent = '이름과 비밀번호를 입력해주세요.'; err.style.display = 'block'; return; }
        btn.disabled = true; btn.textContent = '로그인 중...';
        
        try {
            const resp = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name, password: pass})
            });
            const data = await resp.json();
            
            if (data.success) {
                localStorage.setItem('jhub_logged_in', 'true');
                localStorage.setItem('jhub_user_name', data.name);
                document.getElementById('user-profile-name').textContent = data.name + ' 님';
                if(localStorage.getItem('jhub_badge_knowledge_master') === 'true') {
                    document.getElementById('user-profile-badge').innerHTML = '<span style="background: linear-gradient(135deg, #FFD700, #FDB931); color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; margin-left: 6px; animation: badgeGlow 2s infinite;">지식 마스터 🏅</span>';
                }
                document.getElementById('login-screen').style.display = 'none';
            } else {
                err.textContent = data.message || '이름 또는 비밀번호가 일치하지 않습니다.';
                err.style.display = 'block';
            }
        } catch(e) {
            // 서버 미연결(로컬 파일 모드) 시 기존 방식 fallback
            console.warn('서버 연결 불가, 로컬 모드로 전환:', e);
            err.textContent = '서버에 연결할 수 없습니다. 관리자에게 문의하세요.';
            err.style.display = 'block';
        }
        btn.disabled = false; btn.textContent = '로그인';
    }

    // Check login status on load (서버 세션 확인)
    window.addEventListener('DOMContentLoaded', async () => {
        try {
            const resp = await fetch('/api/check_session');
            const data = await resp.json();
            if (data.success) {
                localStorage.setItem('jhub_logged_in', 'true');
                localStorage.setItem('jhub_user_name', data.user_name);
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('user-profile-name').textContent = data.user_name + ' 님';
                if(localStorage.getItem('jhub_badge_knowledge_master') === 'true') {
                    document.getElementById('user-profile-badge').innerHTML = '<span style="background: linear-gradient(135deg, #FFD700, #FDB931); color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; margin-left: 6px; animation: badgeGlow 2s infinite;">지식 마스터 🏅</span>';
                }
                return;
            }
        } catch(e) { /* 로컬 파일 모드 */ }
        
        if(localStorage.getItem('jhub_logged_in') === 'true') {
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('user-profile-name').textContent = (localStorage.getItem('jhub_user_name') || '') + ' 님';
        }
    });

    // Mode Switch Logic
    function switchMode(mode) {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
        
        document.getElementById('btn-' + mode).classList.add('active');
        document.getElementById('view-' + mode).classList.add('active');
    }

    // Accordion Logic
    function toggleAccordion(element) {
        const container = element.closest('.wa-container');
        container.classList.toggle('collapsed');
    }

    document.addEventListener('DOMContentLoaded', () => {
        checkLogin();
        document.getElementById("login-pass").addEventListener("keypress", e => {
            if(e.key === "Enter") attemptLogin();
        });
    });
</script>
'''

# Generate HTML dynamically from JSON for each workspace section

# 1. Dashboard HTML
dashboard_html = '<div class="grid-2"><div class="card"><div class="card-header"><div class="card-title">현장 핵심 변동</div><span class="chip red">업데이트 완료</span></div><ul style="padding-left: 20px; font-size: 15px; color: var(--ink); line-height: 1.8;">'
for item in ws_data['dashboard']['field_updates']:
    dashboard_html += f'<li><span class="highlight">{item["name"]}</span> — {item["content"]}</li>'
dashboard_html += '</ul></div><div class="card"><div class="card-header"><div class="card-title">법규/정책 핵심 변동</div></div>'
for i, item in enumerate(ws_data['dashboard']['policy_updates']):
    chip_class = "red" if "핵심" in item["chip"] else ("blue" if "예고" in item["chip"] else "green")
    dashboard_html += f'<div class="report-item"><div class="tag-row"><span class="chip {chip_class}">{item["chip"]}</span></div><h3 class="report-title">{item["title"]}</h3><p class="report-desc">{item["desc"]}</p></div>'
    if i < len(ws_data['dashboard']['policy_updates']) - 1:
        dashboard_html += '<div style="height: 1px; background: var(--divider-soft); margin: 8px 0;"></div>'
dashboard_html += '</div></div>'

# 2. Projects HTML
projects_html = '<div class="grid-2"><div><div class="card"><div class="card-header"><div class="card-title">본부별 주요 프로젝트</div></div>'
depts = [
    ("■ 디자인 본부", ws_data['projects']['design_dept']),
    ("■ 도시개발 & 재생 본부", ws_data['projects']['urban_dev_dept']),
    ("■ 도시계획 본부", ws_data['projects']['urban_plan_dept'])
]
for title, items in depts:
    projects_html += f'<h3 style="font-size:16px; margin: 10px 0 5px 0; color:var(--accent);">{title}</h3><table class="card-table"><tr><th>프로젝트</th><th>진행 현황</th></tr>'
    for item in items:
        name_html = f'<span class="highlight">{item["name"]}</span>' if item["highlight"] else item["name"]
        projects_html += f'<tr><td>{name_html}</td><td>{item["status"]}</td></tr>'
    projects_html += '</table>'
projects_html += '</div><div class="card"><div class="card-header"><div class="card-title">입찰/수주 전선 (전략기획)</div><span class="chip red">총력전</span></div><table class="card-table"><tr><th>프로젝트</th><th>일정</th><th>당사 지위</th></tr>'
for item in ws_data['projects']['strategy_bids']:
    name_html = f'<span class="highlight">{item["name"]}</span>' if item["highlight"] else item["name"]
    projects_html += f'<tr><td>{name_html}</td><td>{item["date"]}</td><td>{item["status"]}</td></tr>'
projects_html += '</table></div></div><div><div class="card"><div class="card-header"><div class="card-title">인접지 개발 동향</div><span class="chip">완벽 복원</span></div>'
for adj in ws_data['projects']['adjacent_areas']:
    projects_html += f'<div class="accordion" style="margin-bottom:12px;"><div class="acc-header" style="font-weight:700; margin-bottom:4px;">{adj["region"]}</div><ul class="acc-body">'
    for li in adj['items']:
        projects_html += f'<li>{li}</li>'
    projects_html += '</ul></div>'
projects_html += '</div><div class="card"><div class="card-header"><div class="card-title">정보몽땅 자동 크롤링 (API)</div><span class="chip blue">실시간 연동</span></div><table class="card-table"><tr><th>구역</th><th>상태</th><th>변동 내역</th></tr>'
for api in ws_data['projects']['api_crawling']:
    status_html = '<span style="font-weight:700;">[ 등록 ]</span>' if api['status'] == '등록' else '<span style="color:var(--text-secondary);">[ 미지정 ]</span>'
    projects_html += f'<tr><td><strong>{api["name"]}</strong></td><td>{status_html}</td><td>{api["desc"]}</td></tr>'
projects_html += '</table></div></div></div>'

# 3. Calendar HTML
calendar_html = '<div class="card" style="max-width: 800px; margin: 0 auto;"><div class="card-header"><div class="card-title">7월 3주차 주요 일정</div><button class="chip">캘린더 연동</button></div>'
for day in ws_data['calendar']:
    calendar_html += f'<div class="day-block"><div class="day-header"><div class="day-date">{day["date"]}</div><div class="day-weekday">{day["weekday"]}</div></div>'
    for ev in day['events']:
        imp_class = " important" if ev["important"] else ""
        time_html = f'<div class="event-time">{ev["time"]}</div>' if "time" in ev else ""
        note_html = f'<div class="event-note">{ev["note"]}</div>' if ev["note"] else ""
        calendar_html += f'<div class="event-card{imp_class}">{time_html}<div class="event-name">{ev["name"]}</div>{note_html}</div>'
    calendar_html += '</div>'
calendar_html += '</div>'

# 4. Laws HTML
laws_html = '<div class="grid-2"><div class="card"><div class="card-header"><div class="card-title">신규 시행 법령</div></div><table class="card-table"><tr><th>시행일</th><th>법령</th><th>주요 내용</th></tr>'
for lw in ws_data['laws']['new_laws']:
    laws_html += f'<tr><td>{lw["date"]}</td><td>{lw["law"]}</td><td>{lw["desc"]}</td></tr>'
laws_html += '</table></div><div class="card"><div class="card-header"><div class="card-title">지자체 고시/공고</div></div><ul>'
for no in ws_data['laws']['local_notices']:
    laws_html += f'<li>{no}</li>'
laws_html += '</ul></div><div class="card" style="grid-column: 1 / -1;"><div class="card-header"><div class="card-title">서울시 10대 법령 개정 건의안 추적표</div></div><table class="card-table"><tr><th>건의 항목</th><th>현행</th><th>건의안</th><th>상태</th></tr>'
for req in ws_data['laws']['seoul_10_requests']:
    laws_html += f'<tr><td>{req["item"]}</td><td>{req["current"]}</td><td><strong style="color:var(--text-primary)">{req["request"]}</strong></td><td>{req["status"]}</td></tr>'
laws_html += '</table></div></div>'


# Build Accordion UI for Workspace
workspace_content = f'''
<div class="wa-container">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">1. 전사 일일 및 종합 동향</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">7월 3주차 주요 변동 사항 및 핵심 요약</p>
        {dashboard_html}
    </div>
</div>

<div class="wa-container collapsed">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">2. 전사 프로젝트 통합 뷰</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">본부별 현황, 입찰 전선, 인접지 및 정보몽땅</p>
        {projects_html}
    </div>
</div>

<div class="wa-container collapsed">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">3. 통합 핵심 일정표</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">향후 2주간의 본부별 총회, 미팅, 인허가 일정</p>
        {calendar_html}
    </div>
</div>

<div class="wa-container collapsed">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">4. 법규 아카이브</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">최근 30일 이내 신규 시행 법령 및 10대 건의안 추적</p>
        {laws_html}
    </div>
</div>
'''

html_template = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Jinyang Hub | 진양 저널</title>
    {{swiss_css}}
</head>
<body>

    <!-- Login -->
    <div id="login-screen">
        <div class="login-card">
            <h1>J-Hub</h1>
            <p style="color:#666; margin-bottom: 24px; line-height: 1.5; font-size: 14px;">
                이름을 넣어 주세요.<br>비번은 핸드폰 뒷자리 4자리입니다.
            </p>
            <input type="text" id="login-name" placeholder="이름 (예: 홍길동)">
            <input type="password" id="login-pass" placeholder="보안 암호">
            <p id="login-error" style="color: red; font-size: 13px; display: none; margin-top: -10px; margin-bottom: 10px;">암호가 일치하지 않습니다.</p>
            <button onclick="attemptLogin()">접속하기 (Access)</button>
        </div>
    </div>

    <header style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center;">
            <div>
                <h2 style="margin:0; font-size:24px; letter-spacing: -1.5px;">JINYANG <span style="font-weight:300;">HUB</span></h2>
                <div style="display: flex; align-items: center; margin-top:4px;">
                    <div id="user-profile-name" style="font-size:12px; color:var(--text-secondary);"></div>
                    <div id="user-profile-badge"></div>
                </div>
            </div>
        </div>
        <div class="mode-switch">
            <button id="btn-journal" class="mode-btn active" onclick="switchMode('journal')">Jinyang Journal</button>
            <button id="btn-workspace" class="mode-btn" onclick="switchMode('workspace')">J-Workspace</button>
        </div>
        <div>
            <button onclick="document.getElementById('login-screen').style.display='flex'; localStorage.removeItem('jhub_logged_in'); document.getElementById('user-profile-badge').innerHTML='';" style="background:transparent; border:1px solid #d2d2d7; color:#1d1d1f; padding: 4px 12px; font-size:12px; border-radius: 5px; cursor: pointer;">로그아웃</button>
        </div>
    </header>

    <div id="app-content">
        <!-- MODE 1: JOURNAL (Reading) -->
        <div id="view-journal" class="page-view active">
            {{page_reading}}
        </div>
        
        <!-- MODE 2: WORKSPACE (Accordion based CMS layout) -->
        <div id="view-workspace" class="page-view">
            <div style="background: var(--surface); border: 1px solid var(--accent); padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background-color: #00cc66; box-shadow: 0 0 8px rgba(0,204,102,0.6); animation: pulse 2s infinite;"></div>
                    <span style="font-size: 16px; font-weight: 700; letter-spacing: -0.5px;">최종 업데이트</span>
                </div>
                <div style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">
                    {{updated_at_text}}
                </div>
            </div>
            <style>
                @keyframes pulse {{
                    0% {{ transform: scale(0.95); opacity: 0.8; }}
                    50% {{ transform: scale(1.1); opacity: 1; }}
                    100% {{ transform: scale(0.95); opacity: 0.8; }}
                }}
            </style>
            {{workspace_content}}
        </div>
    </div>
    
    {{sha_script}}
    {{app_logic}}

</body>
</html>
'''

# Compile
compiled_html = html_template.replace('{swiss_css}', swiss_css)
import datetime
build_date = datetime.datetime.now().strftime("%Y-%m-%d")

compiled_html = compiled_html.replace('{page_reading}', read_file('src/pages/reading.html').replace('{build_date_string}', build_date))
compiled_html = compiled_html.replace('{workspace_content}', workspace_content)
compiled_html = compiled_html.replace('{sha_script}', sha_script)
compiled_html = compiled_html.replace('{app_logic}', app_logic)
# ADD-08 FIX: 빌드 시점의 현재 시각을 동적으로 주입
import datetime as _dt
_now_str = _dt.datetime.now().strftime("%Y.%m.%d %H:%M") + ' (빌드 동기화 완료)'
compiled_html = compiled_html.replace('{updated_at_text}', ws_data.get('updated_at', _now_str))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(compiled_html)

print("Build successful! Data decoupled, JSON rendered, Accordion UI integrated into index.html.")
