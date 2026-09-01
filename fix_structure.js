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

let part1 = [];
let part2 = [];
let part3 = [];
let appendix = [];

pages.forEach(p => {
    if (p === coverPage || p === authorPage || p === prologuePage || p === bridgePage || p === epilogue1 || p === epilogue2) return;
    if (p.type === 'image_full' && p.title === '도면 위에 머무는 시간') return;
    if (p.title && p.title.includes('프롤로그: 완벽한 시스템')) return;
    if (p.type === 'author_profile') return;
    if (p.type === 'interlude') return;

    let title = p.title || "";
    
    // PART 3 (PropTech)
    if (title.includes("'깜깜이' 정비사업의 종언") ||
        title.includes("서울시 정비사업 유형별") ||
        title.includes("협력사 에코시스템과 정비사업의 팀플레이") ||
        title.includes("리스크 관리와 법률 쟁점")) {
        part3.push(p);
        return;
    }

    // APPENDIX
    if (title.startsWith('Part A.') || title.startsWith('Part B.') || title.startsWith('Part C.') ||
        title.startsWith('Part D.') || title.startsWith('Part E.') || title.startsWith('Part F.') ||
        title.startsWith('Part G.') || title.startsWith('부록:') || title.startsWith('[부록]') ||
        title.startsWith('QR코드:') || title.includes('쟁이의 마음:') || title.includes('마치는 글:')) {
        appendix.push(p);
        return;
    }
    
    // PART 1
    if (title.match(/^[0-9]+장\./) || // 1장. ~ 13장.
        title.includes('[막간]') || title.includes('막간극') ||
        title.includes('[통찰]') || title.includes('💡') ||
        title.includes('액션 1:') || title.includes('액션 2:') || title.includes('액션 3:') ||
        title.includes('[코멘터리]')) {
        part1.push(p);
        return;
    }
    
    // PART 2
    part2.push(p);
});

let finalPages = [];
if (coverPage) finalPages.push(coverPage);
if (authorPage) finalPages.push(authorPage);
if (prologuePage) finalPages.push(prologuePage);

finalPages.push({ "type": "interlude", "title": "1부. J-Hub 플랫폼 마스터플랜 (실전)", "image": "static/images/13.jpg", "part": "1부: 플랫폼 마스터플랜" });
part1.forEach(p => { p.partCategory = "1부: 플랫폼 마스터플랜"; finalPages.push(p); });

if (bridgePage) finalPages.push(bridgePage);

finalPages.push({ "type": "interlude", "title": "2부. 건축가, 인간을 짓다: 증언과 성찰", "image": "static/images/14.jpg", "part": "2부: 증언과 성찰" });
part2.forEach(p => { p.partCategory = "2부: 증언과 성찰"; finalPages.push(p); });

finalPages.push({ "type": "interlude", "title": "3부. 프롭테크와 정비사업의 미래 (비전)", "image": "static/images/12.jpg", "part": "3부: 미래와 비전" });
part3.forEach(p => { p.partCategory = "3부: 미래와 비전"; finalPages.push(p); });

if (epilogue1) finalPages.push(epilogue1);
if (epilogue2) finalPages.push(epilogue2);

finalPages.push({ "type": "interlude", "title": "[부록] J-Hub 플랫폼 마스터플랜 원본 (SRD)", "image": "static/images/15.jpg", "part": "부록" });
appendix.forEach(p => { p.partCategory = "부록"; finalPages.push(p); });

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(finalPages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Part 1 count:", part1.length);
console.log("Part 2 count:", part2.length);
