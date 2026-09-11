const fs = require('fs');
const vm = require('vm');
const path = require('path');

const code = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(code);
const context = {};
vm.createContext(context);
script.runInContext(context);

let pages = context.bookData.pages;
let targetPage = pages.find(p => p.title && p.title.includes("만들고 있는 것인가, 만들어져 가는 것인가"));

const imgStyle = 'max-width:100%; border-radius:12px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);';

if (targetPage) {
    targetPage.text = `우리는 건축 설계안이나 우리의 삶,<br>
나아가 인간관계에 이르기까지, 이 모든 것을 주도적으로 '만들고 있는' 것일까요?<br>
아니면 어떠한 흐름 속에서 '만들어져 가는' 것일까요?<br>
<br>
<img src="static/images/sketch_making_1.jpg" style="${imgStyle}"><br>
<img src="static/images/sketch_making_3.jpg" style="${imgStyle}"><br>
<br>
요즘 취미로 무언가를 만들며 깨닫는 것이 있습니다.<br>
분명 처음에는 저만의 확고한 생각과 의도를 가지고 시작하지만,<br>
결과물에 이르러서는 마치 <strong>'원래 있어야 할 모습'</strong>을 찾아가듯 아주 자연스럽게 만들어져 간다는 것입니다.<br>
<br>
<img src="static/images/sketch_making_2.jpg" style="${imgStyle}"><br>
<br>
우리가 치밀하게 세운 계획도, 인생도,<br>
처음의 의도와 조금 다르게 흘러간다고 해서 결코 틀린 것이 아닙니다.<br>
어쩌면 그것은 지금 주어진 상황과 환경에 가장 적합한 모습으로 '만들어져 가는' 과정일지도 모릅니다.<br>
<br>
<img src="static/images/sketch_making_4.jpg" style="${imgStyle}"><br>
<br>
가장 중요한 것은, 결과가 내 의도와 다르게 변화해 가더라도<br>
그 안에서 <strong>내 마음의 중심</strong>을 결코 놓지 않는 것입니다.<br>
<br>
<img src="static/images/sketch_making_5.jpg" style="${imgStyle}"><br>
<br>
<blockquote>
내 생각과 다르게 진행된다고 해서 틀린 것이 아닙니다.<br>
비록 흔들거리더라도, 다시 방향을 잡고 나아가면 됩니다.<br>
다 괜찮습니다.
</blockquote>`;
    console.log("Updated episode: 만들고 있는 것인가");
}

const outputString = 'var bookData = ' + JSON.stringify(context.bookData, null, 4) + ';';
fs.writeFileSync('book_data.js', outputString, 'utf8');

// Generate HTML
let html = \`<!DOCTYPE html>
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
        <p style="color: #7a7a7a; font-size: 1.2em; margin-top: 40px;">저자 : 김중일</p>
    </div>\`;

function embedBase64(htmlContent) {
    return htmlContent.replace(/src="(static\\/images\\/[^"]+)"/g, (match, imagePath) => {
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
    if (!page.title && !page.text && !page.image) return;
    html += \`<div class="page">\`;
    if (page.partCategory) html += \`<div class="category">\${page.partCategory}</div>\`;
    if (page.title) html += \`<h2 class="episode-title">\${page.title}</h2>\`;
    
    // Support image in front of text if page.image exists
    let contentHtml = "";
    if (page.image) {
        contentHtml += \`<img src="\${page.image}"><br>\`;
    }
    if (page.text) contentHtml += page.text;
    
    html += \`<div class="content">\${embedBase64(contentHtml)}</div>\`;
    html += \`</div>\`;
});
html += \`</body></html>\`;
fs.writeFileSync('도면위의공유결합_출판투고용_최종본.html', html, 'utf8');

// Generate MD
let md = "# J-Journal: 도면 위의 공유결합 (최종본)\\n\\n";
let currentCategory = "";
context.bookData.pages.forEach((page) => {
    if (page.partCategory && page.partCategory !== currentCategory) {
        currentCategory = page.partCategory;
        md += \`---\\n\\n# \${currentCategory}\\n\\n\`;
    }
    if (page.title) md += \`## \${page.title}\\n\\n\`;
    let contentHtml = "";
    if (page.image) contentHtml += \`<img src="\${page.image}">\\n\\n\`;
    if (page.text) contentHtml += page.text;
    
    if (contentHtml) {
        let text = contentHtml;
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
        text = text.replace(/<img[^>]*>/gi, '\\n\\n[이미지 첨부됨]\\n\\n');
        text = text.replace(/<svg[^>]*>.*<\\/svg>/gi, '\\n\\n[공유결합 다이어그램 SVG]\\n\\n');
        text = text.replace(/\\n{3,}/g, '\\n\\n');
        md += text.trim() + "\\n\\n";
    }
});
fs.writeFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/도면위의공유결합_최종본.md', md, 'utf8');

