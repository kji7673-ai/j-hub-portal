const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// Remove any existing bridges first, just in case
bookData.pages = bookData.pages.filter(p => !(p.title && p.title.includes('[성찰')));

const uniqueBridges = {
    1: [
        { title: "[성찰 1-1] 거울 앞의 건축가", text: "<p style='margin-bottom:20px; line-height:1.9;'>도면을 그릴 때 우리는 종종 전지전능한 창조주의 착각에 빠집니다.</p><p style='margin-bottom:20px; line-height:1.9;'>하지만 선을 하나 그을 때마다 가장 먼저 베이는 것은 우리 자신의 얄팍한 밑천입니다. 당신은 스스로의 한계를 어디까지 인정할 수 있습니까?</p>" },
        { title: "[성찰 1-2] 고독이라는 연료", text: "<p style='margin-bottom:20px; line-height:1.9;'>현장에서 칭찬받는 순간보다, 모두가 떠난 밤 빈 사무실에서 도면과 마주할 때 진짜 성장이 일어납니다.</p><p style='margin-bottom:20px; line-height:1.9;'>이 고독을 견디지 못하면 건축은 한낱 기술로 전락하고 맙니다.</p>" },
        { title: "[성찰 1-3] 가면을 벗는 시간", text: "<p style='margin-bottom:20px; line-height:1.9;'>'전문가'라는 완장. 그것은 때로 우리의 가장 큰 약점을 가리는 방패가 됩니다.</p><p style='margin-bottom:20px; line-height:1.9;'>그 방패를 내려놓고 '모르겠다'고 말할 수 있는 용기. 나의 취약함을 인정하는 그 순간이 바로 진짜 실력의 시작점입니다.</p>" },
        { title: "[성찰 1-4] 불안이라는 나침반", text: "<p style='margin-bottom:20px; line-height:1.9;'>완벽한 확신 속에서 단숨에 그려진 도면은 오히려 위험합니다.</p><p style='margin-bottom:20px; line-height:1.9;'>치열한 의심과 불안 속에서 수백 번 지웠다 다시 그린, 상처투성이의 선만이 끝내 현장의 거친 흙바닥에서 살아남습니다.</p>" },
        { title: "[성찰 1-5] 타협과 굴복 사이", text: "<p style='margin-bottom:20px; line-height:1.9;'>내 철학을 지키기 위해 굽히지 않는 것과, 타인의 말을 듣지 않고 옹고집을 부리는 것의 경계는 참으로 아슬아슬합니다.</p><p style='margin-bottom:20px; line-height:1.9;'>그 선을 아슬아슬하게 넘나드는 치열한 고뇌가 우리를 '기계'가 아닌 진짜 '쟁이'로 만들어 줍니다.</p>" }
    ],
    2: [
        { title: "[성찰 2-1] 보이지 않는 욕망 읽기", text: "<p style='margin-bottom:20px; line-height:1.9;'>건축주가 말하는 '좋은 공간'의 이면에는 차마 말하지 못한 결핍과 불안이 숨어 있습니다.</p><p style='margin-bottom:20px; line-height:1.9;'>우리는 그저 귀로 듣는 자가 아니라, 상대의 그 굳게 닫힌 마음을 해독해 내는 자가 되어야 합니다.</p>" },
        { title: "[성찰 2-2] 적이 아닌 파트너", text: "<p style='margin-bottom:20px; line-height:1.9;'>시공사의 억지스러운 핑계도, 인허가권자의 깐깐한 잣대도 결국 무사히 건물을 세우기 위한 '다른 방식의 책임감'일 때가 많습니다.</p><p style='margin-bottom:20px; line-height:1.9;'>그들의 입장에 1분만 서보는 순간, 갈등은 놀랍게도 해법으로 바뀝니다.</p>" },
        { title: "[성찰 2-3] 감정의 흡수재", text: "<p style='margin-bottom:20px; line-height:1.9;'>수많은 이해관계자들의 뾰족한 짜증과 막연한 불안을 온몸으로 받아내는 감정 노동.</p><p style='margin-bottom:20px; line-height:1.9;'>이것이야말로 AI와 로봇이 수백 년이 지나도 절대 흉내 낼 수 없는, 인간 건축가만의 가장 고귀하고도 지난한 업무입니다.</p>" },
        { title: "[성찰 2-4] 설득의 본질", text: "<p style='margin-bottom:20px; line-height:1.9;'>도면의 정밀한 수치와 논리로 상대를 이기려 하지 마십시오.</p><p style='margin-bottom:20px; line-height:1.9;'>상대의 마음이 움직이지 않으면, 아무리 완벽한 수치도 종이 위의 차가운 잉크에 불과합니다. 진정한 설득은 상대를 논리적으로 굴복시키는 것이 아니라, 마음으로 공감하는 데서 출발합니다.</p>" }
    ],
    3: [
        { title: "[성찰 3-1] 땅이 들려주는 이야기", text: "<p style='margin-bottom:20px; line-height:1.9;'>모니터 속 3D 모델의 대지는 완벽하게 평평하고 깨끗합니다. 하지만 현실의 땅은 수십 년의 상처와 기억을 품고 있습니다.</p><p style='margin-bottom:20px; line-height:1.9;'>대지가 품고 있는 이 고유한 지층을 무시한 설계는 땅에 대한 폭력에 가깝습니다.</p>" },
        { title: "[성찰 3-2] 변수라는 스승", text: "<p style='margin-bottom:20px; line-height:1.9;'>우리는 내 마음대로 통제할 수 없는 '돌발 변수'를 만났을 때 비로소 진정한 창의성을 발휘합니다.</p><p style='margin-bottom:20px; line-height:1.9;'>갑작스러운 비바람, 지하에서 튀어나온 암반, 분노한 이웃의 민원… 이 골치 아픈 불청객들이 사실은 건물을 더 단단하게 만들어 주는 숨은 스승들입니다.</p>" },
        { title: "[성찰 3-3] 머리와 손끝의 시차", text: "<p style='margin-bottom:20px; line-height:1.9;'>에어컨 나오는 사무실에서의 완벽한 기하학이 뙤약볕 아래 현장 반장님의 투박한 손끝에서 번역되는 과정.</p><p style='margin-bottom:20px; line-height:1.9;'>그 사이에서 필연적으로 발생하는 오차와 삐걱거림을, 오히려 유연하고 아름다운 변주곡으로 만들어내는 것이 현장의 진짜 묘미입니다.</p>" },
        { title: "[성찰 3-4] 타협의 미학", text: "<p style='margin-bottom:20px; line-height:1.9;'>모든 것을 내가 처음 기획한 대로 완벽하게 짓는 것은 현실에서 불가능합니다.</p><p style='margin-bottom:20px; line-height:1.9;'>덜 중요한 것을 기꺼이 과감하게 내어주고, 가장 중요한 본질 하나만큼은 끝까지 목숨 걸고 지켜내는 것. 그것이 현장이 우리에게 요구하는 타협의 미학입니다.</p>" }
    ],
    4: [
        { title: "[성찰 4-1] 사람과 시스템의 결합", text: "<p style='margin-bottom:20px; line-height:1.9;'>우리가 도입한 AI와 시스템은 차갑고 오차 없이 정확하지만, 그것을 다루는 우리의 손은 여전히 따뜻하고 흔들리며 불완전합니다.</p><p style='margin-bottom:20px; line-height:1.9;'>그 차가운 논리와 뜨거운 인간성이 부딪치며 서로를 보완할 때, 현장에서는 비로소 기적이 일어납니다.</p>" },
        { title: "[성찰 4-2] 미완성이 주는 희망", text: "<p style='margin-bottom:20px; line-height:1.9;'>완벽하지 않은 사람들이 모여, 흙먼지를 뒤집어쓰고 끊임없이 부딪히고 깨지며 무언가를 끝내 빚어내는 과정.</p><p style='margin-bottom:20px; line-height:1.9;'>그 처절하고도 숭고한 미완성의 몸부림이야말로, 우리가 이 고된 건축의 길을 떠나지 못하고 사랑할 수밖에 없는 이유입니다.</p>" },
        { title: "[성찰 4-3] 여백을 채우는 힘", text: "<p style='margin-bottom:20px; line-height:1.9;'>나의 부족한 1%를 저 밉상인 상대방의 1%가 채워주고, 도면의 실수를 현장의 반장님이 웃으며 덮어줄 때.</p><p style='margin-bottom:20px; line-height:1.9;'>우리는 이것을 '공유결합'이라 부르고, 마음속으로는 '연대'라고 읽습니다. 결국 남는 것은 건물보다도, 함께 비를 맞았던 사람입니다.</p>" }
    ]
};

