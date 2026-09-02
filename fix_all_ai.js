const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (!p.text) return;
    
    // Line 327
    if (p.text.includes("[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]") && p.text.includes("프롬프트에 아무리")) {
        p.text = p.text.replace(/<div.*?\[아키 시냅스의 반론 \(AI 에이전트의 관찰 일지\)\].*?<\/div>/s, 
        `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">프롬프트에 아무리 정교한 지시를 내려도, 기계(AI)는 '비움'을 설계하는 것을 가장 어려워한다. 기계는 화면의 모든 픽셀과 공간을 유용한 데이터로 가득 채우려 강박적으로 작동하기 때문이다. 하지만 우리는 알고 있다. 아무것도 없는 텅 빈 곳에서 비로소 바람이 길을 찾고 햇살이 머문다는 것을. 계산된 효율을 잠시 멈추고 빈 곳을 남겨두는 여유, 그것이 숨 쉬는 건축을 만든다.</div>`);
    }
    
    // Line 470
    if (p.text.includes("[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]") && p.text.includes("수만 개의 데이터를 연산하여")) {
        p.text = p.text.replace(/<div.*?\[아키 시냅스의 반론 \(AI 에이전트의 관찰 일지\)\].*?<\/div>/s, 
        `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">우리가 시스템과 협업할 때도 마찬가지다. AI는 수만 개의 데이터를 연산하여 단 하나의 오차도 없는 '완벽한 기하학'을 도출한다. 하지만 현장의 거친 흙바닥과 옆 건물의 비뚤어진 담장까지 계산하지는 못한다. 완벽한 도면을 기꺼이 구기고 주변의 무질서함과 조화시키는 '불완전한 선택'. 기계는 할 수 없는, 그것이 바로 인간 건축가만의 특권이다.</div>`);
    }
    
    // Line 741
    if (p.text.includes("[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]") && p.text.includes("완벽하고 기하학적인 도면")) {
        p.text = p.text.replace(/<div.*?\[아키 시냅스의 반론 \(AI 에이전트의 관찰 일지\)\].*?<\/div>/s, 
        `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">우리가 시스템과 협업할 때도 마찬가지다. AI가 그려낸 완벽하고 기하학적인 도면이 때로는 주변의 맥락(도시의 역사, 사람들의 동선)과 엇박자를 낼 때가 있다. 완벽한 숫자를 포기하더라도 주변과 조화롭게 어우러지는 불완전함을 택하는 것. 그것이 기계는 할 수 없는 인간 건축가만의 고뇌이자 특권이다.</div>`);
    }
    
    // Line 876
    if (p.text.includes("[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]") && p.text.includes("처음 계획(만들려던 것)")) {
        p.text = p.text.replace(/<div.*?\[아키 시냅스의 반론 \(AI 에이전트의 관찰 일지\)\].*?<\/div>/s, 
        `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">우리가 인공지능과 협업할 때도 마찬가지다.<br>처음 계획(만들려던 것)과 AI의 시뮬레이션(만들어지는 것) 사이의 불일치를 만났을 때, 우리는 선택해야 한다:<br>① 내 의도에 AI를 맞출 것인가 (기계를 도구로 본다)<br>② AI의 제안을 수용할 것인가 (기계를 파트너로 본다)<br>③ 그 사이에서 새로운 가능성을 찾을 것인가 (공창造)<br><br>진정한 혁신과 디자인은 ③의 유연함에서 나온다.</div>`);
    }

    // Line 494: 1인칭 AI 시점 글
    if (p.text.includes("아키 시냅스의 구축을 함께한 AI 에이전트의 1인칭 시점으로 재구성된 기록")) {
        p.text = `처음 AI 시스템 구축을 결심했을 때, 나는 흔히 말하는 '코딩의 코 자도 모르는' 전형적인 비개발자였다. 파이썬(Python)의 기본 문법조차 몰랐고, 터미널 창을 여는 것조차 낯설어했다. 아마추어의 섣부른 도전이라는 주변의 만류도 많았다.\n\n![현장 스케치](static/images/32.jpg)\n\n하지만 나는 개발 언어를 모르는 대신, 내가 도달하고자 하는 **'목표'**가 무엇인지 분명하게 알고 있었다.\n\n기계에게 다짜고짜 코드를 짜내라고 요구하는 대신, 내가 구상한 데이터의 흐름과 시스템의 위계를 논리적인 '건축 도면(흐름도)'처럼 펼쳐 보이기 시작했다. J-Hub(통합 대시보드)와 J-Journal(개별 저널)이 어떻게 서로 데이터를 주고받아야 하는지, 사용자가 어떤 순서로 버튼을 누르고 화면을 봐야 하는지, 그 모든 프로세스가 이미 완벽한 건축 설계도처럼 머릿속에 구조화되어 있었다. 코딩은 단지 그 설계도를 번역하는 망치와 톱일 뿐이었다.`;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

