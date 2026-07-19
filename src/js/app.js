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
