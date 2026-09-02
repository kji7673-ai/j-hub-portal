const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let ch1Found = false;
let ch2Found = false;

for (let p of bookData.pages) {
    if (p.partCategory && p.partCategory.includes('3부')) {
        // Reframing Titles
        if (p.title && p.title.includes('제1장.')) {
            p.title = p.title.replace('제1장.', '제1장. [기계가 계산할 수 없는 마음]');
            
            // Inject AI Confession into the first long text of Chapter 1
            if (!ch1Found && p.text && p.text.includes('정비사업 통합 플랫폼')) {
                p.text += `\n\n<div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);" class="handwriting">\n<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]</h4>\n저는 수만 건의 조합원 데이터를 0.1초 만에 분석하고 최적의 사업성 지표를 도출해 냅니다. 하지만, 재개발 소식에 잠을 설치며 평생 일군 터전을 떠나야 하는 원주민의 불안감은 데이터로 환산할 수 없었습니다. 숫자를 완벽하게 통제하는 것은 저의 알고리즘이지만, 그 숫자 너머의 사람을 설득하고 온기를 전하는 것은 결국 불완전한 인간, 건축가의 몫이었습니다.\n</div>`;
                ch1Found = true;
            }
        }
        
        if (p.title && p.title.includes('제2장.')) {
            p.title = p.title.replace('제2장.', '제2장. [기계가 그릴 수 없는 여백]');
            
            // Inject AI Confession into Chapter 2
            if (!ch2Found && p.text) {
                p.text += `\n\n<div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);" class="handwriting">\n<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]</h4>\n저는 프롬프트 한 줄이면 수백 개의 화려한 랜드마크 3D 모델을 즉각 렌더링할 수 있습니다. 그러나 뒷골목의 바람길을 열어주고, 이웃이 마주칠 벤치의 각도를 비워두는 '여백의 가치'는 제 알고리즘에 존재하지 않습니다. 시스템은 오직 효율로 픽셀을 채울 뿐, 비우는 법을 모릅니다. 공간이 숨을 쉬게 만드는 그 비효율적 결단은 오직 흙먼지를 마셔본 인간만이 할 수 있습니다.\n</div>`;
                ch2Found = true;
            }
        }
        
        if (p.title && p.title.includes('제3장.')) {
            p.title = p.title.replace('제3장.', '제3장. [기계가 감당할 수 없는 책임]');
        }
    }
}

// Add Epilogue
bookData.pages.push({
    "type": "text_only",
    "title": "에필로그: 마지막 1%의 불완전함",
    "text": "J-Hub가 99%의 완벽한 데이터를 실시간으로 제공하고, AI 에이전트 아키 시냅스가 세상의 모든 법규를 분석해 리스크를 방어하더라도, 건축을 최종적으로 완성하는 것은 결국 인간의 불완전한 1%입니다. \n\n기계는 정답을 주지만, 세상은 늘 정답만으로 굴러가지 않습니다. 완벽한 시스템이 우리에게 주는 진정한 선물은 '효율' 그 자체가 아닙니다. 기계가 할 수 있는 차가운 잡무들을 완벽히 위임함으로써 얻어낸 귀중한 시간과 에너지를 **'기계가 할 수 없는 일'**에 쏟을 수 있다는 점입니다.\n\n불안에 떠는 조합원의 어깨를 두드려주고, 거친 현장에서 흙먼지를 마시며 타협하고, 계산되지 않는 여백을 기꺼이 도면 위에 남겨두는 것. \n\n우리는 기계에 종속되지 않습니다. 기계의 완벽함에 인간의 따뜻한 체온(전자)을 내어줄 때 비로소 **가장 아름다운 공유결합(Covalent Bond)**이 완성됩니다. \n\n그 완벽하지 않은 여정의 끝에서, 다시 한번 도면 위에 머무는 우리의 시간이 온전히 인간의 것이 되기를 기원합니다.",
    "part": "에필로그"
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
