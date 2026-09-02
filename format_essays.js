const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newText1 = `내 자신은<br>내가 스스로를<br>더럽히지 않는 한,<br><br>절대,<br>타인에 의해 더럽혀지지는 않는다.<br><br>화가 날 때마다.<br>난 절대,<br>타인에 의해 더럽혀지지 않는다.<br><br>내 스스로 나를 더럽히지 않는 한<br><br>그렇게 난 매번 중얼거린다.<br>근데, 더럽혀진 것은 씻으면 되는데,<br>그게, 상처가 되어 남는다.<br><br>그게, 나로 하여금 오늘을 집중하지 못하게 하고,<br>오늘의 나의 모습이기도 하다.<br><br><div style="margin-top: 40px; padding: 24px; background-color: #f5f5f7; border-radius: 12px; color: #333333; font-size: 15px; line-height: 1.6; border-left: 3px solid #0066cc;">그래, 귀로든 입으로든 들어오는 타인의 불순물에 내가 진짜로 더럽혀지지는 않는다. 그냥 '그렇구나' 하고 내 속에 고여 맴돌게만 두지 않으면 그만이다.<br><br>하지만 참 이상하게도, 어떤 상처는 씻겨 내려가지 않고 아주 오래 남는다. 예전 대학교 졸업할 때, 한 선배가 선물한 책에 적어준 글귀가 떠오른다. "처마에 떨어진 물 한 방울같이 작은 오해가, 우리 사이를 천길 낭떠러지처럼 갈라놓았다"는 말. 지금의 나 역시 그 '물 한 방울' 같은 사소한 앙금으로 누군가와 멀어진 채 후회 속을 걷고 있는지 모른다. 참 별거 아닌 일인데도 지독하게도 오래 품고 산다.<br><br>그런데 어떨 때는, 이 알량하고 뾰족한 상처마저 둥글게 깎아버리고 모든 것에 무던해지면 '나'라는 존재 자체가 뭉개질 것만 같아 모질게 부여잡고 있을 때가 있다. 누구나 가슴속에 절대 아물게 두고 싶지 않은 상처 하나쯤은 독하게 품고 살지 않는가. 그것이 때로는, 부서질 것 같은 자아를 지탱하는 가장 인간적인 고집이 되기도 하니까.</div>`;

const newText2 = `작은 바람에도 부르르 떨고 휘청입니다<br>덩치는 큰 놈이<br>지 몸 생각도 않고 온 몸을 떨고 있습니다<br><br>시간 따라 이 바람도 지나가길 기대하며<br><br>그렇게 휘청입니다.<br><br>어쩌면 좋습니까?<br><br>작은 지지대라도 있으면 이러지 않을까 싶지만,<br><br>작은 산들바람인데 태풍 맞은 것처럼 휘청이니<br><br>내가 이상한가 봅니다<br><br>조금만 더 자연스레 받아들이면 좋았을 텐데<br><br>이젠 그냥 이게 원래 나구나 싶어,<br>더 속으로 움츠러듭니다<br><br>이런저런 핑계로<br>오늘의 날 감싸지만<br>결국은<br>내가 자라지 못했기에 작은 바람에도 죽을 듯 온 몸을 휘청이나 봅니다<br><br>그런가 봅니다.`;

let found1 = false;
let found2 = false;

for (let p of bookData.pages) {
    if (p.title === "내 자신은") {
        p.text = newText1;
        found1 = true;
    }
    if (p.title === "난 약한 사람입니다") {
        p.text = newText2;
        found2 = true;
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Updated both essays. Found1:", found1, "Found2:", found2);
