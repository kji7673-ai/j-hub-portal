const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

function replaceText(index, oldStr, newStr) {
    if (data.pages[index] && data.pages[index].text) {
        if(data.pages[index].text.includes(oldStr)) {
            data.pages[index].text = data.pages[index].text.replace(oldStr, newStr);
        } else {
            console.warn(`WARNING: Could not find string on index ${index}`);
        }
    }
}
function replaceRegex(index, regex, newStr) {
    if (data.pages[index] && data.pages[index].text) {
        if(regex.test(data.pages[index].text)) {
            data.pages[index].text = data.pages[index].text.replace(regex, newStr);
        } else {
            console.warn(`WARNING: Could not match regex on index ${index}`);
        }
    }
}

// 1. Index 199
replaceText(199, "'꼭 필요한 공유결합'을 만들어내는", "'꼭 필요한 연결고리'를 만들어내는");

// 2. Index 205
replaceText(205, "진짜 '공유결합'에 이르게 하는 것", "진짜 '단단한 합의'에 이르게 하는 것");
replaceRegex(205, /<div class="footnote-box">\s*<strong>\* 공유결합 \(건축적 의미\)<\/strong>:.*?<\/div>\s*/, "");

// 3. Index 210
replaceText(210, "다시 공유결합하는 순간이었습니다.", "다시 자연스럽게 스며드는 순간이었습니다.");
replaceRegex(210, /<div class="footnote-box">\s*<strong>\* 공유결합 \(일상적 의미\)<\/strong>:.*?<\/div>\s*/, "");

// 4. Index 218
replaceText(218, "이 공유결합에 있다고 저는 믿습니다.", "이 '서로를 채워주는 관계'에 있다고 저는 믿습니다.");
replaceText(218, "세 가지 공유결합의 원칙이 만나", "세 가지 원칙이 만나");

// 5. Index 223
replaceText(223, "우리의 계획안에서 '공유결합'은 대단한 구호가 아니었습니다.", "우리의 계획안에서 거창한 구호를 외치고 싶었던 것은 아닙니다.");

// 6. Index 224
replaceText(224, "믿는 '공유결합'의 실체입니다.", "믿는 '건축의 진짜 역할'입니다.");

// 7. Index 225
replaceText(225, "의미 있는 형태의 공유결합이었습니다.", "의미 있는 공존이었습니다.");
replaceRegex(225, /<div class="footnote-box">\s*<strong>\* 공유결합 \(공간적 의미\)<\/strong>:.*?<\/div>\s*/, "");

// 8. Index 227
replaceText(227, "'주변 도시 지역과 어떤 공유결합을 맺을 것인가'", "'주변 도시 지역과 어떻게 소통하고 조화를 이룰 것인가'");

// 9. Index 235
replaceText(235, "공유결합은 완성됩니다.", "진정한 합의점은 완성됩니다.");
replaceRegex(235, /<div class="footnote-box">\s*<strong>\* 공유결합 \(사회적 의미\)<\/strong>:.*?<\/div>\s*/, "");

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Successfully replaced words and removed footnotes in Act 4.");
