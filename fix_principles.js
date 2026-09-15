const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// The new exact text for the 3 principles
data.pages[219].text = `"지속가능한 건축의 원리는 '공유결합'으로 설명할 수 있습니다."<br>
각자 부족한 것을 내어주고 서로를 단단히 묶어 가장 안정적인 상태를 이루는 과정. 건축설계의 본질, 현장의 난제를 푸는 방법, 그리고 사람을 신뢰하는 방법의 핵심이 바로 이 공유결합에 있다고 저는 믿습니다.<br><br>

첫째는 나를 잃지 않으면서도 타인을 이롭게 하기 위해 <strong>'홀로 설 수 있는 단단함'</strong>을 갖추는 것,<br>
둘째는 각기 다른 사람들의 투박한 언어와 욕망을 둥근 <strong>'예의와 미소'</strong>로 품어낼 수 있는 여유와 비움을 가질 것,<br>
그리고 셋째는 얽히고설킨 팍팍한 이해관계 속의 이면을 바라볼 수 있는 <strong>'시야'</strong>를 가지는 것입니다.<br><br>

이 세 가지 공유결합의 원칙이 만나 서로의 결핍을 채울 때, 건축은 비로소 단순한 구조물을 넘어 사람의 삶을 품어내는 생명력을 얻게 됩니다.`;

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated Index 219 successfully.");
