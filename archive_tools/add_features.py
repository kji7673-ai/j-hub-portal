import re

with open('reader_index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_inject = """
        .floating-btn {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #ddd;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            color: #333;
            font-family: inherit;
            transition: all 0.2s;
            backdrop-filter: blur(5px);
        }
        .floating-btn:hover { background: #f0f0f0; }
        
        .bookmark-modal, .feedback-modal {
            display: none;
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.5); z-index: 1000;
            justify-content: center; align-items: center;
        }
        .modal-content-box {
            background: #fff; width: 400px; max-width: 90%;
            border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .modal-content-box h3 { margin-top: 0; }
        .bookmark-list-item {
            padding: 10px; border-bottom: 1px solid #eee; cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
        }
        .bookmark-list-item:hover { background: #f9f9f9; }
"""

html_inject = """
    <div style="position: fixed; top: 20px; right: 20px; z-index: 990; display: flex; gap: 8px;">
        <button id="bookmark-toggle-btn" class="floating-btn" onclick="toggleBookmark()">🔖 책갈피 추가</button>
        <button class="floating-btn" onclick="openBookmarkList()">📑 목록</button>
        <button class="floating-btn" onclick="openFeedbackModal()">📝 소감 보내기</button>
    </div>

    <!-- Bookmark List Modal -->
    <div id="bookmark-modal" class="bookmark-modal" onclick="if(event.target===this) this.style.display='none'">
        <div class="modal-content-box">
            <h3>📑 내 책갈피</h3>
            <div id="bookmark-list-container" style="max-height: 300px; overflow-y: auto; margin-bottom: 15px;"></div>
            <div style="text-align:right;">
                <button class="floating-btn" onclick="document.getElementById('bookmark-modal').style.display='none'">닫기</button>
            </div>
        </div>
    </div>

    <!-- Feedback Modal -->
    <div id="feedback-modal" class="feedback-modal" onclick="if(event.target===this) this.style.display='none'">
        <div class="modal-content-box">
            <h3>📝 소감 보내기</h3>
            <p style="font-size:13px; color:#666;">작가에게 책을 읽은 소감이나 피드백을 전달해 주세요!</p>
            <textarea id="feedback-text" style="width:100%; height:120px; box-sizing:border-box; padding:10px; border:1px solid #ddd; border-radius:8px; resize:none; font-family:inherit; margin-bottom:15px;" placeholder="여기에 소감을 작성해 주세요..."></textarea>
            <div style="display:flex; justify-content:space-between;">
                <button class="floating-btn" onclick="document.getElementById('feedback-modal').style.display='none'">취소</button>
                <button class="floating-btn" style="background:#0066cc; color:#fff; border:none;" onclick="sendFeedbackEmail()">메일 앱으로 전송</button>
            </div>
        </div>
    </div>
"""

js_inject = """
        // Bookmark Features
        let bookmarks = JSON.parse(localStorage.getItem('JJournal_bookmarks') || '[]');

        function toggleBookmark() {
            const idx = bookmarks.indexOf(currentPage);
            if (idx === -1) {
                bookmarks.push(currentPage);
                bookmarks.sort((a,b) => a - b);
                alert('현재 페이지를 책갈피에 추가했습니다.');
            } else {
                bookmarks.splice(idx, 1);
                alert('현재 페이지의 책갈피를 해제했습니다.');
            }
            localStorage.setItem('JJournal_bookmarks', JSON.stringify(bookmarks));
            updateBookmarkButton();
        }

        function updateBookmarkButton() {
            const btn = document.getElementById('bookmark-toggle-btn');
            if(btn) {
                if(bookmarks.includes(currentPage)) {
                    btn.innerText = '🔖 책갈피 해제';
                    btn.style.background = '#e6f2ff';
                } else {
                    btn.innerText = '🔖 책갈피 추가';
                    btn.style.background = 'rgba(255, 255, 255, 0.9)';
                }
            }
        }

        function openBookmarkList() {
            const container = document.getElementById('bookmark-list-container');
            container.innerHTML = '';
            if(bookmarks.length === 0) {
                container.innerHTML = '<p style="color:#999; text-align:center; padding:20px 0;">추가된 책갈피가 없습니다.</p>';
            } else {
                bookmarks.forEach(pageIndex => {
                    const title = bookData.pages[pageIndex].title || `페이지 ${pageIndex + 1}`;
                    const div = document.createElement('div');
                    div.className = 'bookmark-list-item';
                    div.innerHTML = `<span>${title}</span> <span>이동 ➔</span>`;
                    div.onclick = () => {
                        currentPage = pageIndex;
                        localStorage.setItem('JJournal_savedScrollTop', 0);
                        const activeEl = document.querySelectorAll('.page-content')[currentPage];
                        if (activeEl) activeEl.scrollTop = 0;
                        updateControls();
                        document.getElementById('bookmark-modal').style.display = 'none';
                    };
                    container.appendChild(div);
                });
            }
            document.getElementById('bookmark-modal').style.display = 'flex';
        }

        // Feedback Feature
        function openFeedbackModal() {
            document.getElementById('feedback-text').value = '';
            document.getElementById('feedback-modal').style.display = 'flex';
        }

        function sendFeedbackEmail() {
            const text = document.getElementById('feedback-text').value;
            if(!text.trim()) {
                alert('내용을 입력해주세요.');
                return;
            }
            const subject = encodeURIComponent('[독자 소감] 기획서는 곧 건축가의 얼굴이다');
            const body = encodeURIComponent(text);
            const mailtoLink = `mailto:kji7673@gmail.com?subject=${subject}&body=${body}`;
            window.location.href = mailtoLink;
            document.getElementById('feedback-modal').style.display = 'none';
        }
"""

html = html.replace('</style>', css_inject + '\n    </style>')
html = html.replace('<div id="book-container"', html_inject + '\n    <div id="book-container"')

# Inject js before the closing </script> tag
# First find the last </script>
parts = html.rsplit('</script>', 1)
html = parts[0] + js_inject + '\n    </script>' + parts[1]

# Make sure updateBookmarkButton is called in updateControls
update_controls_str = 'localStorage.setItem(\'JJournal_savedPage\', currentPage);'
if update_controls_str in html:
    html = html.replace(update_controls_str, update_controls_str + '\n            if(typeof updateBookmarkButton === "function") updateBookmarkButton();')

with open('reader_index.html', 'w', encoding='utf-8') as f:
    f.write(html)
