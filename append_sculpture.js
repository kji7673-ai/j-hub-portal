const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const appendHTML = `
<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">어찌 외로움뿐이겠는가. 허기짐을 메우기 위해 끊임없이 무언가를 욱여넣는 것이나, 부족함을 채우기 위해 자꾸만 무언가를 덧붙이는 행위는 결국 근본적인 위로가 되지 못한다. 설계도 마찬가지다. 무언가를 계속 덧칠하는 순간 본질적인 아름다움과는 멀어지고, '이것이다'라고 강압적으로 지시하는 순간 사람들은 오히려 시선을 거둔다. 반대로 최대한 간결하게 비워낼수록 공간은 더 많은 것을 포용할 수 있게 된다.<br><br>아래의 조형물들은 내가 직접 빚어 만든 것들이다. 가슴에 사랑을 품고 있는 형태지만, 정작 그 가슴통은 텅 비어 있다. 억지로 무언가를 꽉 채워 넣지 않고 텅 비워두었기에, 오히려 더 크고 따뜻하게 누군가를 품어 안을 수 있지 않을까 하는 생각에서였다.</div>
<div style="margin-top: 40px;">
    <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 24px; color: #1d1d1f; text-align: center;">[조형물] 비어 있기에 품을 수 있는</h4>
    <img src="static/images/sculpture_1.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/sculpture_2.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/sculpture_3.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/sculpture_4.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="static/images/sculpture_5.jpg" style="width: 100%; border-radius: 12px; margin-bottom: 16px; border: 1px solid #f0f0f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
</div>
`;

for (let p of bookData.pages) {
    if (p.text && p.text.includes('지나가길 기다려야 되나봅니다')) {
        // Prevent double appending
        if (!p.text.includes('비어 있기에 품을 수 있는')) {
            p.text += appendHTML;
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Appended sculptures.");
