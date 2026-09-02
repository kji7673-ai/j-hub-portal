const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const coverObjects = [
    {
        "type": "image_full",
        "title": "기계 99%, 인간 1%: 신뢰를 짓는 일",
        "subtitle": "도면 위의 공유결합: 26년 현장의 기록",
        "image": "static/images/1.jpg",
        "text": "",
        "partCategory": "프롤로그"
    },
    {
        "type": "author_profile"
    },
    {
        "type": "image_top",
        "title": "프롤로그: 완벽한 시스템이 아닌, 불완전한 쟁이의 생존기",
        "subtitle": "",
        "image": "static/images/05.jpg",
        "text": "<p style=\"font-size: 1.1em; line-height: 1.8; margin-bottom: 24px;\">안녕하세요. 도면 위에서, 그리고 거친 현장에서 26년째 구르고 있는 평범한 건축 쟁이입니다.</p>\n\n<p style=\"margin-bottom: 24px;\">처음 이 기록을 엮기로 마음먹었을 때, 참 많은 망설임이 있었습니다. 시중에는 이미 AI와 혁신을 다루는 훌륭한 전문가들의 책이 차고 넘치기 때문입니다. 하지만 용기를 내어 이 부끄러운 기록을 세상에 꺼내놓는 이유는 기술서나 시스템 개발기를 쓰기 위함이 결코 아닙니다.</p>\n\n<p style=\"margin-bottom: 24px;\">이 책은 <strong>'설계라는 것, 디자인이라는 것이 과연 무엇인가'</strong>에 대해 저의 후배들에게, 그리고 언젠가 이 글을 읽게 될 <strong>내 아들에게 전해주고 싶은 이야기</strong>입니다.</p>",
        "part": "프롤로그",
        "partCategory": "프롤로그"
    },
    {
        "type": "text",
        "title": "프롤로그: 완벽한 시스템이 아닌, 불완전한 쟁이의 생존기 (계속)",
        "subtitle": "",
        "image": "static/images/4.jpg",
        "text": "<p style=\"margin-bottom: 24px;\">언제부터인가 우리는 선을 긋고 공간을 상상하는 시간보다, 엑셀 칸을 채우고 심의 서류를 넘기며 해명하는 데 더 많은 밤을 지새우게 되었습니다. 제가 진양건축의 대표로서 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 구축했던 이유는 기술을 자랑하기 위해서가 아니었습니다. 기계가 할 수 있는 차가운 일들은 기계에게 맡기고, 우리 인간만이 할 수 있는 '따뜻한 본질'과 '공간에 대한 치열한 고민'으로 다시 돌아가기 위한 몸부림이었습니다. (물론 이 책을 읽으시며, 우리 회사가 정비사업에서 얼마나 체계적이고 앞선 AI 시스템을 갖추고 있는지 은연중에 느끼신다면 그것 또한 감사한 일입니다.)</p>\n\n<p style=\"margin-bottom: 24px;\">이 책은 다소 불친절하고 이질적인 세 가지 이야기로 구성되어 있습니다.<br>독자 여러분께 이 책을 어떻게 읽어주십사 하는 작은 <strong>안내(Guide)</strong>를 덧붙입니다.</p>",
        "part": "프롤로그",
        "partCategory": "프롤로그"
    }
];

// Ensure we don't duplicate if they already somehow exist
bookData.pages = bookData.pages.filter(p => p.type !== "author_profile" && p.partCategory !== "프롤로그");

bookData.pages = [...coverObjects, ...bookData.pages];

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
