const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const oldData = eval('(' + match[2] + ')');
const oldPages = oldData.pages;

// Helpers to find pages
function findPageByTitle(title) {
    return oldPages.find(p => p.title && p.title.includes(title));
}

let newPages = [];

// =====================================
// [프롤로그]
// =====================================
newPages.push(findPageByTitle('불완전한 선택: AI 시대 건축가의 성찰'));
newPages.push(findPageByTitle('프롤로그: 완벽한 시스템이 아닌'));

// =====================================
// [1부] 설계의 본질 - 공유결합
// =====================================
const part1Cat = '1부: 설계의 본질 - 공유결합';
newPages.push({ type: 'interlude', title: '1부. 설계의 본질 – 공유결합', partCategory: part1Cat });

// 1-1. 무기가 아닌 약속
let page1_1 = findPageByTitle('기획서는 무기가 아니다');
if(page1_1) { page1_1.partCategory = part1Cat; newPages.push(page1_1); }

// 1-2. 공유결합의 세 가지 질문
newPages.push({
    type: 'text',
    title: '제2장. 공유결합의 세 가지 질문',
    partCategory: part1Cat,
    text: `설계는 단지 도면을 그리는 행위가 아닙니다. 그것은 '내가 누구인지'를 알고, '상대가 무엇을 원하는지'를 이해하며, 우리가 발 디딜 '현장이 어떤 곳인지'를 파악하는 세 가지 질문에서 출발합니다. 이 세 가지가 하나로 만날 때 비로소 화학의 공유결합처럼 단단한 신뢰가 구축됩니다.`
});

let page1_2_q1 = findPageByTitle('공유 결합: 사람을 향한 건축');
if(page1_2_q1) { page1_2_q1.partCategory = part1Cat; newPages.push(page1_2_q1); }

// =====================================
// [2부] 85개 에세이 - 현장의 목소리, 공유결합의 증거
// =====================================
const part2Cat = '2부: 증언과 성찰';
newPages.push({ type: 'interlude', title: '2부. 현장의 목소리, 공유결합의 증거', partCategory: part2Cat });
newPages.push(findPageByTitle('26년 현장의 기록'));

const theme1 = ['찢어진 운동화', '삼켜낸 말과 술 한 잔', '가장 작은 생존 신고, "힘내자"', '무제', '가끔', '우리가 이렇게 살아갑니다', '외로움', '오늘은 우리집 소파에서 또...', '에너지의 소진으로', '요즘 잠을 잘 수가 없다', '내 자신은', '난 약한 사람입니다', '난 슬픔과 기쁨에 반응이 둔한편이다', '작아진 남자', '맘이', '나랑 같이 놀든이가', '가끔 나에게 실망을 했다는 사람들을 본다', '고상하다는 것은 부끄러워한다는 것이며,', '감정 쪼개기', '당신의 세상은 어떤가요?', '쟁이의 마음: 두려움을 넘어 다시 붓을 드는 이유', '흔들리는 오뚝이'];
const theme2 = ['다정함: 인격적 성숙이 곧 디자인이다', '마음을 짓는 일: 공동체 주택 설계', '어제 만난 그 사람을...', '그렇게 하실 것 같습니다.', '사람을 이용할 때', '타인의 시선을 공유한다는것은', '선 긋기와 인생: 전체로 볼 때 직선이면 족하다', '단순화와 포용력', '거짓이 진실을 만났을 때', '뇌물이 괴물이 된다', '단두리', '십원짜리', '\'조은 슈퍼\'', '논리와 감정 사이, 건축가의 \'싫어요\'', '선을', '거름종이 마법이 있다', '말과 마음의 사이', '귀를 통해 마음으로들어간 것이', '침묵이란', '인간의 삶이 나무와 같다 했던가', '천국은', '혹시 다중 우주론이라고아세요?'];
const theme3 = ['주변에 순응하라', 'AI가 읽지 못하는 지역 맥락', '100년의 기억을 덮는다는 것의 무게', '북서향 집이다', '다닥 다닥 붙은 집들', '맥락 속의 완벽함 (Harmony, Not Perfection)', '내가 생각하는 디자인 1', '내가 생각하는 디자인 2', '방향성과 중심성', '스케일과 대비', '사이 공간(Void)의 힘', '비워냄의 미학', '시지프스의 언덕', '생각의 힘: 고정관념을 벗고', '만들고 있는 것인가', '구겨진 도면', '연필로 설계를 할때', '수박으로 시대의 흐름을 판별하는', '만지작거리고 바스락거린다.', '필연의 신은 누구인가요', '하지말아야 될것이 있는것에 익숙해져버렸다'];
const theme4 = ['심의와 설득의 기술', '타당성 검토의 배신', '화려한 조감도 뒤에 가려진 씁쓸한 현실', '페이퍼 아키텍트의 불안', '오늘 건축 심의가 있는 날이다.', '심의전 자문받겠다해서', '설계를 하다보면 페이퍼 아키텍쳐라는...', '현상설계를 진행하며', '노동 쉼터', '선택(Choice)이 곧 건축이다', '건축 설계', '설계하는 일에서 좋은 점은', '기계의 질문, 인간의 답', '목적이 분명한 기획자는', '죽음이후에', '우리 이렇게 오늘도', '우리가 그렇게 오늘을', '설이 왔습니다.', '오늘을 살아라는', '있을뿐', '모두들', '천천히', '오늘을 의지해살아갑니다', '초침하나'];

