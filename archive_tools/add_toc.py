import os
import re

html_path = "book_studio.html"
css_path = "style.css"

# 1. Update HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add TOC Button to floating controls
toc_btn_html = """
        <button class="icon-btn toc-btn" title="목차 보기">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>"""
if "toc-btn" not in html:
    html = html.replace('<div class="floating-controls">', '<div class="floating-controls">\n' + toc_btn_html)

# Add TOC Modal
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

# Add JS for TOC
toc_js = """
        // TOC Logic
        const tocBtn = document.querySelector('.toc-btn');
        const tocModal = document.querySelector('.toc-modal');
        const tocOverlay = document.querySelector('.toc-overlay');
        const closeTocBtn = document.querySelector('.close-toc-btn');
        const tocList = document.getElementById('toc-list');
        
        function populateTOC() {
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
            tocModal.classList.add('active');
            tocOverlay.classList.add('active');
        }
        
        function closeTOC() {
            tocModal.classList.remove('active');
            tocOverlay.classList.remove('active');
        }
        
        if(tocBtn) tocBtn.addEventListener('click', openTOC);
        if(closeTocBtn) closeTocBtn.addEventListener('click', closeTOC);
        if(tocOverlay) tocOverlay.addEventListener('click', closeTOC);
"""
if "populateTOC" not in html:
    html = html.replace('// Keyboard Navigation', toc_js + '\n        // Keyboard Navigation')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update CSS
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

toc_css = """
/* TOC Styles */
.toc-modal {
    position: fixed;
    top: 0;
    right: -350px;
    width: 320px;
    height: 100vh;
    background: var(--surface);
    box-shadow: -5px 0 30px rgba(0,0,0,0.1);
    z-index: 2000;
    transition: right 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    flex-direction: column;
}
.toc-modal.active {
    right: 0;
}
.toc-header {
    padding: 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.toc-header h2 {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0;
    color: var(--text-main);
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
    font-size: 0.95rem;
    color: var(--text-muted);
    transition: all 0.2s;
    line-height: 1.4;
}
.toc-item:hover {
    background: var(--bg-color);
    color: var(--accent);
}
.toc-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.4);
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

if "toc-modal" not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write("\n" + toc_css)

print("TOC implemented successfully.")
