import os

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_studio.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the panel body HTML
old_panel_html = """
        <div class="panel-body">
            <div class="panel-col">
                <div class="panel-label">현재 페이지 원고 (직접 수정 가능)</div>
                <textarea id="panel-original-text" class="panel-textarea"></textarea>
            </div>
            <div class="panel-col" style="flex: 0.3;">
                <div class="panel-label">▶ CEO 추가 의견 / 거친 생각</div>
                <textarea id="panel-ceo-opinion" class="panel-textarea" placeholder="여기에 추가하고 싶은 내용이나 방향성을 편하게 적어주세요."></textarea>
            </div>
            <div class="panel-col">
                <div class="panel-label">💡 AI 레드팀 비판 및 제안</div>
                <div id="panel-feedback" class="feedback-box">
                    '비판 요청' 버튼을 누르면 AI가 냉철한 피드백을 제공합니다.
                </div>
            </div>
        </div>
        <div class="panel-footer">
            <button class="btn-redteam" onclick="requestRedTeam()">🔥 레드팀 비판 요청</button>
            <button class="btn-save" onclick="saveRevision()">💾 최종 원고에 반영</button>
        </div>
"""

new_panel_html = """
        <div class="panel-body">
            <div class="panel-col" style="flex: 0.8;">
                <div class="panel-label">현재 페이지 원고 (AI가 재작성 시 자동 반영됩니다)</div>
                <textarea id="panel-original-text" class="panel-textarea"></textarea>
                
                <div class="panel-label" style="margin-top:15px;">이미지 컨트롤</div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <select id="panel-image-layout" style="padding:8px; border-radius:8px; border:1px solid #ccc; font-family:'SF Pro Text';">
                        <option value="text_only">텍스트만 (이미지 없음)</option>
                        <option value="image_top">상단 스케치 (35% 크기)</option>
                        <option value="image_full">전체 화면 (글씨 없음)</option>
                    </select>
                    <label for="panel-image-upload" class="btn btn-outline" style="margin:0;">새 이미지 업로드</label>
                    <input type="file" id="panel-image-upload" accept="image/*" style="display:none;">
                </div>
            </div>
            
            <div class="panel-col" style="flex: 1.2;">
                <div class="panel-label">💬 AI 레드팀 티키타카 (수정 논의)</div>
                <div id="chat-history" class="feedback-box" style="flex:1; display:flex; flex-direction:column; gap:10px;">
                    <div style="text-align:center; color:#888;">AI 레드팀과 대화를 시작하세요.</div>
                </div>
                
                <div style="display:flex; gap:10px; margin-top:10px;">
                    <textarea id="chat-input" class="panel-textarea" style="height:60px;" placeholder="어떻게 고치면 좋을지 편하게 적어주세요."></textarea>
                    <button class="btn-redteam" onclick="sendChatMessage()" style="border-radius:12px; padding:0 20px;">전송</button>
                </div>
                
                <div class="panel-footer" style="margin-top:10px;">
                    <button class="btn-save" onclick="applyFinalRevision()" style="width:100%;">✨ AI 최종 원고 자동 재작성 및 저장</button>
                </div>
            </div>
        </div>
"""

