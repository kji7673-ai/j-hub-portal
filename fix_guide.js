const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const oldUl = `<ul style="margin-bottom: 24px; padding-left: 20px; line-height: 1.7;">
  <li style="margin-bottom: 12px;"><strong>1부 [플랫폼의 탄생]</strong> 은 쏟아지는 업무의 과부하 속에서 살아남기 위해 발버둥 치며 만들어낸 소박한 '도구'에 대한 이야기입니다. 행정적 늪에 빠져 허우적대는 실무자나 낡은 시스템의 한계를 느끼는 분들께, 정비사업의 투명성과 6가지 길을 안내하는 작은 돌파구가 되기를 바랍니다.</li>
  <li style="margin-bottom: 12px;"><strong>2부 [불완전함 속에서 완전함을 찾다]</strong> 는 그렇게 얻어낸 귀중한 시간 동안 다시 도면 앞에 앉아 고민했던 '건축의 본질'과, 26년 현장의 쟁이로서 느꼈던 솔직한 감정의 파편들입니다. 완벽한 데이터 앞에서도 결국 기꺼이 '불완전한 선택'을 감내한 날것의 일기 85편을 단 한 편도 버리지 않고 4가지 테마로 엮었습니다.</li>
  <li style="margin-bottom: 12px;"><strong>3부 [불완전한 선택의 용기]</strong> 는 이 모든 현장의 고뇌를 딛고 바라본 다가올 10년의 풍경입니다. 기술이 지배할 새로운 시장 속에서도 결코 기계에 넘겨줄 수 없는 건축가의 존엄과 윤리, 그리고 책임감에 대한 묵직한 성찰을 담았습니다.</li>
</ul>`;

const newUl = `<ul style="margin-bottom: 24px; padding-left: 20px; line-height: 1.7;">
  <li style="margin-bottom: 16px;"><strong>1부 [설계의 본질 - 공유결합]</strong>은 건축과 공간, 그리고 사람을 잇는 보이지 않는 연결고리에 대한 철학적 성찰입니다. 단절된 공간을 허물고 관계를 맺어가는 '공유결합'의 개념을 통해, 우리가 지향해야 할 건축의 진짜 본질이 무엇인지 화두를 던집니다.</li>
  <li style="margin-bottom: 16px;"><strong>2부 [증언과 성찰]</strong>은 26년간 도면과 현장 사이에서 치열하게 살아온 한 명의 '쟁이'가 쏟아낸 날것의 일기입니다. 찢어진 운동화를 보며 자격지심을 느끼던 날들, 꾹꾹 침을 삼켜야 했던 외로움, 그리고 어른이라는 무게를 견뎌내며 부르르 떨었던 미완의 감정들을 4가지 테마로 엮었습니다.</li>
  <li style="margin-bottom: 16px;"><strong>3부 [공유결합을 가능하게 하는 시스템]</strong>은 이 모든 이상과 철학을 무너뜨리는 '현실의 행정적 과부하'에서 살아남기 위해 발버둥 치며 만들어낸 소박한 돌파구, 'J-Hub' 시스템에 대한 이야기입니다. 단순한 기술 도입을 넘어, 설계자가 다시 본질에 집중할 수 있도록 돕는 실무적인 도구이자 AI 시대 건축가의 생존 전략을 담았습니다.</li>
</ul>`;

const oldP = "기술과 비전을 기대하셨다면 2부의 감정이 낯설게 느껴지실 수도, 에세이를 기대하셨다면 1부와 3부의 시스템적인 이야기가 딱딱하게 느껴지실 수도 있습니다.";
const newP = "시스템과 기술을 기대하셨다면 1부와 2부의 철학과 감정이 낯설게 느껴지실 수도, 에세이를 기대하셨다면 3부의 시스템적인 이야기가 딱딱하게 느껴지실 수도 있습니다.";

for (let p of bookData.pages) {
    if (p.text) {
        if (p.text.includes("1부 [플랫폼의 탄생]")) {
            p.text = newUl;
        }
        if (p.text.includes(oldP)) {
            p.text = p.text.replace(oldP, newP);
        }
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Guide texts updated.");
