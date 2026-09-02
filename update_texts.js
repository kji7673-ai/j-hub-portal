const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.text && p.text.includes("내 아들에게 전해주고 싶은 이야기")) {
        p.text = p.text.replace("내 아들에게 전해주고 싶은 이야기", "내 가족들에게 전해주고 싶은 이야기");
    }
    
    if (p.text && p.text.includes("엑셀 칸을 채우고 심의 서류를 넘기며 해명하는 데 더 많은 밤을 지새우게 되었습니다.")) {
        // Rewrite the paragraph to smoothly connect the user's intent
        p.text = p.text.replace(
            "언제부터인가 우리는 선을 긋고 공간을 상상하는 시간보다, 엑셀 칸을 채우고 심의 서류를 넘기며 해명하는 데 더 많은 밤을 지새우게 되었습니다. 제가 진양건축의 대표로서 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 구축했던 이유는 기술을 자랑하기 위해서가 아니었습니다. 기계가 할 수 있는 차가운 일들은 기계에게 맡기고, 우리 인간만이 할 수 있는 '따뜻한 본질'과 '공간에 대한 치열한 고민'으로 다시 돌아가기 위한 몸부림이었습니다. (물론 이 책을 읽으시며, 우리 회사가 정비사업에서 얼마나 체계적이고 앞선 AI 시스템을 갖추고 있는지 은연중에 느끼신다면 그것 또한 감사한 일입니다.)",
            "언제부터인가 우리는 선을 긋고 공간을 상상하는 시간보다, 용적률을 채우고 시공사가 원하는 설계 기준에 맞추는 것이 아파트 설계의 주된 업무가 되어 버렸습니다. 제가 진양건축의 대표로서 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 구축했던 이유는 기술을 자랑하기 위해서가 아닙니다. 기계가 할 수 있는 그 차가운 계산과 수치 맞추기는 기계에게 맡기고, 우리 인간만이 할 수 있는 '따뜻한 본질'과 '공간에 대한 치열한 고민'으로 다시 돌아가기 위한 몸부림이었습니다. 제가 이 글을 쓰는 궁극적인 이유는 바로 <strong>AI와 협업하는 건축설계의 진정한 의미</strong>에 대해 이야기하기 위함입니다. 그리고 이는 제가 설계의 가장 중요한 메타포로 삼아온 <strong>'공유결합'</strong>의 철학과도 정확히 일맥상통합니다."
        );
    }
    
    if (p.title === "어느 날, 공유결합이 내게로 왔다") {
        p.title = "공유결합이라고 혹시 들어 보셨나요?";
        
        if (p.text && p.text.includes("그것이 바로 제가 26년 동안 도면 위에서 증명하고자 했던 건축의 진짜 모습입니다.")) {
            p.text = p.text.replace(
                "그것이 바로 제가 26년 동안 도면 위에서 증명하고자 했던 건축의 진짜 모습입니다.",
                "지금까지 그래왔듯이, 이 철학은 앞으로의 저의 설계에 있어서도 흔들리지 않는 굳건한 기준이 될 것입니다. 지금부터 이 공유결합에 대한 이야기를 여러분과 함께 나누고 싶습니다."
            );
        }
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
