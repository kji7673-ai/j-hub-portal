        let currentChapter = 0;
        let currentColumn = 0;
        const COLUMN_GAP = 40;

        function renderBook() {
            const container = document.getElementById('book-container');
            // Remove existing pages
            document.querySelectorAll('.page-content').forEach(p => p.remove());

            bookData.pages.forEach((page, index) => {
                const pageEl = document.createElement('div');
                pageEl.className = 'page-content' + (index === currentChapter ? ' active' : '');
                
                let contentHTML = '';
                
                if (page.type === 'cover') {
                    pageEl.className += ' bg-dark';
                    
                    let rawTitle = page.title;
                    let part = "";
                    let mainTitle = rawTitle;
                    let subtitle = page.subtitle || "";
                    
                    // 1. Extract Subtitle from parentheses
                    if (!subtitle) {
                        const subMatch = rawTitle.match(/(.*?)\s*\((.*?)\)$/);
                        if (subMatch) {
                            mainTitle = subMatch[1].trim();
                            subtitle = subMatch[2].trim();
                        }
                    }
                    
                    // 2. Extract Part / Theme
                    const partMatch = mainTitle.match(/^((?:\d+부\.\s*\[.*?\]|\[.*?\]|막간극.*?:\s*|에필로그:\s*))(.+)$/);
                    if (partMatch) {
                        part = partMatch[1].trim();
                        mainTitle = partMatch[2].trim();
                    }
                    
                    contentHTML += `<div class="cover-content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">`;
                    
                    if (part) {
                        contentHTML += `<p style="font-family: var(--font-display, 'SF Pro Display', sans-serif); font-size: 14px; font-weight: 600; color: var(--primary-on-dark, #2997ff); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">${part}</p>`;
                    }
                    
                    contentHTML += `<h1 class="book-title" style="font-family: var(--font-display, 'SF Pro Display', sans-serif); font-size: clamp(28px, 6vw, 44px); font-weight: 700; color: #ffffff; margin: 0 0 24px 0; line-height: 1.25; letter-spacing: -0.02em; word-break: keep-all;">${mainTitle}</h1>`;
                    
                    if (subtitle) {
                        contentHTML += `<p style="font-family: var(--font-body, 'SF Pro Text', sans-serif); font-size: 18px; font-weight: 300; color: #a0a0a0; margin: 0; word-break: keep-all; line-height: 1.5;">${subtitle}</p>`;
                    }
                    
                    // Decorative line
                    contentHTML += `<div style="width: 40px; height: 1px; background: rgba(255,255,255,0.2); margin-top: 40px;"></div>`;
                    contentHTML += `</div>`;
                }

                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #f5f5f7); border-radius: 18px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid var(--hairline, #e0e0e0); width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    

                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }
 
                else if (page.type === 'image_top') {
                    if(page.image) contentHTML += `<div class="image-container" id="img-container-${index}"><img src="${page.image}" alt="sketch"></div>`;
                    if(page.title) contentHTML += `<h2 class="chapter-title" style="margin-bottom:10px;">${page.title}</h2>`;
                    if(page.text) {
                        const paragraphs = page.text.split('\n\n');
                        paragraphs.forEach(p => {
                            if (p.trim().startsWith('<table') || p.trim().startsWith('<div class="custom-table"')) {
                                contentHTML += p;
                            } else {
                                contentHTML += `<p class="body-text">${p}</p>`;
                            }
                        });
                    }
                }
                else if (page.type === 'image_full') {
                    pageEl.style.padding = '0';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; border-radius:0; z-index:0; background:transparent;"><img src="${page.image}" alt="full_image" style="width:100%; height:100%; object-fit:cover; border-radius:0; box-shadow:none; max-width:none;"></div>`;
                    }
                    contentHTML += `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; background: rgba(255,255,255,0.4); padding: 40px; box-sizing:border-box;">`;
                    if(page.title) contentHTML += `<h1 class="book-title" style="text-align:center; color:#1d1d1f; font-size:48px; margin-bottom:20px; text-shadow: 0 2px 15px rgba(255,255,255,0.9); font-weight:700;">${page.title}</h1>`;
                    if(page.subtitle) contentHTML += `<p style="text-align:center; color:#333; font-size:24px; font-weight:600; text-shadow: 0 1px 10px rgba(255,255,255,0.9);">${page.subtitle}</p>`;
                    if(page.text) {
                        const paragraphs = page.text.split('\n\n');
                        paragraphs.forEach(p => {
                            contentHTML += `<p class="body-text" style="color:#1d1d1f; font-weight:600; text-shadow: 0 1px 10px rgba(255,255,255,0.9); text-align:center; font-size:18px;">${p}</p>`;
                        });
                    }
                    contentHTML += `</div>`;
                }

                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #f5f5f7); border-radius: 18px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid var(--hairline, #e0e0e0); width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    
                    contentHTML += `<ul class="author-list">`;
                    contentHTML += `<li>현(現) 서울시 건축심의위원</li>`;
                    contentHTML += `<li>현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원</li>`;
                    contentHTML += `<li>현(現) 강동구, 양천구 건축심의위원</li>`;
                    contentHTML += `<li>현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원</li>`;
                    contentHTML += `</ul>`;
                    
                    contentHTML += `<p class="author-desc" style="border-top: 1px solid var(--hairline); padding-top: 20px; margin-bottom: 0;">"정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 뼈저리게 목도하고 있는 건축가의 진심 어린 조언이자 따뜻한 혁신의 기록."</p>`;
                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }

                else if (page.type === 'text_only') {
                    if(page.title) contentHTML += `<h2 class="chapter-title">${page.title}</h2>`;
                    if(page.text) {
                        const paragraphs = page.text.split('\n\n');
                        paragraphs.forEach(p => {
                            if (p.trim().startsWith('<table') || p.trim().startsWith('<div class="custom-table"')) {
                                contentHTML += p;
                            } else {
                                contentHTML += `<p class="body-text">${p}</p>`;
                            }
                        });
                    }
                }

                pageEl.innerHTML = contentHTML;
                container.insertBefore(pageEl, container.querySelector('.controls'));
            });

            updateControls();
        }

        function getChapterMaxColumns(chapterIndex) {
            const pageEls = document.querySelectorAll('.page-content');
            const p = pageEls[chapterIndex];
            if (!p) return 1;
            const w = p.clientWidth || document.getElementById('book-container').clientWidth;
            const sw = p.scrollWidth || w;
            return Math.max(1, Math.round((sw + COLUMN_GAP) / (w + COLUMN_GAP)));
        }

        function updateControls() {
            const pageEls = document.querySelectorAll('.page-content');
            
            pageEls.forEach((p, idx) => {
                if (idx === currentChapter) {
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                    p.style.transform = `translateX(0px)`;
                }
            });
            
            const maxCols = getChapterMaxColumns(currentChapter);
            if (currentColumn >= maxCols) currentColumn = maxCols - 1;
            if (currentColumn < 0) currentColumn = 0;
            
            const activePage = pageEls[currentChapter];
            const w = activePage.clientWidth || document.getElementById('book-container').clientWidth;
            const translatePx = currentColumn * (w + COLUMN_GAP);
            activePage.style.transform = `translateX(-${translatePx}px)`;
            
            // Removed heavy loop over all 131 chapters that causes Safari to crash.
            // Now we only calculate maxCols for the CURRENT chapter.
            const totalChapters = bookData.pages.length;
            document.getElementById('prev-btn').disabled = (currentChapter === 0 && currentColumn === 0);
            document.getElementById('next-btn').disabled = (currentChapter === totalChapters - 1 && currentColumn === maxCols - 1);
            document.getElementById('page-num').innerText = `[${currentChapter + 1}/${totalChapters}] ${currentColumn + 1} / ${maxCols}`;
        }

        function prevPage() {
            if (currentColumn > 0) {
                currentColumn--;
                updateControls();
            } else if (currentChapter > 0) {
                currentChapter--;
                currentColumn = 999; // updateControls will clamp it to maxCols - 1
                updateControls();
            }
        }

        function nextPage() {
            const maxCols = getChapterMaxColumns(currentChapter);
            if (currentColumn < maxCols - 1) {
                currentColumn++;
                updateControls();
            } else if (currentChapter < bookData.pages.length - 1) {
                currentChapter++;
                currentColumn = 0;
                updateControls();
            }
        }
        
        window.addEventListener('resize', () => {
            updateControls();
        });

        
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
            if (pw === '9376105152') {
                document.getElementById('secret-modal').style.display = 'none';
                document.getElementById('secret-pw').value = '';
                const toolbar = document.querySelector('.edit-toolbar');
                if (toolbar) toolbar.style.display = 'block';
            } else {
                alert('비밀번호가 일치하지 않습니다.');
                document.getElementById('secret-modal').style.display = 'none';
            }
        }

        function openSecretPanel() {
            const panel = document.getElementById('secret-panel');
            panel.classList.add('open');
            
            // Load current page text
            const activePage = bookData.pages[currentChapter];
            let contentText = activePage.text || '';
            if (!contentText && activePage.title) {
                contentText = activePage.title + (activePage.subtitle ? '\n' + activePage.subtitle : '');
            }
            document.getElementById('panel-original-text').value = contentText;
            document.getElementById('panel-image-layout').value = activePage.type;
            
            // Reset chat
            currentChatHistory = [];
            document.getElementById('chat-history').innerHTML = '<div style="text-align:center; color:#888;">AI 레드팀과 대화를 시작하세요.</div>';
            document.getElementById('chat-input').value = '';
        }
        
        function closeSecretPanel() {
            document.getElementById('secret-panel').classList.remove('open');
        }

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
            msgDiv.innerHTML = content.replace(/\n/g, '<br>');
            
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
            const prevText = currentChapter > 0 ? bookData.pages[currentChapter-1].text : '';
            const nextText = currentChapter < bookData.pages.length - 1 ? bookData.pages[currentChapter+1].text : '';
            
            const saveBtn = document.querySelector('.btn-save');
            const oldSaveText = saveBtn.innerText;
            saveBtn.innerText = 'AI가 재작성 중...';
            saveBtn.disabled = true;
            
            try {
                const response = await fetch('/api/apply_revision', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        page_index: currentChapter, 
                        original_text: originalText,
                        chat_history: currentChatHistory,
                        prev_text: prevText || '',
                        next_text: nextText || ''
                    })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    // Update local object and re-render
                    bookData.pages[currentChapter].text = result.revised_text;
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
                                page_index: currentChapter,
                                image_data: base64Data,
                                image_layout: layout
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {
                            const activePage = bookData.pages[currentChapter];
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
            const activePage = bookData.pages[currentChapter];
            if(activePage.type !== layout) {
                // If we need to just save the type change (requires backend endpoint, but for now we just change it locally. To save permanently, we'd need a save_layout API. Let's just alert.)
                alert("레이아웃만 변경하는 기능은 새 이미지를 업로드할 때 함께 반영되거나, 원고 수정 시 반영됩니다.");
                activePage.type = layout;
                renderBook();
            }
        });

        // Init
        
        // TOC Logic
        const tocBtn = document.querySelector('.toc-btn');
        const tocModal = document.querySelector('.toc-modal');
        const tocOverlay = document.querySelector('.toc-overlay');
        const closeTocBtn = document.querySelector('.close-toc-btn');
        const tocList = document.getElementById('toc-list');
        
        function populateTOC() {
            if(!tocList) return;
            tocList.innerHTML = '';
            bookData.pages.forEach((page, index) => {
                if (page.title && page.title.trim() !== "") {
                    const item = document.createElement('div');
                    item.className = 'toc-item';
                    item.textContent = page.title;
                    item.addEventListener('click', () => {
                        currentChapter = index;
                        currentColumn = 0;
                        updateControls();
                        closeTOC();
                    });
                    tocList.appendChild(item);
                }
            });
        }
        
        function openTOC() {
            populateTOC();
            if(tocModal) tocModal.classList.add('active');
            if(tocOverlay) tocOverlay.classList.add('active');
        }
        
        function closeTOC() {
            if(tocModal) tocModal.classList.remove('active');
            if(tocOverlay) tocOverlay.classList.remove('active');
        }
        
        if(tocBtn) tocBtn.addEventListener('click', openTOC);
        if(closeTocBtn) closeTocBtn.addEventListener('click', closeTOC);
        if(tocOverlay) tocOverlay.addEventListener('click', closeTOC);

        window.onload = renderBook;
