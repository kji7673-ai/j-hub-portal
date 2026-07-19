"""
J-Hub 포털 — 회원 관리 Blueprint
회원가입 신청/승인/등록/비번초기화 API 및 페이지를 제공합니다.
"""
from flask import Blueprint, jsonify, request, session, render_template_string, redirect
from functools import wraps

from user_db import (
    create_join_request, get_join_requests, approve_request, reject_request,
    get_request_by_token, consume_token, register_user, check_user_login,
    get_all_members, reset_user_password, get_user_by_reset_token,
    update_password, toggle_user_active
)

user_bp = Blueprint('user', __name__)


def master_required(f):
    """대표이사 권한 전용 데코레이터"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in') or not session.get('is_master'):
            return jsonify({"success": False, "message": "대표이사 권한이 필요합니다."}), 403
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════
# 공통 스타일
# ═══════════════════════════════════════════════
_COMMON_STYLE = """
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
           background: #000; color: #f5f5f7; min-height: 100vh;
           display: flex; align-items: center; justify-content: center; }
    .container { background: #1d1d1f; border-radius: 18px; padding: 48px;
                 max-width: 480px; width: 90%; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 28px; font-weight: 600; margin-bottom: 8px; letter-spacing: -0.3px; }
    .subtitle { color: #86868b; font-size: 15px; margin-bottom: 32px; line-height: 1.5; }
    label { display: block; font-size: 13px; color: #86868b; margin-bottom: 6px; margin-top: 16px; }
    input, select { width: 100%; padding: 12px 16px; border: 1px solid #424245;
                    border-radius: 12px; background: #2c2c2e; color: #f5f5f7;
                    font-size: 16px; outline: none; transition: border 0.2s; }
    input:focus { border-color: #0066cc; }
    .btn { display: block; width: 100%; padding: 14px; border: none; border-radius: 999px;
           background: #0066cc; color: white; font-size: 17px; font-weight: 600;
           cursor: pointer; margin-top: 28px; transition: background 0.2s; }
    .btn:hover { background: #0071e3; }
    .btn:disabled { background: #424245; cursor: not-allowed; }
    .btn-secondary { background: transparent; border: 1px solid #424245; color: #86868b; }
    .btn-secondary:hover { border-color: #86868b; color: #f5f5f7; }
    .msg { padding: 12px 16px; border-radius: 12px; margin-top: 16px; font-size: 14px; }
    .msg.success { background: rgba(52,199,89,0.15); color: #34c759; }
    .msg.error { background: rgba(255,69,58,0.15); color: #ff453a; }
    .required::after { content: ' *'; color: #ff453a; }
    a { color: #2997ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .back-link { display: block; text-align: center; margin-top: 20px; font-size: 14px; }
</style>
"""


# ═══════════════════════════════════════════════
# 1. 회원가입 신청 페이지 (공개)
# ═══════════════════════════════════════════════

_SIGNUP_PAGE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J-Hub 회원가입 신청</title>
    """ + _COMMON_STYLE + """
</head>
<body>
    <div class="container">
        <h1>회원가입 신청</h1>
        <p class="subtitle">J-Hub 포털 이용을 위해 아래 정보를 입력해 주세요.<br>대표이사 승인 후 아이디와 비밀번호를 설정할 수 있습니다.</p>
        <form id="signupForm">
            <label class="required">이름</label>
            <input type="text" id="name" placeholder="홍길동" required>
            <label class="required">소속 / 부서</label>
            <input type="text" id="department" placeholder="도시개발본부" required>
            <label>직급</label>
            <input type="text" id="position" placeholder="과장">
            <label>연락처</label>
            <input type="text" id="contact" placeholder="010-0000-0000">
            <label>가입 사유</label>
            <input type="text" id="reason" placeholder="업무 활용 목적">
            <button type="submit" class="btn">신청하기</button>
        </form>
        <div id="msg" class="msg" style="display:none;"></div>
        <a href="/" class="back-link">← 메인으로 돌아가기</a>
    </div>
    <script>
        document.getElementById('signupForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = e.target.querySelector('.btn');
            btn.disabled = true; btn.textContent = '신청 중...';
            try {
                const res = await fetch('/api/user/join', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        name: document.getElementById('name').value,
                        department: document.getElementById('department').value,
                        position: document.getElementById('position').value,
                        contact: document.getElementById('contact').value,
                        reason: document.getElementById('reason').value
                    })
                });
                const data = await res.json();
                const msg = document.getElementById('msg');
                msg.style.display = 'block';
                if(data.success) {
                    msg.className = 'msg success';
                    msg.innerHTML = '✅ 신청이 완료되었습니다!<br>대표이사님 승인 후 등록 링크를 안내받으실 수 있습니다.';
                    e.target.style.display = 'none';
                } else {
                    msg.className = 'msg error';
                    msg.textContent = data.message || '신청 실패';
                    btn.disabled = false; btn.textContent = '신청하기';
                }
            } catch(err) {
                alert('서버 오류: ' + err.message);
                btn.disabled = false; btn.textContent = '신청하기';
            }
        });
    </script>
</body>
</html>
"""


# ═══════════════════════════════════════════════
# 2. 계정 등록 페이지 (토큰 보호)
# ═══════════════════════════════════════════════

_REGISTER_PAGE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J-Hub 계정 등록</title>
    """ + _COMMON_STYLE + """
</head>
<body>
    <div class="container">
        <h1>%%TITLE%%</h1>
        <p class="subtitle">%%SUBTITLE%%</p>
        <form id="registerForm">
            <input type="hidden" id="token" value="%%TOKEN%%">
            %%USERNAME_FIELD%%
            <label class="required">비밀번호</label>
            <input type="password" id="password" placeholder="6자 이상" required minlength="6">
            <label class="required">비밀번호 확인</label>
            <input type="password" id="password2" placeholder="비밀번호를 다시 입력" required>
            <button type="submit" class="btn">등록 완료</button>
        </form>
        <div id="msg" class="msg" style="display:none;"></div>
        <a href="/" class="back-link">← 메인으로 돌아가기</a>
    </div>
    <script>
        document.getElementById('registerForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const pw = document.getElementById('password').value;
            if(pw !== document.getElementById('password2').value) {{
                const m = document.getElementById('msg');
                m.style.display='block'; m.className='msg error';
                m.textContent='비밀번호가 일치하지 않습니다.'; return;
            }}
            const btn = e.target.querySelector('.btn');
            btn.disabled = true; btn.textContent = '등록 중...';
            const body = {{
                token: document.getElementById('token').value,
                password: pw
            }};
            const usernameEl = document.getElementById('username');
            if(usernameEl) body.username = usernameEl.value;
            try {{
                const res = await fetch('/api/user/register', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(body)
                }});
                const data = await res.json();
                const msg = document.getElementById('msg');
                msg.style.display = 'block';
                if(data.success) {{
                    msg.className = 'msg success';
                    msg.innerHTML = '✅ 등록이 완료되었습니다!<br>아이디: <strong>' + (data.username || '') + '</strong><br><br>3초 후 로그인 페이지로 이동합니다.';
                    e.target.style.display = 'none';
                    setTimeout(() => window.location.href = '/', 3000);
                }} else {{
                    msg.className = 'msg error';
                    msg.textContent = data.message || '등록 실패';
                    btn.disabled = false; btn.textContent = '등록 완료';
                }}
            }} catch(err) {{
                alert('서버 오류: ' + err.message);
                btn.disabled = false; btn.textContent = '등록 완료';
            }}
        }});
    </script>
</body>
</html>
"""


# ═══════════════════════════════════════════════
# 3. 관리자 회원 관리 페이지
# ═══════════════════════════════════════════════

_ADMIN_PAGE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J-Hub 회원 관리</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
               background: #000; color: #f5f5f7; padding: 24px; }
        .header { max-width: 1200px; margin: 0 auto 32px; display: flex; justify-content: space-between; align-items: center; }
        h1 { font-size: 34px; font-weight: 600; letter-spacing: -0.4px; }
        .back { color: #2997ff; text-decoration: none; font-size: 15px; }
        .section { max-width: 1200px; margin: 0 auto 40px; background: #1d1d1f; border-radius: 18px; padding: 32px; }
        .section-title { font-size: 21px; font-weight: 600; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        .badge { background: #ff453a; color: white; border-radius: 999px; padding: 2px 10px; font-size: 13px; font-weight: 600; }
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; font-size: 12px; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px; padding: 10px 12px; border-bottom: 1px solid #2c2c2e; }
        td { padding: 14px 12px; border-bottom: 1px solid #1a1a1c; font-size: 15px; vertical-align: middle; }
        tr:hover { background: rgba(255,255,255,0.03); }
        .chip { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 500; }
        .chip-pending { background: rgba(255,159,10,0.15); color: #ff9f0a; }
        .chip-active { background: rgba(52,199,89,0.15); color: #34c759; }
        .chip-inactive { background: rgba(142,142,147,0.15); color: #8e8e93; }
        .action-btn { padding: 6px 16px; border-radius: 999px; border: none; font-size: 13px; font-weight: 600; cursor: pointer; margin: 2px; }
        .btn-approve { background: #34c759; color: white; }
        .btn-reject { background: #ff453a; color: white; }
        .btn-reset { background: #ff9f0a; color: white; }
        .btn-copy { background: #2c2c2e; color: #2997ff; border: 1px solid #2997ff; }
        .empty { text-align: center; color: #86868b; padding: 40px; font-size: 15px; }
        .token-link { background: #2c2c2e; padding: 8px 14px; border-radius: 8px; font-family: monospace; font-size: 13px; color: #30d158; word-break: break-all; margin-top: 8px; display: none; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; max-width: 1200px; margin-left: auto; margin-right: auto; }
        .stat-card { background: #1d1d1f; border-radius: 14px; padding: 24px; text-align: center; }
        .stat-num { font-size: 36px; font-weight: 700; color: #0066cc; }
        .stat-label { font-size: 13px; color: #86868b; margin-top: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>회원 관리</h1>
        <a href="/" class="back">← J-Hub 포털로 돌아가기</a>
    </div>

    <div class="stats" id="stats"></div>

    <div class="section">
        <div class="section-title">
            가입 대기 신청 <span class="badge" id="pendingCount">0</span>
        </div>
        <div id="pendingList"></div>
    </div>

    <div class="section">
        <div class="section-title">등록 회원 목록</div>
        <div id="memberList"></div>
    </div>

    <script>
        const BASE = window.location.origin;

        // [S-2] XSS 방어: 사용자 입력 데이터를 HTML 이스케이프
        function esc(str) {
            if(!str) return '';
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

        async function loadData() {
            // 대기 신청 로드
            const reqRes = await fetch('/api/user/admin/requests');
            const reqData = await reqRes.json();
            if(reqData.success) renderPending(reqData.requests);

            // 회원 목록 로드
            const memRes = await fetch('/api/user/admin/members');
            const memData = await memRes.json();
            if(memData.success) renderMembers(memData.members);

            // 통계
            const pending = reqData.requests ? reqData.requests.filter(r => r.status === 'pending').length : 0;
            const active = memData.members ? memData.members.filter(m => m.is_active).length : 0;
            const total = memData.members ? memData.members.length : 0;
            document.getElementById('stats').innerHTML = `
                <div class="stat-card"><div class="stat-num">${pending}</div><div class="stat-label">대기 신청</div></div>
                <div class="stat-card"><div class="stat-num">${active}</div><div class="stat-label">활성 회원</div></div>
                <div class="stat-card"><div class="stat-num">${total}</div><div class="stat-label">전체 등록</div></div>
                <div class="stat-card"><div class="stat-num">122</div><div class="stat-label">레거시 명단</div></div>
            `;
        }

        function renderPending(requests) {
            const pending = requests.filter(r => r.status === 'pending');
            document.getElementById('pendingCount').textContent = pending.length;
            if(pending.length === 0) {
                document.getElementById('pendingList').innerHTML = '<div class="empty">대기 중인 신청이 없습니다.</div>';
                return;
            }
            let html = '<table><tr><th>이름</th><th>소속</th><th>직급</th><th>연락처</th><th>신청일</th><th>처리</th></tr>';
            pending.forEach(r => {
                html += `<tr>
                    <td><strong>${esc(r.name)}</strong></td>
                    <td>${esc(r.department) || '-'}</td>
                    <td>${esc(r.position) || '-'}</td>
                    <td>${esc(r.contact) || '-'}</td>
                    <td>${r.requested_at ? r.requested_at.slice(0,16) : ''}</td>
                    <td>
                        <button class="action-btn btn-approve" onclick="approveReq(${r.id})">승인</button>
                        <button class="action-btn btn-reject" onclick="rejectReq(${r.id})">거절</button>
                    </td>
                </tr>
                <tr id="token_row_${r.id}" style="display:none;">
                    <td colspan="6">
                        <div class="token-link" id="token_${r.id}" style="display:block;"></div>
                    </td>
                </tr>`;
            });
            html += '</table>';
            document.getElementById('pendingList').innerHTML = html;
        }

        function renderMembers(members) {
            if(members.length === 0) {
                document.getElementById('memberList').innerHTML = '<div class="empty">등록된 회원이 없습니다.</div>';
                return;
            }
            let html = '<table><tr><th>이름</th><th>아이디</th><th>소속</th><th>직급</th><th>등록일</th><th>최근 접속</th><th>상태</th><th>관리</th></tr>';
            members.forEach(m => {
                const statusChip = m.is_active
                    ? '<span class="chip chip-active">활성</span>'
                    : '<span class="chip chip-inactive">비활성</span>';
                const lastLogin = m.last_login ? m.last_login.slice(0,16) : '미접속';
                const safeName = esc(m.display_name);
                html += `<tr>
                    <td><strong>${safeName}</strong></td>
                    <td style="color:#86868b;">${esc(m.username)}</td>
                    <td>${esc(m.department) || '-'}</td>
                    <td>${esc(m.position) || '-'}</td>
                    <td>${m.registered_at ? m.registered_at.slice(0,10) : ''}</td>
                    <td style="color:#86868b;">${lastLogin}</td>
                    <td>${statusChip}</td>
                    <td>
                        <button class="action-btn btn-reset" onclick="resetPw(${m.id}, '${safeName.replace(/'/g, "\\'")}')">비번 초기화</button>
                    </td>
                </tr>
                <tr id="reset_row_${m.id}" style="display:none;">
                    <td colspan="8"><div class="token-link" id="reset_${m.id}" style="display:block;"></div></td>
                </tr>`;
            });
            html += '</table>';
            document.getElementById('memberList').innerHTML = html;
        }

        async function approveReq(id) {
            if(!confirm('이 신청을 승인하시겠습니까?')) return;
            const res = await fetch('/api/user/admin/approve', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id})
            });
            const data = await res.json();
            if(data.success) {
                const link = BASE + '/register/' + data.token;
                document.getElementById('token_row_' + id).style.display = '';
                document.getElementById('token_' + id).innerHTML =
                    '✅ 승인 완료! 아래 링크를 신청자에게 전달하세요:<br><br>' +
                    '<a href="' + link + '" target="_blank" style="color:#30d158;">' + link + '</a>' +
                    '<br><br><button class="action-btn btn-copy" onclick="navigator.clipboard.writeText(\\''+link+'\\');this.textContent=\\'복사됨!\\'">링크 복사</button>';
                loadData();
            } else {
                alert(data.message || '승인 실패');
            }
        }

        async function rejectReq(id) {
            const reason = prompt('거절 사유를 입력하세요 (선택):');
            if(reason === null) return;
            const res = await fetch('/api/user/admin/reject', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, reason: reason})
            });
            const data = await res.json();
            if(data.success) { alert('거절 처리되었습니다.'); loadData(); }
            else alert(data.message || '거절 실패');
        }

        async function resetPw(userId, name) {
            if(!confirm(name + '님의 비밀번호를 초기화하시겠습니까?')) return;
            const res = await fetch('/api/user/admin/reset_pw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user_id: userId})
            });
            const data = await res.json();
            if(data.success) {
                const link = BASE + '/reset_pw/' + data.token;
                document.getElementById('reset_row_' + userId).style.display = '';
                document.getElementById('reset_' + userId).innerHTML =
                    '🔑 비밀번호 초기화 완료! 아래 링크를 ' + name + '님에게 전달하세요:<br><br>' +
                    '<a href="' + link + '" target="_blank" style="color:#30d158;">' + link + '</a>' +
                    '<br><br><button class="action-btn btn-copy" onclick="navigator.clipboard.writeText(\\''+link+'\\');this.textContent=\\'복사됨!\\'">링크 복사</button>';
            } else { alert(data.message || '초기화 실패'); }
        }

        loadData();
    </script>
</body>
</html>
"""


# ═══════════════════════════════════════════════
# Page Routes
# ═══════════════════════════════════════════════

@user_bp.route('/signup')
def signup_page():
    """회원가입 신청 페이지 (공개)"""
    return _SIGNUP_PAGE


@user_bp.route('/register/<token>')
def register_page(token):
    """계정 등록 페이지 (토큰 보호)"""
    req = get_request_by_token(token)
    if not req:
        return "<h2 style='text-align:center;padding:100px;font-family:sans-serif;'>⚠️ 유효하지 않은 링크이거나 이미 등록이 완료되었습니다.</h2>", 404
    return (_REGISTER_PAGE
        .replace('%%TITLE%%', '계정 등록')
        .replace('%%SUBTITLE%%', f"<strong>{req['name']}</strong>님, 환영합니다!<br>사용하실 아이디와 비밀번호를 설정해 주세요.")
        .replace('%%TOKEN%%', token)
        .replace('%%USERNAME_FIELD%%', '<label class="required">아이디</label><input type="text" id="username" placeholder="영문/숫자 조합" required minlength="3">')
    )


@user_bp.route('/reset_pw/<token>')
def reset_pw_page(token):
    """비밀번호 재설정 페이지 (토큰 보호)"""
    user = get_user_by_reset_token(token)
    if not user:
        return "<h2 style='text-align:center;padding:100px;font-family:sans-serif;'>⚠️ 유효하지 않은 링크이거나 이미 변경이 완료되었습니다.</h2>", 404
    return (_REGISTER_PAGE
        .replace('%%TITLE%%', '비밀번호 재설정')
        .replace('%%SUBTITLE%%', f"<strong>{user['display_name']}</strong>님, 새 비밀번호를 설정해 주세요.")
        .replace('%%TOKEN%%', token)
        .replace('%%USERNAME_FIELD%%', '')
    )


@user_bp.route('/admin/members')
def admin_members_page():
    """관리자 회원 관리 페이지 (마스터 전용)"""
    if not session.get('logged_in') or not session.get('is_master'):
        return redirect('/')
    return _ADMIN_PAGE


# ═══════════════════════════════════════════════
# API Endpoints
# ═══════════════════════════════════════════════

@user_bp.route('/api/user/join', methods=['POST'])
def api_join_request():
    """회원가입 신청 접수 (공개)"""
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"success": False, "message": "이름은 필수입니다."}), 400

    result = create_join_request(
        name=data['name'],
        department=data.get('department', ''),
        position=data.get('position', ''),
        contact=data.get('contact', ''),
        reason=data.get('reason', '')
    )
    if result:
        return jsonify({"success": True, "message": "가입 신청이 접수되었습니다."})
    return jsonify({"success": False, "message": "신청 처리 중 오류가 발생했습니다."}), 500


@user_bp.route('/api/user/register', methods=['POST'])
def api_register():
    """토큰을 사용한 계정 등록 (신규 가입 + 비번 재설정 공용)"""
    data = request.get_json()
    token = data.get('token', '')
    password = data.get('password', '')

    if not token or not password or len(password) < 6:
        return jsonify({"success": False, "message": "토큰과 비밀번호(6자 이상)가 필요합니다."}), 400

    # 1) 비밀번호 재설정 토큰인지 확인
    user = get_user_by_reset_token(token)
    if user:
        result = update_password(user['id'], password)
        if result:
            return jsonify({"success": True, "message": "비밀번호가 변경되었습니다.", "username": user['username']})
        return jsonify({"success": False, "message": "변경 실패"}), 500

    # 2) 신규 가입 토큰인지 확인
    req = get_request_by_token(token)
    if not req:
        return jsonify({"success": False, "message": "유효하지 않은 토큰입니다."}), 400

    username = data.get('username', '').strip()
    if not username or len(username) < 3:
        return jsonify({"success": False, "message": "아이디는 3자 이상 입력해 주세요."}), 400

    result = register_user(
        username=username,
        password=password,
        display_name=req['name'],
        department=req.get('department', ''),
        position=req.get('position', '')
    )
    if result:
        consume_token(token)
        return jsonify({"success": True, "message": "등록 완료", "username": username})
    return jsonify({"success": False, "message": "이미 사용 중인 아이디입니다. 다른 아이디를 선택해 주세요."}), 400


@user_bp.route('/api/user/admin/requests', methods=['GET'])
@master_required
def api_admin_requests():
    """관리자: 가입 신청 목록"""
    requests_list = get_join_requests()
    return jsonify({"success": True, "requests": requests_list})


@user_bp.route('/api/user/admin/members', methods=['GET'])
@master_required
def api_admin_members():
    """관리자: 등록 회원 목록"""
    members = get_all_members()
    return jsonify({"success": True, "members": members})


@user_bp.route('/api/user/admin/approve', methods=['POST'])
@master_required
def api_admin_approve():
    """관리자: 가입 신청 승인"""
    data = request.get_json()
    request_id = data.get('id')
    if not request_id:
        return jsonify({"success": False, "message": "신청 ID가 필요합니다."}), 400

    token = approve_request(request_id)
    if token:
        return jsonify({"success": True, "token": token, "message": "승인 완료"})
    return jsonify({"success": False, "message": "승인 처리 실패"}), 500


@user_bp.route('/api/user/admin/reject', methods=['POST'])
@master_required
def api_admin_reject():
    """관리자: 가입 신청 거절"""
    data = request.get_json()
    request_id = data.get('id')
    reason = data.get('reason', '')
    if not request_id:
        return jsonify({"success": False, "message": "신청 ID가 필요합니다."}), 400

    result = reject_request(request_id, reason)
    if result:
        return jsonify({"success": True, "message": "거절 처리 완료"})
    return jsonify({"success": False, "message": "거절 처리 실패"}), 500


@user_bp.route('/api/user/admin/reset_pw', methods=['POST'])
@master_required
def api_admin_reset_pw():
    """관리자: 비밀번호 초기화"""
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "사용자 ID가 필요합니다."}), 400

    token = reset_user_password(user_id)
    if token:
        return jsonify({"success": True, "token": token, "message": "비밀번호 초기화 완료"})
    return jsonify({"success": False, "message": "초기화 실패"}), 500
