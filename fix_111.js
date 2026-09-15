const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let page = data.pages[111];

let text = page.text;
// We split by "오늘을 산다는 것은" and replace the second half
let parts = text.split("오늘을 산다는 것은");

if(parts.length === 2) {
    let newHalf = `오늘을 산다는 것은<br>
어제의 눈으로 저의 일상과 사람을 보지 않는 것입니다.<br><br>
세상을 '낯설게 바라보기'를 멈추는 순간, 우리는 익숙함에 속아 삶에 대한 감사를 잃어버리곤 합니다.<br>
늘 곁에 있던 것을 잃고 나서야 그 고마움이 사무치게 다가오듯, 익숙해짐으로 스쳐 지나가는 소중한 것들이 참 많이 있습니다.<br><br>
때로는 후회와 상실이 찾아오겠지만, 그래도 인생이란 이미 벌어진 일에 대한 하루의 무게를 회피하지 않고 온전히 감당해 내는 것이겠지요.<br><br>
오늘도 잠이 듭니다.<br>
내일은 사람도, 공간도, 그리고 나 자신도<br>
매일 새롭게 느끼며 살아내야겠습니다.`;

    data.pages[111].text = parts[0] + newHalf;
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Updated page 112 via split successfully.");
} else {
    console.log("Failed split.");
}
