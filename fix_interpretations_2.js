const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let targetText = `<strong>* 공유결합 (사회적 의미)</strong>: 버팀권, 수익성, 행정 규제 등 서로 얽혀있는 복잡한 이해관계들이 타협점을 찾아 하나의 제도적 프레임 안에서 평화롭게 공존하는 상태를 뜻합니다.`;

// Index 211
if (data.pages[211].text.includes(targetText)) {
    data.pages[211].text = data.pages[211].text.replace(
        targetText,
        `<strong>* 공유결합 (일상적 의미)</strong>: 낡은 골목이 품고 있던 사람들의 발자취와 따뜻한 일상이, 새로 지어질 공간 안에서도 고유의 색을 잃지 않고 자연스럽게 스며들어 공존하는 상태.`
    );
}

// Index 226
if (data.pages[226].text.includes(targetText)) {
    data.pages[226].text = data.pages[226].text.replace(
        targetText,
        `<strong>* 공유결합 (공간적 의미)</strong>: 땅이 가진 본래의 굴곡과 제약을 억지로 밀어버리지 않고, 자연의 흐름에 건축물의 동선을 다정하게 맞대어 서로의 영역을 존중하는 결합.`
    );
}

// Index 236
if (data.pages[236].text.includes(targetText)) {
    data.pages[236].text = data.pages[236].text.replace(
        targetText,
        `<strong>* 공유결합 (사회적 의미)</strong>: 첨예하게 대립하는 상인들의 생존권과 관청의 행정적 잣대 사이에서, 어느 한쪽을 억누르지 않고 모두가 공존할 수 있는 '제도적 프레임'을 찾아가는 타협의 과정.`
    );
}

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated footnote boxes successfully.");
