const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

const newText = `<div style="text-align: left; max-width: 600px; margin: 0;">
내게 있어 만남의 의미는<br><br>
만남과 만남의 연속에서<br><br>
나라는 존재가 만들어져 간다는 것입니다.<br><br>
그렇게 해서<br>
나는 새로운 내가 되고<br>
또 당신이 되어가는 것이겠지요.<br>
그래서 아마 우리는 서로 비슷해지는가 봅니다.<br><br>
이제는 조금 알 것 같습니다.<br>
나라는 개체의 독립성은 나를 위한 것이 아닌 당신을 위한 것이란 것을<br><br>
당신을 위한 것이 나를 위하는 것이란 것을<br>
나를 통한 나라는 존재는 더욱더 옅어지고<br><br>
당신을 통한 나의 존재는 더욱 뚜렷해지기를.<br>
살아간다는 것이 무엇일까요?<br><br>
오늘 하루, 그리고 또 하루 당신을 만나는 만남이 소중한 시간입니다.<br><br>
내가 나로서 존재하고<br>
당신은 당신으로 존재하면서<br>
존재의 본질은 각자가 아닌 서로에게 있음을 느끼며<br><br>
우리는 이렇게 오늘도 살아갑시다.
</div>

<br>"나라는 존재의 본질은 나를 인지하는 당신, 
그리고 '우리' 속에 있는 것일지 모릅니다."`;

data.pages[159].text = newText;
fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated Index 159 (Page 160).");
