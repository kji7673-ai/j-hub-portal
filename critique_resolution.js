const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// Add Disclaimer to Prologue
bookData.pages.forEach(p => {
    if (p.title === '프롤로그: 건축 외에는 아무것도 모르는 바보의 이야기') {
        if (!p.text.includes('일러두기')) {
            p.text += `\n\n<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #555555; font-size: 14px; line-height: 1.6; border-left: 3px solid #0066cc;">
<strong>[일러두기]</strong><br>
본 책에 담긴 모든 에세이와 기술적 제안은 한 명의 실무 건축가로서 치열하게 고민해 온 개인적인 성찰의 기록이며, 현재 제가 속한 서울시 건축심의 위원회 등 공식 기관의 입장과는 무관함을 밝힙니다.<br>
또한 2부에 수록된 단상들은 지난 20여 년간의 과거 현장에서 느꼈던 후회와 현재진행형의 고뇌가 섞인 시간의 파편들이며, 3부에 등장하는 '새로운 디지털 설계 도구'의 구체적 기능들은 완성된 상용 제품이 아닌, 건축 시스템이 나아가야 할 미래를 제시하는 '개념적 프로토타입이자 철학적 제안'임을 일러둡니다.
</div>`;
        }
    }
    
    // Clarify Grandma story
    if (p.title === '제1장. 신뢰를 기록하다') {
        p.text = p.text.replace(/<strong style="color: #1d1d1f;">현장 스케치: 숫자가 눈물을 닦아줄 수 있을까\?<\/strong><br>/, 
            '<strong style="color: #1d1d1f;">현장 스케치: 숫자가 눈물을 닦아줄 수 있을까?</strong><br><span style="font-size: 13px; color: #777;">(*이 에피소드는 과거 정비사업 현장들의 실제 갈등 사례를 바탕으로, 미래의 디지털 도구가 적용되었을 때의 긍정적 변화를 상상하여 재구성한 시나리오입니다.)</span><br>');
    }

    // Eradicate the remaining 99% vs 1% confusion
    if (p.title === 'AI, 그래 넌 AI고 난 JI다' || p.title === '제4장. 다시, 신발을 신다 (에필로그)') {
        // Completely replace any lingering "99" logic with the profound statement
        p.text = p.text.replace(/기계가 99%의.*?오롯이 서게 된다\./g, '');
        p.text = p.text.replace(/99%/, ''); // just blind sweep if any is left
        if (p.title === 'AI, 그래 넌 AI고 난 JI다' && !p.text.includes('기계가 수백 개의 가능성을 제시하더라도')) {
            p.text = p.text.replace(/기계가 수십, 수백 개의 대안을 생성해 낸다 하더라도,/, 
            "기계가 수백 개의 완벽한 가능성을 제시하더라도, 그중 '이것이 진짜 사람의 온기를 담은 공간인가'를 최종 판단하는 선택은 절대 기계의 몫이 될 수 없습니다. 내가 수백 밤을 지새우며 손으로 도면을 그었던 26년의 경험과 눈물, 그 인간적인 고통의 시간이 비로소 그 선택을 지휘하게 됩니다. 기계가 수많은 대안을 내놓는다 하더라도,");
        }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

