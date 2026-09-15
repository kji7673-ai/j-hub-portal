const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let pText = data.pages[245].text;
let toReplace = "이곳에 담긴 수십 편의 조각들은 제가 묵묵한 현장을 뒹굴며 끄적여온 날것의 기록입니다.<br><br>\n";

if (pText.includes(toReplace)) {
    data.pages[245].text = pText.replace(toReplace, "");
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Successfully removed the sentence from Index 245.");
} else {
    console.log("Failed to find exact match. Trying without newline.");
    let toReplace2 = "이곳에 담긴 수십 편의 조각들은 제가 묵묵한 현장을 뒹굴며 끄적여온 날것의 기록입니다.<br><br>";
    if (pText.includes(toReplace2)) {
        data.pages[245].text = pText.replace(toReplace2, "").trim();
        fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
        console.log("Successfully removed the sentence from Index 245 (fallback).");
    }
}