function pushTheme(title, intro, textArr, outro) {
    newPages.push({ type: 'cover', title: title, partCategory: part2Cat });
    newPages.push({ type: 'text', title: '[도입] ' + title, partCategory: part2Cat, text: intro });
    textArr.forEach(t => {
        let p = findPageByTitle(t);
        if(p) { p.partCategory = part2Cat; newPages.push(p); }
    });
    newPages.push({ type: 'text', title: '[성찰] ' + title, partCategory: part2Cat, text: outro });
}

pushTheme('◆ 테마 1: 내가 무엇인가', 
    '설계는 도면을 그리기 전에, 펜을 쥔 내가 어떤 사람인지 마주하는 고독한 작업입니다. 26년간 신발 밑창이 닳도록 뛰어다니며 느꼈던 솔직한 감정들을 엮었습니다.',
    theme1, 
    '자기 정체성 없이는 결코 어떤 선도 온전히 그어질 수 없음을, 이 오랜 외로움과 고뇌를 통해 배웠습니다.');

pushTheme('◆ 테마 2: 상대를 아는 것', 
    '건축은 결국 다른 사람의 삶을 온전히 껴안는 법을 배우는 과정입니다. 조합원, 시공자, 그리고 이웃들의 마음에 공감하려 애썼던 순간들입니다.',
    theme2,
    '결국 설계는 혼자 하는 것이 아니라, 타인과 함께 지어가는 것임을. 그들과의 깊은 공감이 곧 가장 튼튼한 건축의 뼈대임을 깨닫습니다.');

pushTheme('◆ 테마 3: 현장의 맥락 읽기', 
    '백지 위에서 시작하는 설계는 없습니다. 땅이 가진 기억과 돌발변수들을 겸허히 수용하는 것이 진짜 실력입니다.',
    theme3,
    '완벽한 도면은 없습니다. 현장의 제약과 불완전함을 있는 그대로 수용할 때, 설계는 가장 현실적이고 아름다운 해답을 찾아냅니다.');

pushTheme('◆ 테마 4: 공유결합의 순간들', 
    '나와 타인, 그리고 현장이 부딪히며 만들어내는 폭발적인 에너지. 신뢰가 싹트고 인간과 시스템이 결합하는 현장의 생생한 이야기입니다.',
    theme4,
    "이 모든 땀방울이 모여 '신뢰'라는 단단한 공유결합을 이룹니다. 그것이 우리가 서류와 시스템을 넘어 끝까지 지켜내야 할 현장의 가치입니다.");

