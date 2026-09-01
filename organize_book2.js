const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

let pages = bookData.pages;

// 1. Identify specific singular pages to avoid duplicates
let coverPage = pages.find(p => p.type === 'image_full' && p.title === '도면 위에 머무는 시간');
let authorPage = pages.find(p => p.type === 'author_profile');
let prologuePage = pages.find(p => p.title && p.title.includes('프롤로그: 완벽한 시스템'));
let bridgePage = pages.find(p => p.title && p.title.includes('[브릿지]'));
let epilogue1 = pages.find(p => p.title && p.title.includes('에필로그: 26년의 경험'));
let epilogue2 = pages.find(p => p.title && p.title.includes('에필로그 2'));

// 2. Identify chapters
let proptechChapters = [];
let manualChapters = [];
let diaryChapters = [];
let appendixChapters = [];

let currentPart = null;
let seenTitles = new Set();

pages.forEach(p => {
    // Skip the singular ones we already extracted
    if (p === coverPage || p === authorPage || p === prologuePage || p === bridgePage || p === epilogue1 || p === epilogue2) return;
    
    // Skip the exact duplicate cover and prologue (since they appear multiple times in the array)
    if (p.type === 'image_full' && p.title === '도면 위에 머무는 시간') return;
    if (p.title && p.title.includes('프롤로그: 완벽한 시스템')) return;
    if (p.type === 'author_profile') return;
    
    // Process interludes to switch currentPart
    if (p.type === 'interlude') {
        if (p.title.includes('프롭테크') || p.title.includes('1부')) currentPart = 'proptech';
        else if (p.title.includes('마스터플랜') || p.title.includes('2부')) currentPart = 'manual';
        else if (p.title.includes('증언과 성찰') || p.title.includes('3부')) currentPart = 'diary';
        else if (p.title.includes('부록')) currentPart = 'appendix';
        return; // We don't push interludes; we recreate them
    } 
    
    // All other pages are chapter content
    let titleStr = p.title || "";
    if (currentPart === 'proptech') proptechChapters.push(p);
    else if (currentPart === 'manual') manualChapters.push(p);
    else if (currentPart === 'diary') diaryChapters.push(p);
    else if (currentPart === 'appendix') appendixChapters.push(p);
    else {
        // Fallback if currentPart wasn't set properly
        if (titleStr.includes('제1장') || titleStr.includes('제2장') || titleStr.includes('제3장') || titleStr.includes('제4장')) {
            proptechChapters.push(p);
        } else if (titleStr.includes('부록 세부항목') || titleStr.includes('Part ')) {
            appendixChapters.push(p);
        } else if (titleStr.includes('1장.') || titleStr.includes('2장.') || titleStr.includes('3장.') || titleStr.includes('4장.')) {
            diaryChapters.push(p);
        } else {
            diaryChapters.push(p);
        }
    }
});

let finalPages = [];
if (coverPage) finalPages.push(coverPage);
if (authorPage) finalPages.push(authorPage);
if (prologuePage) finalPages.push(prologuePage);

// 1. MANUAL (The Birth of J-Hub)
finalPages.push({
    "type": "interlude",
    "title": "1부. J-Hub 플랫폼 마스터플랜 (실전)",
    "image": "static/images/13.jpg",
    "part": "1부: 플랫폼 마스터플랜"
});
manualChapters.forEach(p => { p.partCategory = "1부: 플랫폼 마스터플랜"; finalPages.push(p); });

// Bridge here to transition
if (bridgePage) finalPages.push(bridgePage);

// 2. DIARY (Human vs Machine)
finalPages.push({
    "type": "interlude",
    "title": "2부. 건축가, 인간을 짓다: 증언과 성찰",
    "image": "static/images/14.jpg",
    "part": "2부: 증언과 성찰"
});
diaryChapters.forEach(p => { p.partCategory = "2부: 증언과 성찰"; finalPages.push(p); });

// 3. PROPTECH (Future Vision)
finalPages.push({
    "type": "interlude",
    "title": "3부. 프롭테크와 정비사업의 미래 (비전)",
    "image": "static/images/12.jpg",
    "part": "3부: 미래와 비전"
});
proptechChapters.forEach(p => { p.partCategory = "3부: 미래와 비전"; finalPages.push(p); });

if (epilogue1) finalPages.push(epilogue1);
if (epilogue2) finalPages.push(epilogue2);

// APPENDIX
finalPages.push({
    "type": "interlude",
    "title": "[부록] J-Hub 플랫폼 비즈니스 로드맵 및 시스템 아키텍처",
    "image": "static/images/15.jpg",
    "part": "부록"
});
appendixChapters.forEach(p => { p.partCategory = "부록"; finalPages.push(p); });

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(finalPages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Success! Final pages:", finalPages.length);
