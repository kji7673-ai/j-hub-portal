const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldText1 = "<p style=\"margin-bottom: 24px;\">이 책은 <strong>'설계라는 것, 디자인이라는 것이 과연 무엇인가'</strong>에 대해 저의 후배들에게, 그리고 언젠가 이 글을 읽게 될 <strong>내 아들에게 전해주고 싶은 이야기</strong>입니다.</p>";
const newText1 = "<p style=\"margin-bottom: 24px;\">이 책은 <strong>'건축이라는 치열한 세계에서 쟁이로 살아남는다는 것은 과연 무엇인가'</strong>에 대해 저의 후배들에게, 그리고 언젠가 이 글을 읽게 될 <strong>내 아들에게 전해주고 싶은 이야기</strong>입니다.</p>";

const oldText2 = "<p style=\"margin-bottom: 24px;\">언제부터인가 우리는 선을 긋고 공간을 상상하는 시간보다, 엑셀 칸을 채우고 심의 서류를 넘기며 해명하는 데 더 많은 밤을 지새우게 되었습니다. 제가 진양건축의 대표로서 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 구축했던 이유는 기술을 자랑하기 위해서가 아니었습니다. 기계가 할 수 있는 차가운 일들은 기계에게 맡기고, 우리 인간만이 할 수 있는 '따뜻한 본질'과 '공간에 대한 치열한 고민'으로 다시 돌아가기 위한 몸부림이었습니다. (물론 이 책을 읽으시며, 우리 회사가 정비사업에서 얼마나 체계적이고 앞선 AI 시스템을 갖추고 있는지 은연중에 느끼신다면 그것 또한 감사한 일입니다.)</p>";
const newText2 = "<p style=\"margin-bottom: 24px;\">언제부터인가 우리는 선을 긋고 사람과 공간의 '연결(공유결합)'을 상상하는 시간보다, 엑셀 칸을 채우고 심의 서류를 넘기며 해명하는 데 더 많은 밤을 지새우게 되었습니다. 제가 진양건축의 대표로서 'J-Hub'와 같은 시스템을 치열하게 구축했던 이유는 결코 기술을 자랑하기 위함이 아니었습니다. 기계가 할 수 있는 차가운 일들은 기계에게 넘기고, 우리 인간만이 할 수 있는 '따뜻한 본질'과 '서로를 품어주는 공간에 대한 고민'으로 다시 돌아가기 위한 처절한 몸부림이었습니다. (물론 이 책을 읽으시며, 우리 회사가 낡은 관행을 깨고 정비사업에서 얼마나 체계적인 시스템을 갖추려 노력해 왔는지 은연중에 느끼신다면 그것 또한 감사한 일입니다.)</p>";

for (let p of bookData.pages) {
    if (p.text) {
        if (p.text.includes(oldText1)) {
            p.text = p.text.replace(oldText1, newText1);
        }
        if (p.text.includes(oldText2)) {
            p.text = p.text.replace(oldText2, newText2);
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Prologue text updated.");
