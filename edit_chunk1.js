const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (!p.text) return;
    
    // Spacing and typo fixes globally
    p.text = p.text.replace(/공유 겹합/g, '공유결합');
    p.text = p.text.replace(/연결 짓고/g, '연결짓고');
    p.text = p.text.replace(/생각든 든/g, '생각이 든');
    p.text = p.text.replace(/설계의도/g, '설계 의도');
    p.text = p.text.replace(/남자아니가/g, '남자아이가');
    p.text = p.text.replace(/죄우/g, '좌우');
    
    // 찢어진 운동화
    if (p.title === '찢어진 운동화') {
        p.text = p.text.replace(/이젠 다 떨어져/, '이젠 다 해져서');
        p.text = p.text.replace(/어쩌면 그렇게도 못 났는지/, '어쩌면 그렇게도 못났는지');
        p.text = p.text.replace(/나만의 착각인가 봅니다/, '나만의 착각이었나 봅니다');
        if(!p.text.includes('공유결합')) {
            p.text += "\n\n<div style=\"margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;\">건축이란 화려한 조감도 속에서만 존재하는 것이 아닙니다. 진짜 건축은 흙먼지 날리는 현장, 거친 바닥을 딛고 서 있는 낡은 운동화 끝에서 완성됩니다. 머릿속의 이상(Theory)과 현장의 거친 현실(Reality)이 만나 서로의 부족함을 메우는 것, 저는 이 닳아빠진 운동화야말로 가장 숭고한 '공유결합'의 증거라고 생각합니다.</div>";
        }
    }

    // 뇌물이 괴물이 된다
    if (p.title === '뇌물이 괴물이 된다') {
        p.text = p.text.replace(/가장 친한 친구처럼 다가온다/, '가장 친절한 얼굴로 다가온다');
        if(!p.text.includes('공유결합')) {
            p.text += "\n\n<div style=\"margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;\">신뢰란, 당장의 달콤한 이익과 타협하지 않는 단호함에서 출발합니다. 뇌물은 관계를 갉아먹는 독이지만, 진실된 협력은 서로를 살리는 '공유결합'의 기초가 됩니다. 현장에서 만나는 유혹들을 단호히 쳐낼 때 비로소 우리는 건물의 토대를 제대로 세울 수 있습니다.</div>";
        }
    }

    // '조은 슈퍼'
    if (p.title === "'조은 슈퍼'") {
        p.text = p.text.replace(/그리워한다/, '그리워합니다');
        if(!p.text.includes('공유결합')) {
            p.text += "\n\n<div style=\"margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #333333;\">기억이 깃든 장소가 하나둘 사라지는 것을 볼 때마다 건축가로서 묘한 책임감을 느낍니다. 새로운 구조물을 세우는 일은 필연적으로 옛것을 허무는 과정이지만, 우리는 공간 속에 사람들의 따뜻한 기억과 새로운 삶이 조화롭게 스며들 수 있도록 설계해야 합니다. 과거의 흔적과 미래의 삶이 서로 온기를 나누는 것, 이것 역시 공간이 이루어내는 아름다운 공유결합입니다.</div>";
        }
    }
});

// Remove stray empty or duplicate pages (like page 18, 19 that are just disconnected text from Yongsan)
bookData.pages = bookData.pages.filter(p => {
    if (p.title === 'No Title' && p.text && p.text.includes('결과적으로 우리는 그 현상설계에서 떨어졌습니다')) return false;
    if (p.title === 'No Title' && p.text && p.text.includes('현장을 둘러보고 인근에서 함께 식사하며')) return false;
    return true;
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
