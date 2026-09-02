const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const startIndex = html.indexOf('function renderBook() {');
const endIndex = html.indexOf('function getChapterMaxColumns(');

if (startIndex === -1 || endIndex === -1) {
    console.error("Could not find renderBook or getChapterMaxColumns");
    process.exit(1);
}

const cleanRenderBook = `function renderBook() {
            const container = document.getElementById('book-container');
            const inner = document.getElementById('book-inner');
            const tocList = document.getElementById('toc-list');
            const isMobile = window.innerWidth <= 768;
            
            // Remove existing pages
            document.querySelectorAll('.page-content').forEach(p => p.remove());

            bookData.pages.forEach((page, index) => {
                const pageEl = document.createElement('div');
                pageEl.className = 'page-content';
                pageEl.id = 'page-' + index;
                
                let contentHTML = '';
                
                if (page.type === 'cover' || page.type === 'interlude') {
                    pageEl.style.backgroundColor = '#1d1d1f';
                    pageEl.style.color = '#ffffff';
                    pageEl.style.padding = '0';
                    let rawTitle = page.title || "";
                    let pText = page.text || "";
                    
                    pText = pText.replace(/<p style='(.*?)'>/g, "<p style='$1 text-shadow: 0 4px 15px rgba(0,0,0,0.8); color: rgba(255,255,255,0.9); font-weight: 300;'>");

                    if(page.image) {
                        contentHTML += \`<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; z-index:0; background:#ffffff; display:flex; justify-content:center; align-items:center; padding: 0; box-sizing: border-box;">
                            <img src="\${page.image}" alt="cover_image" style="width:100%; height:100%; object-fit:cover;">
                            <div style="position:absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(to bottom, rgba(29,29,31,0.2) 0%, rgba(29,29,31,0.8) 100%); z-index:1;"></div>
                        </div>\`;
                    }
                    
                    contentHTML += \`<div class="cover-content" style="position:relative; z-index:2; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">\`;
                    
                    if (rawTitle) {
                        contentHTML += \`<h2 style="font-family:'SF Pro Display', sans-serif; font-size:clamp(24px, 4.5vw, 32px); font-weight:700; color:#ffffff; margin-bottom: 30px; letter-spacing:1px; text-shadow: 0 4px 15px rgba(0,0,0,0.9); line-height: 1.4;">\${rawTitle}</h2>\`;
                    }
                    if (pText) {
                        contentHTML += \`<div style="font-family:'SF Pro Text', sans-serif; font-size:clamp(16px, 3.5vw, 18px); line-height:2.0; color:#ffffff; word-break:keep-all; max-width: 90%;">\${pText}</div>\`;
                    }
                    contentHTML += \`</div>\`;
                }
                else if (page.type === 'bridge') {
                    pageEl.style.backgroundColor = '#1d1d1f';
                    pageEl.style.color = '#ffffff';
                    pageEl.style.padding = '0';
                    let rawTitle = page.title || "";
                    let pText = page.text || "";
                    
                    pText = pText.replace(/<p style='(.*?)'>/g, "<p style='$1 text-shadow: 0 4px 15px rgba(0,0,0,0.8); color: rgba(255,255,255,0.9); font-weight: 300;'>");

                    contentHTML = \`
                    <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; width:100%; height:100%; padding:40px; box-sizing:border-box; text-align:center; background: radial-gradient(circle at center, #2a2a2c 0%, #1d1d1f 100%);">
                        <h2 style="font-family:'SF Pro Display', sans-serif; font-size:clamp(20px, 4vw, 24px); font-weight:600; color:rgba(255,255,255,0.5); margin-bottom: 40px; letter-spacing:2px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">\${rawTitle}</h2>
                        <div style="font-family:'SF Pro Text', sans-serif; font-size:clamp(16px, 3.5vw, 18px); line-height:2.0; color:#ffffff; word-break:keep-all; max-width: 90%;">
                            \${pText}
                        </div>
                    </div>\`;
                }
                else if (page.type === 'image_full') {
                    pageEl.style.padding = '0';
                    if(page.image) {
                        contentHTML += \`<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; padding:0; z-index:0; background:#ffffff;">
                            <img src="\${page.image}" alt="full_image" style="width:100%; height:100%; object-fit:cover;">
                            <div style="position:absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(to bottom, rgba(29,29,31,0.1) 0%, rgba(29,29,31,0.85) 100%); z-index:1;"></div>
                        </div>\`;
                    }
                    if(page.title || page.subtitle || page.text) {
                        let rawTitle = page.title || "";
                        let mainTitle = rawTitle;
                        let subtitle = page.subtitle || "";

                        contentHTML += \`<div style="position:relative; z-index:2; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 40px 20px; box-sizing:border-box;">\`;
                        
                        if (mainTitle || subtitle) {
                            contentHTML += \`<div style="display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 90%;">\`;
                            if(mainTitle) {
                                contentHTML += \`<h1 class="book-title" style="color:#ffffff; font-size:clamp(32px, 6vw, 56px); margin-bottom:20px; font-weight:800; letter-spacing: -0.03em; line-height: 1.2; word-break: keep-all; text-shadow: 0 4px 20px rgba(0,0,0,0.9);">\${mainTitle}</h1>\`;
                            }
                            if(subtitle) {
                                contentHTML += \`<p style="color:rgba(255,255,255,0.9); font-size:clamp(18px, 3vw, 24px); font-weight:500; word-break: keep-all; margin:0; text-shadow: 0 4px 15px rgba(0,0,0,0.8);">\${subtitle}</p>\`;
                            }
                            contentHTML += \`</div>\`;
                        }
                        
                        if(page.text) {
                            let formattedText = page.text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: #ffffff;">$1</strong>');
                            const paragraphs = formattedText.split('\\n\\n');
                            contentHTML += \`<div style="margin-top: 40px; width: 100%; max-width: 700px;">\`;
                            paragraphs.forEach(p => {
                                let htmlP = p.replace(/\\n(?=\\d+\\.\\s)/g, '<br><br>').replace(/\\n/g, '<br>');
                                contentHTML += \`<p class="body-text" style="color: rgba(255,255,255,0.9); font-weight: 400; text-align:center; font-size: 18px; line-height: 1.8; margin: 0 auto 15px auto; text-shadow: 0 2px 8px rgba(0,0,0,0.8);">\${htmlP}</p>\`;
                            });
                            contentHTML += \`</div>\`;
                        }
                        contentHTML += \`</div>\`;
                    }
                }
                else if (page.type === 'author_profile') {
                    contentHTML += \`<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">\`;
                    contentHTML += \`<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>\`;
                    contentHTML += \`<div style="background: var(--canvas-parchment, #ffffff); border-radius: 0; padding: 40px; box-shadow: none; border: none; width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">\`;
                    contentHTML += \`<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>\`;
                    contentHTML += \`<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>\`;
                    contentHTML += \`</div></div>\`;
                }
                else if (page.type === 'image_top') {
                    pageEl.className += ' page-text-flow page-layout';
                    if(page.image) contentHTML += \`<div class="image-container" id="img-container-\${index}" style="max-width: 800px; width: 90%; margin-bottom: 45px;"><img src="\${page.image}" alt="sketch"></div>\`;
                    if(page.title) contentHTML += \`<h2 class="chapter-title" style="margin-bottom:20px;">\${page.title}</h2>\`;
                    if(page.text) {
                        let formattedText = page.text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                        formattedText = formattedText.replace(/!\\[(.*?)\\]\\((.*?)\\)/g, '<img src="$2" alt="$1" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">');
                        const paragraphs = formattedText.split('\\n\\n');
                        paragraphs.forEach(p => {
                            const trimmed = p.trim();
                            if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                                contentHTML += \`<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">\${p}</div>\`;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                                let bqText = trimmed.replace(/^&gt;\\s?/gm, '').replace(/^>\\s?/gm, '');
                                bqText = bqText.replace(/\\n/g, '<br>');
                                contentHTML += \`<blockquote class="pull-quote">\${bqText}</blockquote>\`;
                            } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                                contentHTML += \`<p class="subheading">\${trimmed}</p>\`;
                            } else {
                                let htmlP = p.replace(/\\n(?=\\d+\\.\\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\\n/g, '<br>');
                                contentHTML += \`<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">\${htmlP}</p>\`;
                            }
                        });
                    }
                    contentHTML = \`<div class="page-inner">\${contentHTML}</div>\`;
                }
                else {
                    pageEl.className += ' page-text-flow page-layout';
                    if(page.title) contentHTML += \`<h2 class="chapter-title" style="margin-bottom:20px;">\${page.title}</h2>\`;
                    if(page.text) {
                        let formattedText = page.text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                        formattedText = formattedText.replace(/!\\[(.*?)\\]\\((.*?)\\)/g, '<img src="$2" alt="$1" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">');
                        const paragraphs = formattedText.split('\\n\\n');
                        paragraphs.forEach(p => {
                            const trimmed = p.trim();
                            if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                                contentHTML += \`<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">\${p}</div>\`;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                                let bqText = trimmed.replace(/^&gt;\\s?/gm, '').replace(/^>\\s?/gm, '');
                                bqText = bqText.replace(/\\n/g, '<br>');
                                contentHTML += \`<blockquote class="pull-quote">\${bqText}</blockquote>\`;
                            } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                                contentHTML += \`<p class="subheading">\${trimmed}</p>\`;
                            } else {
                                let htmlP = p.replace(/\\n(?=\\d+\\.\\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\\n/g, '<br>');
                                contentHTML += \`<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">\${htmlP}</p>\`;
                            }
                        });
                    }
                    contentHTML = \`<div class="page-inner">\${contentHTML}</div>\`;
                }
                
                pageEl.innerHTML = contentHTML;
                inner.appendChild(pageEl);
            });
            
            // Rebuild TOC
            if(tocList) {
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
                        li.innerHTML = \`<span class="toc-title">\${page.title}</span>\`;
                        li.onclick = () => {
                            currentChapter = index;
                            currentColumn = 0;
                            updateControls();
                            document.getElementById('toc-modal').style.display = 'none';
                        };
                        tocList.appendChild(li);
                    }
                });
            }

            // Restore position if possible
            const savedChapter = localStorage.getItem('JJournal_savedChapter');
            const savedColumn = localStorage.getItem('JJournal_savedColumn');
            if (savedChapter !== null && savedColumn !== null) {
                const parsedChap = parseInt(savedChapter, 10);
                const parsedCol = parseInt(savedColumn, 10);
                if(!isNaN(parsedChap) && !isNaN(parsedCol)) {
                    currentChapter = Math.max(0, Math.min(parsedChap, bookData.pages.length - 1));
                    currentColumn = parsedCol;
                }
            }
            updateBookmarkButton();
        }
`;

const newHtml = html.substring(0, startIndex) + cleanRenderBook + html.substring(endIndex);
fs.writeFileSync('index.html', newHtml, 'utf8');

