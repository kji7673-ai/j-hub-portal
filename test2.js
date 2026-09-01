        let currentChapter = 0;
        let currentColumn = 0;
        const COLUMN_GAP = 40;

        function renderBook() {
            const container = document.getElementById('book-container');
            // Remove existing pages
            document.querySelectorAll('.page-content').forEach(p => p.remove());

            let isPhilosophySection = false; // Tracks if we are in Part 5+

            bookData.pages.forEach((page, index) => {
                // Detect start of philosophy section
                if (page.title && (page.title.includes('5부.') || page.title.includes('[철학편]'))) {
                    isPhilosophySection = true;
                }

                const pageEl = document.createElement('div');
                pageEl.className = 'page-content' + (index === currentChapter ? ' active' : '');
                
                // Apply philosophy-mode if in philosophy section
                if (isPhilosophySection) {
                    pageEl.className += ' philosophy-mode';
                }
                
                let contentHTML = '';
                
                // Default fallback for legacy book_data.js structure
                page.type = page.type || 'image_top';
                page.image = page.image || page.bgImage;
                
                if (page.image && !page.image.startsWith('http') && !page.image.startsWith('static/images/')) {
                    page.image = 'static/images/' + page.image;
                }
                
                if (page.type === 'cover') {
                    pageEl.className += ' bg-dark';
                    
                    let rawTitle = page.title;
                    let part = "";
                    let mainTitle = rawTitle;
                    let subtitle = page.subtitle || "";
                    
                    // 1. Extract Subtitle from parentheses
                    if (!subtitle) {
                        const subMatch = rawTitle.match(/(.*?)\s*\((.*?)\)$/);
                        if (subMatch) {
                            mainTitle = subMatch[1].trim();
                            subtitle = subMatch[2].trim();
                        }
                    }
                    
                    // 2. Extract Part / Theme
                    const partMatch = mainTitle.match(/^((?:\d+부\.\s*\[.*?\]|\[.*?\]|막간극.*?:\s*|에필로그:\s*))(.+)$/);
                    if (partMatch) {
                        part = partMatch[1].trim();
                        mainTitle = partMatch[2].trim();
                    }
                    
                    contentHTML += `<div class="cover-content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">`;
                    
                    if (part) {
                        contentHTML += `<p style="font-family: var(--font-display, 'SF Pro Display', sans-serif); font-size: 14px; font-weight: 600; color: var(--primary-on-dark, #2997ff); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">${part}</p>`;
                    }
                    
                    contentHTML += `<h1 class="book-title" style="font-family: var(--font-display, 'SF Pro Display', sans-serif); font-size: clamp(28px, 6vw, 44px); font-weight: 700; color: #ffffff; margin: 0 0 24px 0; line-height: 1.25; letter-spacing: -0.02em; word-break: keep-all;">${mainTitle}</h1>`;
                    
                    if (subtitle) {
                        contentHTML += `<p style="font-family: var(--font-body, 'SF Pro Text', sans-serif); font-size: 18px; font-weight: 300; color: #a0a0a0; margin: 0; word-break: keep-all; line-height: 1.5;">${subtitle}</p>`;
                    }
                    
                    // Decorative line
                    contentHTML += `<div style="width: 40px; height: 1px; background: rgba(255,255,255,0.2); margin-top: 40px;"></div>`;
                    contentHTML += `</div>`;
                }

                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #ffffff); border-radius: 0; padding: 40px; box-shadow: none; border: none; width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    

                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }
 
                else if (page.type === 'image_top') {
                    pageEl.className += ' page-text-flow page-layout';
                    let extraImgStyle = "";
                    if (page.part === "Part 8") {
                        if (page.text && page.text.length < 200) {
                            extraImgStyle = "max-width: 900px; width: 100%; margin-bottom: 50px;";
                        } else if (page.text && page.text.length < 400) {
                            extraImgStyle = "max-width: 800px; width: 90%; margin-bottom: 45px;";
                        } else {
                            extraImgStyle = "max-width: 700px; width: 80%; margin-bottom: 40px;";
                        }
                    }
                    if(page.image) contentHTML += `<div class="image-container" id="img-container-${index}" style="${extraImgStyle}"><img src="${page.image}" alt="sketch"></div>`;
                    if(page.title) contentHTML += `<h2 class="chapter-title" style="margin-bottom:20px;">${page.title}</h2>`;
                    if(page.text) {
                        let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                        const paragraphs = formattedText.split('\n\n');
                        paragraphs.forEach(p => {
                            const trimmed = p.trim();
                            if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                                contentHTML += `<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">${p}</div>`;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                                let bqText = trimmed.replace(/^&gt;\s?/gm, '').replace(/^>\s?/gm, '');
                                bqText = bqText.replace(/\n/g, '<br>');
                                contentHTML += `<blockquote class="pull-quote">${bqText}</blockquote>`;
                            } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                                contentHTML += `<p class="subheading">${trimmed}</p>`;
                            } else {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">${htmlP}</p>`;
                            }
                        });
                    }
                    contentHTML = `<div class="page-inner">${contentHTML}</div>`;
                }
                else if (page.type === 'image_full') {
                    pageEl.style.padding = '0';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; padding:0; z-index:0; background:#ffffff;">
                            <img src="${page.image}" alt="full_image" style="width:100%; height:100%; object-fit:cover; ">
                        </div>`;
                    }
                    if(page.title || page.subtitle || page.text) {
                        let rawTitle = page.title || "";
                        let part = "";
                        let mainTitle = rawTitle;
                        let subtitle = page.subtitle || "";

                        if (!subtitle) {
                            const subMatch = rawTitle.match(/(.*?)\s*\((.*?)\)$/);
                            if (subMatch) {
                                mainTitle = subMatch[1].trim();
                                subtitle = subMatch[2].trim();
                            }
                        }
                        
                        const partMatch = mainTitle.match(/^((?:\d+부\.\s*\[.*?\]|\[.*?\]|막간극.*?\s*|에필로그:\s*|부록:\s*|에피소드.*?:\s*))(.+)$/);
                        if (partMatch) {
                            part = partMatch[1].trim();
                            mainTitle = partMatch[2].trim();
                        }
                        
                        // Parse part into number and category (e.g. 1부, 시스템편)
                        let partNumber = "";
                        let partCategory = "";
                        if (part) {
                            const subPartMatch = part.match(/^(\d+부)\.?\s*\[(.*?)\]$/);
                            if (subPartMatch) {
                                partNumber = subPartMatch[1];
                                partCategory = subPartMatch[2];
                            } else {
                                partNumber = part;
                            }
                        }

                        // Create the glassmorphism panel
                        contentHTML += `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 20px; box-sizing:border-box;">`;
                        
                        // Only add the glassmorphism panel if there is text
                        if (part || mainTitle || subtitle) {
                            contentHTML += `<div style="padding: 50px 40px; display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 80%; display:flex; flex-direction:column; align-items:center; text-align:center;">`;
                            
                            if (partNumber || partCategory) {
                                contentHTML += `<div style="display:flex; flex-direction:column; align-items:center; margin-bottom: 24px;">`;
                                if (partNumber) {
                                    contentHTML += `<div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--primary-on-dark, #2997ff); letter-spacing: 0.15em; text-shadow: 0 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; margin-bottom: ${partCategory ? '12px' : '0'};">${partNumber}</div>`;
                                }
                                if (partNumber && partCategory) {
                                    contentHTML += `<div style="width: 2px; height: 24px; background: rgba(0, 102, 204, 0.3); margin-bottom: 12px;"></div>`;
                                }
                                if (partCategory) {
                                    contentHTML += `<div style="padding: 6px 16px; background: var(--primary); color: #ffffff; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; box-shadow: 0 4px 15px rgba(0,102,204,0.3);">${partCategory}</div>`;
                                }
                                contentHTML += `</div>`;
                            }
                            
                            if(mainTitle) {
                                contentHTML += `<h1 class="book-title" style="color:#ffffff; font-size:clamp(32px, 5vw, 48px); margin-bottom:16px; font-weight:800; letter-spacing: -0.03em; line-height: 1.2; word-break: keep-all; text-shadow: 0 4px 12px rgba(0,0,0,0.5);">${mainTitle}</h1>`;
                            }
                            
                            if(subtitle) {
                                contentHTML += `<p style="color:rgba(255,255,255,0.9); font-size:clamp(18px, 2.5vw, 24px); font-weight:500; word-break: keep-all; margin:0; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">${subtitle}</p>`;
                            }
                            
                            contentHTML += `</div>`;
                        }
                        // close the outer wrapper ONLY if there was no text.
                        // Wait! The previous code didn't have an outer wrapper.
                        // My code adds a flex wrapper for alignment, then the panel.
                        // But wait, the outer wrapper `contentHTML += \`<div style="position:relative...` MUST be closed!
                        // Oh! The old code didn't close it before `if(page.text)`!
                        // The old code closed it after `page.text` processing.
                        // So I should not close the outer wrapper here. I should just let it remain open.
                        // My outer wrapper is: `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 20px; box-sizing:border-box;">`
                        
                        if(page.text) {
                            let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #1d1d1f;">$1</strong>');
                            const paragraphs = formattedText.split('\n\n');
                            paragraphs.forEach(p => {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="color: #333; font-weight: 500; text-align:center; font-size: 18px; line-height: 1.8; max-width: 600px; margin: 0 auto 15px auto; text-shadow: 0 1px 5px rgba(255,255,255,0.8);">${htmlP}</p>`;
                            });
                        }
                        contentHTML += `</div>`;
                    }
                }
                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #ffffff); border-radius: 0; padding: 40px; box-shadow: none; border: none; width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    

                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }
 
                else if (page.type === 'image_top') {
                    pageEl.className += ' page-text-flow page-layout';
                    let extraImgStyle = "";
                    if (page.part === "Part 8") {
                        if (page.text && page.text.length < 200) {
                            extraImgStyle = "max-width: 900px; width: 100%; margin-bottom: 50px;";
                        } else if (page.text && page.text.length < 400) {
                            extraImgStyle = "max-width: 800px; width: 90%; margin-bottom: 45px;";
                        } else {
                            extraImgStyle = "max-width: 700px; width: 80%; margin-bottom: 40px;";
                        }
                    }
                    if(page.image) contentHTML += `<div class="image-container" id="img-container-${index}" style="${extraImgStyle}"><img src="${page.image}" alt="sketch"></div>`;
                    if(page.title) contentHTML += `<h2 class="chapter-title" style="margin-bottom:20px;">${page.title}</h2>`;
                    if(page.text) {
                        let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                        const paragraphs = formattedText.split('\n\n');
                        paragraphs.forEach(p => {
                            const trimmed = p.trim();
                            if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                                contentHTML += `<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">${p}</div>`;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                                let bqText = trimmed.replace(/^&gt;\s?/gm, '').replace(/^>\s?/gm, '');
                                bqText = bqText.replace(/\n/g, '<br>');
                                contentHTML += `<blockquote class="pull-quote">${bqText}</blockquote>`;
                            } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                                contentHTML += `<p class="subheading">${trimmed}</p>`;
                            } else {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">${htmlP}</p>`;
                            }
                        });
                    }
                    contentHTML = `<div class="page-inner">${contentHTML}</div>`;
                }
                else if (page.type === 'image_full') {
                    pageEl.style.padding = '0';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; border-radius:0; z-index:0; background:#ffffff; display:flex; justify-content:center; align-items:center; padding: 40px; box-sizing: border-box;"><img src="${page.image}" alt="full_image" style="max-width:100%; max-height:100%; width:auto; height:auto; object-fit:contain; border-radius:0; box-shadow: none;"></div>`;
                    }
                    if(page.title || page.subtitle || page.text) {
                        let rawTitle = page.title || "";
                        let part = "";
                        let mainTitle = rawTitle;
                        let subtitle = page.subtitle || "";

                        if (!subtitle) {
                            const subMatch = rawTitle.match(/(.*?)\s*\((.*?)\)$/);
                            if (subMatch) {
                                mainTitle = subMatch[1].trim();
                                subtitle = subMatch[2].trim();
                            }
                        }
                        
                        const partMatch = mainTitle.match(/^((?:\d+부\.\s*\[.*?\]|\[.*?\]|막간극.*?\s*|에필로그:\s*|부록:\s*|에피소드.*?:\s*))(.+)$/);
                        if (partMatch) {
                            part = partMatch[1].trim();
                            mainTitle = partMatch[2].trim();
                        }
                        
                        // Parse part into number and category (e.g. 1부, 시스템편)
                        let partNumber = "";
                        let partCategory = "";
                        if (part) {
                            const subPartMatch = part.match(/^(\d+부)\.?\s*\[(.*?)\]$/);
                            if (subPartMatch) {
                                partNumber = subPartMatch[1];
                                partCategory = subPartMatch[2];
                            } else {
                                partNumber = part;
                            }
                        }

                        // Create the glassmorphism panel
                        contentHTML += `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 20px; box-sizing:border-box;">`;
                        
                        // Only add the glassmorphism panel if there is text
                        if (part || mainTitle || subtitle) {
                            contentHTML += `<div style="padding: 50px 40px; display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 80%; display:flex; flex-direction:column; align-items:center; text-align:center;">`;
                            
                            if (partNumber || partCategory) {
                                contentHTML += `<div style="display:flex; flex-direction:column; align-items:center; margin-bottom: 24px;">`;
                                if (partNumber) {
                                    contentHTML += `<div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--primary-on-dark, #2997ff); letter-spacing: 0.15em; text-shadow: 0 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; margin-bottom: ${partCategory ? '12px' : '0'};">${partNumber}</div>`;
                                }
                                if (partNumber && partCategory) {
                                    contentHTML += `<div style="width: 2px; height: 24px; background: rgba(0, 102, 204, 0.3); margin-bottom: 12px;"></div>`;
                                }
                                if (partCategory) {
                                    contentHTML += `<div style="padding: 6px 16px; background: var(--primary); color: #ffffff; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; box-shadow: 0 4px 15px rgba(0,102,204,0.3);">${partCategory}</div>`;
                                }
                                contentHTML += `</div>`;
                            }
                            
                            if(mainTitle) {
                                contentHTML += `<h1 class="book-title" style="color:#ffffff; font-size:clamp(32px, 5vw, 48px); margin-bottom:16px; font-weight:800; letter-spacing: -0.03em; line-height: 1.2; word-break: keep-all; text-shadow: 0 4px 12px rgba(0,0,0,0.5);">${mainTitle}</h1>`;
                            }
                            
                            if(subtitle) {
                                contentHTML += `<p style="color:rgba(255,255,255,0.9); font-size:clamp(18px, 2.5vw, 24px); font-weight:500; word-break: keep-all; margin:0; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">${subtitle}</p>`;
                            }
                            
                            contentHTML += `</div>`;
                        }
                        // close the outer wrapper ONLY if there was no text.
                        // Wait! The previous code didn't have an outer wrapper.
                        // My code adds a flex wrapper for alignment, then the panel.
                        // But wait, the outer wrapper `contentHTML += \`<div style="position:relative...` MUST be closed!
                        // Oh! The old code didn't close it before `if(page.text)`!
                        // The old code closed it after `page.text` processing.
                        // So I should not close the outer wrapper here. I should just let it remain open.
                        // My outer wrapper is: `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 20px; box-sizing:border-box;">`
                        
                        if(page.text) {
                            let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #1d1d1f;">$1</strong>');
                            const paragraphs = formattedText.split('\n\n');
                            paragraphs.forEach(p => {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="color: #333; font-weight: 500; text-align:center; font-size: 18px; line-height: 1.8; max-width: 600px; margin: 0 auto 15px auto; text-shadow: 0 1px 5px rgba(255,255,255,0.8);">${htmlP}</p>`;
                            });
                        }
                        contentHTML += `</div>`;
                    }
                }
                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #ffffff); border-radius: 0; padding: 40px; box-shadow: none; border: none; width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    

                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }
 
                else if (page.type === 'image_top') {
                    pageEl.className += ' page-text-flow';
                    if (page.text && page.text.length < 350) {
                        pageEl.className += ' layout-short';
                    } else {
                        pageEl.className += ' layout-long';
                    }
                    let extraImgStyle = "";
                    if (page.part === "Part 8") {
                        if (page.text && page.text.length < 200) {
                            extraImgStyle = "max-width: 900px; width: 100%; margin-bottom: 50px;";
                        } else if (page.text && page.text.length < 400) {
                            extraImgStyle = "max-width: 800px; width: 90%; margin-bottom: 45px;";
                        } else {
                            extraImgStyle = "max-width: 700px; width: 80%; margin-bottom: 40px;";
                        }
                    }
                    if(page.image) contentHTML += `<div class="image-container" id="img-container-${index}" style="${extraImgStyle}"><img src="${page.image}" alt="sketch"></div>`;
                    if(page.title) contentHTML += `<h2 class="chapter-title" style="margin-bottom:10px;">${page.title}</h2>`;
                    if(page.text) {
                        let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                        const paragraphs = formattedText.split('\n\n');
                        paragraphs.forEach(p => {
                            const trimmed = p.trim();
                            if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                                contentHTML += `<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">${p}</div>`;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                                let bqText = trimmed.replace(/^&gt;\s?/gm, '').replace(/^>\s?/gm, '');
                                bqText = bqText.replace(/\n/g, '<br>');
                                contentHTML += `<blockquote class="pull-quote">${bqText}</blockquote>`;
                            } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                                contentHTML += `<p class="subheading">${trimmed}</p>`;
                            } else {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="line-height: 1.9;">${htmlP}</p>`;
                            }
                        });
                    }
                    contentHTML = `<div class="page-inner">${contentHTML}</div>`;
                }
                else if (page.type === 'image_full') {
                    pageEl.style.padding = '0';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; border-radius:0; z-index:0; background:#ffffff; display:flex; justify-content:center; align-items:center; padding: 20px; box-sizing: border-box;"><img src="${page.image}" alt="full_image" style="max-width:100%; max-height:100%; width:auto; height:auto; object-fit:contain; border-radius:0; box-shadow: none;"></div>`;
                    }
                    if(page.title || page.subtitle || page.text) {
                        let rawTitle = page.title || "";
                        let part = "";
                        let mainTitle = rawTitle;
                        let subtitle = page.subtitle || "";

                        if (!subtitle) {
                            const subMatch = rawTitle.match(/(.*?)\s*\((.*?)\)$/);
                            if (subMatch) {
                                mainTitle = subMatch[1].trim();
                                subtitle = subMatch[2].trim();
                            }
                        }
                        
                        const partMatch = mainTitle.match(/^((?:\d+부\.\s*\[.*?\]|\[.*?\]|막간극.*?\s*|에필로그:\s*|부록:\s*|에피소드.*?:\s*))(.+)$/);
                        if (partMatch) {
                            part = partMatch[1].trim();
                            mainTitle = partMatch[2].trim();
                        }
                        
                        // Parse part into number and category (e.g. 1부, 시스템편)
                        let partNumber = "";
                        let partCategory = "";
                        if (part) {
                            const subPartMatch = part.match(/^(\d+부)\.?\s*\[(.*?)\]$/);
                            if (subPartMatch) {
                                partNumber = subPartMatch[1];
                                partCategory = subPartMatch[2];
                            } else {
                                partNumber = part;
                            }
                        }

                        // Create the glassmorphism panel
                        contentHTML += `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 20px; box-sizing:border-box;">`;
                        
                        // Only add the glassmorphism panel if there is text
                        if (part || mainTitle || subtitle) {
                            contentHTML += `<div style="padding: 50px 40px; display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 80%; display:flex; flex-direction:column; align-items:center; text-align:center;">`;
                            
                            if (partNumber || partCategory) {
                                contentHTML += `<div style="display:flex; flex-direction:column; align-items:center; margin-bottom: 24px;">`;
                                if (partNumber) {
                                    contentHTML += `<div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--primary-on-dark, #2997ff); letter-spacing: 0.15em; text-shadow: 0 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; margin-bottom: ${partCategory ? '12px' : '0'};">${partNumber}</div>`;
                                }
                                if (partNumber && partCategory) {
                                    contentHTML += `<div style="width: 2px; height: 24px; background: rgba(0, 102, 204, 0.3); margin-bottom: 12px;"></div>`;
                                }
                                if (partCategory) {
                                    contentHTML += `<div style="padding: 6px 16px; background: var(--primary); color: #ffffff; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; box-shadow: 0 4px 15px rgba(0,102,204,0.3);">${partCategory}</div>`;
                                }
                                contentHTML += `</div>`;
                            }
                            
                            if(mainTitle) {
                                contentHTML += `<h1 class="book-title" style="color:#ffffff; font-size:clamp(32px, 5vw, 48px); margin-bottom:16px; font-weight:800; letter-spacing: -0.03em; line-height: 1.2; word-break: keep-all; text-shadow: 0 4px 12px rgba(0,0,0,0.5);">${mainTitle}</h1>`;
                            }
                            
                            if(subtitle) {
                                contentHTML += `<p style="color:rgba(255,255,255,0.9); font-size:clamp(18px, 2.5vw, 24px); font-weight:500; word-break: keep-all; margin:0; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">${subtitle}</p>`;
                            }
                            
                            contentHTML += `</div>`;
                        }
                        // close the outer wrapper ONLY if there was no text.
                        // Wait! The previous code didn't have an outer wrapper.
                        // My code adds a flex wrapper for alignment, then the panel.
                        // But wait, the outer wrapper `contentHTML += \`<div style="position:relative...` MUST be closed!
                        // Oh! The old code didn't close it before `if(page.text)`!
                        // The old code closed it after `page.text` processing.
                        // So I should not close the outer wrapper here. I should just let it remain open.
                        // My outer wrapper is: `<div style="position:relative; z-index:1; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding: 20px; box-sizing:border-box;">`
                        
                        if(page.text) {
                            let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                            const paragraphs = formattedText.split('\n\n');
                            paragraphs.forEach(p => {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="color:#1d1d1f; font-weight:600; text-shadow: 0 1px 10px rgba(255,255,255,0.9); text-align:center; font-size:18px; line-height: 1.9;">${htmlP}</p>`;
                            });
                        }
                        contentHTML += `</div>`;
                    }
                }

                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #ffffff); border-radius: 0; padding: 40px; box-shadow: none; border: none; width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    
                    contentHTML += `<ul class="author-list">`;
                    contentHTML += `<li>현(現) 서울시 건축심의위원</li>`;
                    contentHTML += `<li>현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원</li>`;
                    contentHTML += `<li>현(現) 강동구, 양천구 건축심의위원</li>`;
                    contentHTML += `<li>현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원</li>`;
                    contentHTML += `</ul>`;
                    
                    contentHTML += `<p class="author-desc" style="border-top: 1px solid var(--hairline); padding-top: 20px; margin-bottom: 0;">"정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 뼈저리게 목도하고 있는 건축가의 진심 어린 조언이자 따뜻한 혁신의 기록."</p>`;
                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }

                else if (page.type === 'text_only') {
                    pageEl.className += ' page-text-flow page-layout';
                    if(page.title) contentHTML += `<h2 class="chapter-title" style="margin-bottom:20px;">${page.title}</h2>`;
                    if(page.text) {
                        let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                        const paragraphs = formattedText.split('\n\n');
                        paragraphs.forEach(p => {
                            const trimmed = p.trim();
                            if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
                                contentHTML += `<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">${p}</div>`;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
                                let bqText = trimmed.replace(/^&gt;\s?/gm, '').replace(/^>\s?/gm, '');
                                bqText = bqText.replace(/\n/g, '<br>');
                                contentHTML += `<blockquote class="pull-quote">${bqText}</blockquote>`;
                            } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
                                contentHTML += `<p class="subheading">${trimmed}</p>`;
                            } else {
                                let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
                                htmlP = htmlP.replace(/\n/g, '<br>');
                                contentHTML += `<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">${htmlP}</p>`;
                            }
                        });
                    }
                    contentHTML = `<div class="page-inner">${contentHTML}</div>`;
                }
                pageEl.innerHTML = contentHTML;
                container.insertBefore(pageEl, container.querySelector('.controls'));
            });

            updateControls();
        }

        function getChapterMaxColumns(chapterIndex) {
            const pageEls = document.querySelectorAll('.page-content');
            const activePage = pageEls[chapterIndex];
            if (!activePage) return 1;
            
            const inner = activePage.querySelector('.page-inner');
            if (!inner) return 1;
            
            const colWidth = inner.clientWidth;
            const scrollWidth = inner.scrollWidth;
            if (colWidth === 0) return 1;
            return Math.max(1, Math.round(scrollWidth / colWidth));
        }

        function updateControls() {
            const pageEls = document.querySelectorAll('.page-content');
            
            pageEls.forEach((p, idx) => {
                if (idx === currentChapter) {
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                    const inner = p.querySelector('.page-inner');
                    if (inner) inner.style.transform = `translateX(0px)`;
                }
            });
            
            const maxCols = getChapterMaxColumns(currentChapter);
            if (currentColumn >= maxCols) currentColumn = maxCols - 1;
            if (currentColumn < 0) currentColumn = 0;
            
            const activePage = pageEls[currentChapter];
            const inner = activePage.querySelector('.page-inner');
            if (inner) {
                const w = inner.clientWidth;
                const translatePx = currentColumn * (w + COLUMN_GAP);
                inner.style.transform = `translateX(-${translatePx}px)`;
            }
            
            const totalChapters = bookData.pages.length;
            document.getElementById('prev-btn').disabled = (currentChapter === 0 && currentColumn === 0);
            document.getElementById('next-btn').disabled = (currentChapter === totalChapters - 1 && currentColumn === maxCols - 1);
            document.getElementById('page-num').innerText = `[${currentChapter + 1}/${totalChapters}] ${currentColumn + 1} / ${maxCols}`;
        }
            if(typeof saveProgress === 'function') saveProgress();

        function prevPage() {
            if (currentColumn > 0) {
                currentColumn--;
                updateControls();
            } else if (currentChapter > 0) {
                currentChapter--;
                currentColumn = 999; // updateControls will clamp it to maxCols - 1
                updateControls();
            }
        }

        function nextPage() {
            const maxCols = getChapterMaxColumns(currentChapter);
            if (currentColumn < maxCols - 1) {
                currentColumn++;
                updateControls();
            } else if (currentChapter < bookData.pages.length - 1) {
                currentChapter++;
                currentColumn = 0;
                updateControls();
            }
        }
        
        window.addEventListener('resize', () => {
            updateControls();
        });

        // Edge Click and Swipe Navigation
        let touchstartX = 0;
        let touchendX = 0;

        function handleGesture() {
            if (touchendX < touchstartX - 50) {
                nextPage(); // Swipe Left
            }
            if (touchendX > touchstartX + 50) {
                prevPage(); // Swipe Right
            }
        }

        document.addEventListener('touchstart', e => {
            touchstartX = e.changedTouches[0].screenX;
        }, {passive: true});

        document.addEventListener('touchend', e => {
            touchendX = e.changedTouches[0].screenX;
            handleGesture();
        }, {passive: true});

        document.addEventListener('click', e => {
            if (e.target.closest('button') || e.target.closest('a') || e.target.closest('input') || e.target.closest('textarea') || e.target.closest('.secret-modal') || e.target.closest('.edit-panel') || e.target.closest('.toc-modal')) {
                return;
            }
            
            const screenWidth = window.innerWidth;
            const clickX = e.clientX;
            const edgeThreshold = screenWidth * 0.25; // 25% of screen width

            if (clickX < edgeThreshold) {
                prevPage();
            } else if (clickX > screenWidth - edgeThreshold) {
                nextPage();
            }
        });


        
        // Secret Room Logic
        let clickCount = 0;
        let clickTimer;
        
        // Listen for clicks on the book container (but specifically we want to target top header area or just globally handle 4 clicks fast)
        document.body.addEventListener('click', function(e) {
            // Only trigger if clicking on empty space or the container itself to avoid interfering with buttons
            if(e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            
            clickCount++;
            clearTimeout(clickTimer);
            clickTimer = setTimeout(() => { clickCount = 0; }, 500);
            
            if (clickCount >= 4) {
                clickCount = 0;
                document.getElementById('secret-modal').style.display = 'flex';
                document.getElementById('secret-pw').focus();
            }
        });

        function checkSecretPassword() {
            const pw = document.getElementById('secret-pw').value;
            if (pw === '937610') {
                document.getElementById('secret-modal').style.display = 'none';
                document.getElementById('secret-pw').value = '';
                const toolbar = document.querySelector('.edit-toolbar');
                if (toolbar) toolbar.style.display = 'block';
            } else {
                alert('비밀번호가 일치하지 않습니다.');
                document.getElementById('secret-modal').style.display = 'none';
            }
        }

        function openSecretPanel() {
            const panel = document.getElementById('secret-panel');
            panel.classList.add('open');
            
            // Load current page text
            const activePage = bookData.pages[currentChapter];
            let contentText = activePage.text || '';
            if (!contentText && activePage.title) {
                contentText = activePage.title + (activePage.subtitle ? '\n' + activePage.subtitle : '');
            }
            document.getElementById('panel-original-text').value = contentText;
            document.getElementById('panel-image-layout').value = activePage.type;
            
            // Reset chat
            currentChatHistory = [];
            document.getElementById('chat-history').innerHTML = '<div style="text-align:center; color:#888;">AI 레드팀과 대화를 시작하세요.</div>';
            document.getElementById('chat-input').value = '';
        }
        
        function closeSecretPanel() {
            document.getElementById('secret-panel').classList.remove('open');
        }

        let currentChatHistory = [];
        
        function appendChatMessage(role, content) {
            const historyBox = document.getElementById('chat-history');
            const msgDiv = document.createElement('div');
            msgDiv.style.padding = '10px 14px';
            msgDiv.style.borderRadius = '12px';
            msgDiv.style.maxWidth = '85%';
            msgDiv.style.fontSize = '14px';
            msgDiv.style.lineHeight = '1.5';
            
            if (role === 'user') {
                msgDiv.style.background = '#0066cc';
                msgDiv.style.color = '#fff';
                msgDiv.style.alignSelf = 'flex-end';
                msgDiv.style.borderBottomRightRadius = '4px';
            } else {
                msgDiv.style.background = '#e5e5ea';
                msgDiv.style.color = '#1d1d1f';
                msgDiv.style.alignSelf = 'flex-start';
                msgDiv.style.borderBottomLeftRadius = '4px';
            }
            msgDiv.innerHTML = content.replace(/\n/g, '<br>');
            
            // Remove empty placeholder if first message
            if (historyBox.children.length === 1 && historyBox.children[0].innerText.includes('시작하세요')) {
                historyBox.innerHTML = '';
            }
            
            historyBox.appendChild(msgDiv);
            historyBox.scrollTop = historyBox.scrollHeight;
            
            if (role !== 'system') {
                currentChatHistory.push({ role: role, content: content });
            }
        }

        async function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const originalText = document.getElementById('panel-original-text').value;
            const msg = input.value.trim();
            
            if (!msg) return;
            
            input.value = '';
            appendChatMessage('user', msg);
            appendChatMessage('system', '<i>답변 생성 중...</i>');
            
            try {
                const response = await fetch('/api/redteam_chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        original_text: originalText, 
                        chat_history: currentChatHistory.slice(0, -1), // Exclude the one just added temporarily
                        message: msg 
                    })
                });
                const result = await response.json();
                
                // Remove the 'system' loading message
                const historyBox = document.getElementById('chat-history');
                historyBox.removeChild(historyBox.lastChild);
                
                appendChatMessage('model', result.feedback);
            } catch (e) {
                const historyBox = document.getElementById('chat-history');
                historyBox.removeChild(historyBox.lastChild);
                appendChatMessage('system', '<span style="color:red;">서버 통신 오류가 발생했습니다.</span>');
            }
        }

        async function applyFinalRevision() {
            if(!confirm('AI가 대화 내역과 앞뒤 문맥을 고려하여 최종 원고를 덮어씁니다. 진행하시겠습니까?')) return;
            
            const originalText = document.getElementById('panel-original-text').value;
            const prevText = currentChapter > 0 ? bookData.pages[currentChapter-1].text : '';
            const nextText = currentChapter < bookData.pages.length - 1 ? bookData.pages[currentChapter+1].text : '';
            
            const saveBtn = document.querySelector('.btn-save');
            const oldSaveText = saveBtn.innerText;
            saveBtn.innerText = 'AI가 재작성 중...';
            saveBtn.disabled = true;
            
            try {
                const response = await fetch('/api/apply_revision', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        page_index: currentChapter, 
                        original_text: originalText,
                        chat_history: currentChatHistory,
                        prev_text: prevText || '',
                        next_text: nextText || ''
                    })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    // Update local object and re-render
                    bookData.pages[currentChapter].text = result.revised_text;
                    document.getElementById('panel-original-text').value = result.revised_text;
                    renderBook();
                    alert('AI가 앞뒤 문맥에 맞게 최종 원고를 성공적으로 재작성했습니다.');
                } else {
                    alert('저장 실패: ' + result.message);
                }
            } catch (e) {
                alert('오류 발생: 서버와 통신할 수 없습니다.');
            }
            
            saveBtn.innerText = oldSaveText;
            saveBtn.disabled = false;
        }
        
        // Setup image upload in panel
        document.getElementById('panel-image-upload').addEventListener('change', async function(e) {
            if(e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                const layout = document.getElementById('panel-image-layout').value;
                const reader = new FileReader();
                
                const uploadLabel = document.querySelector('label[for="panel-image-upload"]');
                const originalLabel = uploadLabel.innerText;
                uploadLabel.innerText = "업로드 중...";
                
                reader.onload = async function(e) {
                    const base64Data = e.target.result;
                    
                    try {
                        const response = await fetch('/api/upload_image', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                page_index: currentChapter,
                                image_data: base64Data,
                                image_layout: layout
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {
                            const activePage = bookData.pages[currentChapter];
                            activePage.image = result.image_url;
                            activePage.type = layout;
                            
                            renderBook();
                            uploadLabel.innerText = originalLabel;
                        } else {
                            alert("업로드 실패: " + result.message);
                            uploadLabel.innerText = originalLabel;
                        }
                    } catch (error) {
                        alert("서버 통신 오류: " + error.message);
                        uploadLabel.innerText = originalLabel;
                    }
                }
                reader.readAsDataURL(file);
            }
        });
        
        // Handle Layout Change without upload
        document.getElementById('panel-image-layout').addEventListener('change', async function(e) {
            const layout = e.target.value;
            const activePage = bookData.pages[currentChapter];
            if(activePage.type !== layout) {
                // If we need to just save the type change (requires backend endpoint, but for now we just change it locally. To save permanently, we'd need a save_layout API. Let's just alert.)
                alert("레이아웃만 변경하는 기능은 새 이미지를 업로드할 때 함께 반영되거나, 원고 수정 시 반영됩니다.");
                activePage.type = layout;
                renderBook();
            }
        });

        // Init
        
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
                        currentChapter = index;
                        currentColumn = 0;
                        updateControls();
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

        window.onload = renderBook;
    
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

