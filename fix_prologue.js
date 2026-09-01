const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if (p.partCategory === '프롤로그' && p.title && p.title.includes('완벽한 시스템이 아닌')) {
        p.text = p.text.replace(
            /1부 \[실전편\][\s\S]*?바랍니다\./,
            "1부 [플랫폼의 탄생] 은 쏟아지는 업무의 과부하 속에서 살아남기 위해 발버둥 치며 만들어낸 소박한 '도구'에 대한 이야기입니다. 행정적 늪에 빠져 허우적대는 실무자나 낡은 시스템의 한계를 느끼는 분들께, 정비사업의 투명성과 6가지 길을 안내하는 작은 돌파구가 되기를 바랍니다."
        );
        p.text = p.text.replace(
            /2부 \[증언과 성찰편\][\s\S]*?남겨두었습니다\./,
            "2부 [불완전함 속에서 완전함을 찾다] 는 그렇게 얻어낸 귀중한 시간 동안 다시 도면 앞에 앉아 고민했던 '건축의 본질'과, 26년 현장의 쟁이로서 느꼈던 솔직한 감정의 파편들입니다. 완벽한 데이터 앞에서도 결국 기꺼이 '불완전한 선택'을 감내한 날것의 일기 85편을 4가지 테마로 엮었습니다."
        );
        p.text = p.text.replace(
            /3부 \[미래 비전편\][\s\S]*?담았습니다\./,
            "3부 [불완전한 선택의 용기] 는 이 모든 현장의 고뇌를 딛고 바라본 다가올 10년의 풍경입니다. 기술이 지배할 새로운 시장 속에서도 결코 기계에 넘겨줄 수 없는 건축가의 존엄과 윤리, 그리고 책임감에 대한 묵직한 성찰을 담았습니다."
        );
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Prologue updated.");
