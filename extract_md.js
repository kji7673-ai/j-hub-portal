const fs = require('fs');
const vm = require('vm');

const data = fs.readFileSync('book_data.js', 'utf8');
const sandbox = {};
vm.runInNewContext(data, sandbox);
const pages = sandbox.bookData.pages;

let md = "# 도면 위의 공유결합\n\n";
let currentPart = "";

pages.forEach(p => {
    // 표지 패스
    if (p.type === 'cover') return; 

    // 챕터 분류가 있고, 이전 챕터와 다르면 출력
    if (p.partCategory && p.partCategory !== currentPart) {
        md += `\n## ${p.partCategory}\n\n`;
        currentPart = p.partCategory;
    }

    // 소제목
    if (p.title && p.title !== currentPart) {
        md += `### ${p.title}\n\n`;
    }

    if (p.subtitle) {
        md += `**${p.subtitle}**\n\n`;
    }

    // 본문 텍스트 태그 정리
    if (p.text) {
        let t = p.text;
        t = t.replace(/<br\s*\/?>/gi, '\n'); // br을 줄바꿈으로
        t = t.replace(/<\/p>/gi, '\n\n'); // p 닫는 태그를 두줄바꿈으로
        t = t.replace(/<[^>]+>/g, ''); // 나머지 모든 HTML 태그 제거
        t = t.replace(/&nbsp;/gi, ' ');
        t = t.replace(/&lt;/gi, '<').replace(/&gt;/gi, '>');
        
        md += `${t.trim()}\n\n`;
    }
    
    // 페이지 구분선
    md += `---\n\n`;
});

// 파일로 저장
fs.writeFileSync('도면위의공유결합_원고.md', md, 'utf8');
console.log(md);
