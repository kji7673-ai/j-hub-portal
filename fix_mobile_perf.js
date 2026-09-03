const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// I will write a regex to replace the entire <script> ... </script> block except the beginning.
// Actually, it's easier to just find `function renderBook()` and replace the relevant parts.

let newScript = `
        function renderTOC() {
            const tocList = document.getElementById('toc-list');
            if(!tocList) return;
            tocList.innerHTML = '';
            let currentCategory = null;

            bookData.pages.forEach((page, index) => {
                if (page.type === "author_profile") return;
                if (page.title && page.title.trim() !== "" && !page.title.includes("(계속)")) {
                    let cat = page.partCategory || "프롤로그";
                    if (cat !== currentCategory) {
                        currentCategory = cat;
                        const catHeader = document.createElement('div');
                        catHeader.className = 'toc-category';
                        catHeader.innerText = cat;
                        tocList.appendChild(catHeader);
                    }
                    
                    const li = document.createElement('li');
                    li.className = 'toc-item';
                    li.innerHTML = '<span class="toc-title">' + page.title + '</span>';
                    li.onclick = () => {
                        currentChapter = index;
                        currentColumn = 0;
                        renderCurrentChapter();
                        document.getElementById('toc-modal').style.display = 'none';
                    };
                    tocList.appendChild(li);
                }
            });
        }

        function renderCurrentChapter() {
            const container = document.getElementById('book-container');
            // Keep the controls div intact
            const controls = document.querySelector('.controls');
            
            // Remove all existing page-content
            document.querySelectorAll('.page-content').forEach(p => p.remove());

            const page = bookData.pages[currentChapter];
            if(!page) return;

            const pageEl = document.createElement('div');
            pageEl.className = 'page-content active';
            pageEl.id = 'page-' + currentChapter;
            
            let contentHTML = '';
            
            if (page.type === 'cover' || page.type === 'interlude') {
                pageEl.style.backgroundColor = '#ffffff';
                pageEl.style.color = '#1d1d1f';
                pageEl.style.padding = '0';
                let rawTitle = page.title || "";
                let pText = page.text || "";
                let bgStyle = page.image ? 'background: url('+page.image+') center center / cover no-repeat;' : 'background: #f5f5f7;';
                
                contentHTML += '<div class="cover-content" style="position:relative; z-index:2; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">';
                if(page.type === 'cover' && page.image) {
                    contentHTML += '<div style="position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(255,255,255,0.7); z-index:-1;"></div>';
                }
                contentHTML += '<h1 style="font-size:2.5em; font-weight:800; margin-bottom:20px; letter-spacing:-0.5px; line-height:1.2;">' + rawTitle + '</h1>';
                if(pText) contentHTML += '<p style="font-size:1.2em; font-weight:400; color:#555; max-width:80%; line-height:1.6;">' + pText + '</p>';
                contentHTML += '</div>';
                pageEl.innerHTML = contentHTML;
            }
            else {
                pageEl.className += ' page-text-flow page-layout';
                if(page.image) contentHTML += '<div class="image-container" id="img-container-'+currentChapter+'" style="max-width: 800px; width: 90%; margin-bottom: 45px;"><img src="'+page.image+'" alt="sketch"></div>';
                if(page.title) contentHTML += '<h2 class="chapter-title" style="margin-bottom:20px;">' + page.title + '</h2>';
                if(page.text) {
                    let formattedText = page.text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                    formattedText = formattedText.replace(/!\\[(.*?)\\]\\((.*?)\\)/g, '<img src="$2" alt="$1" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">');
                    const paragraphs = formattedText.split('\\n\\n');
                    paragraphs.forEach(p => {
                        const trimmed = p.trim();
                        if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                            contentHTML += '<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">' + p + '</div>';
                        } else if (trimmed.startsWith('<h') || trimmed.startsWith('<ul') || trimmed.startsWith('<ol') || trimmed.startsWith('<div')) {
                            contentHTML += trimmed;
                        } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                            let bqText = trimmed.replace(/^&gt;\\s?/gm, '').replace(/^>\\s?/gm, '');
                            bqText = bqText.replace(/\\n/g, '<br>');
                            contentHTML += '<blockquote class="pull-quote">' + bqText + '</blockquote>';
                        } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                            contentHTML += '<p class="subheading">' + trimmed + '</p>';
                        } else {
                            let htmlP = p.replace(/\\n(?=\\d+\\.\\s)/g, '<br><br>');
                            htmlP = htmlP.replace(/\\n/g, '<br>');
                            contentHTML += '<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">' + htmlP + '</p>';
                        }
                    });
                }
                pageEl.innerHTML = '<div class="page-inner">' + contentHTML + '</div>';
            }
            
            // Insert before controls
            container.insertBefore(pageEl, controls);
            
            // Reset scroll position to top whenever a new chapter is loaded
            pageEl.scrollTop = 0;

            updateControls();
        }

        function renderBook() {
            renderTOC();
            
            // Restore position if possible
            const savedChapter = localStorage.getItem('JJournal_savedChapter');
            if (savedChapter !== null) {
                const parsedChap = parseInt(savedChapter, 10);
                if(!isNaN(parsedChap)) {
                    currentChapter = Math.max(0, Math.min(parsedChap, bookData.pages.length - 1));
                }
            }
            
            renderCurrentChapter();
            updateBookmarkButton();
        }

        function updateControls() {
            const totalChapters = bookData.pages.length;
            document.getElementById('prev-btn').disabled = (currentChapter === 0);
            document.getElementById('next-btn').disabled = (currentChapter === totalChapters - 1);
            
            // Since we abandoned multi-column horizontal pagination in favor of vertical scrolling, 
            // currentColumn is basically obsolete, but we keep the UI simple:
            document.getElementById('page-num').innerText = '[' + (currentChapter + 1) + ' / ' + totalChapters + ']';
            
            if(typeof saveProgress === 'function') saveProgress();
        }

        function prevPage() {
            if (currentChapter > 0) {
                currentChapter--;
                currentColumn = 0;
                renderCurrentChapter();
            }
        }

        function nextPage() {
            if (currentChapter < bookData.pages.length - 1) {
                currentChapter++;
                currentColumn = 0;
                renderCurrentChapter();
            }
        }
`;

// Now we need to replace the old functions in index.html with these new ones.
// We can use a regex to match from `function renderBook() {` down to the end of `function nextPage() { ... }` 
// But a safer way is to just inject our new script and comment out the old one, or use substring replacement.

const startIndex = html.indexOf('function renderBook() {');
const endIndex = html.indexOf('function getChapterMaxColumns(chapterIndex)'); 
// wait, the file has getChapterMaxColumns and then updateControls, prevPage, nextPage.
const endOfNextPage = html.indexOf('function prevPage()');
const endOfNextPageFunc = html.indexOf('}', html.indexOf('function nextPage() {')) + 1;

if (startIndex !== -1 && endOfNextPageFunc !== -1) {
    let before = html.substring(0, startIndex);
    // Find the end of nextPage
    // Let's just find "function openBookmarkList()" which comes after prevPage/nextPage.
    const bookmarkFuncIndex = html.indexOf('function toggleBookmark()');
    let after = html.substring(bookmarkFuncIndex);
    
    // Write the new JS
    html = before + newScript + "\n\n        " + after;
    fs.writeFileSync('index.html', html, 'utf8');
    console.log("Successfully replaced rendering logic for mobile performance.");
} else {
    console.log("Failed to find injection points.");
}
