const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const appendHTML = `
<div style="margin-top: 60px;">
    <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 24px; color: #1d1d1f; text-align: center;">[스케치] 서울에서 찾아낸 얼굴들</h4>
    <img src="static/images/face_1.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/face_2.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/face_3.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/face_4.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/face_5.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
</div>
`;

for (let p of bookData.pages) {
    if (p.text && p.text.includes('가만히 벽지의 무늬를 바라보다보면')) {
        // Append only once
        if (!p.text.includes('서울에서 찾아낸 얼굴들')) {
            p.text += appendHTML;
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended face sketches.");
