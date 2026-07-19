#!/usr/bin/env python3
"""
build_jhub.py — J-Hub 포털 빌드 스크립트 (v3.0 모듈 분리 버전)

■ 구조:
  - CSS, JS, 각 페이지 HTML은 src/ 폴더의 독립 파일로 관리
  - 이 스크립트는 JSON 데이터 → HTML 렌더링 + 조립만 담당
  - Weekly Report, Master 제안함 탭은 독립 파일이므로 빌드 수정과 무관하게 보존됨

■ 파일 구조:
  src/css/main.css         ← CSS
  src/js/app.js            ← 인증/모드 전환/아코디언 JS
  src/js/crypto.min.js     ← SHA-256 라이브러리
  src/pages/reading.html   ← Journal 탭 (기사 모자이크)
  src/pages/weekly.html    ← Weekly Report 탭 (iframe + 피드백)
  src/pages/master.html    ← Master 제안함 탭
  src/data/workspace.json  ← Workspace 데이터
"""

import os
import sys
import json
import glob
import datetime
import tempfile

# CWD를 스크립트 위치로 고정 (H-02 해결)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════
# 유틸리티
# ═══════════════════════════════════════════════════════════

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def ensure_schema(data, schema):
    """workspace.json에 필수 키가 없으면 기본값을 주입 (C-03 해결)"""
    for key, default in schema.items():
        if key not in data:
            data[key] = default if not isinstance(default, dict) else {}
        if isinstance(default, dict):
            ensure_schema(data[key], default)
    return data


REQUIRED_SCHEMA = {
    'dashboard': {'field_updates': [], 'policy_updates': []},
    'projects': {
        'design_dept': [], 'urban_dev_dept': [], 'urban_plan_dept': [],
        'strategy_bids': [], 'adjacent_areas': [], 'api_crawling': []
    },
    'calendar': [],
    'laws': {'new_laws': [], 'local_notices': [], 'seoul_10_requests': []}
}


# ═══════════════════════════════════════════════════════════
# 1. 데이터 로드 + 스키마 검증
# ═══════════════════════════════════════════════════════════

with open('src/data/workspace.json', 'r', encoding='utf-8') as f:
    ws_data = json.load(f)

ws_data = ensure_schema(ws_data, REQUIRED_SCHEMA)


# ═══════════════════════════════════════════════════════════
# 2. Workspace 동적 HTML 렌더링 (JSON → HTML)
# ═══════════════════════════════════════════════════════════

today_dt = datetime.datetime.now()
# 월요일 기준 주차 계산 (ISO 표준: 1일~7일=1주, 8일~14일=2주, ...)
import math
week_num = math.ceil(today_dt.day / 7)
current_week_str = f"{today_dt.month}월 {week_num}주차"

# --- 2-1. Dashboard ---
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

# --- 2-2. Projects ---
projects_html = '<div class="grid-2"><div><div class="card"><div class="card-header"><div class="card-title">본부별 주요 프로젝트</div></div>'
depts = [
    ("■ 디자인 본부", ws_data['projects']['design_dept']),
    ("■ 도시개발 & 재생 본부", ws_data['projects']['urban_dev_dept']),
    ("■ 도시계획 본부", ws_data['projects']['urban_plan_dept'])
]
for title, items in depts:
    changed_items = [item for item in items if item.get("highlight", False)]
    if not changed_items:
        continue
    projects_html += f'<h3 style="font-size:16px; margin: 10px 0 5px 0; color:var(--accent);">{title}</h3><table class="card-table"><tr><th>프로젝트</th><th>진행 현황 (변동사항)</th></tr>'
    for item in changed_items:
        name_html = f'<span class="highlight">{item["name"]}</span>'
        projects_html += f'<tr><td>{name_html}</td><td>{item["status"]}</td></tr>'
    projects_html += '</table>'
projects_html += '</div><div class="card"><div class="card-header"><div class="card-title">입찰/수주 전선 (전략기획)</div><span class="chip red">총력전</span></div><table class="card-table"><tr><th>프로젝트</th><th>일정</th><th>당사 지위</th></tr>'
for item in ws_data['projects']['strategy_bids']:
    name_html = f'<span class="highlight">{item["name"]}</span>' if item.get("highlight") else item["name"]
    projects_html += f'<tr><td>{name_html}</td><td>{item.get("date","")}</td><td>{item.get("status","")}</td></tr>'
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

