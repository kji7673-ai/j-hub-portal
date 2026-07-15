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

# Read Auth Hash Data
auth_data_js = read_file('src/components/auth_data.js')

# Advanced SHA-256 Script
sha_script = '''
<script>
async function sha256(message) {
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
    // Authentication Logic
    ''' + auth_data_js + '''
    
    async function attemptLogin() {
        const name = document.getElementById("login-name").value.trim();
        const pass = document.getElementById("login-pass").value.trim();
        const err = document.getElementById("login-error");
        
        if(allowedUsersHash[name]) {
            const hashedPass = await sha256(pass);
            if (hashedPass === allowedUsersHash[name]) {
                localStorage.setItem("jhub_logged_in", "true");
                localStorage.setItem("jhub_user_name", name);
                document.getElementById("user-profile-name").textContent = name + " 님";
                document.getElementById("login-screen").style.display = "none";
                return;
            }
        }
        err.style.display = "block";
    }

    function checkLogin() {
        if (localStorage.getItem("jhub_logged_in") === "true") {
            const userName = localStorage.getItem("jhub_user_name");
            document.getElementById("user-profile-name").textContent = userName + " 님";
            document.getElementById("login-screen").style.display = "none";
        }
    }

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
            <p style="color:#666; margin-bottom: 24px;">진양 엔지니어링 건축사사무소</p>
            <input type="text" id="login-name" placeholder="이름 (예: 홍길동)">
            <input type="password" id="login-pass" placeholder="보안 암호">
            <p id="login-error" style="color: red; font-size: 13px; display: none; margin-top: -10px; margin-bottom: 10px;">암호가 일치하지 않습니다.</p>
            <button onclick="attemptLogin()">접속하기 (Access)</button>
        </div>
    </div>

    <header>
        <div>
            <h2 style="margin:0; font-size:24px; letter-spacing: -1.5px;">JINYANG <span style="font-weight:300;">HUB</span></h2>
            <div id="user-profile-name" style="font-size:12px; color:var(--text-secondary); margin-top:4px;"></div>
        </div>
        <div class="mode-switch">
            <button id="btn-journal" class="mode-btn active" onclick="switchMode('journal')">Jinyang Journal</button>
            <button id="btn-workspace" class="mode-btn" onclick="switchMode('workspace')">J-Workspace</button>
        </div>
    </header>

    <div id="app-content">
        <!-- MODE 1: JOURNAL (Reading) -->
        <div id="view-journal" class="page-view active">
            {{page_reading}}
        </div>
        
        <!-- MODE 2: WORKSPACE (Accordion based CMS layout) -->
        <div id="view-workspace" class="page-view">
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
compiled_html = compiled_html.replace('{page_reading}', read_file('src/pages/reading.html'))
compiled_html = compiled_html.replace('{workspace_content}', workspace_content)
compiled_html = compiled_html.replace('{sha_script}', sha_script)
compiled_html = compiled_html.replace('{app_logic}', app_logic)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(compiled_html)

print("Build successful! Data decoupled, JSON rendered, Accordion UI integrated into index.html.")
