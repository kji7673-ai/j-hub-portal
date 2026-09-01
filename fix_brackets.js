const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

let newPages = [];

for (let i = 0; i < data.pages.length; i++) {
    let p = data.pages[i];
    
    // Add cover for Y구역 2
    if (p.title === '[Y구역 현장 기록 2] AI가 읽지 못하는 지역 맥락: 달동네의 바람길') {
        newPages.push({ type: 'cover', title: 'Y구역 현장 기록', partCategory: p.partCategory, image: 'static/images/24.jpg' });
        p.title = 'AI가 읽지 못하는 지역 맥락: 달동네의 바람길';
    }
    // Add cover for 디자인 철학
    else if (p.title === '[디자인 철학] 내가 생각하는 디자인 1: 존중과 순응') {
        newPages.push({ type: 'cover', title: '내가 생각하는 디자인이란?', partCategory: p.partCategory, image: 'static/images/24.jpg' });
        p.title = '내가 생각하는 디자인 1: 존중과 순응';
    }
    // Fix others
    else if (p.title === '[디자인 철학] 내가 생각하는 디자인 2: 포용과 사이 공간') {
        p.title = '내가 생각하는 디자인 2: 포용과 사이 공간';
    }
    else if (p.title === '[디자인 철학] 시지프스의 언덕과 인간다움의 회복') {
        p.title = '시지프스의 언덕과 인간다움의 회복';
    }
    // Add cover for Y구역 3,1 (they are sequential in Theme 4)
    else if (p.title === '[Y구역 현장 기록 3] 완벽한 보고서의 패배: 심의와 설득의 기술') {
        newPages.push({ type: 'cover', title: 'Y구역 현장 기록', partCategory: p.partCategory, image: 'static/images/25.jpg' });
        p.title = '완벽한 보고서의 패배: 심의와 설득의 기술';
    }
    else if (p.title === '[Y구역 현장 기록 1] 서류 완벽주의의 함정: 타당성 검토의 배신') {
        p.title = '서류 완벽주의의 함정: 타당성 검토의 배신';
    }
    else if (p.title === '[통찰] 기획서는 무기가 아니다, 신뢰의 기록이다') {
        p.title = '기획서는 무기가 아니다, 신뢰의 기록이다';
    }
    else if (p.title && p.title.includes('막간극(Interlude). [AI의 시선] 목적이 분명한 기획자는 어떻게 기계를 움직이는가')) {
        p.title = '막간극: 목적이 분명한 기획자는 어떻게 기계를 움직이는가';
    }
    
    newPages.push(p);
}

data.pages = newPages;
const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Bracket titles fixed.");
