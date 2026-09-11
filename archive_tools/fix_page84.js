const fs = require('fs');
const vm = require('vm');

const data = fs.readFileSync('book_data.js', 'utf8');
const sandbox = {};
vm.runInNewContext(data, sandbox);
let pages = sandbox.bookData.pages;

// '[임시 전시]' 라는 제목을 가진 페이지 찾아서 완전 삭제
pages = pages.filter(p => p.title !== '[임시 전시] 도면 조형물 (위치 결정용)');

// 에필로그 페이지의 이미지를 01.jpg로 교체
pages.forEach(p => {
    if (p.type === 'epilogue' || p.title === '에필로그: 도면 위의 공유결합') {
        p.image = 'static/images/01.jpg'; // 또는 user_01.jpg 
    }
});

sandbox.bookData.pages = pages;
const output = 'var bookData = ' + JSON.stringify(sandbox.bookData, null, 4) + ';';
fs.writeFileSync('book_data.js', output);
console.log("Deleted temporary page and updated epilogue image.");
