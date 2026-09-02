const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const createAIPanel = (text) => `\n\n<div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);" class="handwriting">\n<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>J-Hub 코어: 아키 시냅스 시스템 로그</h4>\n${text}\n</div>`;

for (let p of bookData.pages) {
    // 1. Phase 1: The Bridge ("2부를 마치며")
    if (p.title === "2부를 마치며") {
        p.text = "어느 날 밤이었습니다. 현장의 진흙탕 속에서 수십 년간 펜과 종이로 빼곡하게 옮겨 적었던 20년 치의 기록과 신뢰가, 한 조합원의 차가운 의심 한마디에 속절없이 무너져 내리는 것을 보았습니다.\n\n\"대표님, 그 숫자 확실합니까? 당신들끼리 짜맞춘 거 아니오?\"\n\n억울함에 밤을 새워 서류 뭉치를 뒤적였지만, 한 번 금이 간 신뢰의 유리는 인간의 호소력 짙은 땀방울만으로는 다시 붙일 수 없었습니다. 그 절망의 새벽, 저는 뼈저리게 깨달았습니다. 이 얽히고설킨 흙먼지 같은 현장의 혼란을 견뎌내려면, 인간의 '진심'만으로는 부족하다는 것을. 흔들리지 않는 절대적인 '기록의 증인'이 필요하다는 것을요.\n\n그래서 저는 기계를 거부하지 않고 그들과 기꺼이 손을 잡기로 결심했습니다. 저는 AI를 내 밥그릇을 뺏는 '경쟁자'나 화려한 도면을 뽑아내는 '마법 지팡이'로 부르지 않았습니다. 내가 내린 인간적 결단과 눈물을 가장 객관적이고 투명하게 증명해 줄 '증인'으로 현장에 초대하기로 한 것입니다.\n\n1부에서 선언한 '공유결합'의 철학은, 2부의 이 처절한 혼란과 상처들을 딛고, 마침내 3부에서 투명한 데이터와 시스템(J-Hub)이라는 형태를 입고 부활합니다. 그 기적 같은 전환의 현장으로 여러분을 안내합니다.";
    }

    // 2. Phase 2: Add AI log to Chapter 2
    if (p.title === "제2장. 불완전함을 설계하다") {
        if (!p.text.includes("아키 시냅스 시스템 로그")) {
            p.text += createAIPanel("<b>아키 시냅스 (AI):</b><br>\"나의 데이터 전송 알고리즘은 0.1초 만에 모든 원가 내역을 1,000명의 조합원 스마트폰에 동시에 전송할 수 있습니다. 그것이 기계가 이해하는 완벽한 투명성입니다.<br>그러나 누구에게 무엇을 열어주고, 무엇을 기다리게 할지 판단하는 '윤리적 댐'의 수문장 역할은 당신에게 있습니다. 완벽한 정보의 폭주를 막는 것은, 오직 인간의 불완전한 배려뿐입니다.\"");
        }
    }

    // 3. Phase 3: Polish a short essay
    if (p.title === "삼켜낸 말과 술 한 잔") {
        p.text += "\n\n그 침을 꿀꺽 삼키는 짧은 찰나, 내 안에서는 수십 가지의 논리와 반박이 요동칩니다. '그건 법적으로 불가능하다', '당신의 욕심이다'. 하지만 결국 그 모든 말을 삼켜내고 소주잔을 비우는 이유는, 내가 이겨서 얻는 얄팍한 승리보다 그 사람의 불안을 온전히 들어줌으로써 지켜내는 '신뢰'가 결국 이 거대한 프로젝트를 끝까지 밀고 나갈 유일한 동력임을 알기 때문입니다.";
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

