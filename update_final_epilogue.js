const fs = require("fs");

const code = fs.readFileSync("book_data.js", "utf8");
const jsonStr = code.replace("var bookData = ", "").replace(/;$/, "");
const bookData = JSON.parse(jsonStr);
let pages = bookData.pages || bookData;

// 에필로그 페이지 찾기
let epilogue = pages[pages.length - 1];

epilogue.text = `공유결합.
어쩌면 이 단어 하나를 제 삶과 건축에 대입하기 위해 그동안 수많은 도면을 그렸는지도 모르겠습니다.<br><br>돌이켜보면 설계란 늘 차가운 선과 기호로 시작하지만, 도면 밖으로 나가는 순간부터는 온전히 '사람의 일'이 되었습니다. 전혀 다른 환경의 건축주, 이익이 얽힌 조합원들, 그리고 제도를 앞세우는 관청까지. 처음에는 그 다름이 저를 가로막는 벽이라고 생각했습니다. 하지만 제 고집을 조금 덜어내고 그들의 이야기에 귀 기울였을 때, 서로 다른 원자들이 각자의 본질을 잃지 않으면서도 단단히 묶이는 '공유결합'을 현장에서 경험했습니다.<br><br>하지만 제가 말씀드리고 싶은 공유결합은, 단순히 원만한 처세술이나 관계의 기술을 뜻하는 흔한 자기계발 이론이 아닙니다.<br><br>제가 진정으로 바라는 것은 건축 설계와 제도를 통해 우리 사회의 물리적 환경을 제대로 엮어내는 것입니다. 각각의 건물과 주변 환경, 지역과 지역, 그리고 그 사이를 잇는 가로(거리) 환경이 마치 <strong>'피에트 몬드리안(Piet Mondrian)의 그림 속 검정색 테두리'</strong> 같은 역할을 하기를 원합니다.<br><br>몬드리안의 그림에서 굵고 단단한 검은 선들이 프레임이 되어줄 때, 그 안의 빨강, 노랑, 파랑의 색상들이 비로소 각자의 고유한 개성을 완벽하게 뽐낼 수 있듯이 말입니다.<br><br>건축과 제도가 우리 사회를 지탱하는 튼튼한 테두리가 되어줄 때, 각 요소들은 고유의 개성을 잃지 않고 조화롭게 묶일 수 있습니다. 그리고 그 안정된 틀 속에서 사람들의 관계는 더 깊어지고, 우리는 다 함께 공유되는 행복을 누릴 수 있을 것입니다.<br><br>화곡동의 오래된 골목에서, 서계동의 비탈진 언덕에서, 그리고 유성시장의 회의 테이블에서 제가 실천하고자 했던 것도 결국 그것이었습니다.<br><br>이제 저는 다시 비어있는 하얀 도면 앞에 섭니다.<br>그리고 여러분께 묻고 싶습니다.<br><br>당신이 발 딛고 서 있는 그곳에서, 당신은 오늘 어떤 '선'을 긋고, 어떤 '공유결합'을 만들어가고 계십니까?`;

let finalData = { pages: pages };
fs.writeFileSync(
  "book_data.js",
  "var bookData = " + JSON.stringify(finalData, null, 4) + ";",
  "utf8",
);
console.log("Epilogue successfully updated.");
