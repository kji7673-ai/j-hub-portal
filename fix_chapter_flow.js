const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let p197 = data.pages[197];
let p198 = data.pages[198];
let p199 = data.pages[199];

// Store original texts
let textA_climax = p197.text;
// textB_setup will be completely replaced by the user's requested text
let newTextB_setup = "강동구에서는 꽤 오랜 시간 심의위원으로 활동을 했습니다. 한번은 제가 경관심의위원을 맡게된해의 이야기 입니다.<br>어느 날, 제 눈앞에 놓인 계획안 하나가 시선을 멈추게 했습니다.<br>'용역원실'이 자연 채광도 환기도 전혀 되지 않는 지하 2층에 덩그러니 배치되어 있었기 때문입니다.<br>올해 제 분야는 '경관'이었습니다. 누군가 지적하겠지... 계속 기다렸습니다. <br>심의가 끝나갑니다. '굳이 말을 해야 할까? 그냥 넘어갈까? 제가 왜 심의위원을 하고 있지...'<br>이런저런 생각을 하다가, 끝내 마이크를 잡았습니다.<br>\"제가 경관 분야이긴 합니다만, 건축 부분에 대해 한 말씀 드리겠습니다.\"";

// Apply new order
// 197: Image 1 + Setup Text
p197.text = newTextB_setup;
p197.isContinuation = false;

// 198: Image 2 (bighands)
p198.isContinuation = true;
p198.isImageOnly = true;

// 199: Climax Text
p199.text = textA_climax;
p199.isContinuation = true;
p199.isImageOnly = false;
p199.type = "text_only";

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Successfully reordered pages and updated text for '용역원실에서 노동 쉼터로'");