# --- 2-3. Calendar ---
calendar_html = f'<div class="card" style="max-width: 800px; margin: 0 auto;"><div class="card-header"><div class="card-title"><span class="dynamic-week-label">{current_week_str}</span> 주요 일정</div><button class="chip">캘린더 연동</button></div>'
for day in ws_data['calendar']:
    calendar_html += f'<div class="day-block"><div class="day-header"><div class="day-date">{day["date"]}</div><div class="day-weekday">{day["weekday"]}</div></div>'
    for ev in day['events']:
        imp_class = " important" if ev["important"] else ""
        time_html = f'<div class="event-time">{ev["time"]}</div>' if "time" in ev and ev["time"] else ""
        note_html = f'<div class="event-note">{ev["note"]}</div>' if ev.get("note") else ""
        calendar_html += f'<div class="event-card{imp_class}">{time_html}<div class="event-name">{ev["name"]}</div>{note_html}</div>'
    calendar_html += '</div>'
calendar_html += '</div>'

# --- 2-4. Laws ---
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


# ═══════════════════════════════════════════════════════════
# 3. Workspace 아코디언 조립
# ═══════════════════════════════════════════════════════════

workspace_content = f'''
<div class="wa-container">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">1. 진양 일일 및 종합 동향</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;"><span class="dynamic-week-label">{current_week_str}</span> 주요 변동 사항 및 핵심 요약</p>
        {dashboard_html}
    </div>
</div>

<div class="wa-container collapsed">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">2. 진양 프로젝트 통합 뷰</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">본부별 현황, 입찰 전선, 인접지 및 정보몽땅</p>
        {projects_html}
    </div>
</div>

<div class="wa-container">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">3. 통합 핵심 일정표</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">향후 2주간의 본부별 총회, 미팅, 인허가 일정</p>
        {calendar_html}
    </div>
</div>

<div class="wa-container">
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

# --- 5. 주간 회의록 원본 Iframe ---
report_files = glob.glob('reports/*주간*보고*.html')
if not report_files:
    report_files = [f for f in glob.glob('reports/*.html') if 'regulatory' not in f]

if report_files:
    latest_report = max(report_files, key=os.path.getmtime)
    report_filename = os.path.basename(latest_report)
    iframe_src = f"./reports/{report_filename}"
    workspace_content += f'''
<div class="wa-container">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">5. 주간 회의록 원본</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">{report_filename}</p>
        <div class="card" style="padding: 0; border-radius: 8px; overflow: hidden; height: 1600px; border: 2px dashed #ccc;">
            <iframe src="{iframe_src}" style="width: 100%; height: 100%; border: none;" loading="lazy"></iframe>
        </div>
    </div>
</div>
'''
else:
    print("⚠️ WARNING: 주간 보고서 파일 미발견 — iframe 섹션 생략")

# --- 6. 법규 동향 보고서 Iframe ---
if os.path.exists('reports/regulatory_report.html'):
    workspace_content += '''
<div class="wa-container">
    <div class="wa-header" onclick="toggleAccordion(this)">
        <h2 class="wa-title">6. 법규 동향 보고서 (풀 리포트)</h2>
        <div class="wa-icon">▼</div>
    </div>
    <div class="wa-content">
        <p style="color:var(--text-secondary); margin-top:0;">법규, 정책, 인허가 동향에 대한 상세 8+2 섹션 풀 리포트</p>
        <div class="card" style="padding: 0; border-radius: 8px; overflow: hidden; height: 1600px; border: 2px dashed #ccc;">
            <iframe src="./reports/regulatory_report.html" style="width: 100%; height: 100%; border: none;" loading="lazy"></iframe>
        </div>
    </div>
