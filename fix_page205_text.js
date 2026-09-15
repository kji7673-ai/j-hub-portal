const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

const originalStr = `그 묵묵한 현장이라는 무대 위에서 얽히고설킨 수많은 이들의 요구사항들. 그 복잡한 욕망의 덩어리를 묵묵히 조율하여 마침내 눈에 보이는 하나의 결과물로 묶어내는 행위. 그것이 바로 건축가의 '계획안'입니다.<br><br>
계획안이란 결코 화려하게 치장된 프레젠테이션이 아닙니다. 각자의 입장에서 바라는 것들을 조율하고 현실 가능성을 더하여 주민들 앞에 내놓는 단단한 신뢰이자, 우리가 함께 도출해 낸 <strong>'최선의 약속'</strong>입니다.`;

const replacementStr = `계획안이란 화려한 프레젠테이션으로 끝나면 안 됩니다. 이 사업과 관련된 수많은 사람들과의 관계에서 조율되고, 협의된, 그리고 현실 가능성을 더하여 주민들 앞에 내놓는 단단한 신뢰이자, 우리가 함께 도출해 낸 <strong>'최선의 약속'</strong>입니다.`;

let pText = data.pages[204].text;
if (pText.includes(originalStr)) {
    data.pages[204].text = pText.replace(originalStr, replacementStr);
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Successfully updated Index 204.");
} else {
    // Maybe spaces or linebreaks differ
    console.log("Could not find the exact string to replace. Trying regex...");
    let regex = /그 묵묵한 현장이라는 무대 위에서 얽히고설킨.*?<strong>'최선의 약속'<\/strong>입니다\./s;
    if (regex.test(pText)) {
        data.pages[204].text = pText.replace(regex, replacementStr);
        fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
        console.log("Successfully updated Index 204 using Regex.");
    } else {
        console.log("Still failed.");
    }
}
