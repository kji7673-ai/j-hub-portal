const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let md = "# 불완전한 선택: AI 시대 건축가의 성찰\n\n";

bookData.pages.forEach((p, idx) => {
    if (p.title) {
        md += `## ${p.title}\n\n`;
    }
    
    if (p.subtitle) {
        md += `### ${p.subtitle}\n\n`;
    }
    
    if (p.text) {
        // Simple HTML to Markdown conversion
        let text = p.text.replace(/<br\s*\/?>/gi, '\n');
        text = text.replace(/<p[^>]*>/gi, '');
        text = text.replace(/<\/p>/gi, '\n\n');
        
        // Handle reflections (divs)
        text = text.replace(/<div[^>]*>/gi, '\n\n> ');
        text = text.replace(/<\/div>/gi, '\n\n');
        
        // Handle images
        text = text.replace(/<img[^>]*src="([^"]+)"[^>]*>/gi, '\n![Image]($1)\n');
        
        // Handle headings
        text = text.replace(/<h4[^>]*>(.*?)<\/h4>/gi, '\n#### $1\n');
        
        text = text.replace(/<strong>/gi, '**').replace(/<\/strong>/gi, '**');
        
        // Clean up multiple newlines
        text = text.replace(/\n{3,}/g, '\n\n');
        
        md += `${text.trim()}\n\n`;
    }
    
    md += `---\n\n`; // Page separator
});

fs.writeFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_text_final_v4.md', md, 'utf8');
console.log("Markdown exported cleanly.");
