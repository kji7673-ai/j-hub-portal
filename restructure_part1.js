const fs = require('fs');

// Read book data
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const pages = bookData.pages;

// Titles of pages to move
const toChapter2 = [
    "찢어진 운동화",
    "뇌물이 괴물이 된다",
    "'조은 슈퍼'"
];

const toChapter3 = [
    "우리가 이렇게 살아갑니다",
    "삼켜낸 말과 술 한 잔",
    "난 약한 사람입니다"
];

// Find original indices
const chapter2Pages = [];
const chapter3Pages = [];

const remainingPages = [];

// Separate out the pages to move
pages.forEach(p => {
    if (toChapter2.includes(p.title)) {
        chapter2Pages.push({...p, partCategory: "1부. 설계의 본질 – 공유결합"});
    } else if (toChapter3.includes(p.title)) {
        chapter3Pages.push({...p, partCategory: "1부. 설계의 본질 – 공유결합"});
    } else {
        remainingPages.push(p);
    }
});

// Reconstruct
const newPages = [];
let part1Done = false;

remainingPages.forEach(p => {
    // Inject just before "1부를 마치며" or at end of part 1
    if (!part1Done && p.title === "1부를 마치며") {
        
        // Add Chapter 2 Bridge
        newPages.push({
            type: "bridge",
            title: "제2장. 현장에서 배운 것들",
            text: "시공자와의 갈등, 주민들과의 만남, 그리고 피할 수 없는 타협의 순간들.<br>현장의 진흙탕 속에서 비로소 '공유결합'의 진짜 의미를 깨닫다.",
            partCategory: "1부. 설계의 본질 – 공유결합"
        });
        
        chapter2Pages.forEach(cp => newPages.push(cp));
        
        // Add Chapter 3 Bridge
        newPages.push({
            type: "bridge",
            title: "제3장. 26년의 신뢰 기록",
            text: "완벽함이 아닌 불완전함을 인정할 때 비로소 싹트는 것.<br>수많은 밤을 지새우며 삼켜냈던 감정들과, 그 빈자리를 채워준 사람들의 이야기.",
            partCategory: "1부. 설계의 본질 – 공유결합"
        });
        
        chapter3Pages.forEach(cp => newPages.push(cp));
        
        part1Done = true;
        
        // Add the "1부를 마치며"
        newPages.push(p);
    } else {
        newPages.push(p);
    }
});

// Update partCategory for all part 1 elements to match exactly
let currentPart = "프롤로그";
newPages.forEach(p => {
    if (p.title === "1부. 설계의 본질 – 공유결합") currentPart = "1부. 설계의 본질 – 공유결합";
    if (p.title === "2부. 현장의 목소리, 공유결합의 증거") currentPart = "2부. 현장의 목소리, 공유결합의 증거";
    //...
    
    // Actually, just let it be. The moved ones already have partCategory updated.
});


bookData.pages = newPages;

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

console.log("Moved chapter 2 items: " + chapter2Pages.map(p=>p.title).join(", "));
console.log("Moved chapter 3 items: " + chapter3Pages.map(p=>p.title).join(", "));
