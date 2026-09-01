const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

let fullText = "# J-Journal (도면 위에 머무는 시간)\n\n";
bookData.pages.forEach(p => {
    if (p.title) fullText += `\n## ${p.title}\n\n`;
    if (p.subtitle) fullText += `> ${p.subtitle}\n\n`;
    if (p.text) fullText += `${p.text.replace(/<[^>]+>/g, '')}\n\n`; // Strip simple HTML
});
fs.writeFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_text_final.md', fullText);
