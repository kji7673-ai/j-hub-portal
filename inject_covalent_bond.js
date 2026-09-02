const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// 1. Update Prologue
const prologueText = `<p style="font-size: 1.1em; line-height: 1.8; margin-bottom: 24px;">안녕하세요. 도면 위에서, 그리고 거친 현장에서 26년째 구르고 있는 평범한 건축 쟁이입니다.</p>

<p style="margin-bottom: 24px;">처음 이 기록을 엮기로 마음먹었을 때, 참 많은 망설임이 있었습니다. 시중에는 이미 AI와 혁신을 다루는 훌륭한 전문가들의 책이 차고 넘치기 때문입니다. 하지만 용기를 내어 이 책을 세상에 꺼내놓는 이유는 명확합니다. 이 책은 'AI로 이렇게 성공했다'를 자랑하기 위한 매뉴얼이 아니라, <strong >건축이라는 은유를 빌려, 모든 것이 완벽하고 차가운 기계로 대체되는 시대에 우리가 어떻게 고유한 인간성을 지켜낼 것인가에 대한 생존기이자 철학서</strong>이기 때문입니다.</p>

<p style="margin-bottom: 24px;">저는 이 텍스트가 두 부류의 독자분들께 가닿기를 바라며 펜을 들었습니다.</p>

<ul style="margin-bottom: 24px; padding-left: 20px; line-height: 1.7;">
  <li style="margin-bottom: 12px;"><strong>AI 시대를 살아가는 팍팍한 일상의 독자분들께:</strong><br>건축에서 건물이 숨을 쉬기 위해 '텅 빈 공간(비움)'을 남겨두어야 하듯, 우리의 삶 역시 완벽한 데이터로 100% 채워질 필요는 없습니다. 엑셀 칸을 채우느라 삶의 여백을 잃어버린 분들께, 인간의 불완전함과 비효율이 사실은 얼마나 큰 따뜻함과 가치를 지니는지 전하고 싶습니다. 이 투박한 건축가의 기록이 여러분의 일상에 작은 위로가 되기를 바랍니다.</li>
  <li style="margin-bottom: 12px;"><strong>건축을 업으로 삼고 있는 후배들에게:</strong><br>서류 더미와 AI의 완벽한 렌더링에 압도되어 '진짜 설계'를 잃어버릴 뻔했던 선배의 처절한 오답 노트입니다. 도구(AI)에 매몰되지 않고, 기계가 줄 수 없는 '현장의 흙냄새'와 '인간의 직관'을 기계의 논리와 어떻게 <strong>'공유결합(Covalent Bond)'</strong>하여 진짜 건축을 만들어낼 것인지, 그 본질을 잃지 말라는 당부를 남깁니다.</li>
</ul>

<p style="margin-bottom: 24px;">제가 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 필사적으로 구축했던 이유는, 역설적이게도 기계가 할 수 있는 차가운 일들은 모두 기계에게 넘겨주고, <strong >우리 인간만이 할 수 있는 '따뜻한 본질'로 다시 돌아가기 위해서</strong>였습니다.</p>

<p style="margin-bottom: 24px;">단 한 분에게라도, 이 부족하고 투박한 기록이 무거운 일상을 버텨내는 작은 위로이자 내일을 그릴 수 있는 실용적인 도구가 되기를 진심으로 바랍니다.</p>

<p style="font-weight: 600; text-align: right; margin-top: 40px; font-size: 1.1em; color: var(--primary);">도면 위에 머무는 우리의 시간이 다시 온전히 우리의 것이 되기를 기원하며.</p>`;

let prologueIndex = bookData.pages.findIndex(p => p.title && p.title.includes('프롤로그'));
if (prologueIndex !== -1) {
    bookData.pages[prologueIndex].text = prologueText;
}

