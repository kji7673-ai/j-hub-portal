const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});
let pages = bookData.pages;

// 1. Text Replacements
const repl1_old = "제가 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 필사적으로 구축했던 이유는 기술이 좋아서가 아니었습니다. 기계가 할 수 있는 차가운 일들은 기계에게 모두 넘겨주고, 우리 인간만이 할 수 있는 '따뜻한 본질'로 다시 돌아가기 위한 몸부림이었습니다.";
const repl1_new = "제가 '아키 시냅스(Archisynapse)'라는 AI 시스템을 필사적으로 구축한 이유는 단 하나입니다. 최신 기술을 좇기 위해서가 아니라, 기계가 가장 잘하는 '차가운 연산'은 기계에게 모두 넘기고, 우리 인간만이 빚어낼 수 있는 '건축의 따뜻한 본질'로 돌아가기 위한 처절한 몸부림이었습니다.";

const repl2_old = "그 긴 시간 동안 신입들은 단순 반복적인 PPT 작업이나 방어적인 서류 작업에만 소모되고 있다. 왜 신입들이 오면 설계를 못 할까? 답은 간단하다. 회사가 그들에게 설계의 전체 프로세스를 경험하게 할 시간도, 법규 실무 지식을 체계적으로 가르쳐 줄 여력도 없기 때문이다.";
const repl2_new = "하지만 현실은 참혹하다. 건축의 낭만을 안고 입사한 신입들은 단순 반복적인 PPT 작업이나 방어적인 서류 작업에 청춘을 소모하고 있다. 왜 우리 신입들은 스스로 설계를 하지 못할까? 그들의 능력이 부족해서가 아니다. 회사가 그들에게 설계의 전체 프로세스를 경험하게 할 '시간'을 빼앗았고, 실무 지식을 체계적으로 가르쳐 줄 '여력'을 잃어버렸기 때문이다.";

const repl3_old = "설계사무소에서 대화형 AI 채팅창(Chat window)에 묻고 답을 얻는 방식은 완전히 틀렸다는 사실을 말이다.";
const repl3_new = "건축 실무에서 대화형 AI의 '채팅창(Chat window)'에 질문을 던지고 그 답변을 맹신하는 방식은, 혁신이 아니라 도박이며 완전히 틀린 접근이라는 사실을 말이다.";

// 2. 5060 Exec Conversation
const exec_old = "그들은 손가락으로 부드럽게 타일을 넘기며, 처음으로 미소를 지었다. \"아, 이제야 우리가 무엇을 해야 하는지 명확히 보이네요.\" 그 순간은 우리 프로젝트의 거대한 전환점이었다. 아름다움은 단순한 장식이 아니었다. 그것은 복잡함을 정복하고 사람의 마음을 여는, 가장 강력하고 실용적인 비즈니스 무기였다.";
const exec_new = `그들은 손가락으로 부드럽게 타일을 넘기며, 처음으로 미소를 지었다. "아, 이제야 우리가 무엇을 해야 하는지 명확히 보이네요."<br><br>하지만 칭찬으로 끝날 자리가 아니었다. 재무를 담당하는 김 상무가 예리하게 파고들었다.<br>"대표님, 화면 깔끔해진 건 좋은데, 이 시스템 껍데기 바꾸는 데 시간과 비용이 얼마나 들었습니까?"<br><br>나는 준비했던 데이터를 스크린에 띄우며 담담하게 답했다.<br><strong style="color:var(--primary)">"3개월의 개발비가 들었습니다. 하지만 상무님, 이 화면 하나 덕분에 지난달 Y구역 조합장님 미팅에서 '신뢰할 수 있다'는 한마디와 함께 수천만 원짜리 유료 기획 설계 계약을 따냈습니다. 그동안 무료로 던져주던 1장짜리 엑셀 보고서로는 결코 얻어내지 못했던 결과입니다. 아름다움은 사치가 아니라, 우리 회사의 가장 강력하고 수익성 높은 영업 무기입니다."</strong><br><br>회의실에는 짧은 정적이 흘렀다. 비용을 묻던 임원들의 고개가 조용히 끄덕여졌다. 그 순간은 우리 프로젝트의 거대한 전환점이었다. 아름다움은 단순한 장식이 아니었다. 그것은 복잡함을 정복하고 사람의 마음을 여는, 가장 강력하고 실용적인 비즈니스 무기였다.`;

