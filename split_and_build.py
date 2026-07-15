import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Helper to extract blocks based on comments
def extract_block(text, start_str, end_str):
    try:
        start_idx = text.index(start_str)
        end_idx = text.index(end_str) + len(end_str)
        return text[start_idx:end_idx]
    except ValueError:
        return ""

# Split parts
head = html.split('</head>')[0] + '</head>'

# Body start to Login Modal
body_start = html.split('<div id="login-screen"')[0].split('</head>')[1]
login_modal = '<div id="login-screen"' + html.split('<div id="login-screen"')[1].split('<!-- App Content -->')[0]

# Global header (Title + Mode switch)
app_content_start = '<!-- App Content -->\n<div id="app-content"'
header_section = extract_block(html, '<header', '</header>')
nav_section = extract_block(html, '<!-- Navigation -->', '</nav>')

# Tabs
tab_dashboard = extract_block(html, '<!-- TAB 1: 대시보드 -->', '<!-- TAB 2: 업무 지침 -->')
tab_laws = extract_block(html, '<!-- TAB 2: 업무 지침 -->', '<!-- TAB 3: 프로젝트 현황 -->')
tab_projects = extract_block(html, '<!-- TAB 3: 프로젝트 현황 -->', '<!-- TAB 4: 주간 일정 -->')
tab_calendar = extract_block(html, '<!-- TAB 4: 주간 일정 -->', '<!-- TAB 5: 오늘의 읽을거리 (Today\'s Reading) -->')
tab_reading = extract_block(html, '<!-- TAB 5: 오늘의 읽을거리 (Today\'s Reading) -->', '<!-- Javascript for Tab Switching and Accordion -->')

# Scripts
scripts_section = extract_block(html, '<!-- Javascript for Tab Switching and Accordion -->', '</html>')

# Write to src/components
os.makedirs('src/components', exist_ok=True)
os.makedirs('src/pages', exist_ok=True)

with open('src/components/head.html', 'w', encoding='utf-8') as f: f.write(head)
with open('src/components/login.html', 'w', encoding='utf-8') as f: f.write(login_modal)
with open('src/components/header.html', 'w', encoding='utf-8') as f: f.write(header_section)

with open('src/pages/dashboard.html', 'w', encoding='utf-8') as f: f.write(tab_dashboard)
with open('src/pages/laws.html', 'w', encoding='utf-8') as f: f.write(tab_laws)
with open('src/pages/projects.html', 'w', encoding='utf-8') as f: f.write(tab_projects)
with open('src/pages/calendar.html', 'w', encoding='utf-8') as f: f.write(tab_calendar)
with open('src/pages/reading.html', 'w', encoding='utf-8') as f: f.write(tab_reading)

# We will rewrite the Scripts to include SHA-256 Auth.
# Let's create build_jhub.py
build_script = """import os

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

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

/* Workspace Grid */
.workspace-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}
.workspace-card {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 24px;
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

# New JS Logic for Modes
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

    document.addEventListener('DOMContentLoaded', () => {
        checkLogin();
        // Bind enter key
        document.getElementById("login-pass").addEventListener("keypress", e => {
            if(e.key === "Enter") attemptLogin();
        });
    });
</script>
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
        
        <!-- MODE 2: WORKSPACE (Dashboard + Projects + Calendar + Laws) -->
        <div id="view-workspace" class="page-view">
            <div class="workspace-grid">
                <div class="workspace-card" style="grid-column: 1 / -1;">
                    {{page_dashboard}}
                </div>
                <div class="workspace-card">
                    {{page_projects}}
                </div>
                <div class="workspace-card">
                    {{page_calendar}}
                </div>
                <div class="workspace-card" style="grid-column: 1 / -1;">
                    {{page_laws}}
                </div>
            </div>
        </div>
    </div>
    
    {{sha_script}}
    {{app_logic}}

</body>
</html>
'''

# Compile
compiled_html = html_template.replace('{{swiss_css}}', swiss_css)
compiled_html = compiled_html.replace('{{page_reading}}', read_file('src/pages/reading.html'))
compiled_html = compiled_html.replace('{{page_dashboard}}', read_file('src/pages/dashboard.html'))
compiled_html = compiled_html.replace('{{page_projects}}', read_file('src/pages/projects.html'))
compiled_html = compiled_html.replace('{{page_calendar}}', read_file('src/pages/calendar.html'))
compiled_html = compiled_html.replace('{{page_laws}}', read_file('src/pages/laws.html'))
compiled_html = compiled_html.replace('{{sha_script}}', sha_script)
compiled_html = compiled_html.replace('{{app_logic}}', app_logic)

# To ensure the articles.js script logic still works properly inside the new structure, we let it be.
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(compiled_html)

print("Build successful! index.html updated.")
"""

with open('build_jhub.py', 'w', encoding='utf-8') as f:
    f.write(build_script)
