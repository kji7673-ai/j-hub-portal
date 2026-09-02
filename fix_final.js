const fs = require('fs');

// 1. Fix Syntax Error in index.html
let html = fs.readFileSync('index.html', 'utf8');
html = html.replace(/font-weight: '600';/g, "item.style.fontWeight = '600';");

// Make headings left-aligned if it's currently centering everything.
fs.writeFileSync('index.html', html, 'utf8');

// 2. Check book_data.js
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let targetPage = bookData.pages.find(p => p.title && p.title.includes("부록 C. 생각을 명확히 하는 법"));
if (targetPage) {
    console.log("Target page type:", targetPage.type);
    // If it's image_full, the text is center aligned by default. We should change it to text or format it.
    if (targetPage.type === 'image_full') {
        targetPage.type = 'text'; // change to regular text page
    }
    
    // Properly format the markdown to HTML so it renders nicely
    targetPage.text = `이 프롬프트들은 'AI를 능숙하게 부리는 테크닉'이 아닙니다. 완벽한 기계 앞에서 **'당신 자신의 사고를 정리하고, 무엇을 지시할지 철학적 기준을 세우는 도구'**입니다. 기계에게 질문하기 전에, 먼저 우리 스스로에게 질문하기 위해 이 프롬프트들을 사용하십시오.

<h3 style="margin-top: 40px; margin-bottom: 15px; font-size: 20px; font-weight: 700;">프롬프트 01. 공간의 감정선</h3>
<blockquote class="pull-quote" style="margin-bottom: 20px;">"이 공간에서 가장 소외될 수 있는 사용자는 누구이며, 그들이 이 문을 열었을 때 가장 먼저 느껴야 할 감정은 무엇인가?"</blockquote>
<ul style="margin-bottom: 20px; padding-left: 20px; line-height: 1.8;">
<li><strong>AI의 응답:</strong> 사용자의 동선, 시야각, 채광량 데이터를 계산하여 최적의 물리적 치수를 도출합니다.</li>
<li><strong>당신의 몫:</strong> 그 치수 위에 '안도감'과 '따뜻함'이라는 질감을 부여하는 결정.</li>
</ul>
<div style="background-color: #f5f5f7; padding: 20px; border-radius: 8px; font-size: 14px; margin-bottom: 40px;">
<strong>[실무 적용 사례]</strong> 서초구 하이엔드 주거 프로젝트 초기 기획 회의에서, AI는 수익성 1순위 타겟인 '3040 고소득층'의 동선을 최적화했습니다. 하지만 이 프롬프트를 던진 후, 우리는 수익성에 잡히지 않는 '휠체어를 탄 노년층'이 로비에 들어섰을 때 느낄 위축감을 발견했습니다. 결국 메인 램프의 경사도를 낮추고 벤치를 배치하는 쪽으로 도면이 수정되었습니다.
</div>

<h3 style="margin-top: 40px; margin-bottom: 15px; font-size: 20px; font-weight: 700;">프롬프트 02. 유산과 기억</h3>
<blockquote class="pull-quote" style="margin-bottom: 20px;">"숫자로 환산할 수 없는 100년 전의 기억 중, 미래 세대에게 100년 후까지 남겨주어야 할 단 하나의 유산은 무엇인가?"</blockquote>
<ul style="margin-bottom: 20px; padding-left: 20px; line-height: 1.8;">
<li><strong>AI의 응답:</strong> 보존 시 발생하는 용적률 손실과 분양 수익 저하 리스크를 퍼센트(%)로 경고합니다.</li>
<li><strong>당신의 몫:</strong> 그 재무적 손실을 감수하고서라도 지켜내야 할 '문화적 프리미엄'을 조합원에게 설득하는 일.</li>
</ul>
<div style="background-color: #f5f5f7; padding: 20px; border-radius: 8px; font-size: 14px; margin-bottom: 40px;">
<strong>[실무 적용 사례]</strong> 강북 재개발 단지 설계 시, AI는 한옥 터를 밀어버리면 분양 수익이 30% 증가한다고 보고했습니다. 그러나 우리는 이 프롬프트에 답하기 위해 한옥 터의 주춧돌을 보존한 덮개 공원을 설계했습니다. 당장 수익은 줄었지만, 완공 후 이 공원은 단지의 시그니처 랜드마크가 되어 오히려 전체 아파트 가치를 프리미엄급으로 끌어올렸습니다.
</div>

<h3 style="margin-top: 40px; margin-bottom: 15px; font-size: 20px; font-weight: 700;">프롬프트 03. 대립의 중재</h3>
<blockquote class="pull-quote" style="margin-bottom: 20px;">"조합원의 극대화된 욕망(수익)과 도시가 요구하는 공공성(기부채납)이 충돌할 때, 양측이 모두 동의할 수 있는 제3의 경계선은 어디인가?"</blockquote>
<ul style="margin-bottom: 20px; padding-left: 20px; line-height: 1.8;">
<li><strong>AI의 응답:</strong> 법적 허용 범위 내에서 수익과 공공성이 교차하는 100개의 수학적 시나리오를 나열합니다.</li>
<li><strong>당신의 몫:</strong> 그 100개의 시나리오 중, 현실의 욕망과 타협할 수 있는 단 하나의 '정의(Justice)'를 골라내는 일.</li>
</ul>
<div style="background-color: #f5f5f7; padding: 20px; border-radius: 8px; font-size: 14px; margin-bottom: 40px;">
<strong>[실무 적용 사례]</strong> 인허가청은 15% 기부채납을 요구했고, 조합은 5%를 주장하며 사업이 6개월간 멈췄을 때였습니다. J-Hub에 시나리오를 돌린 후, 우리는 기부채납 비율을 10%로 맞추되 그 공간을 단순한 공원이 아닌 '지하 공영 주차장 + 상부 문화센터'로 입체화하는 대안(제3의 경계선)을 찾았습니다. AI의 시뮬레이션 덕분에 인허가청과 조합 모두 명분을 챙기며 극적인 합의를 이뤄냈습니다.
</div>`;
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

