const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

function markdownTableToHtml(markdown) {
    let lines = markdown.trim().split('\n');
    if (lines.length < 2) return markdown;
    
    let html = '<div class="custom-table" style="background: var(--canvas-parchment, #f5f5f7); border-radius: 11px; padding: 24px; margin-top: 20px; border: 1px solid var(--hairline, #e0e0e0); margin-bottom: 24px; overflow-x: auto; font-size: 14px;"><table style="width:100%; border-collapse: collapse;">';
    
    let headers = lines[0].split('|').filter(x => x).map(x => x.trim());
    html += '<thead><tr>' + headers.map(h => `<th style="border-bottom: 2px solid var(--primary); padding: 10px; text-align: left; color: var(--ink);">${h}</th>`).join('') + '</tr></thead><tbody>';
    
    for (let i = 2; i < lines.length; i++) {
        let cells = lines[i].split('|').filter(x => x).map(x => x.trim());
        html += '<tr>' + cells.map(c => `<td style="border-bottom: 1px solid var(--hairline); padding: 10px; color: var(--ink-muted-80);">${c}</td>`).join('') + '</tr>';
    }
    
    html += '</tbody></table></div>';
    return html;
}

bookData.pages.forEach((page, index) => {
    if (page.text) {
        // Fix markdown tables
        page.text = page.text.replace(/(?:\|.*?\|\n)+/g, match => {
            if (match.includes('|---|')) {
                return markdownTableToHtml(match);
            }
            return match;
        });

        // Fix ASCII diagrams (Code blocks)
        page.text = page.text.replace(/```([\s\S]*?)```/g, (match, p1) => {
            return `<div class="custom-table" style="background: var(--surface-tile-1, #272729); color: #fff; padding: 20px; border-radius: 11px; overflow-x: auto; font-family: monospace; font-size: 12px; line-height: 1.4; margin-top: 20px; margin-bottom: 24px;"><pre style="margin:0; white-space: pre;">${p1.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre></div>`;
        });
    }
});

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Markdown parsing fixed.");
