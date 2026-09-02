const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const sneakerOldReflection = "우스운 이야기지만, 현재의 나는 애써 운동화를 탓하던 과거의 그 모습에서 조금도 더 강해지지 않은 것 같다. 서울시 건축심의위원이라는 번듯한 직함을 달고 회의 자리에서 내 의견을 이야기할 때조차, 여전히 목소리가 미세하게 떨리는 나 자신을 발견할 때면 '너는 참 어쩔 수 없구나' 하며 쓴웃음을 짓게 된다.\n\n하지만 어쩌면 다행인지도 모른다. 그때나 지금이나 나는 무장한 듯 완벽하고 빈틈없는 전문가로 보이기보다는, 여전히 치열하게 생각하고, 진심으로 스케치하고, 묵묵히 글을 쓰며, 사람의 마음과 감정을 소중히 다룰 줄 아는 그런 사람으로 남고 싶으니까.";

const sneakerFormattedReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;"><strong>[현재의 단상]</strong><br><br>우스운 이야기지만, 현재의 나는 애써 운동화를 탓하던 과거의 그 모습에서 조금도 더 강해지지 않은 것 같다. 서울시 건축심의위원이라는 번듯한 직함을 달고 회의 자리에서 내 의견을 이야기할 때조차, 여전히 목소리가 미세하게 떨리는 나 자신을 발견할 때면 '너는 참 어쩔 수 없구나' 하며 쓴웃음을 짓게 된다.<br><br>하지만 어쩌면 다행인지도 모른다. 그때나 지금이나 나는 무장한 듯 완벽하고 빈틈없는 전문가로 보이기보다는, 여전히 치열하게 생각하고, 진심으로 스케치하고, 묵묵히 글을 쓰며, 사람의 마음과 감정을 소중히 다룰 줄 아는 그런 사람으로 남고 싶으니까.</div>`;

const drinkOldText = "내 앞 술잔 하나 놓고, 세상 일 중에 이 작은 잔에 담지 못할 것은 없다.";
const drinkNewReflection = `<div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;"><strong>[현재의 단상]</strong><br><br>세상 일 중에 이 술잔에 담지 못할 것이 무엇이 있을까. 꾹꾹 눌러 담아 탁 털어 넣어버리곤 하지만, 나는 여전히 이따금씩 술에 취해 정신을 잃고 만다.<br><br>나이 쉰이 훌쩍 넘고 그 긴 세월을 겪었으면서도, 나는 아직도 정신을 못 차린 것이다. 어쩌면 영원히 못 차릴지도 모르겠다.</div>`;

for (let p of bookData.pages) {
    if (p.text) {
        if (p.text.includes(sneakerOldReflection)) {
            p.text = p.text.replace('\n\n' + sneakerOldReflection, '\n\n' + sneakerFormattedReflection);
        }
        
        if (p.text.includes(drinkOldText) && !p.text.includes('[현재의 단상]')) {
            p.text = p.text.replace(drinkOldText, drinkOldText + '\n\n' + drinkNewReflection);
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Formatted reflections appended.");
