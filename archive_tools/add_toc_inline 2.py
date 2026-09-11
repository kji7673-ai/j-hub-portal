import re
import sys

html_path = "book_studio.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add TOC CSS
toc_css = """
        /* TOC Styles */
        .toc-modal {
            position: fixed;
            top: 0;
            right: -320px;
            width: 300px;
            height: 100vh;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: -5px 0 30px rgba(0,0,0,0.1);
            z-index: 2000;
            transition: right 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            border-left: 1px solid var(--hairline);
        }
        .toc-modal.active {
            right: 0;
        }
        .toc-header {
            padding: 24px;
            border-bottom: 1px solid var(--hairline);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .toc-header h2 {
            font-size: 21px; /* tagline size */
            font-family: var(--font-display);
            font-weight: 600;
            letter-spacing: 0.231px;
            margin: 0;
            color: var(--ink);
        }
        .toc-list {
            padding: 16px;
            overflow-y: auto;
            flex: 1;
        }
        .toc-item {
            padding: 12px 16px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-family: var(--font-body);
            color: var(--ink-muted-80, #333333);
            transition: all 0.2s;
            line-height: 1.4;
        }
        .toc-item:hover {
            background: var(--canvas-parchment);
            color: var(--primary);
        }
        .toc-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0,0,0,0.2);
            z-index: 1999;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.4s ease;
        }
        .toc-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
"""
if ".toc-modal" not in html:
    html = html.replace('</style>', toc_css + '\n    </style>')

# Add TOC Button to floating controls
toc_btn_html = """
        <button class="icon-btn toc-btn" title="목차 보기">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>"""
if "toc-btn" not in html:
    html = html.replace('<div class="floating-controls">', '<div class="floating-controls">\n' + toc_btn_html)

# Add TOC Modal before closing body
toc_modal_html = """
    <!-- TOC Modal -->
    <div class="toc-modal">
        <div class="toc-header">
            <h2>목차</h2>
            <button class="icon-btn close-toc-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
        </div>
        <div class="toc-list" id="toc-list">
            <!-- Dynamically populated -->
        </div>
    </div>
    <div class="toc-overlay"></div>
"""
if "toc-modal" not in html:
    html = html.replace('</body>', toc_modal_html + '\n</body>')

# Add JS logic for TOC
toc_js = """
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
                        currentPageIndex = index;
                        updateLayout(currentPageIndex);
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
"""
if "populateTOC" not in html:
    html = html.replace('// Keyboard Navigation', toc_js + '\n        // Keyboard Navigation')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("TOC implemented successfully in book_studio.html.")
