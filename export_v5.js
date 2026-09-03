const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let md = `# 공유결합: 사람을 향한 건축, 용산 현장의 기억\n\n`;

let currentCategory = "";

bookData.pages.forEach(p => {
    if (p.partCategory && p.partCategory !== currentCategory) {
        currentCategory = p.partCategory;
        md += `\n---\n\n## ${currentCategory}\n\n`;
    }
    
    if (p.title) {
        md += `### ${p.title}\n\n`;
    }
    
    if (p.text) {
        let text = p.text.replace(/<br\s*\/?>/gi, '\n');
        text = text.replace(/<p[^>]*>/gi, '');
        text = text.replace(/<\/p>/gi, '\n\n');
        text = text.replace(/<blockquote>/gi, '> ');
        text = text.replace(/<\/blockquote>/gi, '\n');
        text = text.replace(/<strong>/gi, '**');
        text = text.replace(/<\/strong>/gi, '**');
        text = text.replace(/<span[^>]*>/gi, '');
        text = text.replace(/<\/span>/gi, '');
        md += `${text}\n\n`;
    }
});

fs.writeFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_manuscript_v5.md', md, 'utf8');
console.log('Exported v5');
