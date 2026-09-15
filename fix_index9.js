const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let targetText = "우린 세상을 '널리 이롭게 하기 위함(홍익인간)'이라고 배웠습니다.";
let newText = "우린 이미 '널리 사람을 이롭게 한다'에 대해선 배웠습니다.";

let pageText = data.pages[9].text;

if (pageText.includes(targetText)) {
    data.pages[9].text = pageText.replace(targetText, newText);
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Updated Index 9 successfully.");
} else {
    console.log("Failed to find exact target text.");
}
