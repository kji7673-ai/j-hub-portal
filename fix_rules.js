const fs = require('fs');

// 1. Fix HTML rendering colors (Rule 1)
let html = fs.readFileSync('index.html', 'utf8');

// Replace dark mode in cover/interlude
html = html.replace(/pageEl\.style\.backgroundColor = '#1d1d1f';\s*pageEl\.style\.color = '#ffffff';/g, "pageEl.style.backgroundColor = '#ffffff';\n                    pageEl.style.color = '#1d1d1f';");

// Remove text-shadow for white text, change color to ink
html = html.replace(/text-shadow: 0 4px 15px rgba\(0,0,0,0\.8\); color: rgba\(255,255,255,0\.9\);/g, "color: rgba(29,29,31,0.9);");
html = html.replace(/color:#ffffff;/g, "color:#1d1d1f;");
html = html.replace(/color:rgba\(255,255,255,0\.5\);/g, "color:rgba(29,29,31,0.5);");
html = html.replace(/text-shadow: 0 4px 15px rgba\(0,0,0,0\.9\);/g, "");
html = html.replace(/text-shadow: 0 2px 10px rgba\(0,0,0,0\.5\);/g, "");
html = html.replace(/text-shadow: 0 2px 8px rgba\(0,0,0,0\.8\);/g, "");

// Bridge radial gradient update
html = html.replace(/background: radial-gradient\(circle at center, #2a2a2c 0%, #1d1d1f 100%\);/g, "background: radial-gradient(circle at center, #ffffff 0%, #f5f5f7 100%);");

// Cover linear gradient update (make it light instead of dark)
html = html.replace(/background: linear-gradient\(to bottom, rgba\(29,29,31,0\.2\) 0%, rgba\(29,29,31,0\.8\) 100%\);/g, "background: linear-gradient(to bottom, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.9) 100%);");
html = html.replace(/background: linear-gradient\(to bottom, rgba\(29,29,31,0\.1\) 0%, rgba\(29,29,31,0\.85\) 100%\);/g, "background: linear-gradient(to bottom, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.95) 100%);");

// Fix body text color in image_full
html = html.replace(/color: rgba\(255,255,255,0\.9\); font-weight: 400;/g, "color: #1d1d1f; font-weight: 400;");
html = html.replace(/<strong style="color: #ffffff;">/g, '<strong style="color: #1d1d1f;">');

fs.writeFileSync('index.html', html, 'utf8');

// 2. Fix book_data.js (Rule 2 & 4)
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let currentPart = "프롤로그";
bookData.pages.forEach(p => {
    // Determine TOC part based on title markers
    if (p.title.includes("프롤로그:") || p.title === "도면 위의 공유결합") {
        currentPart = "프롤로그";
    } else if (p.title === "1부. 설계의 본질 – 공유결합") {
        currentPart = "1부. 설계의 본질 – 공유결합";
    } else if (p.title === "2부. 현장의 목소리, 공유결합의 증거") {
        currentPart = "2부. 현장의 목소리, 공유결합의 증거";
    } else if (p.title === "중간 장. 기계를 거부하지 않기로 결심한 날") {
        currentPart = "중간 장. 전환점";
    } else if (p.title === "철학의 기술화" || p.title.includes("제1장. 신뢰를 기록하다")) {
        currentPart = "3부. 공유결합의 완성, J-Hub";
    } else if (p.title.includes("에필로그")) {
        currentPart = "에필로그";
    } else if (p.title.includes("부록")) {
        currentPart = "부록";
    }
    
    // Check if it's the specific bridges to rewrite (Rule 2)
    if (p.title === "제2장. 현장에서 배운 것들" && p.type === "bridge") {
        p.text = "오늘의 내가 26년 전 현장의 진흙탕을 다시 들여다본다.<br><br>시공자와의 갈등, 주민들과의 만남, 피할 수 없었던 수많은 타협의 순간들 속에서<br>나는 비로소 '공유결합'의 진짜 의미를 온몸으로 깨달아가고 있었다.";
    }
    if (p.title === "제3장. 26년의 신뢰 기록" && p.type === "bridge") {
        p.text = "수많은 밤을 지새우며 억울함과 두려움을 삼켜내야 했던 과거의 나를 가만히 바라본다.<br><br>완벽함이 아닌 나의 불완전함을 스스로 인정했을 때,<br>비로소 내 곁의 사람들이 그 빈자리를 채워주며 현장에는 진짜 신뢰가 싹트기 시작했다.";
    }
    
    // Enforce currentPart onto the page
    if (p.type !== "author_profile") {
        p.partCategory = currentPart;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