// =====================================
// [3부] 시스템 - 공유결합을 가능하게 하는 구조
// =====================================
const part3Cat = '3부: 공유결합을 가능하게 하는 시스템';
newPages.push({ type: 'interlude', title: '3부. 공유결합을 가능하게 하는 시스템', partCategory: part3Cat });

newPages.push({
    type: 'text',
    title: '제1장. 진양건축의 26년 - 신뢰의 축적',
    partCategory: part3Cat,
    text: `우리는 오랜 시간 하나의 질문을 던졌습니다. "이 무형의 신뢰를 어떻게 기술로, 시스템으로 옮길 수 있을까?"\n\n조합원이 기획서를 의심할 때, 시공자가 설계의 의도를 모를 때, 그리고 시간이 지나 누군가 '그때 왜 그렇게 결정했지?'라고 물을 때... 우리는 이 모든 불투명함을 걷어내기 위해 모든 과정을 '기록'하고 '투명하게' 공개하는 시스템을 만들었습니다.\n\n그것이 바로 'J-Hub'입니다. 기획부터 준공까지의 6단계(Phase 0~5) 여정은 단순한 기술의 나열이 아닙니다. 그것은 기획서와 도면이 온전한 '신뢰'가 되도록 뒷받침하는 진양건축 26년 철학의 집약체입니다.`
});

let p0 = findPageByTitle('제1장. 투명성의 약속'); if(p0) { p0.partCategory = part3Cat; p0.title = "제2장. 투명성의 약속 (투 트랙 시스템)"; newPages.push(p0); }
let p1 = findPageByTitle('제2장. 6가지 길'); if(p1) { p1.partCategory = part3Cat; p1.title = "제3장. 6가지 길 중 당신의 길 찾기"; newPages.push(p1); }
let p2 = findPageByTitle('제3장. 누가, 언제, 무엇을 하는가'); if(p2) { p2.partCategory = part3Cat; p2.title = "제4장. 누가, 언제, 무엇을 하는가?"; newPages.push(p2); }

let pA = findPageByTitle('챕터 A. 기술이 풀 수 없는 것들'); if(pA) { pA.partCategory = part3Cat; newPages.push(pA); }
let pB = findPageByTitle('챕터 B. 10년 뒤 정비사업의 풍경'); if(pB) { pB.partCategory = part3Cat; newPages.push(pB); }
let pC = findPageByTitle('챕터 C. 건축가의 존엄을 지키는 법'); if(pC) { pC.partCategory = part3Cat; newPages.push(pC); }

// 에필로그
let ep1 = findPageByTitle('다시, 신발을 신다'); if(ep1) { ep1.partCategory = part3Cat; newPages.push(ep1); }

// =====================================
// [부록]
// =====================================
const appCat = '부록';
newPages.push({ type: 'interlude', title: '부록. 기술 상세 및 원문', partCategory: appCat });
oldPages.filter(p => p.partCategory === '부록').forEach(p => {
    // Keep only some core appendix items to shorten as requested
    if(p.title && (p.title.includes('QR') || p.title.includes('마스터 프롬프트') || p.title.includes('자가 진단'))) {
        p.partCategory = appCat;
        newPages.push(p);
    }
});
// Add a short summary for the rest
newPages.push({
    type: 'text',
    title: '[부록] J-Hub 플랫폼 및 아키텍처 상세',
    partCategory: appCat,
    text: `본 책에서는 원고의 무게를 덜고 철학적 메시지에 집중하기 위해 방대한 기술 문서(SRD, 아키텍처 다이어그램, 5개 협력사 역할 상세 등)를 축약하였습니다.\n\n더 상세한 기술 문서와 정비사업 유형별 세부 해설은 진양건축의 온라인 포털을 통해 확인하실 수 있습니다.`
});

// Update data
oldData.pages = newPages;

const newContent = match[1] + JSON.stringify(oldData, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Rebuild complete. Total pages: " + newPages.length);
