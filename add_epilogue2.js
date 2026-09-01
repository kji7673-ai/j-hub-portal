const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

let epilogueIndex = bookData.pages.findIndex(p => p.title && p.title.includes('에필로그: 26년의 경험'));

if (epilogueIndex !== -1) {
    let newEpilogue = {
        "type": "text_only",
        "title": "에필로그 2: 통제라는 이름의 괴물",
        "text": "**[나는 괴물을 만들었는가]**\n이 책의 원고를 거의 다 마무리지어갈 무렵, 나의 가장 날 선 동료이자 비판자인 한 '레드팀' 멤버가 원고를 읽고 나에게 던진 서늘한 질문 하나가 있었다.\n\n\"대표님, 우리는 직원들을 엑셀과 노가다에서 '해방'시키기 위해 J-Hub를 만들었다고 자부합니다. 하지만 그 시스템 안에서 직원들의 마우스 커서 움직임 하나까지 데이터로 수집되고, 3분짜리 쇼츠로 행동을 교정받으며, 심지어 안면 인식으로 생체 데이터를 출입에 사용합니다. 대표님은 지금 구성원을 해방시킨 것입니까, 아니면 완벽한 감시 시스템이라는 '괴물'의 배 속에 모두를 가둔 것입니까?\"\n\n그 순간, 나는 망치로 머리를 얻어맞은 듯한 충격을 받았다. 그의 말이 맞았다. 효율성이라는 이름표를 달고 내가 구축한 이 완벽한 톱니바퀴는, 내가 그토록 경멸했던 '인간을 부품으로 만드는 시스템'의 또 다른 이름일지도 모른다. 나는 기술로 건축가를 구원하겠다는 '메시아 콤플렉스'에 빠져, 나 스스로가 가장 끔찍한 빅 브라더(Big Brother)가 되어가고 있다는 사실을 외면하고 있었던 것이다.\n\n**[모순을 품고 걷는 길]**\n그의 질문 앞에 나는 이 책의 결론을 아름다운 성공담으로 포장하려던 알량한 욕심을 버리기로 했다. \n\n솔직하게 고백한다. J-Hub는 완벽하지 않다. 인간을 기계적인 반복 업무에서 구원한 것은 사실이지만, 동시에 우리를 더 촘촘한 디지털 통제망 속으로 밀어넣은 것도 부인할 수 없는 사실이다. 이것은 우리가 평생 안고 가야 할 거대한 모순(Irony)이다.\n\n그럼에도 불구하고 우리가 이 길을 계속 걸어야 하는 이유는 단 하나다. 그 모순을 끊임없이 의심하고 경계하는 '인간의 고뇌'가 살아있는 한, 기계는 결코 우리의 영혼까지 통제할 수 없기 때문이다. J-Hub는 완성된 정답이 아니라, 기계와 인간이 아슬아슬하게 공존하는 경계선 위에서 벌어지는 처절한 줄다리기일 뿐이다.\n\n그래서 나는 앞으로도 기꺼이 '레드팀'의 서늘한 비판을 맞을 것이다. 시스템이 완벽하다고 믿는 순간, 우리는 정말로 기계의 노예가 될 테니까.",
        "part": "에필로그",
        "partCategory": "에필로그"
    };

    bookData.pages.splice(epilogueIndex + 1, 0, newEpilogue);
    console.log("Inserted new epilogue at index", epilogueIndex + 1);
}

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
