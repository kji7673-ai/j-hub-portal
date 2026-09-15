const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

const newText = "사실 '나'라는 존재는 세상 모든 일의 이유이자 출발점입니다.<br>우리가 그토록 이야기해 온 공유결합 역시, 각 원자가 지닌 <strong>'홀로 설 수 있는 단단함'</strong>에서 출발합니다.<br><br>사람은 누군가와 함께 묶여 소속감을 느낄 때 큰 안정감을 얻습니다.<br>하지만 그 소속감이 곧 나의 개성과 특성이 무시되어도 좋다는 뜻은 결코 아닙니다.<br>두 원자가 서로의 빈자리를 채우며 튼튼하게 결합하기 위해서는, 먼저 각자 고유한 색을 지닌 개체로서 뚜렷하게 존재해야만 합니다.<br><br>여기서 개체로서 홀로 선다는 것은, 결코 내가 서기 위해 타인을 짓밟거나 누군가보다 우위에 서서 존재 가치를 증명하려는 것이 아닙니다.<br>전체 속에 휩쓸려 나를 잃어버리지 않고, 건강한 관계 속에서 서로를 이롭게 하기 위함입니다.<br><br>타인과 진정한 결합을 맺기 전에,<br>먼저 '나'라는 개체가 흔들림 없이, 그러나 다정하게 홀로 서 있어야 합니다.";

data.pages[74].text = newText;
fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated Index 74 successfully.");
