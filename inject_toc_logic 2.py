import re

html_path = "book_studio.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

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
                        currentPage = index;
                        renderBook();
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

if "function populateTOC()" not in html:
    # Insert before window.onload = renderBook;
    html = html.replace("window.onload = renderBook;", toc_js + "\n        window.onload = renderBook;")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
