const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// Group pages into buckets
let prologue = [];
let part1 = [];
let part2 = [];
let part3 = [];
let part4 = [];
let appendices = [];
let unassigned = [];

// Helper to find and extract by exact title
function pullByTitle(title) {
    const idx = bookData.pages.findIndex(p => p.title === title);
    if (idx !== -1) {
        return bookData.pages.splice(idx, 1)[0];
    }
    return null;
}

function pullByKeyword(keyword) {
    const idx = bookData.pages.findIndex(p => p.title && p.title.includes(keyword));
    if (idx !== -1) {
        return bookData.pages.splice(idx, 1)[0];
    }
    return null;
}

// 1. Prologue Setup
prologue.push(pullByTitle("프롤로그: 건축 외에는 아무것도 모르는 바보의 이야기"));
prologue.push(pullByTitle("어느 날, 공유결합이 내게로 왔다"));

// 2. Part 1 (Philosophy)
part1.push(pullByTitle("1부. 설계의 본질 – 공유결합"));
part1.push(pullByTitle("공유결합이라고 혹시 들어 보셨나요?"));
part1.push(pullByTitle("공유결합의 첫 질문"));
part1.push(pullByTitle("질문의 확장: \"그렇다면 상대는 어떤가?\""));
part1.push(pullByTitle("공유결합의 두 번째 질문"));
part1.push(pullByTitle("질문의 확장: \"그 상대가 살 현장은 어떤가?\""));
part1.push(pullByTitle("공유결합의 세 번째 질문"));
part1.push(pullByTitle("계획안, 신뢰의 기록"));
part1.push(pullByTitle("공유 결합: 사람을 향한 건축, 용산 현장의 기억"));
part1.push(pullByTitle("내가 생각하는 디자인 1: 존중과 순응"));
part1.push(pullByTitle("주변에 순응하라"));
part1.push(pullByTitle("내가 생각하는 디자인 2: 포용과 사이 공간"));
part1.push(pullByTitle("사이 공간(Void)의 힘"));
part1.push(pullByTitle("맥락 속의 완벽함 (Harmony, Not Perfection)"));
part1.push(pullByTitle("방향성과 중심성"));
part1.push(pullByTitle("스케일과 대비"));
part1.push(pullByTitle("단순화와 포용력"));

// 3. Part 2 (Field Stories)
part2.push(pullByTitle("2부. 현장의 목소리, 공유결합의 증거"));
part2.push(pullByTitle("26년 현장의 기록"));
part2.push(pullByTitle("찢어진 운동화"));
part2.push(pullByTitle("뇌물이 괴물이 된다"));
part2.push(pullByTitle("'조은 슈퍼'"));
part2.push(pullByTitle("삼켜낸 말과 술 한 잔"));
part2.push(pullByTitle("우리가 이렇게 살아갑니다"));
part2.push(pullByTitle("난 약한 사람입니다"));
part2.push(pullByTitle("쟁이의 마음: 두려움을 넘어 다시 붓을 드는 이유"));
part2.push(pullByTitle("100년의 기억을 덮는다는 것의 무게"));
part2.push(pullByTitle("오뚝이"));
part2.push(pullByTitle("구겨진 도면"));
part2.push(pullByTitle("연필로 설계를 할때"));
part2.push(pullByTitle("설계하는 일에서 좋은 점은"));
part2.push(pullByTitle("현상설계를 진행하며"));
part2.push(pullByTitle("가장 작은 생존 신고, \"힘내자\""));
part2.push(pullByTitle("가끔"));
part2.push(pullByTitle("외로움"));

// 4. Part 3 (AI and System)
let p3_cover = pullByKeyword("기계를 거부하지 않기로 결심한 날");
if(p3_cover) part3.push(p3_cover);
part3.push(pullByKeyword("2부를 마치며")); // Transition text to AI
part3.push(pullByTitle("기계의 질문, 인간의 답"));
part3.push(pullByTitle("AI, 그래 넌 AI고 난 JI다"));
part3.push(pullByTitle("페이퍼 아키텍트의 불안과 진짜 설계의 무게"));
part3.push(pullByTitle("막간극: 목적이 분명한 기획자는 어떻게 기계를 움직이는가"));
part3.push(pullByTitle("기술이 지워진 자리에 남은 것 (비워냄의 미학)"));
part3.push(pullByTitle("시지프스의 언덕과 인간다움의 회복"));

