const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (!p.text) return;
    
    // Replace inline color vars and specific colors
    p.text = p.text.replace(/color: var\(--primary\);/g, "color: #1d1d1f;");
    p.text = p.text.replace(/border-left: 4px solid var\(--primary\);/g, "border-left: 4px solid #333333;");
    p.text = p.text.replace(/border-left: 3px solid #0066cc;/g, "border-left: 3px solid #333333;");
    
    // Rewrite AI Logs
    if (p.text.includes("아키 시냅스 시스템 로그")) {
        // Log 1: 종전자산
        if (p.text.includes("종전자산 3D 그래프")) {
            p.text = p.text.replace(/<div style="background-color: var\(--canvas-parchment\);.*<\/div>/s, 
            `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">J-Hub는 0.1초 만에 반경 5km 내의 100만 건의 부동산 공시지가, 건축 연한, 접도율 데이터를 분석하여 오차 없는 '종전자산 3D 그래프'를 모니터에 렌더링한다.<br><br>하지만 그 차가운 모니터를 돌려 분통을 터뜨리는 할머니와 눈을 맞추고, 그 숫자가 결코 당신의 삶을 깎아내리는 것이 아님을, 이것이 의미하는 '정당함'이 무엇인지를 차분한 목소리로 설득하는 일. 마침내 억울함에 꽉 쥐어졌던 그 두 손을 스르르 풀게 만드는 일. 그것은 수백만 번의 연산을 거친 기계가 아니라, 오직 투박한 온기를 가진 인간만이 할 수 있는 일이다.</div>`);
        }
        // Log 2: 일조량 배치
        else if (p.text.includes("일조량과 채광 데이터")) {
            p.text = p.text.replace(/<div style="background-color: var\(--canvas-parchment\);.*<\/div>/s, 
            `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">이 시스템은 0.1초 만에 100만 개 건물의 일조량과 채광 데이터를 분석해 '햇빛이 가장 오래 드는 최적의 유닛 배치'를 수학적 좌표로 도출해 낸다.<br><br>하지만 그 완벽한 배치 좌표를 보고서도, '할머니가 아침 창문을 열었을 때 마주칠 이웃의 생활 소음'을 염려하여 벽면을 5cm 비켜서 방음 식재를 심는 불합리한 결단을 내리는 것은 오직 인간의 몫이다. 기계는 데이터를 계산하지만, 인간은 배려를 설계한다.</div>`);
        }
        // Log 3: 용적률 35층 타워
        else if (p.text.includes("수익률이 극대화되는")) {
            p.text = p.text.replace(/<div style="background-color: var\(--canvas-parchment\);.*<\/div>/s, 
            `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;">기계는 수익률이 극대화되는 가장 효율적인 선을 도면 위에 제안한다.<br><br>하지만 그 효율적인 선을 지우고, 이웃이 마주칠 벤치의 각도를 비워두는 비효율적인 결단은 알고리즘에 존재하지 않는다. 그 숭고한 결단과 결과에 대한 무거운 책임은 오직 설계하는 자, 인간의 몫으로 남는다.</div>`);
        }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

let html = fs.readFileSync('index.html', 'utf8');
html = html.replace(/--primary: #0066cc;/g, '--primary: #1d1d1f;');
// Also update hover colors for toc item if any
html = html.replace(/item.onmouseover = \(\) => \{ item.style.color = '#0071e3'; item.style.backgroundColor = '#f5f5f7'; \};/g, "item.onmouseover = () => { item.style.color = '#1d1d1f'; item.style.backgroundColor = '#f5f5f7'; font-weight: '600'; };");

fs.writeFileSync('index.html', html, 'utf8');

