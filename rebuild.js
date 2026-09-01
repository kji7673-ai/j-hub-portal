const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
const pages = bookData.pages;

// Helper to find index ranges
function findIndexByTitle(titleFragment) {
    return pages.findIndex(p => p.title && p.title.includes(titleFragment));
}
function findIndexByPart(partFragment) {
    return pages.findIndex(p => p.part && p.part.includes(partFragment));
}

// We need to carefully split the existing pages into blocks.
// The array currently contains:
// 0: Cover
// ...
// 284: image_full
// 285: 4부 interlude
// 286: 4부 1장
// 287: 4부 2장
// 288: 4부 3장
// 289: 4부 4장
// 290: 4부 5장
// 291: 부록 cover ...

// Let's manually reconstruct based on the exact structure we know.
let newPages = [];

// [0] Cover
newPages.push(pages[0]);

// --- NEW PART 1 ---
newPages.push({
    "type": "interlude",
    "title": "1부. 프롭테크와 정비사업의 미래 (비전)",
    "image": "static/images/15.jpg",
    "part": "1부: 프롭테크와 정비사업의 미래"
});
// 4부 1~4장 (Indices 286 to 289)
for(let i = 286; i <= 289; i++) {
    let p = Object.assign({}, pages[i]);
    p.part = "1부: 프롭테크와 정비사업의 미래";
    newPages.push(p);
}
// 1부 프롤로그 (We need to find it. It's in the original 1부)
// original 1부 starts at index 1 (image_full) then index 2 (interlude 1부).
// wait, looking at my previous list:
// [1] image_full
// [2] 1부 interlude
// [3] image_full
// [4] 프롤로그 (let's assume it's index 4)
let progIdx = pages.findIndex(p => p.title && p.title.includes('프롤로그'));
if(progIdx !== -1) {
    let p = Object.assign({}, pages[progIdx]);
    p.part = "1부: 프롭테크와 정비사업의 미래";
    if(pages[progIdx-1].type === 'image_full') newPages.push(pages[progIdx-1]);
    newPages.push(p);
}

// --- NEW PART 2 ---
newPages.push({
    "type": "interlude",
    "title": "2부. J-Hub 플랫폼 마스터플랜 (실전)",
    "image": "static/images/05.jpg",
    "part": "2부: J-Hub 플랫폼 마스터플랜"
});
// The rest of old 1부 and all of old 2부.
// 1부 starts around index 5 (after prologue). 2부 ends just before 3부 (which starts around index 40? let's find 3부 interlude)
let part3InterludeIdx = pages.findIndex(p => p.type === 'interlude' && p.title && p.title.includes('3부'));
let startPart2 = progIdx + 1; // skip prologue
for(let i = startPart2; i < part3InterludeIdx; i++) {
    // skip any old interludes if they got caught
    if(pages[i].type === 'interlude' && pages[i].title && (pages[i].title.includes('1부') || pages[i].title.includes('2부'))) continue;
    let p = Object.assign({}, pages[i]);
    if(p.part && (p.part.includes('1부') || p.part.includes('2부'))) {
        p.part = "2부: J-Hub 플랫폼 마스터플랜";
    }
    newPages.push(p);
}

// --- NEW PART 3 ---
newPages.push({
    "type": "interlude",
    "title": "3부. 정비나침반 실행 로드맵 (비즈니스)",
    "image": "static/images/11.jpg",
    "part": "3부: 정비나침반 실행 로드맵"
});
// old 4부 5장 (Index 290)
let p5 = Object.assign({}, pages[290]);
p5.part = "3부: 정비나침반 실행 로드맵";
newPages.push(p5);

// --- NEW PART 4 ---
newPages.push({
    "type": "interlude",
    "title": "4부. 건축가, 인간을 짓다: 증언과 성찰",
    "image": "static/images/14.jpg",
    "part": "4부: 증언과 성찰"
});
// old 3부 (from part3InterludeIdx to index 284)
for(let i = part3InterludeIdx + 1; i <= 284; i++) {
    let p = Object.assign({}, pages[i]);
    if(p.part && p.part.includes('3부')) {
        p.part = "4부: 증언과 성찰";
    }
    newPages.push(p);
}

// --- APPENDIX ---
// from index 291 to end
for(let i = 291; i < pages.length; i++) {
    newPages.push(pages[i]);
}

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(newPages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Rebuild complete.");
