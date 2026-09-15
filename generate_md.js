const fs = require('fs');
const data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let md = "# J Journal: 도면 위의 공유결합 (최종 통합본)\n\n";

for (let i = 0; i < data.pages.length; i++) {
    const page = data.pages[i];
    if (page.type === "author_profile") continue;
    
    if (!page.isContinuation || page.title) {
        md += `## [Page ${i + 1}] ${page.title || '제목 없음'}\n\n`;
    }
    
    if (page.image && page.image !== "") {
        let absPath = "/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/" + page.image;
        md += `![${page.title || '이미지'}](${absPath})\n\n`;
    }

    if (page.isImageOnly) {
        md += `*(이미지 단독 페이지)*\n\n---\n\n`;
        continue;
    }
    
    let text = page.text || "";
    
    text = text.replace(/<img[^>]+src="(static\/images\/[^"]+)"[^>]*alt="([^"]*)"[^>]*>/gi, (match, src, alt) => {
        let absPath = "/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/" + src;
        return `\n![${alt}](${absPath})\n`;
    });
    text = text.replace(/<img[^>]+src="(static\/images\/[^"]+)"[^>]*>/gi, (match, src) => {
        if (match.includes("![") === false) {
            let absPath = "/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/" + src;
            return `\n![이미지](${absPath})\n`;
        }
        return match;
    });

    // Handle blockquotes cleanly
    text = text.replace(/<blockquote[^>]*>([\s\S]*?)<\/blockquote>/gi, (match, content) => {
        let lines = content.split(/<br\s*\/?>|\n/i);
        let block = lines.map(l => l.trim()).filter(l => l !== "").map(l => '> ' + l).join('\n');
        return '\n\n' + block + '\n\n';
    });
    
    text = text.replace(/<svg.*?>[\s\S]*?<\/svg>/gi, '');
    text = text.replace(/<div.*?>/gi, '\n');
    text = text.replace(/<\/div>/gi, '\n');
    text = text.replace(/<br\s*\/?>/gi, '\n');
    text = text.replace(/<p.*?>/gi, '');
    text = text.replace(/<\/p>/gi, '\n\n');
    text = text.replace(/<strong>(.*?)<\/strong>/gi, '**$1**');
    text = text.replace(/<span.*?>/gi, '');
    text = text.replace(/<\/span>/gi, '');
    text = text.replace(/\n{3,}/g, '\n\n');
    text = text.replace(/&nbsp;/g, ' ');
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&amp;/g, '&');
    
    if (text.trim() !== "") {
        md += text.trim() + "\n\n";
    }
    
    md += "---\n\n";
}

fs.writeFileSync('full_manuscript_latest.md', md);
console.log("Successfully generated markdown!");
