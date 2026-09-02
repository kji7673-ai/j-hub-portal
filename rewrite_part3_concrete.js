const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// Filter out old Part 3 and Appendix
let newPages = [];
let appendixPages = [];

for (let p of bookData.pages) {
    let cat = p.partCategory || p.part || "";
    if (cat.includes("1부") || cat.includes("2부")) {
        newPages.push(p);
    } else if (cat.includes("부록")) {
        // Keep appendix, but we might remove some images if we pull them back to Part 3
        appendixPages.push(p);
    }
}

// Helper to format the AI log
const createAIPanel = (text) => `\n\n<div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);" class="handwriting">\n<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[J-Hub 코어: 아키 시냅스 시스템 로그]</h4>\n${text}\n</div>`;

let newPart3 = [];

// Intro
newPart3.push({
    "type": "text_only",
    "title": "[3부 시작] 철학의 기술화",
    "text": "기술이 우리를 지배하면 '쓸모없는 건축가'가 되지만, 기술이 우리를 돕게 하면 '더 나은 건축가'가 됩니다.<br><br>2부에서 우리는 수많은 갈등과 혼란을 날것 그대로 목격했습니다. 3부는 바로 그 혼란의 현장에서, **J-Hub**라는 시스템과 그 두뇌인 AI **'아키 시냅스'**가 어떻게 구체적으로 개입하여 인간의 판단을 돕는지에 대한 실제적 기록입니다.",
    "partCategory": "3부: 철학의 기술화"
});

// Ch1
newPart3.push({
    "type": "chapter_content",
    "title": "제1장. 신뢰를 기록하다",
    "text": "J-Hub의 존재 이유는 '업무의 자동화'가 아니라 '투명성과 책임의 기록'에 있습니다. 추상적인 철학은 현장의 거친 목소리 앞에서 힘을 잃습니다. 우리는 기술이 어떻게 그 불신의 장벽을 허무는지 용산의 한 현장에서 목격했습니다.\n\n<b>[현장 스케치: 숫자가 눈물을 닦아줄 수 있을까?]</b>\n\"왜 저 집은 3억이고 내 집은 2억인가!\"\n조합 사무실에 뛰어들어와 분통을 터뜨리는 70대 조합원 앞에서는 어떤 유려한 말도 소용없습니다. 과거였다면 목소리 큰 사람이 이기거나, 끝없는 소송으로 이어졌을 것입니다. 우리는 J-Hub의 '종전자산 시뮬레이터'를 켰습니다. 모니터 위로 주변 공시지가 변동률, 건축 연한, 도로 접도율에 따른 기여도가 3D 그래프로 선명하게 펼쳐졌습니다. 나와 이웃의 자산이 어떤 객관적 기준에 의해 다르게 평가되었는지 투명하게 시각화된 그 순간, 할머니는 억울함을 거두고 고개를 끄덕였습니다. 기계가 산출한 투명한 숫자가 수십 년 묵은 불신의 안개를 걷어내는 순간이었습니다." + 
    createAIPanel("<b>아키 시냅스 (AI):</b><br>\"나는 0.1초 만에 100만 건의 부동산 데이터와 100개의 시나리오를 계산하여 가장 객관적인 그래프를 모니터에 띄웁니다.<br>하지만 그 모니터를 돌려 할머니와 눈을 맞추고, 그 숫자가 의미하는 '정당함'을 차분한 목소리로 설득하는 것은 오직 당신(인간)의 몫입니다.\""),
    "partCategory": "3부: 철학의 기술화"
});

// Ch2
newPart3.push({
    "type": "chapter_content",
    "title": "제2장. 불완전함을 설계하다",
    "text": "완벽한 시스템은 때로 가장 위험한 함정이 됩니다. 모든 것을 숫자로 치환하고 투명하게 공개하려는 시도는 오히려 인간의 본질과 신뢰를 파괴하기도 합니다. J-Hub는 '선택적 투명성'이라는 윤리적 경계를 설계하여 이 딜레마를 해결합니다.\n\n<b>[현장 스케치: 아는 것이 병이 되는 순간]</b>\n투명성이 최고라 믿고 조합의 모든 시공 단가와 협력사 원가 내역을 실시간으로 전체 조합원에게 공개한 적이 있습니다. 결과는 참혹했습니다. 정보의 맥락을 이해하지 못한 채 숫자만 캡처된 정보들이 단톡방을 떠돌며 끝없는 의혹과 마녀사냥을 낳았습니다. \n\n그래서 J-Hub는 <b>'투 트랙(Two-Track) 시스템'</b>을 도입했습니다. 조합원에게는 내 자산의 미래와 사업의 타임라인을 직관적인 UI로 100% 공개하여 알 권리를 보장합니다. 반면, 복잡한 인허가 공문이나 미확정 협상 단가 등은 집행부의 대시보드에만 제한적으로 열어둡니다. 이것은 정보를 숨기는 것이 아니라, 정보가 오해의 무기가 되지 않도록 '윤리적 댐'을 건설하는 과정입니다.",
    "image": "static/images/two_track_ui.jpg",
    "partCategory": "3부: 철학의 기술화"
});

