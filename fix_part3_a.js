const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if (p.partCategory === '3부: 불완전한 선택의 용기' && p.title && p.title.includes('챕터 A. 기술이 풀 수 없는 것들')) {
        p.text = p.text.replace(
            /시스템이 두 조합원의 분담금을 동일하게 500만 원으로 산출했습니다\.[\s\S]*?기술은 '공정'을 추구하지만, 건축가는 거기서 한 발 더 나아가 '정의'를 고민해야 합니다\./,
            "시스템이 두 조합원의 추가 분담금을 동일하게 2억 5천만 원으로 산출했습니다.\n\n한 분은 여러 채의 부동산을 보유한 전직 경영인이었고, 다른 한 분은 이 한 집이 전 재산인 일용직 노동자였습니다. 같은 숫자, 전혀 다른 무게.\n\nAI는 이 차이를 알 수 없습니다. 재개발에서 사업의 성공만큼 중요한 것은 '원주민 정착률'입니다. 재개발 사업지가 아무리 좋은 아파트 단지로 거듭난다 하더라도, 원래 그곳에 살던 사람들이 감당하지 못해 쫓겨나듯 떠나야 한다면 결코 좋은 개발의 모델이 될 수 없습니다.\n\n그래서 기계가 내놓은 답 뒤에는 반드시 사람이 있어야 한다고 생각합니다. 기술은 주어진 데이터를 바탕으로 기계적인 '공정'을 추구하지만, 건축가는 거기서 한 발 더 나아가 그곳에 사는 사람들의 삶을 껴안는 '정의'를 고민해야 합니다."
        );
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Part 3 Chapter A updated.");
