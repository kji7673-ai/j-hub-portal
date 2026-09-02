const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// We will keep Part 1 and Part 2 untouched.
let newPages = [];
let part3Raw = [];
let appendixRaw = [];

// Separate existing pages
for (let p of bookData.pages) {
    let cat = p.partCategory || p.part || "";
    if (cat.includes("1부") || cat.includes("2부")) {
        newPages.push(p);
    } else {
        // Collect everything else to recycle their contents if needed
        part3Raw.push(p);
    }
}

// Function to find existing text chunks
function findText(keyword) {
    for (let p of part3Raw) {
        if (p.text && p.text.includes(keyword)) return p;
        if (p.title && p.title.includes(keyword)) return p;
    }
    return null;
}

// Extract specific existing content
let techPhase = findText("Phase 0");
let techTwoTrack = findText("투 트랙");
let tech6Paths = findText("6가지");
let techScenarios = findText("시나리오");
let techResolves = findText("다섯 가지");
let techPrompts = findText("프롬프트");
let epilogueOld = findText("마지막 1%");

const createAIPanel = (text) => `\n\n<div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);" class="handwriting">\n<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[아키 시냅스의 반론]</h4>\n${text}\n</div>`;

// Build New Part 3
let newPart3 = [];
newPart3.push({
    "type": "text_only",
    "title": "[3부 시작] 기술은 철학을 이기지 못한다",
    "text": "기술이 우리를 지배하면 '쓸모없는 건축가'가 되지만, 기술이 우리를 돕게 하면 '더 나은 건축가'가 됩니다.<br><br>이제 우리는 2부에서 배운 그 치열한 '불완전함'을 기술의 언어로 번역하는 과정을 마주하게 될 것입니다. 3부는 J-Hub라는 시스템이 어떻게 인간의 불완전함을 겸허히 받아들이고, 가장 인간다운 건축을 완성하도록 돕는지에 대한 기록입니다.",
    "partCategory": "3부: 철학의 기술화"
});

newPart3.push({
    "type": "chapter_content",
    "title": "제1장. 신뢰를 기록하다",
    "text": "J-Hub의 존재 이유는 '업무의 자동화'가 아니라 '투명성과 책임의 기록'에 있습니다. 우리는 2부의 에세이들을 통해 수많은 의심과 갈등이 빚어내는 비극을 보았습니다. 기계는 계산할 수 없는 마음들을 위로하기 위해, 역설적으로 가장 투명하고 차가운 데이터를 제시합니다. \n\n이 시스템은 묻습니다. 기술이 모든 것을 투명하게 보여줄 때, 그 투명성을 해석하고 설득하는 책임은 누구에게 있는가? 그것은 결국 현장에서 흙먼지를 마셔본 자의 몫입니다." + 
    createAIPanel("<b>아키 시냅스 (AI):</b><br>\"나는 완벽하고 투명한 데이터를 실시간으로 제시합니다.<br>그러나 그 데이터를 현장의 맥락으로 해석하는 것,<br>그리고 그 결정으로 파생되는 눈물과 기쁨에 책임지는 것은 오직 당신(인간)입니다.\""),
    "partCategory": "3부: 철학의 기술화"
});

newPart3.push({
    "type": "chapter_content",
    "title": "제2장. 불완전함을 설계하다",
    "text": "완벽한 시스템은 때로 가장 위험한 함정이 됩니다. 모든 것을 숫자로 치환하려는 시도는 인간의 본질을 지워버립니다. J-Hub는 '선택적 투명성'이라는 경계를 두어 데이터와 윤리 사이의 균형을 맞춥니다.\n\n기계가 결코 풀 수 없는 4가지가 있습니다.\n1. <b>같은 금액의 다른 무게:</b> 시스템의 2억 5천만 원은 그저 숫자지만, 조합원에게는 평생의 피땀입니다.\n2. <b>투명성에 따르는 책임:</b> 공개된 정보가 갈등의 무기가 되지 않도록 조율하는 윤리적 판단.\n3. <b>감정이 빠진 결정의 외로움:</b> 기계는 최적해를 내놓고 돌아서지만, 사람은 그 결정의 여파를 껴안고 밤을 지새웁니다.\n4. <b>미래의 가치:</b> 과거의 데이터로 학습된 AI는 100년 뒤의 기억과 가치를 상상하지 못합니다." +
    createAIPanel("<b>아키 시냅스 (AI):</b><br>\"나는 0.1초 만에 가장 효율적인 최적해를 연산합니다.<br>그러나 현장의 수많은 욕망 속에서 무엇이 진정한 '정의(Justice)'인지 판단하는 알고리즘은 나에게 없습니다. 그것은 불완전한 당신만이 할 수 있습니다.\""),
    "partCategory": "3부: 철학의 기술화"
});

