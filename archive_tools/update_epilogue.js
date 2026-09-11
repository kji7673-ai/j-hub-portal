const fs = require('fs');
const vm = require('vm');
const path = require('path');

const code = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(code);
const context = {};
vm.createContext(context);
script.runInContext(context);

let pages;
if (Array.isArray(context.bookData)) {
    pages = context.bookData;
} else if (context.bookData && context.bookData.pages) {
    pages = context.bookData.pages;
}

const newEpilogueText = `건축을 하며 수없이 많은 날 동안 무수한 선을 그었습니다.<br>
종이 위에서 그었던 그 선들은 어떨 때는 사람과 사람을 잇는 '연결의 선'이 되기도 했고, 어떨 때는 저를 지독한 '외톨이로 만드는 선'이 되기도 했습니다.<br><br>
처음 졸업을 하고 직장 생활을 시작할 때만 해도, 저 역시 남들처럼 '유명한 건축가'가 되고 싶었고 번듯한 '작품집'도 내고 싶었습니다.<br>
하지만 현실은 그저 팍팍한 세상살이를 버텨내는 것만으로도 힘겨웠습니다.<br><br>
그래도 묵묵히 설계를 하며 저만의 흔들리지 않는 기준 하나를 붙잡은 것이 바로 '공유결합'입니다.<br>
이 단어는 제가 설계하며 만나는 사람과 상황, 그리고 수많은 계획안을 풀어내는 저만의 해답이 되었습니다.<br>
동료나 후배분들도 이미 현장에서 몸으로 다 알고 계실 내용이겠지만, 그래도 우리가 치열하게 버텨낸 이 과정들이 하나의 작은 이론으로라도 남겨지면 좋겠다는 마음에 용기를 내었습니다.<br><br>
거기에 더해, 도면 밖의 현실에서 짊어져야 했던 삶의 무게와 정체성의 혼란, 사람과의 관계 속에서 겪었던 뼈아픈 갈등들도 함께 엮었습니다.<br><br>
애초에 어떤 거창한 의도를 가지고 쓴 글들이 아닙니다.<br>
그저 가슴에 담아두기가 너무 힘겨워, 마음속에 맺힌 것들을 하나씩 덜어내는 심정으로 적어 내려간 글들이라 세상에 내놓기가 몹시 부끄럽습니다.<br><br>
하지만 도면 위에 그었던 그 모든 선들이, 결국 사람과 사람을 연결하는 선이 되길 진심으로 바랍니다.<br>
혹은 누군가에게 그 선이 '내가 혼자가 아니구나'라는 따뜻한 확인이 되어줄 수 있다면, 저의 26년 도면 위의 여정은 이제 당신의 손에서 아름답게 이어질 것입니다.`;

let modified = false;

// 에필로그 찾아서 덮어쓰기
pages.forEach(p => {
    if (p.title && p.title.includes('에필로그')) {
        p.text = newEpilogueText;
        modified = true;
    }
});

if (modified) {
    let finalData = { pages: pages };
    const outputString = 'var bookData = ' + JSON.stringify(finalData, null, 4) + ';';
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

    pages.forEach(page => {
        if (!page.title && !page.text && !page.image) return;
        html += \`<div class="page">\`;
        if (page.partCategory) html += \`<div class="category">\${page.partCategory}</div>\`;
        if (page.title) html += \`<h2 class="episode-title">\${page.title}</h2>\`;
        let contentHtml = "";
        if (page.image) contentHtml += \`<img src="\${page.image}"><br>\`;
        if (page.text) contentHtml += page.text;
        html += \`<div class="content">\${embedBase64(contentHtml)}</div>\`;
        html += \`</div>\`;
    });
    html += \`</body></html>\`;
    fs.writeFileSync('도면위의공유결합_출판투고용_최종본.html', html, 'utf8');
}
