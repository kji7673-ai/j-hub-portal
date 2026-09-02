const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let part1 = [];
let part2Intro = [];
let theme1 = [];
let theme2 = [];
let theme3 = [];
let theme4 = [];
let bridges = {};
let part3 = [];
let appendices = [];
let other = [];

let currentTheme = 1;

for (let p of bookData.pages) {
    if (p.title) {
        p.title = p.title.replace(/\[\d+부.*?\]\s*/g, '');
        p.title = p.title.replace(/\[부록.*?\]\s*/g, '');
    }
    
    // Catch bridges explicitly
    if (p.title === "Theme 1을 마치며") { bridges[1] = p; continue; }
    if (p.title === "Theme 2를 마치며") { bridges[2] = p; continue; }
    if (p.title === "Theme 3을 마치며") { bridges[3] = p; continue; }
    if (p.title === "2부를 마치며" && p.partCategory === "2부: 철학편") { bridges[4] = p; continue; }

    // Catch AI log bracket styling specifically
    if (p.text) {
        p.text = p.text.replace(/\[J-Hub 코어: 아키 시냅스 시스템 로그\]/g, 'J-Hub 코어: 아키 시냅스 시스템 로그');
        p.text = p.text.replace(/<b>\[현장 스케치:\s*(.*?)\]<\/b>/g, '<strong style="color: var(--primary);">현장 스케치: $1</strong>');
        p.text = p.text.replace(/\[현장 스케치:\s*(.*?)\]/g, '<strong style="color: var(--primary);">현장 스케치: $1</strong>');
    }

    let cat = p.partCategory || p.part || "";
    let t = p.title || p.type || "";

    if (t.includes("테마 1") || t.includes("Theme 1")) currentTheme = 1;
    if (t.includes("테마 2") || t.includes("Theme 2")) currentTheme = 2;
    if (t.includes("테마 3") || t.includes("Theme 3")) currentTheme = 3;
    if (t.includes("테마 4") || t.includes("Theme 4")) currentTheme = 4;

    if (cat.includes("1부")) {
        // Fix undefined partCategory
        p.partCategory = "1부: 설계의 본질";
        part1.push(p);
    } else if (cat.includes("2부") || cat.includes("undefined")) {
        // Fix undefined for "1부를 마치며" and "2부를 마치며"
        if (t === "1부를 마치며" || t === "기록의 무게") {
            p.partCategory = "2부: 증언과 성찰";
            part2Intro.push(p);
        } else if (t === "2부를 마치며" && cat.includes("undefined")) {
            // Drop old undefined 2부를 마치며
            continue;
        } else {
            p.partCategory = "2부: 증언과 성찰";
            if (currentTheme === 1) theme1.push(p);
            else if (currentTheme === 2) theme2.push(p);
            else if (currentTheme === 3) theme3.push(p);
            else theme4.push(p);
        }
    } else if (cat.includes("3부")) {
        p.partCategory = "3부: 철학의 기술화";
        part3.push(p);
    } else if (cat.includes("부록")) {
        // deduplicate Prompts
        if (t === "자기 사고의 구조화 (마스터 프롬프트)") continue;
        p.partCategory = cat;
        if (!p.title.startsWith("부록")) p.title = "부록. " + p.title;
        appendices.push(p);
    } else {
        other.push(p);
    }
}

// Ensure proper prefixes for appendices
for (let p of appendices) {
    if (p.partCategory.includes("부록 A") && !p.title.includes("부록 A")) p.title = "부록 A. " + p.title.replace("부록. ", "");
    if (p.partCategory.includes("부록 B") && !p.title.includes("부록 B")) p.title = "부록 B. " + p.title.replace("부록. ", "");
    if (p.partCategory.includes("부록 C") && !p.title.includes("부록 C")) p.title = "부록 C. " + p.title.replace("부록. ", "");
}

// Assemble Part 2
let part2 = [...part2Intro, ...theme1, bridges[1], ...theme2, bridges[2], ...theme3, bridges[3], ...theme4, bridges[4]];

bookData.pages = [...part1, ...part2, ...part3, ...appendices, ...other];

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

// Print TOC to verify ordering
bookData.pages.forEach((p, i) => {
    console.log(`${i+1}. [${p.partCategory}] ${p.title || p.type}`);
});