</div>
'''


# ═══════════════════════════════════════════════════════════
# 4. 외부 파일 로드 (모듈 분리된 정적 파일)
# ═══════════════════════════════════════════════════════════

css_content = read_file('src/css/main.css')
crypto_js = read_file('src/js/crypto.min.js')
app_js = read_file('src/js/app.js')

build_date = today_dt.strftime("%Y-%m-%d")
page_reading = read_file('src/pages/reading.html').replace('{build_date_string}', build_date)
page_reading += f'<div style="margin-top: 48px;">{calendar_html}</div>'

page_weekly = read_file('src/pages/weekly.html')
page_master = read_file('src/pages/master.html')

updated_at_text = ws_data.get('updated_at',
    today_dt.strftime("%Y.%m.%d %H:%M") + ' (빌드 동기화 완료)')


# ═══════════════════════════════════════════════════════════
# 5. 최종 HTML 조립
# ═══════════════════════════════════════════════════════════

html_output = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Jinyang Hub | 진양 저널</title>
    <style>
{css_content}
    </style>
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
            <button id="btn-weekly" class="mode-btn" style="color:#e30000; font-weight:700;" onclick="switchMode('weekly')">Weekly Report</button>
            <button id="btn-master" class="mode-btn" style="color:#800080; font-weight:700; display:none;" onclick="switchMode('master')">제안함 (Master)</button>
            <a href="./edu/index.html" target="_blank" style="display:inline-block; padding:8px 14px; font-size:13px; color:#0066cc; text-decoration:none; font-weight:600; border-radius:20px; border:1px solid #0066cc;">📚 교육자료</a>
        </div>
        <div>
            <button onclick="(async()=>{{try{{await fetch('/api/logout',{{method:'POST'}})}}catch(e){{}}localStorage.removeItem('jhub_logged_in');localStorage.removeItem('jhub_user_name');document.getElementById('login-screen').style.display='flex';document.getElementById('user-profile-badge').innerHTML='';}})();" style="background:transparent; border:1px solid #d2d2d7; color:#1d1d1f; padding: 4px 12px; font-size:12px; border-radius: 5px; cursor: pointer;">로그아웃</button>
        </div>
    </header>

    <div id="app-content">
        <!-- MODE 1: JOURNAL -->
        <div id="view-journal" class="page-view active">
            {page_reading}
        </div>
        
        <!-- MODE 2: WORKSPACE -->
        <div id="view-workspace" class="page-view">
            <div style="background: var(--surface); border: 1px solid var(--accent); padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background-color: #00cc66; box-shadow: 0 0 8px rgba(0,204,102,0.6); animation: pulse 2s infinite;"></div>
                    <span style="font-size: 16px; font-weight: 700; letter-spacing: -0.5px;">최종 업데이트</span>
                </div>
                <div style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">
                    {updated_at_text}
                </div>
            </div>
            <style>
                @keyframes pulse {{
                    0% {{ transform: scale(0.95); opacity: 0.8; }}
                    50% {{ transform: scale(1.1); opacity: 1; }}
                    100% {{ transform: scale(0.95); opacity: 0.8; }}
                }}
            </style>
            {workspace_content}
        </div>

        <!-- MODE 3: WEEKLY REPORT (독립 파일에서 로드 — 빌드 수정에 영향받지 않음) -->
        <div id="view-weekly" class="page-view">
            {page_weekly}
        </div>

        <!-- MODE 4: MASTER (독립 파일에서 로드 — 빌드 수정에 영향받지 않음) -->
        <div id="view-master" class="page-view">
            {page_master}
        </div>
    </div>
    
    <script>
{crypto_js}
    </script>
    <script>
{app_js}
    </script>

    <!-- 동적 주차 라벨 자동 업데이트 (접속 시점 기준) -->
    <script>
    (function() {{
        const now = new Date();
        const month = now.getMonth() + 1;
        const week = Math.ceil(now.getDate() / 7);
        const label = month + '월 ' + week + '주차';
        document.querySelectorAll('.dynamic-week-label').forEach(el => {{
            el.textContent = label;
        }});
    }})();
    </script>

</body>
</html>
'''


# ═══════════════════════════════════════════════════════════
# 6. Atomic Write (H-03 해결) + Smoke Test (H-04 해결)
# ═══════════════════════════════════════════════════════════

# 백업 생성
if os.path.exists('index.html'):
    import shutil
    shutil.copy2('index.html', 'index.html.bak')

# Atomic write: 임시 파일에 먼저 쓰고, 성공하면 교체
tmp_fd, tmp_path = tempfile.mkstemp(suffix='.html', dir='.')
try:
    with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
        f.write(html_output)
    os.replace(tmp_path, 'index.html')
except Exception as e:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
    print(f"🚨 빌드 실패: {e}")
    sys.exit(1)

# Smoke Test
REQUIRED_MARKERS = [
    ('view-weekly', 1, 'Weekly Report 탭'),
    ('view-master', 1, 'Master 제안함 탭'),
    ('view-workspace', 1, 'Workspace 뷰'),
    ('view-journal', 1, 'Journal 뷰'),
    ('iframe', 3, 'iframe (Weekly+법규+Workspace)'),
    ('mode-btn', 4, '모드 전환 버튼 4개'),
]

smoke_passed = True
for marker, min_count, desc in REQUIRED_MARKERS:
    count = html_output.count(marker)
    if count < min_count:
        print(f"🚨 SMOKE FAIL: {desc} — 기대 ≥{min_count}, 실제 {count}")
        smoke_passed = False

if not smoke_passed:
    # 롤백
    if os.path.exists('index.html.bak'):
        os.replace('index.html.bak', 'index.html')
        print("🔄 롤백 완료: index.html.bak → index.html")
    sys.exit(1)

file_size = os.path.getsize('index.html')
print(f"✅ Build successful! (v3.0 모듈 분리)")
print(f"   파일 크기: {file_size:,} bytes")
print(f"   모드: Journal / Workspace / Weekly Report / Master")
print(f"   Smoke Test: PASSED ✅")