// Helper for annotations
function getAnnotation(title, text) {
    let annotation = "";
    if (title.includes("순응") || text.includes("주변에 순응하라")) {
        annotation = "[연결된 철학: 2부 1장 '존중과 순응' / 시스템: J-Hub 대지 분석 AI]";
    } else if (title.includes("단순화") || title.includes("포용력")) {
        annotation = "[연결된 철학: 2부 2장 '포용과 사이 공간' / 시스템: J-Edu 지식 통합]";
    } else if (title.includes("페이퍼 아키텍트") || title.includes("불안")) {
        annotation = "[연결된 철학: 1부 2장 '엑셀과 서류에 짓눌린 건축가들' / 시스템: 아키 시냅스 자동 검토]";
    } else if (title.includes("논리와 감정") || title.includes("싫어요")) {
        annotation = "[연결된 철학: 2부 3장 '시지프스의 언덕과 인간다움의 회복' / 시스템: 통합 보고서의 통제권]";
    } else if (title.includes("마음을 짓는 일") || title.includes("공동체")) {
        annotation = "[연결된 철학: 2부 1장 '존중과 순응' / 시스템: J-Journal 현장 소통]";
    } else if (text.includes("AI") || title.includes("AI")) {
        annotation = "[연결된 철학: 1부 4장 '환각의 숲을 지나다' / 시스템: 레드팀 감찰 체계]";
    } else {
        annotation = "[연결된 철학: 2부 3장 '인간다움의 회복' / 증언: 현장 건축가의 고뇌]";
    }
    
    return `<div style="background-color: var(--surface-pearl, #fafafc); padding: 12px 16px; border-radius: 8px; margin-bottom: 24px; border-left: 3px solid var(--primary, #0066cc); font-size: 0.9em; color: var(--ink-muted-80, #333333); font-weight: 600; display: inline-block;">
    <svg style="vertical-align: middle; margin-right: 6px; margin-top: -2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
    ${annotation}
    </div><br>`;
}

let toRemove = [];

pages.forEach((p, index) => {
    if (p.text) {
        // Replacements
        p.text = p.text.replace(repl1_old, repl1_new);
        p.text = p.text.replace(repl2_old, repl2_new);
        p.text = p.text.replace(repl3_old, repl3_new);
        p.text = p.text.replace(exec_old, exec_new);
        p.text = p.text.replace(/\[AI와의 대화\]/g, "[아키 시냅스의 반론 (AI 에이전트의 관찰 일지)]");
    }
    
    // Part 4 filtering and annotation
    if (p.part === "4부: 증언과 성찰" && p.type !== 'interlude' && p.type !== 'image_full') {
        let t = p.title || "";
        // Remove specific unwanted chapters (like cockroach, aliens, multiverse)
        if (t.includes("바퀴벌레") || t.includes("새벽의 방문객") || t.includes("외계인") || t.includes("다중우주")) {
            toRemove.push(index);
        } else if (p.text) {
            // Apply annotation if it doesn't already have one
            if (!p.text.includes("[연결된 철학:")) {
                p.text = getAnnotation(t, p.text) + p.text;
            }
        }
    }
});

// Remove backwards to not mess up indices
for (let i = toRemove.length - 1; i >= 0; i--) {
    let idx = toRemove[i];
    pages.splice(idx, 1);
    console.log("Removed page at index " + idx);
}

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Update complete.");
