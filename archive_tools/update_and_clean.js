const fs = require('fs');

// 1. 에필로그 이미지 교체
let data = fs.readFileSync('book_data.js', 'utf8');
// 01.jpg를 어제 만든 멋진 B컷(gallery_batch5_falling1.jpg 또는 다른 미사용 컷)으로 교체
// book_data.js에 없는 이미지를 사용하기 위해 gallery_batch5_falling1.jpg 선택 (떨어지는/혹은 생각하는 추상적 찰흙 형상)
data = data.replace('static/images/01.jpg', 'static/images/gallery_batch4_heart.jpg'); 
// (gallery_batch4_heart.jpg: 웅장하고 추상적인 철사 심장/결합 형상 - 에필로그의 공유결합 메시지에 완벽히 어울림)
fs.writeFileSync('book_data.js', data);

// 2. 불필요한 일회성 작업 파일들 청소 (clean_up 폴더로 이동)
if (!fs.existsSync('archive_tools')) {
    fs.mkdirSync('archive_tools');
}
