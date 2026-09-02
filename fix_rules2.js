const fs = require('fs');

// 2. Fix book_data.js (Rule 2 & 4)
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let currentPart = "프롤로그";
bookData.pages.forEach(p => {
    let t = p.title || "";
    
    // Determine TOC part based on title markers
    if (t.includes("프롤로그:") || t === "도면 위의 공유결합") {
        currentPart = "프롤로그";
    } else if (t === "1부. 설계의 본질 – 공유결합") {
        currentPart = "1부. 설계의 본질 – 공유결합";
    } else if (t === "2부. 현장의 목소리, 공유결합의 증거") {
        currentPart = "2부. 현장의 목소리, 공유결합의 증거";
    } else if (t === "중간 장. 기계를 거부하지 않기로 결심한 날") {
        currentPart = "중간 장. 전환점";
    } else if (t === "철학의 기술화" || t.includes("제1장. 신뢰를 기록하다")) {
        currentPart = "3부. 공유결합의 완성, J-Hub";
    } else if (t.includes("에필로그") || t === "제4장. 다시, 신발을 신다 (에필로그)") {
        currentPart = "에필로그";
    } else if (t.includes("부록")) {
        currentPart = "부록";
    }
    
    // Check if it's the specific bridges to rewrite (Rule 2)
    if (t === "제2장. 현장에서 배운 것들" && p.type === "bridge") {
        p.text = "오늘의 내가 26년 전 현장의 진흙탕을 다시 들여다본다.<br><br>시공자와의 갈등, 주민들과의 만남, 피할 수 없었던 수많은 타협의 순간들 속에서<br>나는 비로소 '공유결합'의 진짜 의미를 온몸으로 깨달아가고 있었다.";
    }
    if (t === "제3장. 26년의 신뢰 기록" && p.type === "bridge") {
        p.text = "수많은 밤을 지새우며 억울함과 두려움을 삼켜내야 했던 과거의 나를 가만히 바라본다.<br><br>완벽함이 아닌 나의 불완전함을 스스로 인정했을 때,<br>비로소 내 곁의 사람들이 그 빈자리를 채워주며 현장에는 진짜 신뢰가 싹트기 시작했다.";
    }
    if (t === "어느 날, 공유결합이 내게로 왔다" && p.text) {
        // Just make sure it starts nicely if we want to enforce the tone
        // Not rewriting entire essays right now to avoid messing up the good ones, 
        // but applying to major intros if they conflict.
    }
    
    // Enforce currentPart onto the page
    if (p.type !== "author_profile") {
        p.partCategory = currentPart;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

