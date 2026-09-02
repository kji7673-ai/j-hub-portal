const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let part1 = [];
let part2Interlude = [];
let theme1 = [];
let theme2 = [];
let theme3 = [];
let theme4 = [];
let part3Interlude = [];
let part3Content = [];
let appendix = [];
let epilogue = [];

// Categorize pages
for (let p of bookData.pages) {
    let cat = p.partCategory || p.part || "";
    if (cat.includes("1부")) {
        part1.push(p);
    } else if (cat.includes("2부")) {
        if (p.type === 'interlude' || (p.title && (p.title.includes("1부를 마치며") || p.title.includes("2부 시작")))) {
            part2Interlude.push(p);
        } else if (p.partTitle && p.partTitle.includes("Theme 1")) {
            theme1.push(p);
        } else if (p.partTitle && p.partTitle.includes("Theme 2")) {
            theme2.push(p);
        } else if (p.partTitle && p.partTitle.includes("Theme 3")) {
            theme3.push(p);
        } else if (p.partTitle && p.partTitle.includes("Theme 4")) {
            theme4.push(p);
        } else {
            theme1.push(p); // safe fallback
        }
    } else if (cat.includes("3부")) {
        if (p.type === 'interlude' || (p.title && (p.title.includes("2부를 마치며") || p.title.includes("3부를 시작하며")))) {
            part3Interlude.push(p);
        } else {
            part3Content.push(p);
        }
    } else if (cat.includes("에필로그")) {
        epilogue.push(p);
    } else if (cat.includes("부록")) {
        appendix.push(p);
    } else {
        part1.push(p);
    }
}

// 1. Setup Part 2 (Sorted Themes + Bridges)
part2Interlude.push({
    "type": "text_only",
    "title": "[2부 시작] 기록의 무게",
    "text": "다음 70여 편의 에세이는 앞서 선언한 '공유결합 이론'이 현장에서 구체적으로 어떻게 무너지고, 어떻게 다시 세워지는지를 보여주는 생생한 증거입니다. 각 에세이는 하나의 판단의 순간, 신뢰가 깨지거나 회복되는 찰나를 기록했습니다. 이 치열한 기록들이 결국 어떤 시스템으로 응축되는지 지켜봐 주십시오.",
    "partCategory": "2부: 철학편"
});

let bridge1 = { "type": "text_only", "title": "Theme 1을 마치며", "text": "이러한 혹독한 자기성찰의 시간은, 결국 나 아닌 다른 이들—타인을 이해하기 위한 필연적인 통과의례였습니다. 이제 우리의 시선은 내면에서 현장의 타인들로 향합니다.", "partCategory": "2부: 철학편", "partTitle": "Theme 1. 자기성찰: 내면의 거울" };
let bridge2 = { "type": "text_only", "title": "Theme 2를 마치며", "text": "타인에 대한 깊은 이해조차도, 얽히고설킨 이권과 변수가 난무하는 실제 현장 앞에서는 무력해지곤 합니다. 다음은 그 혼란의 한가운데서 기록한 저항과 수용의 순간들입니다.", "partCategory": "2부: 철학편", "partTitle": "Theme 2. 타인이해: 관계의 렌즈" };
let bridge3 = { "type": "text_only", "title": "Theme 3을 마치며", "text": "수많은 혼란과 저항 속에서, 건축가가 끝까지 타협하지 않은 단 하나의 본질. 그것이 다음 장에서 펼쳐질 새로운 미래를 향한 신뢰와 다짐의 기반이 되었습니다.", "partCategory": "2부: 철학편", "partTitle": "Theme 3. 현장의 혼란: 리얼리티" };
let bridge4 = { "type": "text_only", "title": "2부를 마치며", "text": "수십 년간 쌓인 이 모든 판단과 신뢰의 순간들은, 이제 하나의 거대한 시스템 안에서 어떻게 형태를 갖추게 될까요? 그 해답을 3부에서 펼쳐 보입니다.", "partCategory": "2부: 철학편", "partTitle": "Theme 4. 신뢰의 순간: 관계의 결실" };

let part2 = [...part2Interlude, ...theme1, bridge1, ...theme2, bridge2, ...theme3, bridge3, ...theme4, bridge4];

