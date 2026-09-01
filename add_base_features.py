import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First, ensure we haven't already added this
if 'bookmark-toggle-btn' in html:
    print("Already added")
    exit(0)

injection = """
    <!-- Bookmark & Feedback Floating Action Buttons -->
    <div style="position: fixed; top: 70px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 8px;">
        <button id="bookmark-toggle-btn" class="floating-btn" onclick="toggleBookmark()">🔖 책갈피 추가</button>
        <button class="floating-btn" onclick="openBookmarkList()">📑 목록</button>
        <button class="floating-btn" onclick="openFeedbackModal()">📝 소감 보내기</button>
    </div>

    <!-- Modals -->
    <style>
        .floating-btn {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #ddd;
            padding: 10px 14px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            color: #333;
            font-family: inherit;
            transition: all 0.2s;
            backdrop-filter: blur(5px);
            font-weight: 600;
        }
        .floating-btn:hover { background: #f0f0f0; }
        
        .bookmark-modal, .feedback-modal {
            display: none;
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.5); z-index: 10000;
            justify-content: center; align-items: center;
            backdrop-filter: blur(2px);
        }
        .modal-content-box {
            background: #fff; width: 400px; max-width: 90%;
            border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .modal-content-box h3 { margin-top: 0; color: #1d1d1f; }
        .bookmark-list-item {
            padding: 12px 10px; border-bottom: 1px solid #eee; cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
            color: #0066cc; font-weight: 600;
        }
        .bookmark-list-item:hover { background: #f9f9f9; }
        
        /* Optional: Hide buttons on print */
        @media print {
            .floating-btn { display: none !important; }
        }
    </style>

    <div id="bookmark-modal" class="bookmark-modal" onclick="if(event.target===this) this.style.display='none'">
        <div class="modal-content-box">
            <h3>📑 내 책갈피</h3>
            <div id="bookmark-list-container" style="max-height: 300px; overflow-y: auto; margin-bottom: 15px;"></div>
            <div style="text-align:right;">
                <button class="floating-btn" onclick="document.getElementById('bookmark-modal').style.display='none'">닫기</button>
            </div>
        </div>
    </div>

    <div id="feedback-modal" class="feedback-modal" onclick="if(event.target===this) this.style.display='none'">
        <div class="modal-content-box">
            <h3>📝 소감 보내기</h3>
            <p style="font-size:13px; color:#666; margin-bottom: 15px;">작가에게 책을 읽은 소감이나 피드백을 전달해 주세요!</p>
            <textarea id="feedback-text" style="width:100%; height:120px; box-sizing:border-box; padding:12px; border:1px solid #ddd; border-radius:8px; resize:none; font-family:inherit; margin-bottom:15px; font-size:14px;" placeholder="여기에 소감을 작성해 주세요..."></textarea>
            <div style="display:flex; justify-content:space-between;">
                <button class="floating-btn" onclick="document.getElementById('feedback-modal').style.display='none'">취소</button>
                <button class="floating-btn" style="background:#0066cc; color:#fff; border:none;" onclick="sendFeedbackEmail()">메일 앱으로 전송</button>
            </div>
        </div>
    </div>

    <!-- Resume Prompt Modal -->
    <div id="resume-modal" class="bookmark-modal">
        <div class="modal-content-box" style="text-align:center;">
            <h3>📖 이어서 읽기</h3>
            <p style="font-size:14px; color:#666; margin-bottom: 20px;">이전에 읽던 페이지가 있습니다. 이어서 보시겠습니까?</p>
            <div style="display:flex; justify-content:center; gap:10px;">
                <button class="floating-btn" onclick="document.getElementById('resume-modal').style.display='none'">아니오, 처음부터</button>
                <button class="floating-btn" style="background:#0066cc; color:#fff; border:none;" onclick="resumeReading()">네, 이어서 보기</button>
            </div>
        </div>
    </div>

    <script>
        // Feature: Auto Resume & Bookmark & Feedback
        (function() {
            const currentPath = window.location.pathname;
            const currentFile = currentPath.split('/').pop() || 'index.html';
            const pageTitle = document.title;
            
            // 1. Auto Resume Logic
            // Save current position if it's a content page (not index)
            if (currentFile !== 'index.html' && currentFile !== '') {
                localStorage.setItem('JJournal_lastUrl', currentFile);
                
                // Save scroll periodically or on scroll
                let scrollTimeout;
                window.addEventListener('scroll', () => {
                    clearTimeout(scrollTimeout);
                    scrollTimeout = setTimeout(() => {
                        localStorage.setItem('JJournal_lastScroll', window.scrollY);
                    }, 200);
                });
                
                // Restore scroll if we just loaded this page
                window.addEventListener('load', () => {
                    const savedScroll = localStorage.getItem('JJournal_lastScroll');
                    if (savedScroll) {
                        window.scrollTo({ top: parseInt(savedScroll, 10), behavior: 'smooth' });
                    }
                    updateBookmarkButton();
                });
            } else {
                // If on index.html, check if there's a saved resume point
                window.addEventListener('load', () => {
                    const lastUrl = localStorage.getItem('JJournal_lastUrl');
                    if (lastUrl && lastUrl !== 'index.html') {
                        document.getElementById('resume-modal').style.display = 'flex';
                    }
                });
            }

            window.resumeReading = function() {
                const lastUrl = localStorage.getItem('JJournal_lastUrl');
                if (lastUrl) {
                    window.location.href = lastUrl;
                }
            };

            // 2. Bookmark Logic
            let bookmarks = JSON.parse(localStorage.getItem('JJournal_pages_bookmarks') || '[]');

            window.toggleBookmark = function() {
                if (currentFile === 'index.html' || currentFile === '') {
                    alert('본문 페이지에서만 책갈피를 추가할 수 있습니다.');
                    return;
                }
                const idx = bookmarks.findIndex(b => b.url === currentFile);
                if (idx === -1) {
                    bookmarks.push({ url: currentFile, title: pageTitle, time: new Date().getTime() });
                    alert('현재 페이지를 책갈피에 추가했습니다.');
                } else {
                    bookmarks.splice(idx, 1);
                    alert('현재 페이지의 책갈피를 해제했습니다.');
                }
                localStorage.setItem('JJournal_pages_bookmarks', JSON.stringify(bookmarks));
                updateBookmarkButton();
            };

            window.updateBookmarkButton = function() {
                const btn = document.getElementById('bookmark-toggle-btn');
                if (btn) {
                    if (currentFile === 'index.html' || currentFile === '') {
                        btn.style.display = 'none';
                        return;
                    }
                    const isBookmarked = bookmarks.some(b => b.url === currentFile);
                    if(isBookmarked) {
                        btn.innerText = '🔖 책갈피 해제';
                        btn.style.background = '#e6f2ff';
                    } else {
                        btn.innerText = '🔖 책갈피 추가';
                        btn.style.background = 'rgba(255, 255, 255, 0.95)';
                    }
                }
            };

            window.openBookmarkList = function() {
                const container = document.getElementById('bookmark-list-container');
                container.innerHTML = '';
                bookmarks.sort((a, b) => a.time - b.time); // sort by time
                
                if(bookmarks.length === 0) {
                    container.innerHTML = '<p style="color:#999; text-align:center; padding:20px 0;">추가된 책갈피가 없습니다.</p>';
                } else {
                    bookmarks.forEach(b => {
                        const div = document.createElement('div');
                        div.className = 'bookmark-list-item';
                        // Clean up title (remove "- J-Hub Portal" if present)
                        const cleanTitle = b.title.replace(' - J-Hub Portal', '');
                        div.innerHTML = `<span>${cleanTitle}</span> <span>이동 ➔</span>`;
                        div.onclick = () => {
                            window.location.href = b.url;
                        };
                        container.appendChild(div);
                    });
                }
                document.getElementById('bookmark-modal').style.display = 'flex';
            };

            // 3. Feedback Logic
            window.openFeedbackModal = function() {
                document.getElementById('feedback-text').value = '';
                document.getElementById('feedback-modal').style.display = 'flex';
            };

            window.sendFeedbackEmail = function() {
                const text = document.getElementById('feedback-text').value;
                if(!text.trim()) {
                    alert('내용을 입력해주세요.');
                    return;
                }
                const subject = encodeURIComponent(`[독자 소감] ${pageTitle}`);
                const body = encodeURIComponent(text);
                const mailtoLink = `mailto:kji7673@gmail.com?subject=${subject}&body=${body}`;
                window.location.href = mailtoLink;
                document.getElementById('feedback-modal').style.display = 'none';
            };
        })();
    </script>
"""

html = html.replace('</body>', injection + '\n</body>')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Injected base features successfully.")
