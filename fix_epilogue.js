const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if (p.partCategory === '3부: 불완전한 선택의 용기' && p.title && p.title.includes('에필로그: 다시, 신발을 신다')) {
        p.text = "26년 동안 설계라는 한길을 걸었습니다. 제가 걸어온 길 중에 이제 거의 20년이 정비사업 분야입니다. 그 수많은 현장에서 수없이 밑창이 닳아갔던 신발들은, 제가 정말 그 치열한 삶의 현장에 함께 있었다는 조용한 증거입니다.\n\n이제 그 수많은 발자국들이 데이터베이스 위의 픽셀로 변했습니다. 하지만 그 차가운 픽셀 안에는 여전히, 흙바닥을 밟았던 모든 무게가 담겨 있습니다.\n\n새로운 기술이라는 신발은 더 정확하게 발걸음을 기록하고, 더 빠르게 목적지에 닿게 해줍니다. 하지만 신발을 신는 발은 여전히 불완전한 우리의 발이고, 그 발이 밟는 땅은 여전히 다른 사람들의 팍팍한 삶입니다.\n\n기술은 우리가 신는 신발을 훨씬 편하게 개선해 주었지만, 결국 어느 방향으로 걸어갈지는 여전히 사람이 결정해야 합니다.\n\n완벽한 시스템을 갖추는 것도 중요하지만, 그 시스템을 사람을 위해 올바르게 쓸 용기가 훨씬 더 중요합니다.\n\n새로운 기술의 신발을 신은 우리의 발걸음이, 그 용기를 잃지 않고 묵묵히 나아가기를 조용히 바랍니다.";
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Epilogue updated.");
