const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const commonStyle = 'margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;';

bookData.pages.forEach(p => {
    if (!p.text) return;
    
    if (p.text.includes("[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]")) {
        // Find the index of the title
        let marker = "[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]";
        
        if (p.text.includes("var(--canvas-parchment)")) {
            let splitText = p.text.split('<div style="background-color: var(--canvas-parchment)');
            let mainText = splitText[0].replace(/<br><br>$/, '');
            let contentStr = splitText[1].split('</h4>\n')[1].split('\n</div></div>')[0];
            p.text = `${mainText}<br><br><div style="${commonStyle}"><b>[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]</b><br><br>${contentStr}</div>`;
        } else {
            // For the specific line 806 style
            let rx = /---<br><br><div class="handwriting" style="margin-top: 10px;"><b>\[아키 시냅스의 반론 \(AI 에이전트의 관찰 일지\)\]<\/b><br>([\s\S]*?)<\/div>/;
            let match = p.text.match(rx);
            if (match) {
                let contentStr = match[1];
                let mainText = p.text.replace(rx, '');
                p.text = `${mainText}<div style="${commonStyle}"><b>[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]</b><br><br>${contentStr}</div>`;
            }
        }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated formats.");
