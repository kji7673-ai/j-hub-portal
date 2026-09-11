const fs = require("fs");

const code = fs.readFileSync("book_data.js", "utf8");
const jsonStr = code.replace("var bookData = ", "").replace(/;$/, "");
const bookData = JSON.parse(jsonStr);
let pages = bookData.pages || bookData;

// 1. 에필로그 내용 추출
const epilogue = pages[pages.length - 1];
console.log("=== 현재 에필로그 ===");
console.log(epilogue.text.replace(/<[^>]+>/g, " ").replace(/\s+/g, " "));
console.log("\n====================\n");

// 2. 제4막 프로젝트 추출 및 공유결합 언급 여부 스캔
console.log("=== 제4막 프로젝트 분석 ===");
let act4Pages = pages.filter(
  (p) => p.partCategory && p.partCategory.includes("제4막"),
);

act4Pages.forEach((p) => {
  let text = p.text ? p.text.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ") : "";
  let hasBonding =
    text.includes("공유결합") ||
    text.includes("결합") ||
    text.includes("순응") ||
    text.includes("관계") ||
    text.includes("존중");
  console.log(`[프로젝트] ${p.title}`);
  console.log(`- 길이: ${text.length}자`);
  console.log(
    `- 테마(공유결합/관계 등) 포함 여부: ${hasBonding ? "있음" : "부족함"}`,
  );
  console.log(`- 결론부: ...${text.substring(text.length - 150)}`);
  console.log("------------------------");
});

// 제3막 제목 수정 적용
let updated = false;
pages.forEach((p) => {
  if (p.partCategory && p.partCategory.includes("제3막")) {
    p.partCategory = "제3막: 관계의 깊이, 나와 너의 공유결합";
    updated = true;
  }
  if (p.title && p.title.includes("여는 글: 제3막")) {
    p.title = "여는 글: 제3막: 관계의 깊이, 나와 너의 공유결합";
  }
});

if (updated) {
  let finalData = { pages: pages };
  fs.writeFileSync(
    "book_data.js",
    "var bookData = " + JSON.stringify(finalData, null, 4) + ";",
    "utf8",
  );
  console.log(
    "\n(제3막 제목이 '관계의 깊이, 나와 너의 공유결합'으로 수정되었습니다.)",
  );
}