# Replace JS logic
old_js = """
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

new_js = """
        let currentChatHistory = [];
        
        function appendChatMessage(role, content) {
            const historyBox = document.getElementById('chat-history');
            const msgDiv = document.createElement('div');
            msgDiv.style.padding = '10px 14px';
            msgDiv.style.borderRadius = '12px';
            msgDiv.style.maxWidth = '85%';
            msgDiv.style.fontSize = '14px';
            msgDiv.style.lineHeight = '1.5';
            
            if (role === 'user') {
                msgDiv.style.background = '#0066cc';
                msgDiv.style.color = '#fff';
                msgDiv.style.alignSelf = 'flex-end';
                msgDiv.style.borderBottomRightRadius = '4px';
            } else {
                msgDiv.style.background = '#e5e5ea';
                msgDiv.style.color = '#1d1d1f';
                msgDiv.style.alignSelf = 'flex-start';
                msgDiv.style.borderBottomLeftRadius = '4px';
            }
            msgDiv.innerHTML = content.replace(/\\n/g, '<br>');
            
            // Remove empty placeholder if first message
            if (historyBox.children.length === 1 && historyBox.children[0].innerText.includes('시작하세요')) {
                historyBox.innerHTML = '';
            }
            
            historyBox.appendChild(msgDiv);
            historyBox.scrollTop = historyBox.scrollHeight;
            
            if (role !== 'system') {
                currentChatHistory.push({ role: role, content: content });
            }
        }

        async function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const originalText = document.getElementById('panel-original-text').value;
            const msg = input.value.trim();
            
            if (!msg) return;
            
            input.value = '';
            appendChatMessage('user', msg);
            appendChatMessage('system', '<i>답변 생성 중...</i>');
            
            try {
                const response = await fetch('/api/redteam_chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        original_text: originalText, 
                        chat_history: currentChatHistory.slice(0, -1), // Exclude the one just added temporarily
                        message: msg 
                    })
                });
                const result = await response.json();
                
                // Remove the 'system' loading message
                const historyBox = document.getElementById('chat-history');
                historyBox.removeChild(historyBox.lastChild);
                
                appendChatMessage('model', result.feedback);
            } catch (e) {
                const historyBox = document.getElementById('chat-history');
                historyBox.removeChild(historyBox.lastChild);
                appendChatMessage('system', '<span style="color:red;">서버 통신 오류가 발생했습니다.</span>');
            }
        }

        async function applyFinalRevision() {
            if(!confirm('AI가 대화 내역과 앞뒤 문맥을 고려하여 최종 원고를 덮어씁니다. 진행하시겠습니까?')) return;
            
            const originalText = document.getElementById('panel-original-text').value;
            const prevText = currentPage > 0 ? bookData.pages[currentPage-1].text : '';
            const nextText = currentPage < bookData.pages.length - 1 ? bookData.pages[currentPage+1].text : '';
            
            const saveBtn = document.querySelector('.btn-save');
            const oldSaveText = saveBtn.innerText;
            saveBtn.innerText = 'AI가 재작성 중...';
            saveBtn.disabled = true;
            
            try {
                const response = await fetch('/api/apply_revision', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        page_index: currentPage, 
                        original_text: originalText,
                        chat_history: currentChatHistory,
                        prev_text: prevText || '',
                        next_text: nextText || ''
                    })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    // Update local object and re-render
                    bookData.pages[currentPage].text = result.revised_text;
                    document.getElementById('panel-original-text').value = result.revised_text;
                    renderBook();
                    alert('AI가 앞뒤 문맥에 맞게 최종 원고를 성공적으로 재작성했습니다.');
                } else {
                    alert('저장 실패: ' + result.message);
                }
            } catch (e) {
                alert('오류 발생: 서버와 통신할 수 없습니다.');
            }
            
            saveBtn.innerText = oldSaveText;
            saveBtn.disabled = false;
        }
        
        // Setup image upload in panel
        document.getElementById('panel-image-upload').addEventListener('change', async function(e) {
            if(e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                const layout = document.getElementById('panel-image-layout').value;
                const reader = new FileReader();
                
                const uploadLabel = document.querySelector('label[for="panel-image-upload"]');
                const originalLabel = uploadLabel.innerText;
                uploadLabel.innerText = "업로드 중...";
                
                reader.onload = async function(e) {
                    const base64Data = e.target.result;
                    
                    try {
                        const response = await fetch('/api/upload_image', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                page_index: currentPage,
                                image_data: base64Data,
                                image_layout: layout
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {
                            const activePage = bookData.pages[currentPage];
                            activePage.image = result.image_url;
                            activePage.type = layout;
                            
                            renderBook();
                            uploadLabel.innerText = originalLabel;
                        } else {
                            alert("업로드 실패: " + result.message);
                            uploadLabel.innerText = originalLabel;
                        }
                    } catch (error) {
                        alert("서버 통신 오류: " + error.message);
                        uploadLabel.innerText = originalLabel;
                    }
                }
                reader.readAsDataURL(file);
            }
        });
        
        // Handle Layout Change without upload
        document.getElementById('panel-image-layout').addEventListener('change', async function(e) {
            const layout = e.target.value;
            const activePage = bookData.pages[currentPage];
            if(activePage.type !== layout) {
                // If we need to just save the type change (requires backend endpoint, but for now we just change it locally. To save permanently, we'd need a save_layout API. Let's just alert.)
                alert("레이아웃만 변경하는 기능은 새 이미지를 업로드할 때 함께 반영되거나, 원고 수정 시 반영됩니다.");
                activePage.type = layout;
                renderBook();
            }
        });
"""

# Open panel reset history
old_open_panel = """
        function openSecretPanel() {
            const panel = document.getElementById('secret-panel');
            panel.classList.add('open');
            
            // Load current page text
            const activePage = bookData.pages[currentPage];
            document.getElementById('panel-original-text').value = activePage.text || '';
            document.getElementById('panel-ceo-opinion').value = '';
            document.getElementById('panel-feedback').innerHTML = "'비판 요청' 버튼을 누르면 AI가 냉철한 피드백을 제공합니다.";
        }
"""
new_open_panel = """
        function openSecretPanel() {
            const panel = document.getElementById('secret-panel');
            panel.classList.add('open');
            
            // Load current page text
            const activePage = bookData.pages[currentPage];
            document.getElementById('panel-original-text').value = activePage.text || '';
            document.getElementById('panel-image-layout').value = activePage.type;
            
            // Reset chat
            currentChatHistory = [];
            document.getElementById('chat-history').innerHTML = '<div style="text-align:center; color:#888;">AI 레드팀과 대화를 시작하세요.</div>';
            document.getElementById('chat-input').value = '';
        }
"""

if "btn-redteam" in html:
    html = html.replace(old_panel_html.strip(), new_panel_html.strip())
    
if "async function requestRedTeam" in html:
    html = html.replace(old_js.strip(), new_js.strip())
    
if "document.getElementById('panel-ceo-opinion')" in html:
    html = html.replace(old_open_panel.strip(), new_open_panel.strip())

# Remove the old upload button from edit-toolbar to prevent confusion
old_edit_toolbar = """
    <div class="edit-toolbar">
        <label for="image-upload" class="btn btn-outline">이미지 업로드</label>
        <input type="file" id="image-upload" accept="image/*">
        <button class="btn" onclick="openSecretPanel()">원고 수정 / 비판 요청</button>
    </div>
"""
new_edit_toolbar = """
    <div class="edit-toolbar">
        <button class="btn" onclick="openSecretPanel()">원고 수정 / 비판 요청</button>
    </div>
"""

if "id=\"image-upload\"" in html and "edit-toolbar" in html:
    html = html.replace(old_edit_toolbar.strip(), new_edit_toolbar.strip())

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_studio.html', 'w', encoding='utf-8') as f:
    f.write(html)
