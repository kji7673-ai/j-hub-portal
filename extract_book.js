const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

let md = "# J-Journal 전체 본문\n\n";

bookData.pages.forEach((page, index) => {
    if (page.type === 'cover') {
        md += `---\n\n# 표지: ${page.title || ''}\n\n`;
    } else if (page.type === 'interlude') {
        md += `---\n\n## [간지] ${page.title || ''}\n\n`;
    } else {
        if (page.part) {
            md += `### ${page.part}\n`;
        }
        if (page.partTitle) {
            md += `#### ${page.partTitle}\n`;
        }
        if (page.title) {
            md += `## ${page.title}\n\n`;
        }
    }
    
    if (page.text) {
        let text = page.text.replace(/<br\s*\/?>/gi, '\n');
        md += text + "\n\n";
    }
});

fs.writeFileSync('full_book_text.md', md);
console.log("Extracted to full_book_text.md");