// 5. Part 4 (Epilogue / Conclusion)
let p4_cover = pullByKeyword("에필로그");
if(p4_cover) part4.push(p4_cover);
part4.push(pullByTitle("결론을 향하여: \"내+상대+현장이 만날 때\""));
part4.push(pullByTitle("공유결합의 완성"));

// 6. Appendices
appendices.push(pullByTitle("부록 A. J-Hub 기술 개요"));
appendices.push(pullByTitle("부록 A. [기계가 계산할 수 없는 마음] 진양건축의 26년 - 신뢰의 축적"));
appendices.push(pullByTitle("부록 B. 자기 조직 진단 체크리스트"));
appendices.push(pullByTitle("부록 C. 생각을 명확히 하는 법 (마스터 프롬프트)"));

// Anything else left behind? Filter out "No Title", nulls, or random snippet artifacts
let remaining = bookData.pages.filter(p => p !== null && p.title && p.title !== 'No Title' && !p.title.includes("마치며") && !p.title.includes("테마"));

// Combine them all in a clean array, filtering out nulls
let finalPages = [
    ...prologue,
    ...part1,
    ...part2,
    ...part3,
    ...part4,
    ...remaining, // Put remaining poems at the end before appendices or inside part 2
    ...appendices
].filter(p => p !== null);

bookData.pages = finalPages;

// Editoral Rewrite Pass
bookData.pages.forEach(p => {
    if (!p.text) return;
    
    // Spelling fixes
    p.text = p.text.replace(/포크레인/g, '굴착기'); // Standard Korean
    p.text = p.text.replace(/욱여넣을/g, '욱여넣을'); 
    p.text = p.text.replace(/보고싶은대로/g, '보고 싶은 대로');
    p.text = p.text.replace(/고정되어진/g, '고정된');
    
    // Enhance Prologue
    if (p.title && p.title.includes('어느 날, 공유결합이')) {
        p.text = p.text.replace("이 말에 그래 우린 몸도 이온과 공유결합으로 이루어 져 있는데, 나와 사람과의 관계 모든 관계성에 공유 겹합이 있구나, 하늘과 땅 그리고 사람. 사람은 \"네~\"라고 응당할수 있으며, 연결 짓고, 연결하는 창조자의 위치까지도 있구나 하는 생각든 든 날이였습니다. 그날 이후 전 \"공유결합\"이라는 메타포를 가지고 설계를 하고 있습니다. _ 이 내용이 어떤가요?", "이온 결합이 서로의 전자를 빼앗거나 주면서 결합한다면, 공유결합은 각자의 전자를 '공유'하여 가장 안정적인 상태를 이룹니다. 이 말에 문득 깨달음이 왔습니다. 아, 우리의 몸도, 건축도, 사람과 사람의 관계도 결국 서로의 것을 내어주고 공유하며 안정된 구조를 이루는 '공유결합'이구나. 하늘과 땅, 그리고 그 사이를 잇는 사람. '왜'가 아닌 '네'라고 응답하며 타인과 기꺼이 마음을 나누고 공간을 연결하는 창조자. 그날 이후, 저는 이 '공유결합'이라는 메타포를 가슴에 품고 제 모든 설계의 바탕으로 삼았습니다.");
    }
    
    // Unify AI/JI
    if (p.title === "AI, 그래 넌 AI고 난 JI다") {
        if(!p.text.includes('정일(JI)')) {
            p.text = p.text.replace(/JI/g, 'JI(Jeong-Il)');
        }
        if(!p.text.includes('공유결합')) {
            p.text += "\n\n<p style=\"margin-top: 24px;\">AI라는 막강한 기술마저도 결국 인간 건축가의 따뜻한 숨결, 즉 '인간(JI)과의 공유결합'을 통해서만 비로소 진정한 건축으로 거듭날 수 있습니다.</p>";
        }
    }

    // Enhance Conclusion
    if (p.title === '공유결합의 완성') {
        p.text = p.text.replace("이것으로 기나긴 증언과 성찰의 일지를 마칩니다.", "이 책에 담긴 26년의 궤적이, 차가운 콘크리트 속에서도 온기를 피워내는 진짜 건축을 꿈꾸는 이들에게 작은 위로와 영감이 되기를 바랍니다. 이것으로 기나긴 증언과 성찰의 일지를 마칩니다.");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Reorganized and edited book_data.js successfully. New page count:", bookData.pages.length);