let ch3Text = "현장의 복잡한 얽힘 속에서, J-Hub는 다양한 길을 제시합니다. 재개발, 재건축, 리모델링 등 수많은 선택지가 지도 위에 펼쳐집니다.\n\n2035년을 향해 가는 길목에서 우리는 세 가지 시나리오를 마주합니다. 기술이 모든 것을 지배하는 디스토피아, 기술을 거부하다 도태되는 실패, 그리고 인간과 기술이 완벽한 공유결합을 이루는 조화.\n\n건축가는 기계의 제안을 맹신하지 않고, 자신의 철학으로 최종 결단을 내리기 위해 다섯 가지 다짐을 가슴에 새깁니다. 기술은 제안할 뿐, 결정은 인간이 합니다.";
if (tech6Paths) ch3Text += "\n\n" + tech6Paths.text;
if (techScenarios) ch3Text += "\n\n" + techScenarios.text;
if (techResolves) ch3Text += "\n\n" + techResolves.text;

newPart3.push({
    "type": "chapter_content",
    "title": "제3장. 판단하는 건축가가 되다",
    "text": ch3Text + createAIPanel("<b>아키 시냅스 (AI):</b><br>\"나는 모든 가능한 시나리오와 발생할 수 있는 리스크를 빠짐없이 보여줄 수 있습니다.<br>하지만 최종적으로 도면 위에 선을 긋고, 그 무거운 결과에 책임을 지는 것은 언제나 당신입니다.\""),
    "partCategory": "3부: 철학의 기술화",
    "image": tech6Paths ? tech6Paths.image : null
});

newPart3.push({
    "type": "text_only",
    "title": "제4장. 다시, 신발을 신다 (에필로그)",
    "text": "기술은 우리가 신는 신발을 훨씬 편하게 개선해 주었지만, 결국 어느 방향으로 걸어갈지는 여전히 사람이 결정해야 합니다.\n\nJ-Hub가 99%의 완벽한 데이터를 제공하더라도, 건축을 최종적으로 완성하는 것은 결국 인간의 불완전한 1%입니다. 기계와의 26년 협업에서 얻은 진짜 깨달음은, 기술이 우리를 흠결 없는 완벽한 존재로 만들어 주는 것이 아니라는 점이었습니다.\n\n오히려 기술은 우리의 불완전함을 겸허히 받아들이게 하고, 기계가 할 수 없는 그 따뜻한 온기의 영역(타인에 대한 공감, 책임감, 윤리)에 집중하게 함으로써 우리를 더욱 '인간다운 건축가'로 만들어 줍니다.\n\n그 완벽하지 않은 여정의 끝에서, 다시 한번 먼지 묻은 신발 끈을 고쳐 매고 현장으로 향합니다. 우리의 시간이 온전히 사람의 것이 되기를 기원하며.",
    "partCategory": "3부: 철학의 기술화"
});

// Appendices
let newApp = [];

// App A
newApp.push({
    "type": "interlude",
    "title": "[부록 A] J-Hub 기술 개요",
    "text": "본서는 철학적 결합에 집중하기 위해 순수 기술 가이드를 부록으로 분리했습니다. J-Hub 시스템의 'Phase 0~5'와 '투 트랙(Two-Track) 시스템' 등 구체적인 기술 스펙에 관심 있는 독자들을 위한 개요입니다.",
    "partCategory": "부록 A: J-Hub 기술 개요"
});
if (techPhase) { techPhase.partCategory = "부록 A: J-Hub 기술 개요"; newApp.push(techPhase); }
if (techTwoTrack) { techTwoTrack.partCategory = "부록 A: J-Hub 기술 개요"; newApp.push(techTwoTrack); }
for(let p of part3Raw) {
    if (p.image && (p.image.includes("timeline") || p.image.includes("flowchart") || p.image.includes("orchestra") || p.image.includes("kanban"))) {
        p.partCategory = "부록 A: J-Hub 기술 개요";
        newApp.push(p);
    }
}

// App B
newApp.push({
    "type": "interlude",
    "title": "[부록 B] 자기 조직 진단 체크리스트",
    "text": "현장의 리스크를 방어하고 투명성을 유지하기 위해 J-Hub가 활용하는 실무 체크리스트입니다.",
    "partCategory": "부록 B: 체크리스트"
});
for(let p of part3Raw) {
    if (p.image && (p.image.includes("minefield") || p.image.includes("legal"))) {
        p.partCategory = "부록 B: 체크리스트";
        newApp.push(p);
    }
}

// App C
newApp.push({
    "type": "interlude",
    "title": "[부록 C] 생각을 명확히 하는 법 (마스터 프롬프트)",
    "text": "이 프롬프트들은 'AI를 능숙하게 부리는 테크닉'이 아닙니다. 완벽한 기계 앞에서 **'당신 자신의 사고를 정리하고, 무엇을 지시할지 철학적 기준을 세우는 도구'**입니다. 기계에게 질문하기 전에, 먼저 우리 스스로에게 질문하기 위해 이 프롬프트들을 사용하십시오.",
    "partCategory": "부록 C: 생각을 명확히 하는 법"
});
if (techPrompts) { 
    techPrompts.partCategory = "부록 C: 생각을 명확히 하는 법"; 
    techPrompts.title = "자기 사고의 구조화 (마스터 프롬프트)";
    newApp.push(techPrompts); 
}

// Ensure unique entries
let finalApp = [...new Set(newApp)];

bookData.pages = [...newPages, ...newPart3, ...finalApp];

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
