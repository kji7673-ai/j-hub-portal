import os

with open('book_studio.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS for Slide-over Panel and Password Modal
css_to_insert = """
        /* Secret Room UI */
        .secret-modal {
            display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;
        }
        .secret-modal-content {
            background: #fff; padding: 30px; border-radius: 18px; width: 300px; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .secret-modal input {
            width: 100%; padding: 10px; margin: 15px 0; border: 1px solid #ccc; border-radius: 8px; text-align: center;
            font-size: 20px; letter-spacing: 5px;
        }
        
        .secret-panel {
            position: fixed; bottom: -100%; left: 0; right: 0; height: 70vh;
            background: rgba(250, 250, 252, 0.95); backdrop-filter: blur(20px);
            border-top-left-radius: 24px; border-top-right-radius: 24px;
            box-shadow: 0 -10px 40px rgba(0,0,0,0.15); z-index: 900;
            transition: bottom 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex; flex-direction: column; padding: 30px 8%;
            border-top: 1px solid rgba(0,0,0,0.05);
        }
        .secret-panel.open { bottom: 0; }
        
        .panel-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
        }
        .panel-title { font-family: 'SF Pro Display', sans-serif; font-weight: 600; font-size: 20px; color: #1d1d1f; }
        .close-panel { background: none; border: none; font-size: 24px; cursor: pointer; color: #1d1d1f; }
        
        .panel-body { display: flex; gap: 20px; flex: 1; min-height: 0; }
        .panel-col { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .panel-label { font-size: 14px; font-weight: 600; color: #1d1d1f; margin-bottom: 5px; }
        .panel-textarea {
            flex: 1; border: 1px solid #d2d2d7; border-radius: 12px; padding: 15px;
            font-family: 'SF Pro Text', sans-serif; font-size: 15px; line-height: 1.5;
            resize: none; background: #fff;
        }
        .feedback-box {
            flex: 1; border: 1px solid #d2d2d7; border-radius: 12px; padding: 15px;
            background: #f5f5f7; font-family: 'SF Pro Text', sans-serif; font-size: 14px;
            overflow-y: auto; line-height: 1.5; color: #1d1d1f;
        }
        .panel-footer { margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px; }
        
        .btn-redteam { background: #000; color: #fff; border: none; padding: 12px 24px; border-radius: 999px; cursor: pointer; font-weight: 600; }
        .btn-save { background: #0066cc; color: #fff; border: none; padding: 12px 24px; border-radius: 999px; cursor: pointer; font-weight: 600; }
"""
html = html.replace('</style>', css_to_insert + '\n    </style>')

# 2. Add HTML for Password Modal and Slide-over Panel
html_to_insert = """
    <!-- Secret Room UI -->
    <div class="secret-modal" id="secret-modal">
        <div class="secret-modal-content">
            <h3 style="margin-bottom:10px;">비밀 집필실</h3>
            <p style="font-size:12px; color:#666;">접근 코드를 입력하세요</p>
            <input type="password" id="secret-pw" maxlength="6">
            <button class="btn" onclick="checkSecretPassword()">입장</button>
        </div>
    </div>
    
    <div class="secret-panel" id="secret-panel">
        <div class="panel-header">
            <div class="panel-title">🧠 Red Team 집필 스튜디오</div>
            <button class="close-panel" onclick="closeSecretPanel()">×</button>
        </div>
        <div class="panel-body">
            <div class="panel-col">
                <div class="panel-label">현재 원고 (수정 가능)</div>
                <textarea class="panel-textarea" id="panel-original-text"></textarea>
            </div>
            <div class="panel-col">
                <div class="panel-label">CEO 추가 의견 / 철학적 지시사항</div>
                <textarea class="panel-textarea" id="panel-ceo-opinion" placeholder="여기에 추가할 내용이나 비판받을 의견을 적어주세요."></textarea>
            </div>
            <div class="panel-col">
                <div class="panel-label">레드팀 비판 결과</div>
                <div class="feedback-box" id="panel-feedback">
                    '비판 요청' 버튼을 누르면 AI가 냉철한 피드백을 제공합니다.
                </div>
            </div>
        </div>
        <div class="panel-footer">
            <button class="btn-redteam" onclick="requestRedTeam()">🔥 레드팀 비판 요청</button>
            <button class="btn-save" onclick="saveRevision()">💾 최종 원고에 반영 (덮어쓰기)</button>
        </div>
    </div>
"""
html = html.replace('    <div class="book-container"', html_to_insert + '\n    <div class="book-container"')

# 3. Add JS for the new logic
js_to_insert = """
        // Secret Room Logic
        let clickCount = 0;
        let clickTimer;
        
        // Listen for clicks on the book container (but specifically we want to target top header area or just globally handle 3 clicks fast)
        document.body.addEventListener('click', function(e) {
            // Only trigger if clicking on empty space or the container itself to avoid interfering with buttons
            if(e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            
            clickCount++;
            clearTimeout(clickTimer);
            clickTimer = setTimeout(() => { clickCount = 0; }, 500);
            
            if (clickCount >= 3) {
                clickCount = 0;
                document.getElementById('secret-modal').style.display = 'flex';
                document.getElementById('secret-pw').focus();
            }
        });

        function checkSecretPassword() {
            const pw = document.getElementById('secret-pw').value;
            if (pw === '937610') {
                document.getElementById('secret-modal').style.display = 'none';
                document.getElementById('secret-pw').value = '';
                openSecretPanel();
            } else {
                alert('코드가 일치하지 않습니다.');
                document.getElementById('secret-modal').style.display = 'none';
            }
        }

        function openSecretPanel() {
            const panel = document.getElementById('secret-panel');
            panel.classList.add('open');
            
            // Load current page text
            const activePage = bookData.pages[currentPage];
            document.getElementById('panel-original-text').value = activePage.text || '';
            document.getElementById('panel-ceo-opinion').value = '';
            document.getElementById('panel-feedback').innerHTML = "'비판 요청' 버튼을 누르면 AI가 냉철한 피드백을 제공합니다.";
        }
        
        function closeSecretPanel() {
            document.getElementById('secret-panel').classList.remove('open');
        }

        async function requestRedTeam() {
            const originalText = document.getElementById('panel-original-text').value;
            const ceoOpinion = document.getElementById('panel-ceo-opinion').value;
            const feedbackBox = document.getElementById('panel-feedback');
            
            if (!ceoOpinion.trim()) {
                alert('CEO 의견을 입력해주세요.');
                return;
            }
            
            feedbackBox.innerHTML = '<span style="color:#0066cc;">AI 레드팀이 비판적 피드백을 생성 중입니다...</span>';
            
            try {
                const response = await fetch('/api/redteam', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ original_text: originalText, ceo_opinion: ceoOpinion })
                });
                const result = await response.json();
                feedbackBox.innerHTML = result.feedback.replace(/\\n/g, '<br>');
            } catch (e) {
                feedbackBox.innerHTML = '<span style="color:red;">오류 발생: 서버와 통신할 수 없습니다.</span>';
            }
        }

        async function saveRevision() {
            const revisedText = document.getElementById('panel-original-text').value;
            
            if(!confirm('이 내용을 실제 원고(book_data.js)에 영구적으로 덮어쓰시겠습니까?')) return;
            
            try {
                const response = await fetch('/api/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ page_index: currentPage, revised_text: revisedText })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert('성공적으로 반영되었습니다.');
                    // Update local object and re-render
                    bookData.pages[currentPage].text = revisedText;
                    renderBook();
                    closeSecretPanel();
                } else {
                    alert('저장 실패: ' + result.message);
                }
            } catch (e) {
                alert('오류 발생: 서버와 통신할 수 없습니다.');
            }
        }
"""
html = html.replace('// Init', js_to_insert + '\n        // Init')

with open('book_studio.html', 'w', encoding='utf-8') as f:
    f.write(html)