// 2. Setup Part 3 (Meta Interpretation Layer)
part3Interlude.push({
    "type": "text_only",
    "title": "[3부 시작] 철학과 기술의 교차점",
    "text": "이제 우리는 앞서 2부에서 살펴본 70여 개의 에피소드에서 패턴을 찾아봅니다. 기술이 그 혼란과 감정을 포착할 수 있는가? 포착했다면, 완벽한 기계 앞에서 건축가의 역할은 어떻게 변하는가?<br><br>3부의 각 장은 2부의 테마들을 읽은 후 도달한 <b>'기술적 재해석'</b>입니다.",
    "partCategory": "3부: 미래와 비전"
});

let p3_ch1 = [{ "type": "chapter_content", "title": "제1장. 신뢰의 축적 (Theme 1 재해석)", "text": "테마 1의 자기성찰 에세이들에 나타난 '판단의 순간'들은 시스템 안에서 어떻게 구현되는가? J-Hub는 흔들리는 인간의 판단을 돕기 위해 '선택적 투명성'과 데이터의 축적을 설계했습니다.", "partCategory": "3부: 미래와 비전" }];
let p3_ch2 = [{ "type": "chapter_content", "title": "제2장. 불완전함의 깊이 (Theme 2 재해석)", "text": "테마 2에서 마주한 '타인과의 타협'은 완벽한 계산으로는 풀 수 없는 딜레마였습니다. 이 장에서는 인간의 직관과 불완전함이, 차가운 기술을 어떻게 보완하고 온기를 불어넣는지 확인합니다.", "partCategory": "3부: 미래와 비전" }];
let p3_ch3 = [{ "type": "chapter_content", "title": "제3장. 비판받을 용기 (Theme 3 재해석)", "text": "테마 3의 현장 혼란 속에서 건축가가 클라이언트·규제·기술 사이에서 선택했던 저항의 방식은, 이제 J-Hub의 리스크 방어 체계와 결정 알고리즘으로 기록되고 학습됩니다.", "partCategory": "3부: 미래와 비전" }];
let p3_ch4 = [{ "type": "chapter_content", "title": "제4장. 2035년을 준비하며 (Theme 4 재해석)", "text": "테마 4가 던진 미래 신호들에 대한 응답입니다. AI가 할 수 없는 것은 무엇이며, 그 속에서 건축가의 존엄은 어떻게 지켜지는가. 기술의 시대에 던지는 다섯 가지 다짐입니다.", "partCategory": "3부: 미래와 비전" }];

let totalP3 = part3Content.length;
for (let i=0; i<totalP3; i++) {
    let p = part3Content[i];
    p.partCategory = "3부: 미래와 비전";
    if(p.title) p.title = p.title.replace(/제\d장\.\s*/, '');
    
    // Distribute remaining tech content into the 4 meta chapters
    if (i < totalP3 * 0.25) p3_ch1.push(p);
    else if (i < totalP3 * 0.5) p3_ch2.push(p);
    else if (i < totalP3 * 0.75) p3_ch3.push(p);
    else p3_ch4.push(p);
}

// 3. Move purely structural/heavy tech diagrams to Appendix
let heavy_images = ["six_stages_timeline.jpg", "decision_flowchart.jpg", "orchestra_map.jpg", "kanban_board.jpg", "minefield_risk.jpg", "legal_shields.jpg"];
let final_p3_chunks = [p3_ch1, p3_ch2, p3_ch3, p3_ch4];

for (let chunk of final_p3_chunks) {
    for (let i=0; i<chunk.length; i++) {
        let p = chunk[i];
        if (p.image && heavy_images.some(img => p.image.includes(img))) {
            let app_page = {...p};
            app_page.partCategory = "부록: 시스템 가이드 및 체크리스트";
            if(app_page.part) delete app_page.part;
            appendix.push(app_page);
            chunk.splice(i, 1);
            i--;
        }
    }
}

if (appendix.length > 0) {
    appendix.unshift({
        "type": "interlude",
        "title": "부록. J-Hub 기술 상세 및 프롬프트",
        "text": "본문에서 다루지 못한 J-Hub의 구체적인 시스템 플로우차트와 기술적 상세 가이드, 그리고 실무에서 활용 가능한 체크리스트를 수록합니다.",
        "partCategory": "부록: 시스템 가이드 및 체크리스트"
    });
}

let part3 = [...part3Interlude, ...p3_ch1, ...p3_ch2, ...p3_ch3, ...p3_ch4];

// Merge everything
let finalPages = [...part1, ...part2, ...part3, ...epilogue, ...appendix];
bookData.pages = finalPages;

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
