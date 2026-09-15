const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

const newText = "설계자와 의뢰인, 그리고 현장. 이 세 가지 요소는 결코 어느 하나가 부족하거나 불완전하지 않으며, 각자 뚜렷한 특성과 요구를 가지고 있습니다.<br><br>중요한 것은 이 세 주체가 결국 하나의 '도면(계획안)'을 매개로 합의해 가는 과정을 겪는다는 점입니다. 제가 설계를 하며 가지는 가장 큰 욕심은, 이 강한 개성들을 적당히 타협시켜 섞어버리는 것이 아닙니다. 서로의 필요에 귀 기울이고 합의를 이끌어내는 노력을 통해, 셋 모두가 도면 위에서 결코 떼어낼 수 없는 '필수 요소'로 단단하게 묶이는 것입니다.<br><br>문득 첫 회사에서 모시던 소장님이 떠오릅니다.<br>그분이 그려내던 평면은 단순한 선의 조합이 아니라, 바로 그 치밀한 합의가 담긴 결과물이었습니다. 어떤 한 요소를 변경하려 하면 다른 것들이 모두 틀어져 버릴 만큼, 각 요소가 톱니바퀴처럼 완벽하게 맞물려 있었습니다.";

data.pages[28].text = newText;
fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Updated Index 28 successfully.");
