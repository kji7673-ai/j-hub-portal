const fs = require('fs');
let content = fs.readFileSync('book_data.js', 'utf8');

content = content.replace(/1부 \\\[시스템편\\\]/g, '1부 [실전편]');
content = content.replace(/만들어낸 '도구'에 대한 기록입니다/g, "만들어낸 '도구(J-Hub)'에 대한 실전 기록입니다");

content = content.replace(/2부 \\\[철학편\\\]/g, '2부 [증언과 성찰편]');
content = content.replace(/건축의 본질'에 대한 이야기입니다/g, "건축의 본질'과, 현장의 쟁이로서 느꼈던 찌질하고도 솔직한 감정의 파편들입니다");
content = content.replace(/여백을 남기고 주변에 순응하는 '불완전한 선택'은 우리 인간의 몫이어야 함을 담았습니다/g, "기꺼이 '불완전한 선택'을 감내한 날것의 일기를 그대로 남겨두었습니다");

content = content.replace(/3부 \\\[증언과 성찰\\\]/g, '3부 [미래 비전편]');
content = content.replace(/은 화려한 시스템과 거창한 철학 뒤에 숨겨진, 한 명의 쟁이로서 느꼈던 찌질하고도 솔직한 감정의 파편들입니다. 찢어진 운동화, 억지스러운 타협, 텅 빈 도면 앞에서의 외로움 등 날것의 일기를 그대로 남겨두었습니다/g, "은 이 모든 현장의 고뇌를 딛고 바라본 '프롭테크와 정비사업의 거시적 미래'입니다. 낡은 시스템이 붕괴하고 투명한 데이터가 지배할 새로운 시장의 방향성을 담았습니다");

fs.writeFileSync('book_data.js', content, 'utf8');
console.log("Prologue regex replace done!");
