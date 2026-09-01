const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let pages = bookData.pages;

// Helper to find range of pages for a specific condition
// We'll just filter / move them around.

let newPages = [];

// 1. Cover
let cover = pages.shift(); // assuming first is cover
newPages.push(cover);

// 2. Part 1: 프롭테크와 정비사업의 미래 (Why)
newPages.push({
    "type": "interlude",
    "title": "1부. 프롭테크와 정비사업의 미래",
    "image": "static/images/15.jpg",
    "part": "1부: 프롭테크와 정비사업의 미래"
});

// old 4부 Ch 1~4
let old4buCh1_4 = pages.filter(p => p.part === "4부: 비전과 확장" && p.type !== "interlude" && p.title.includes("제5장") === false);
old4buCh1_4.forEach(p => { p.part = "1부: 프롭테크와 정비사업의 미래"; newPages.push(p); });

// old 1부 프롤로그
let old1buPrologue = pages.filter(p => p.part && p.part.includes("1부: 시스템편") && p.title && p.title.includes("프롤로그"));
old1buPrologue.forEach(p => { p.part = "1부: 프롭테크와 정비사업의 미래"; newPages.push(p); });

// 3. Part 2: J-Hub 플랫폼, 시스템과 현장의 혁신 (What & How)
newPages.push({
    "type": "interlude",
    "title": "2부. J-Hub 플랫폼, 시스템과 현장의 혁신",
    "image": "static/images/05.jpg",
    "part": "2부: J-Hub 플랫폼 마스터플랜"
});

// old 1부 remaining
let old1buRem = pages.filter(p => p.part && p.part.includes("1부: 시스템편") && (!p.title || !p.title.includes("프롤로그")));
// also need to grab the image_fulls that preceded them.
// Actually, it's safer to just iterate and move blocks.
// Let's do a simpler block move using indices.

