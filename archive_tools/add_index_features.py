import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First check if we already added it
if 'bookmark-toggle-btn' in html:
    print("Already added to index.html")
    exit(0)

# We want to add the floating buttons next to the toc-btn or just below it.
# toc-btn is at top:20px; right:20px;
# So we can put our new buttons at top: 80px; right: 20px;

html_inject = """
    <!-- Bookmark & Feedback Floating Action Buttons -->
    <div style="position: fixed; top: 80px; right: 20px; z-index: 1500; display: flex; flex-direction: column; gap: 10px;">
        <button id="bookmark-toggle-btn" class="floating-btn" onclick="toggleBookmark()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">🔖 책갈피 추가</button>
        <button class="floating-btn" onclick="openBookmarkList()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">📑 목록</button>
        <button class="floating-btn" onclick="openFeedbackModal()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">📝 소감 보내기</button>
    </div>

    <!-- Modals -->
    <style>
        .floating-btn:hover { background: #f0f0f0 !important; }
        .bookmark-modal, .feedback-modal {
            display: none;
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.5); z-index: 2000;
            justify-content: center; align-items: center;
            backdrop-filter: blur(2px);
        }
        .modal-content-box {
            background: #fff; width: 400px; max-width: 90%;
            border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .modal-content-box h3 { margin-top: 0; color: #1d1d1f; font-size: 18px; margin-bottom: 12px; }
        .bookmark-list-item {
            padding: 12px 10px; border-bottom: 1px solid #eee; cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
            color: #0066cc; font-weight: 600; font-size: 14px;
        }
        .bookmark-list-item:hover { background: #f9f9f9; }
    </style>

    <div id="bookmark-modal" class="bookmark-modal" onclick="if(event.target===this) this.style.display='none'">
        <div class="modal-content-box">
            <h3>📑 내 책갈피</h3>
            <div id="bookmark-list-container" style="max-height: 300px; overflow-y: auto; margin-bottom: 15px;"></div>
            <div style="text-align:right;">
                <button class="floating-btn" onclick="document.getElementById('bookmark-modal').style.display='none'" style="background:rgba(255,255,255,0.9); border:1px solid #e0e0e0; border-radius:20px; padding:8px 16px; cursor:pointer;">닫기</button>
            </div>
        </div>
    </div>

    <div id="feedback-modal" class="feedback-modal" onclick="if(event.target===this) this.style.display='none'">
        <div class="modal-content-box">
            <h3>📝 소감 보내기</h3>
            <p style="font-size:13px; color:#666; margin-bottom: 15px;">작가에게 책을 읽은 소감이나 피드백을 전달해 주세요!</p>
            <textarea id="feedback-text" style="width:100%; height:120px; box-sizing:border-box; padding:12px; border:1px solid #ddd; border-radius:8px; resize:none; font-family:inherit; margin-bottom:15px; font-size:14px;" placeholder="여기에 소감을 작성해 주세요..."></textarea>
            <div style="display:flex; justify-content:space-between;">
                <button class="floating-btn" onclick="document.getElementById('feedback-modal').style.display='none'" style="background:rgba(255,255,255,0.9); border:1px solid #e0e0e0; border-radius:20px; padding:8px 16px; cursor:pointer;">취소</button>
                <button class="floating-btn" style="background:#0066cc; color:#fff; border:none; border-radius:20px; padding:8px 16px; cursor:pointer;" onclick="sendFeedbackEmail()">메일 앱으로 전송</button>
            </div>
        </div>
    </div>
"""

js_inject = """
        // Bookmark & Auto Resume Features for index.html
        let bookmarks = JSON.parse(localStorage.getItem('JJournal_bookmarks_v2') || '[]');
        
        // Restore progress on load
        window.addEventListener('DOMContentLoaded', () => {
            const savedChapter = localStorage.getItem('JJournal_savedChapter');
            const savedColumn = localStorage.getItem('JJournal_savedColumn');
            if (savedChapter !== null && savedColumn !== null) {
                currentChapter = parseInt(savedChapter, 10);
                currentColumn = parseInt(savedColumn, 10);
            }
            updateBookmarkButton();
        });

        function saveProgress() {
            localStorage.setItem('JJournal_savedChapter', currentChapter);
            localStorage.setItem('JJournal_savedColumn', currentColumn);
            updateBookmarkButton();
        }

        function toggleBookmark() {
            const chapterData = bookData.pages[currentChapter];
            if (!chapterData) return;
            
            // Generate a unique ID for this position
            const posId = currentChapter + '-' + currentColumn;
            const idx = bookmarks.findIndex(b => b.id === posId);
            
            if (idx === -1) {
                // Determine title snippet
                let titleSnippet = chapterData.title || '페이지 ' + (currentChapter+1);
                bookmarks.push({ 
                    id: posId, 
                    chapter: currentChapter, 
                    column: currentColumn, 
                    title: titleSnippet, 
                    time: new Date().getTime() 
                });
                alert('현재 페이지를 책갈피에 추가했습니다.');
            } else {
                bookmarks.splice(idx, 1);
                alert('현재 페이지의 책갈피를 해제했습니다.');
            }
            localStorage.setItem('JJournal_bookmarks_v2', JSON.stringify(bookmarks));
            updateBookmarkButton();
        }

        function updateBookmarkButton() {
            const btn = document.getElementById('bookmark-toggle-btn');
            if (btn) {
                const posId = currentChapter + '-' + currentColumn;
                const isBookmarked = bookmarks.some(b => b.id === posId);
                if(isBookmarked) {
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
            bookmarks.sort((a, b) => a.time - b.time); // sort by time
            
            if(bookmarks.length === 0) {
                container.innerHTML = '<p style="color:#999; text-align:center; padding:20px 0;">추가된 책갈피가 없습니다.</p>';
            } else {
                bookmarks.forEach(b => {
                    const div = document.createElement('div');
                    div.className = 'bookmark-list-item';
                    div.innerHTML = `<span>[${b.chapter + 1}장] ${b.title}</span> <span>이동 ➔</span>`;
                    div.onclick = () => {
                        currentChapter = b.chapter;
                        currentColumn = b.column;
                        updateControls();
                        document.getElementById('bookmark-modal').style.display = 'none';
                    };
                    container.appendChild(div);
                });
            }
            document.getElementById('bookmark-modal').style.display = 'flex';
        }

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
            const chapterTitle = bookData.pages[currentChapter]?.title || '';
            const subject = encodeURIComponent(`[독자 소감] 기획서는 곧 건축가의 얼굴이다 (${chapterTitle} 읽음)`);
            const body = encodeURIComponent(text);
            const mailtoLink = `mailto:kji7673@gmail.com?subject=${subject}&body=${body}`;
            window.location.href = mailtoLink;
            document.getElementById('feedback-modal').style.display = 'none';
        }
"""

html = html.replace('<body>', '<body>\n' + html_inject)

# Find updateControls and inject saveProgress() at the end
# It ends with:
# document.getElementById('page-num').innerText = `[${currentChapter + 1}/${totalChapters}] ${currentColumn + 1} / ${maxCols}`;
# }
update_pattern = r"(document\.getElementById\('page-num'\)\.innerText = `\[\$\{currentChapter \+ 1\}/\$\{totalChapters\}\] \$\{currentColumn \+ 1\} / \$\{maxCols\}`;.*?})"
html = re.sub(update_pattern, r"\1\n            if(typeof saveProgress === 'function') saveProgress();", html, flags=re.DOTALL)

# Inject JS before closing </script>
parts = html.rsplit('</script>', 1)
html = parts[0] + js_inject + '\n    </script>' + parts[1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Injected into index.html")
