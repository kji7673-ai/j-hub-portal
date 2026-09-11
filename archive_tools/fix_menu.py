import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

menu_html = """
    <!-- Bookmark & Feedback Floating Action Buttons -->
    <div style="position: fixed; top: 80px; right: 20px; z-index: 1500; display: flex; flex-direction: column; gap: 10px; align-items: flex-end;">
        <button id="floating-menu-toggle" onclick="toggleFloatingMenu()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:50%; width:44px; height:44px; box-shadow:0 4px 12px rgba(0,0,0,0.15); cursor:pointer; font-size:20px; color:#333; display:flex; justify-content:center; align-items:center; transition:all 0.2s;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
        <div id="floating-menu-items" style="display: none; flex-direction: column; gap: 10px; align-items: flex-end;">
            <button id="bookmark-toggle-btn" class="floating-btn" onclick="toggleBookmark(); toggleFloatingMenu();" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">🔖 책갈피 추가</button>
            <button class="floating-btn" onclick="openBookmarkList(); toggleFloatingMenu();" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">📑 목록</button>
            <button class="floating-btn" onclick="openFeedbackModal(); toggleFloatingMenu();" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">📝 소감 보내기</button>
        </div>
    </div>
"""

old_menu = """    <!-- Bookmark & Feedback Floating Action Buttons -->
    <div style="position: fixed; top: 80px; right: 20px; z-index: 1500; display: flex; flex-direction: column; gap: 10px;">
        <button id="bookmark-toggle-btn" class="floating-btn" onclick="toggleBookmark()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">🔖 책갈피 추가</button>
        <button class="floating-btn" onclick="openBookmarkList()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">📑 목록</button>
        <button class="floating-btn" onclick="openFeedbackModal()" style="background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:20px; padding:8px 12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; font-size:13px; font-weight:600; color:#333; transition:all 0.2s;">📝 소감 보내기</button>
    </div>"""

html = html.replace(old_menu, menu_html)

js_code = """
        function toggleFloatingMenu() {
            const menu = document.getElementById('floating-menu-items');
            if (menu.style.display === 'none') {
                menu.style.display = 'flex';
            } else {
                menu.style.display = 'none';
            }
        }
"""

html = html.replace("function toggleBookmark() {", js_code + "\n        function toggleBookmark() {")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
