const fs = require('fs');
const vm = require('vm');
const path = require('path');

const code = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(code);
const context = {};
vm.createContext(context);
script.runInContext(context);

let pages = context.bookData.pages;
let targetPage = pages.find(p => p.title === "금기에 익숙해진다는 것" || p.title === "익숙해진다는 것");

if (targetPage) {
    targetPage.title = "익숙해진다는 것";
    targetPage.text = `타인의 시선에 익숙해져 버렸습니다.<br>
타인의 시선 속의 내가 되어 버렸습니다.<br>
<br>
나의 맘과는 상관없이<br>
그저 모난 소리 듣기 싫어, 힘들어도 참고 인내하는 것에<br>
<br>
내 행동의 의미보다는<br>
타인의 시선 속에서 나를 찾기 시작했습니다.<br>
<br>
눈치껏 살아가는 게 좋은 것이겠죠?<br>
상대에게 좋은 말 듣는 삶이 좋은 것이겠죠?<br>
<br>
나를 인정해주는 말들이 그물처럼 느껴집니다.<br>
<br>
인정해준다는 것은<br>
<br>
나와 타자의 동등한 관계에서 나오는 말일까요?<br>
내가 나를 인정해 줄 수 있을 때 그게 더 좋을 것 같습니다.<br>
<br>
<blockquote>
진정한 관계성이 이루어지려면, 동등한 개인 즉, 본인 자신에 대해 무겁게 해야 합니다.<br>
그래야 상대에게 딸려가지 않는 관계가 형성될 수 있습니다.
</blockquote>`;
    console.log("Successfully updated the page.");
} else {
    console.log("Page not found.");
}

// Write back book_data.js
const outputString = 'var bookData = ' + JSON.stringify(context.bookData, null, 4) + ';';
fs.writeFileSync('book_data.js', outputString, 'utf8');

// Regenerate HTML
let html = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>도면 위의 공유결합 - 출판 투고용 최종 원고</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        body { font-family: 'Pretendard', sans-serif; line-height: 1.8; color: #1d1d1f; max-width: 860px; margin: 0 auto; padding: 40px 20px; background-color: #f5f5f7; word-break: keep-all; }
        .page { background: #ffffff; padding: 60px 80px; margin-bottom: 40px; border-radius: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.04); }
        @media (max-width: 768px) { .page { padding: 40px 30px; } }
        h1.book-title { font-size: 2.5em; color: #1d1d1f; margin-bottom: 20px; text-align: center; font-weight: 800; letter-spacing: -0.03em; }
        h1.book-title span { display: block; font-size: 0.45em; color: #7a7a7a; font-weight: 400; margin-top: 15px; }
        h2.episode-title { font-size: 1.8em; color: #1d1d1f; margin-top: 0; margin-bottom: 30px; font-weight: 700; letter-spacing: -0.02em; }
        .category { display: inline-block; font-size: 0.9em; color: #0066cc; font-weight: 600; margin-bottom: 15px; padding: 4px 12px; background-color: rgba(0, 102, 204, 0.08); border-radius: 999px; }
        img { max-width: 100%; height: auto; border-radius: 12px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .content { font-size: 1.1em; color: #333333; }
        blockquote { padding: 24px; background: #fafafc; border-left: 4px solid #0066cc; border-radius: 0 12px 12px 0; margin: 32px 0; color: #1d1d1f; }
        hr { border: 0; height: 1px; background: #e0e0e0; margin: 40px 0; }
    </style>
</head>
<body>
    <div class="page" style="text-align: center; padding: 120px 40px;">
        <h1 class="book-title">도면 위의 공유결합<br><span>건축과 사람, 그리고 삶을 잇는 단단한 흔적들</span></h1>
        <p style="color: #7a7a7a; font-size: 1.2em; margin-top: 40px;">저자 : 평범한 건축 쟁이</p>
    </div>`;

function embedBase64(htmlContent) {
    return htmlContent.replace(/src="(static\/images\/[^"]+)"/g, (match, imagePath) => {
        try {
            let fullPath = path.join(__dirname, imagePath);
            if (fs.existsSync(fullPath)) {
                let ext = path.extname(fullPath).substring(1);
                if (ext === 'jpg') ext = 'jpeg';
                let base64 = fs.readFileSync(fullPath, 'base64');
                return \`src="data:image/\${ext};base64,\${base64}"\`;
            }
        } catch (e) {}
        return match; 
    });
}

context.bookData.pages.forEach(page => {
    if (!page.title && !page.text) return;
    html += \`<div class="page">\`;
    if (page.partCategory) html += \`<div class="category">\${page.partCategory}</div>\`;
    if (page.title) html += \`<h2 class="episode-title">\${page.title}</h2>\`;
    if (page.text) html += \`<div class="content">\${embedBase64(page.text)}</div>\`;
    html += \`</div>\`;
});
html += \`</body></html>\`;
fs.writeFileSync('J_Journal_최종_출판투고용_v79.html', html, 'utf8');

// Generate MD
let md = "# J-Journal: 도면 위의 공유결합 (v79)\n\n";
let currentCategory = "";
context.bookData.pages.forEach((page) => {
    if (page.partCategory && page.partCategory !== currentCategory) {
        currentCategory = page.partCategory;
        md += \`---\\n\\n# \${currentCategory}\\n\\n\`;
    }
    if (page.title) md += \`## \${page.title}\\n\\n\`;
    if (page.text) {
        let text = page.text;
        text = text.replace(/<br\\s*\\/?>/gi, '\\n');
        text = text.replace(/<\\/p>/gi, '\\n\\n');
        text = text.replace(/<p[^>]*>/gi, '');
        text = text.replace(/<blockquote[^>]*>/gi, '\\n> ');
        text = text.replace(/<\\/blockquote>/gi, '\\n\\n');
        text = text.replace(/<div[^>]*>/gi, '\\n> ');
        text = text.replace(/<\\/div>/gi, '\\n\\n');
        text = text.replace(/<span[^>]*>/gi, '');
        text = text.replace(/<\\/span>/gi, '');
        text = text.replace(/<strong[^>]*>/gi, '**');
        text = text.replace(/<\\/strong>/gi, '**');
        text = text.replace(/<b[^>]*>/gi, '**');
        text = text.replace(/<\\/b>/gi, '**');
        text = text.replace(/<em[^>]*>/gi, '*');
        text = text.replace(/<\\/em>/gi, '*');
        text = text.replace(/<img[^>]*>/gi, '\\n\\n[이미지]\\n\\n');
        text = text.replace(/<svg[^>]*>.*<\\/svg>/gi, '\\n\\n[공유결합 다이어그램 SVG]\\n\\n');
        text = text.replace(/\\n{3,}/g, '\\n\\n');
        md += text.trim() + "\\n\\n";
    }
});
fs.writeFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_manuscript_v79_FINAL.md', md, 'utf8');

