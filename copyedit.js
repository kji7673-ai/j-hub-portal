const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

for (let p of bookData.pages) {
    if (p.text) {
        // Minor copyedits for flow and emotional resonance
        p.text = p.text.replace("어떤 유려한 말도 소용없습니다", "어떤 화려한 언변도 무력해집니다");
        p.text = p.text.replace("도면에 제시합니다", "도면 위에 제안합니다");
        p.text = p.text.replace("이 딜레마를 해결합니다", "이 치명적인 딜레마를 해결합니다");
        p.text = p.text.replace("내 손가락을 대신 움직여주지 않습니다", "내 손가락을 대신 움직여 도면을 그려주지 않습니다");
        p.text = p.text.replace("내가 더 빠르고 더 명확하게 생각하여, 그들에게 쏟을 시간을 벌어줄 뿐입니다", "나의 복잡한 연산을 덜어주어, 그들의 손을 맞잡고 설득할 귀중한 '인간의 시간'을 벌어줄 뿐입니다");
        p.text = p.text.replace("기계는 수익성 저하 경고를 띄웠지만", "시스템은 즉각 '수익성 저하' 경고등을 띄웠지만");
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
