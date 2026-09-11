const fs = require('fs');
const vm = require('vm');
const path = require('path');

const code = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(code);
const context = {};
vm.createContext(context);
script.runInContext(context);

let pages = context.bookData.pages;
let targetPage = pages.find(p => p.title && p.title.includes("생각의 힘: 고정관념을 벗고"));

if (targetPage) {
    targetPage.text = `제가 생각하는 '생각의 진짜 힘'은 시간 여행이 가능하다는 것입니다.<br>
시간을 거슬러 과거, 현재, 미래를 오갈 수 있다는 뜻입니다.<br>
<br>
자신이 세운 가정을 토대로 미래를 짚어보고,<br>
새로운 정보를 추가해 다시 과거를 복기하며 오가는 과정.<br>
하지만 조심해야 합니다.<br>
마침내 확신이 드는 그 순간, 오히려 그것은 진짜 사실이 아닐 수 있습니다.<br>
<br>
확신은 반드시 사실을 기반으로 해야 합니다.<br>
그래서 저는 후배들에게 "네가 생각한 것이 진짜 사실인지를 끊임없이 확인하라"고 당부합니다.<br>
<br>
가장 먼저, 그것이 '진짜 사실'인지 확인하십시오.<br>
설계를 하다 보면, 본인이 설정한 기준이나 아이디어에 대해 끊임없이 의심해 볼 필요가 있습니다. 본인이 만든 디자인과 설정이 정말 좋은 것인지, 단순히 내 고집일 뿐인지 스스로에게 물어봐야 합니다.<br>
<br>
"사실", "진짜", "변하지 않는 것" 등을 엄격하게 구분해야 합니다.<br>
특히, <strong>"내가 과거에 경험을 해봤는데..."</strong>로 시작하는 생각은 가장 먼저 의심해 보아야 합니다. 누가 이야기하더라도 본인 스스로 수긍이 되어야 합니다.<br>
<br>
당신이 지금 하고 있는 설계가 진정한 '사실'에 기반하고 있나요?<br>
디자인은 감각이라기보다는, 이 지독한 생각의 힘입니다.<br>
<br>
<blockquote>
공유결합의 세 번째 기둥을 기억하시나요? 상황의 이면을 볼 줄 알아야 한다는 것.<br>
그 이면을 보는 눈은 오직 '사실'에 기반해야 합니다. 그렇지 않으면 진정한 공유결합은 이루어질 수 없습니다.<br>
<br>
인간관계에서도 마찬가지입니다. 한 걸음 물러서서 스스로를 객관화해 보아야 합니다. 내가 저 사람이 싫은 이유가 정말 상대의 잘못(사실) 때문인지, 아니면 내 안의 편견 때문인지 치열하게 확인해야 합니다.<br>
<br>
시간과 노력이 드는, 참으로 고단하고 힘든 과정입니다.
</blockquote>`;
    console.log("Updated '생각의 힘' episode!");
}

const outputString = 'var bookData = ' + JSON.stringify(context.bookData, null, 4) + ';';
fs.writeFileSync('book_data.js', outputString, 'utf8');

// Generate HTML
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
        <p style="color: #7a7a7a; font-size: 1.2em; margin-top: 40px;">저자 : 김중일</p>
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
    if (!page.title && !page.text && !page.image) return;
    html += \`<div class="page">\`;
    if (page.partCategory) html += \`<div class="category">\${page.partCategory}</div>\`;
    if (page.title) html += \`<h2 class="episode-title">\${page.title}</h2>\`;
    if (page.text) html += \`<div class="content">\${embedBase64(page.text)}</div>\`;
    html += \`</div>\`;
});
html += \`</body></html>\`;
fs.writeFileSync('도면위의공유결합_출판투고용_최종본.html', html, 'utf8');

// Generate MD
let md = "# J-Journal: 도면 위의 공유결합 (최종본)\n\n";
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
fs.writeFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/도면위의공유결합_최종본.md', md, 'utf8');