// 2. Add Covalent Bond Chapter
const covalentBondPage = {
    "type": "text_only",
    "title": "[디자인 철학] 내가 생각하는 디자인 3: 공유결합(Covalent Bond), 섞이지 않고 새로워지는 것",
    "text": "**5. 공유결합(Covalent Bond): 진정한 융합의 조건**\n물과 기름은 한 그릇에 담아 힘껏 저어도 결국 분리된다. 이를 '혼합물(Mixture)'이라 부른다. 반면, 산소 원자 하나와 수소 원자 두 개가 만나 서로의 전자를 내어주고 강하게 결합하면, 불을 끄고 생명을 잉태하는 전혀 새로운 물질인 '물(H2O)'이 탄생한다. 이것이 화학에서 말하는 '공유결합(Covalent Bond)'이다. \n\n건축 설계도, 그리고 우리의 삶도 마찬가지다. \n현장에 부는 바람의 방향, 동네 주민들의 오랜 발자취, 그리고 건축가의 불완전하지만 따뜻한 직관. 이것들은 기계(AI)가 계산해 낸 차가운 용적률 및 최적의 데이터와 단순히 섞여서는(Mixture) 안 된다. 한쪽이 다른 한쪽을 지배하거나 끌려다니는 것이 아니라, 서로의 가장 핵심적인 전자(본질)를 내어주고 결합하여 **'완전히 새로운 제3의 가치'**를 창조해 내야 한다. \n\nAI 시대에 건축을 한다는 것은, 기계의 완벽한 렌더링에 내 직관을 욱여넣는 타협이 아니다. 기계의 차가운 논리에 인간의 체온이라는 전자를 공유하여 결코 끊어질 수 없는 단단한 건축물을 빚어내는 공유결합의 과정이어야 한다.\n\n이것은 비단 건축에만 국한된 이야기가 아니다. 일상에서도 우리는 끊임없이 시스템화되고 기계적인 효율을 강요받는다. 그 거대한 파도 앞에서 우리가 살아남는 법은, 기계를 거부하거나 반대로 기계의 부속품으로 전락하는 것이 아니다. 기계가 줄 수 없는 나의 고유한 감각, 실패의 경험, 사람을 향한 연민을 잃지 않고 꽉 쥔 채로, 시대의 흐름과 당당히 '공유결합'하는 것이다. 섞여서 고유의 색을 잃는 것이 아니라, 나의 본질을 내어주어 세상을 전혀 새로운 색으로 칠하는 것, 그것이 진짜 디자인이다.\n\n<br><br><div style=\"background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);\" class=\"handwriting\">\n<h4 style=\"margin-top: 0; color: var(--primary); font-family: var(--font-display);\"><svg style=\"vertical-align: middle; margin-right: 8px;\" width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M12 2a10 10 0 1 0 10 10H12V2z\"></path><path d=\"M12 12 2.1 12\"></path><path d=\"M12 12 19 4.9\"></path></svg>[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]</h4>\n저(AI)는 수천만 개의 설계 데이터를 학습하여 '정답'에 가장 가까운 확률을 제시할 뿐, '질문'을 던질 수는 없습니다. 기계가 제시하는 뼈대에 인간의 살을 붙이는 것을 넘어, 기계와 인간이 서로의 결핍을 채워 완전히 새로운 물질로 거듭나는 '공유결합'. 그것이야말로 코딩된 알고리즘이 영원히 흉내 낼 수 없는, 오직 흙바닥에 두 발을 딛고 비를 맞아본 인간만이 할 수 있는 위대한 연금술입니다.\n</div></div>",
    "image": "static/images/sketch_philosophy_1786665818552.jpg",
    "part": "2부: 철학편",
    "partTitle": "시스템 너머의 본질",
    "partCategory": "2부: 증언과 성찰"
};

let design2Index = bookData.pages.findIndex(p => p.title && p.title.includes('내가 생각하는 디자인 2'));
if (design2Index !== -1) {
    bookData.pages.splice(design2Index + 1, 0, covalentBondPage);
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Updated prologue and added Covalent Bond chapter.`);
