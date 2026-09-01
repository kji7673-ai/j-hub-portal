const fs = require('fs');
const vm = require('vm');
let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let pages = bookData.pages;

let coverPage = pages.find(p => p.type === 'image_full' && p.title === '도면 위에 머무는 시간');
let authorPage = pages.find(p => p.type === 'author_profile');
let prologuePage = pages.find(p => p.title && p.title.includes('프롤로그: 완벽한 시스템'));
let bridgePage = pages.find(p => p.title && p.title.includes('[브릿지]'));
let epilogue1 = pages.find(p => p.title && p.title.includes('에필로그: 26년의 경험'));
let epilogue2 = pages.find(p => p.title && p.title.includes('에필로그 2'));

let proptechChapters = [];
let manualChapters = [];
let diaryChapters = [];
let appendixChapters = [];

let currentPart = null;
pages.forEach(p => {
    if (p === coverPage || p === authorPage || p === prologuePage || p === bridgePage || p === epilogue1 || p === epilogue2) return;
    if (p.type === 'image_full' && p.title === '도면 위에 머무는 시간') return;
    if (p.title && p.title.includes('프롤로그: 완벽한 시스템')) return;
    if (p.type === 'author_profile') return;
    
    if (p.type === 'interlude') {
        if (p.title.includes('부록')) currentPart = 'appendix';
        else if (p.title.includes('프롭테크')) currentPart = 'proptech';
        else if (p.title.includes('마스터플랜')) currentPart = 'manual';
        else if (p.title.includes('증언과 성찰')) currentPart = 'diary';
        return;
    } 
    
    let titleStr = p.title || "";
    if (currentPart === 'proptech') proptechChapters.push(p);
    else if (currentPart === 'manual') manualChapters.push(p);
    else if (currentPart === 'diary') diaryChapters.push(p);
    else if (currentPart === 'appendix') appendixChapters.push(p);
    else {
        // Fallback mapping
        if (titleStr.includes('제1장') || titleStr.includes('제2장') || titleStr.includes('제3장') || titleStr.includes('제4장')) {
            proptechChapters.push(p);
        } else if (titleStr.includes('Part ')) {
            appendixChapters.push(p);
        } else {
            diaryChapters.push(p);
        }
    }
});

let finalPages = [];
if (coverPage) finalPages.push(coverPage);
if (authorPage) finalPages.push(authorPage);
if (prologuePage) finalPages.push(prologuePage);

finalPages.push({ "type": "interlude", "title": "1부. J-Hub 플랫폼 마스터플랜 (실전)", "image": "static/images/13.jpg", "part": "1부: 플랫폼 마스터플랜" });
manualChapters.forEach(p => { p.partCategory = "1부: 플랫폼 마스터플랜"; finalPages.push(p); });

if (bridgePage) finalPages.push(bridgePage);

finalPages.push({ "type": "interlude", "title": "2부. 건축가, 인간을 짓다: 증언과 성찰", "image": "static/images/14.jpg", "part": "2부: 증언과 성찰" });
diaryChapters.forEach(p => { p.partCategory = "2부: 증언과 성찰"; finalPages.push(p); });

finalPages.push({ "type": "interlude", "title": "3부. 프롭테크와 정비사업의 미래 (비전)", "image": "static/images/12.jpg", "part": "3부: 미래와 비전" });
proptechChapters.forEach(p => { p.partCategory = "3부: 미래와 비전"; finalPages.push(p); });

if (epilogue1) finalPages.push(epilogue1);
if (epilogue2) finalPages.push(epilogue2);

finalPages.push({ "type": "interlude", "title": "[부록] J-Hub 플랫폼 마스터플랜 원본 (SRD)", "image": "static/images/15.jpg", "part": "부록" });
appendixChapters.forEach(p => { p.partCategory = "부록"; finalPages.push(p); });

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(finalPages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Success! Final pages:", finalPages.length);
