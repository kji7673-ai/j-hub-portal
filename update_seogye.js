const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

for (let p of bookData.pages) {
    if (p.text && p.text.includes('나이 지긋하신 할머니 한 분이')) {
        p.text = p.text.replace('그 가파른 언덕길을, 나이 지긋하신 할머니 한 분이 조금 걷다 쉬고, 또 조금 걷다 쉬며 위태롭게 오르고 계셨습니다. 회사의 신입 직원 한 명에게 그 할머니가 계단을 걸어 올라가시는 영상을 뒤에서 찍어보라 했습니다. 나중에 그 직원은 "정말 너무 힘들어 보였습니다"라며 먹먹해했습니다.',
        '진눈깨비 날리던 그날, 직원들과 함께 차가 다닐 수도 없는 비좁은 골목과 가파른 계단을 올랐습니다. 길이 조금만 미끄러워도, 아니면 아차 하는 순간 큰 사고가 날 수 있겠다는 아찔한 생각이 들었습니다.');
        p.image = 'static/images/seogye_sketch.jpg';
    }
    
    if (p.text && p.text.includes('그 잰걸음을 보며 결심했습니다.')) {
        p.text = p.text.replace("그 잰걸음을 보며 결심했습니다. '이곳에 수십 년을 살아오신 분들에게, 이제는 제로 레벨(Zero Level)의 평지화 설계를 해드려야겠다.'",
        "현장을 둘러보고 인근에서 함께 식사하며 우리는 자연스럽게 서로의 느낌을 나누었습니다. '이렇게 단차가 심한 지형에서 수십 년간 불편을 겪으셨을 분들을 위해 제로 레벨(Zero Level), 즉 평탄한 지형을 최대한 만들어 보자.' 그렇게 우리의 진심을 모아 '서경연화'라는 이름으로 계획안을 제출했습니다.");
        p.image = 'static/images/seogye_render.jpg';
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated Seogye texts and images.");