const newPages = [];
let currentTheme = 0;
let essayCountInTheme = 0;
let bridgeCount = 0;

for (let p of bookData.pages) {
    if (p.title === '공유결합의 첫 질문') {
        currentTheme = 1; essayCountInTheme = 0; bridgeCount = 0;
    } else if (p.title === '공유결합의 두 번째 질문') {
        currentTheme = 2; essayCountInTheme = 0; bridgeCount = 0;
    } else if (p.title === '공유결합의 세 번째 질문') {
        currentTheme = 3; essayCountInTheme = 0; bridgeCount = 0;
    } else if (p.title === '신뢰가 만들어지는 현장') {
        currentTheme = 4; essayCountInTheme = 0; bridgeCount = 0;
    }
    
    // Add page
    newPages.push(p);

    // After an essay, maybe add bridge
    if (currentTheme >= 1 && currentTheme <= 4) {
        if (!p.title.includes('질문의 확장') && !p.title.includes('결론을 향하여') && !p.title.includes('공유결합의') && !p.title.includes('신뢰가 만들어지는') && !p.title.includes('부록')) {
            essayCountInTheme++;
            if (essayCountInTheme > 0 && essayCountInTheme % 6 === 0) {
                if (uniqueBridges[currentTheme] && bridgeCount < uniqueBridges[currentTheme].length) {
                    let b = uniqueBridges[currentTheme][bridgeCount];
                    newPages.push({
                        type: "text_only",
                        title: b.title,
                        text: b.text
                    });
                    bridgeCount++;
                }
            }
        }
    }
}

bookData.pages = newPages;

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Injected unique bridges. Total pages:", newPages.length);