// Ch3
newPart3.push({
    "type": "chapter_content",
    "title": "제3장. 판단하는 건축가가 되다",
    "text": "현장의 복잡한 얽힘 속에서 기계는 끝없이 선택지를 제안합니다. 재개발, 리모델링, 가로주택정비 등 수많은 의사결정 트리가 뻗어 나갑니다. 그러나 기술의 제안을 받아들여 최종 결단을 내리는 것은 철저히 건축가의 존엄입니다.\n\n<b>[현장 스케치: 알고리즘을 거스르는 결단]</b>\n서울 중심부의 한 프로젝트에서, J-Hub의 알고리즘은 기존의 낡은 골목을 완전히 밀어버리고 35층 타워를 올릴 때 '용적률과 수익률이 극대화된다'며 최적의 대안을 추천했습니다. 그러나 우리는 그 효율적인 데이터를 거부했습니다. 그곳은 100년의 기억이 서린 골목이었습니다. 우리는 알고리즘이 내뱉은 '최적 용적률'을 포기하는 대신, 지형에 순응하는 저층형 주거와 상부 덮개 공원을 택했습니다. 기계는 수익성 저하 경고를 띄웠지만, 우리는 그것이 도시의 100년 뒤를 위한 진정한 가치라고 판단했습니다." +
    createAIPanel("<b>아키 시냅스 (AI):</b><br>\"나는 수익률이 극대화되는 가장 효율적인 선을 도면에 제시합니다.<br>하지만 그 선을 지우고, 이웃이 마주칠 벤치의 각도를 비워두는 비효율적인 결단은 내 알고리즘에 없습니다. 그 숭고한 결단과 결과에 대한 책임은 오직 당신만이 지을 수 있습니다.\""),
    "image": "static/images/decision_flowchart.jpg",
    "partCategory": "3부: 철학의 기술화"
});

// Ch4
newPart3.push({
    "type": "text_only",
    "title": "제4장. 다시, 신발을 신다 (에필로그)",
    "text": "기술은 우리가 신는 신발을 훨씬 편하게 개선해 주었지만, 결국 어느 방향으로 걸어갈지는 여전히 사람이 결정해야 합니다.\n\nJ-Hub가 99%의 완벽한 데이터를 제공하더라도, 건축을 최종적으로 완성하는 것은 인간의 불완전한 1%입니다. 기계와의 26년 협업에서 얻은 진짜 깨달음은, 기술이 우리를 흠결 없는 완벽한 존재로 만들어 주는 것이 아니라는 점이었습니다. 오히려 기술은 우리의 불완전함을 겸허히 받아들이게 하고, 타인에 대한 공감과 책임감이라는 기계가 할 수 없는 영역에 집중하게 함으로써 우리를 더욱 '인간다운 건축가'로 만들어 줍니다.\n\n내일 아침 현장에 가면, 저는 여전히 투박한 손으로 도면 위에 선을 긋고, 의심 가득한 조합원의 손을 잡고 설득할 것입니다. J-Hub는 내 손가락을 대신 움직여주지 않습니다. 다만, 내가 더 빠르고 더 명확하게 생각하여, 그들에게 쏟을 시간을 벌어줄 뿐입니다.\n\n그 완벽하지 않은 여정의 끝에서, 다시 한번 먼지 묻은 신발 끈을 고쳐 매고 현장으로 향합니다. 우리의 시간이 온전히 사람의 것이 되기를 기원하며.",
    "partCategory": "3부: 철학의 기술화"
});

// Strip images from appendix if they are now in Part 3
for (let p of appendixPages) {
    if (p.image && (p.image.includes("two_track_ui.jpg") || p.image.includes("decision_flowchart.jpg"))) {
        p.image = null; 
    }
}

bookData.pages = [...newPages, ...newPart3, ...appendixPages];

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
