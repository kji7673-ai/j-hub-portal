import re

html_path = "book_studio.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS for .page-content
css_update = """
        .page-content {
            flex: 1;
            padding: 10% 12% 15% 12%; 
            display: block;
            opacity: 0;
            transition: opacity 0.3s ease;
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            overflow-y: hidden;
            overflow-x: hidden;
            column-width: 100vw; /* Force single column per viewport */
            column-gap: 24vw; /* Huge gap so next column is completely out of view */
            column-fill: auto;
            height: 100%;
            box-sizing: border-box;
            scroll-behavior: smooth;
        }
        
        .page-content > * {
            break-inside: avoid;
        }
        
        .page-content p {
            break-inside: auto; /* Allow paragraphs to break across columns */
        }
"""

html = re.sub(r'\.page-content\s*\{[^}]+\}', css_update.strip(), html)

# 2. Update nextPage() and prevPage()
js_update = """
        function updatePageNum() {
            document.getElementById('page-num').innerText = (currentPage + 1) + ' / ' + bookData.pages.length;
        }

        function nextPage() {
            const activePage = document.querySelector('.page-content.active');
            if (activePage && Math.ceil(activePage.scrollLeft + activePage.clientWidth) < activePage.scrollWidth) {
                activePage.scrollBy({ left: activePage.clientWidth + (window.innerWidth * 0.24), behavior: 'smooth' });
            } else if (currentPage < bookData.pages.length - 1) {
                currentPage++;
                renderBook();
                updatePageNum();
            }
        }

        function prevPage() {
            const activePage = document.querySelector('.page-content.active');
            if (activePage && activePage.scrollLeft > 0) {
                activePage.scrollBy({ left: -(activePage.clientWidth + (window.innerWidth * 0.24)), behavior: 'smooth' });
            } else if (currentPage > 0) {
                currentPage--;
                renderBook();
                updatePageNum();
                
                // If we went back, we should ideally jump to the last column of the previous page,
                // but for simplicity, we start at the beginning of the previous page.
            }
        }
"""

html = re.sub(r'function nextPage\(\)\s*\{[\s\S]*?\}\s*function prevPage\(\)\s*\{[\s\S]*?\}', js_update.strip(), html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
