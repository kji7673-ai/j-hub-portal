const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newPage = {
    title: "만지작거리고 바스락거린다",
    partCategory: "제 2 부. 현장의 목소리 - 조율의 기술",
    type: "text",
    text: `<div style="text-align: center; max-width: 500px; margin: 0 auto;">
<p style="text-align: left; line-height: 2.2; font-size: 1.1em; color: #333; margin-top: 40px; margin-bottom: 60px; display: inline-block;">
먹고 난 포장지를 만지작거리면 바스락거리고,<br>
조금씩 만들어진 조각난 면들이 만나,<br>
날카로운 선들을 새롭게 만들어가고,<br>
만들어진 선들은 이전 것 위에 겹쳐진다.<br><br>

그렇게 만들어진 조각난 포장지,<br>
조각보는 손 안에서 뭉쳐졌다 펼쳐졌다 하며<br>
더욱더 많은 조각들로 나뉘어지고,<br><br>

난 더 이상 바스락거리지 않는<br>
그것, 그것을 아쉬워하며,<br><br>

이제는 손가락 하나하나를 움직여<br>
흐름을 만들어 보내었다 불렀다 한다.<br><br>

텅 빈 손안을 채운 것은<br>
버려진 조각들이 만들어낸 선. 그 선들은<br>
아직도 내 손에 남아 나를 간지럽히며,<br>
작은 상처를 만들어간다.<br><br>

습관처럼<br>
엄지와 검지를 서로 비벼본다.<br><br>

서로가 서로를 어루만지고, 느끼며 좋아한다.<br>
언제나 이렇게 서로의 감촉을 느낀다 생각했는데,<br><br>

그렇게 붙어있다 생각한 것은, 그것은 착각이네요.<br>
엄지와 검지 사이 어느새 그 사이에<br><br>

내가 버린 것들이 얇고도 투명한 막을 만들어 놓고,<br><br>

서로를 부빈다 생각한 것은<br>
서로가 아닌,<br>
내가 만들어낸 조각난 나의 조각보.<br><br>

현실은 우리를 공기도 물도 통하지 않는<br><br>

서로가 다른 공간에 있음을 알리고,<br>
함께 있다고 생각한 우리의 과거를 깨트린다.<br><br>

언제나 만지작거리면 바스락거리는<br>
그 소리와 그 감촉은<br><br>

그것은 얇고도 투명한<br>
나의 포장지, 나의 조각보.
</p>
</div>`
};

let insertIndex = bookData.pages.findIndex(p => p.title && p.title.includes('구겨진 도면'));
if (insertIndex !== -1) {
    bookData.pages.splice(insertIndex + 1, 0, newPage);
    console.log("Inserted right after '구겨진 도면'");
} else {
    bookData.pages.splice(40, 0, newPage);
    console.log("Inserted at index 40");
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
