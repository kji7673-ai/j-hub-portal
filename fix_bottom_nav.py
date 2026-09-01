import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove the hamburger menu
menu_regex = r'<!-- Bookmark & Feedback Floating Action Buttons -->.*?</div>\s*</div>'
html = re.sub(menu_regex, '', html, flags=re.DOTALL)

# Also remove the toggleFloatingMenu JS function
js_regex = r'function toggleFloatingMenu\(\)\s*\{.*?\}'
html = re.sub(js_regex, '', html, flags=re.DOTALL)

# Inject the new bottom navigation bar right before <!-- Modals -->
bottom_nav = """
    <!-- Bottom Floating Navigation Bar -->
    <style>
        .bottom-nav {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            background: rgba(250, 250, 252, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 9999px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            padding: 6px 8px;
            gap: 4px;
            z-index: 1500;
            border: 1px solid rgba(0,0,0,0.05);
        }
        .bottom-nav button {
            background: transparent;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            color: #1d1d1f;
            border-radius: 9999px;
            cursor: pointer;
            transition: background 0.2s;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        .bottom-nav button:hover, .bottom-nav button:active {
            background: rgba(0,0,0,0.08);
        }
        .bottom-nav button svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
            fill: none;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }
    </style>
    
    <div class="bottom-nav">
        <button onclick="toggleBookmark()" id="bookmark-toggle-btn">
            <svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"></path></svg>
            <span>책갈피</span>
        </button>
        <button onclick="openBookmarkList()">
            <svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
            <span>목록</span>
        </button>
        <button onclick="openFeedbackModal()">
            <svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"></path></svg>
            <span>소감</span>
        </button>
    </div>

    <!-- Modals -->"""

html = html.replace('<!-- Modals -->', bottom_nav)

# Fix JS toggle button state styling for the new button format
js_old = """
                    btn.innerText = '🔖 책갈피 해제';
                    btn.style.background = '#e6f2ff';
                } else {
                    btn.innerText = '🔖 책갈피 추가';
                    btn.style.background = 'rgba(255, 255, 255, 0.9)';
"""
js_new = """
                    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"></path></svg><span>해제</span>';
                    btn.style.color = '#0066cc';
                } else {
                    btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"></path></svg><span>책갈피</span>';
                    btn.style.color = '#1d1d1f';
"""
html = html.replace(js_old, js_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
