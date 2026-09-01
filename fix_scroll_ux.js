const fs = require('fs');
const indexPath = 'index.html';

let content = fs.readFileSync(indexPath, 'utf8');

// Add CSS for the scroll indicator
const cssToAdd = `
        .scroll-indicator {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 102, 204, 0.9);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            pointer-events: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            animation: bounce 2s infinite;
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 6px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0) translateX(-50%); }
            40% { transform: translateY(-10px) translateX(-50%); }
            60% { transform: translateY(-5px) translateX(-50%); }
        }
`;
content = content.replace(/(<\/style>\s*<\/head>)/i, cssToAdd + "\n$1");

// Add the JS logic to render and hide the scroll indicator
// We will inject this logic right after rendering the page HTML
const jsLogic = `
                // Inject scroll indicator
                pageEl.innerHTML += \`<div class="scroll-indicator" id="scroll-ind-\${index}">↓ 아래로 스크롤해서 계속 읽기</div>\`;
                
                // Add scroll event listener to the page to hide indicator
                const pageContentDiv = pageEl.querySelector('.page-content');
                if(pageContentDiv) {
                    pageContentDiv.addEventListener('scroll', function() {
                        const ind = pageEl.querySelector('.scroll-indicator');
                        if(ind) {
                            // If scrolled down even a little, fade it out
                            if(this.scrollTop > 20) {
                                ind.style.opacity = '0';
                            } else {
                                ind.style.opacity = '1';
                            }
                        }
                    });
                }
`;

// Find where pageEl.innerHTML = contentHTML; is and append logic
content = content.replace(/(pageEl\.innerHTML = contentHTML;)/, "$1\n" + jsLogic);

// Add a check in renderBook to show indicator ONLY if content overflows
const showLogic = `
            // Check if page has scrollable content and show indicator
            setTimeout(() => {
                const activeEl = document.querySelectorAll('.page')[currentChapter];
                if(activeEl) {
                    const contentDiv = activeEl.querySelector('.page-content');
                    const ind = activeEl.querySelector('.scroll-indicator');
                    if(contentDiv && ind) {
                        // If content is taller than container, it's scrollable
                        if(contentDiv.scrollHeight > contentDiv.clientHeight + 10) {
                            if(contentDiv.scrollTop <= 20) {
                                ind.style.opacity = '1';
                            }
                        } else {
                            ind.style.opacity = '0';
                        }
                    }
                }
            }, 300); // Wait for transition
`;
content = content.replace(/(updateControls\(\);)/, "$1\n" + showLogic);

fs.writeFileSync(indexPath, content, 'utf8');
console.log("Scroll UX fixed.");
