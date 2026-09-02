const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// 1. Terminology unification
bookData.pages.forEach(p => {
    if (p.title) {
        p.title = p.title.replace(/공유 결합/g, '공유결합');
        p.title = p.title.replace(/JHub/gi, 'J-Hub');
        p.title = p.title.replace(/J - Hub/gi, 'J-Hub');
    }
    if (p.text) {
        p.text = p.text.replace(/공유 결합/g, '공유결합');
        p.text = p.text.replace(/JHub/gi, 'J-Hub');
        p.text = p.text.replace(/J - Hub/gi, 'J-Hub');
        
        // Minor formatting: remove multiple spaces
        // p.text = p.text.replace(/ {2,}/g, ' '); 
    }
});

// 3. Expand Master Prompts
bookData.pages.forEach(p => {
    if (p.title === "부록 C. 생각을 명확히 하는 법 (마스터 프롬프트)") {
        if (!p.text.includes("4. [형태와 매스(Mass) 최적화 프롬프트]")) {
            p.text += `\n\n<h4 style="font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #1d1d1f; border-bottom: 2px solid #0066cc; padding-bottom: 8px;">4. [형태와 매스(Mass) 최적화 프롬프트]</h4>
<p style="margin-bottom: 24px;">주변의 도시 맥락과 일조권, 사선 제한 등의 법적 한계선을 입력하여 최적의 건축적 볼륨을 찾아낼 때 사용합니다.</p>
<div style="margin-bottom: 32px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; font-family: monospace; font-size: 14px; line-height: 1.6; color: #333; overflow-x: auto;">
<strong>[입력창]</strong><br>
"너는 도시 맥락과 법규를 고려하여 조형을 다듬는 파사드/매스 디자이너야.<br>
다음 대지 조건(일조 사선, 건폐율, 용적률)을 바탕으로,<br>
주변 환경(남측에 고층 건물, 북측에 공원)에 순응하면서도<br>
건축물의 인지성을 높일 수 있는 3가지 매스(Mass) 분절 대안을 제안해 줘.<br>
각 대안별로 자연 채광 확보율과 풍길(Wind path) 형성 효과를 설명해 줘."
</div>

<h4 style="font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #1d1d1f; border-bottom: 2px solid #0066cc; padding-bottom: 8px;">5. [공간 동선 및 사용자 경험(UX) 프롬프트]</h4>
<p style="margin-bottom: 24px;">건물 내부에서 사람이 이동하며 느끼는 공간의 감정선과 시퀀스를 시뮬레이션할 때 유용합니다.</p>
<div style="margin-bottom: 32px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; font-family: monospace; font-size: 14px; line-height: 1.6; color: #333; overflow-x: auto;">
<strong>[입력창]</strong><br>
"너는 사람의 심리와 행동 패턴을 연구하는 공간 경험(UX) 기획자야.<br>
이 복합문화공간 1층 로비에서 3층 도서관까지 이어지는 주 진입 동선을 설계할 거야.<br>
사용자가 '호기심 -> 전이 -> 개방감'이라는 감정선을 경험할 수 있도록,<br>
계단, 사이 공간(Void), 빛의 유입 방식을 활용한 동선 시나리오를 작성해 줘."
</div>

<h4 style="font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #1d1d1f; border-bottom: 2px solid #0066cc; padding-bottom: 8px;">6. [친환경 및 지속가능성 분석 프롬프트]</h4>
<p style="margin-bottom: 24px;">자연 에너지를 활용하고 에너지를 절감하는 패시브 디자인 요소들을 기획 단계에서 검토할 때 사용합니다.</p>
<div style="margin-bottom: 32px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; font-family: monospace; font-size: 14px; line-height: 1.6; color: #333; overflow-x: auto;">
<strong>[입력창]</strong><br>
"너는 제로 에너지 건축과 패시브 디자인(Passive Design) 전문가야.<br>
이 공동주택 프로젝트에서 기계적 설비에 의존하지 않고 에너지를 절감할 방안을 찾고 있어.<br>
서향 빛을 차단하기 위한 루버(Louver) 디자인 아이디어와,<br>
단지 내 미세먼지를 저감하고 바람길을 유도할 수 있는 조경/식재 배치 전략을 제시해 줘."
</div>`;
        }
    }
});

// Write updated data
const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

// 2. Check images referenced in text
const imageRegex = /!\[.*?\]\((.*?)\)/g;
let imagesFound = [];
bookData.pages.forEach(p => {
    if (p.text) {
        let match;
        while ((match = imageRegex.exec(p.text)) !== null) {
            imagesFound.push(match[1]);
        }
    }
});
console.log("Referenced Markdown Images:");
imagesFound.forEach(img => {
    if (!fs.existsSync(img)) {
        console.log(`MISSING: ${img}`);
    } else {
        console.log(`EXISTS: ${img}`);
    }
});

