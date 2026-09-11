const fs = require("fs");

const code = fs.readFileSync("book_data.js", "utf8");
const jsonStr = code.replace(/var bookData = /, "").replace(/;\s*$/, "");
const bookData = JSON.parse(jsonStr);
const pages = bookData.pages || bookData;

const lastPage = pages[pages.length - 1];
console.log("=== 에필로그 페이지 데이터 ===");
console.log("Type:", lastPage.type);
console.log("Title:", lastPage.title);
console.log("Image:", lastPage.image);

const htmlCode = fs.readFileSync("index.html", "utf8");
// 배경 이미지 처리 로직 주변을 살펴봅니다.
let lines = htmlCode.split("\n");
let bgLogic = [];
let capturing = false;
for (let i = 0; i < lines.length; i++) {
  if (
    lines[i].includes("let bgHTML =") ||
    lines[i].includes("if (page.image)")
  ) {
    capturing = true;
  }
  if (capturing) {
    bgLogic.push(lines[i]);
  }
  if (capturing && lines[i].includes("contentHTML = bgHTML")) {
    capturing = false;
    break; // 충분히 캡처됨
  }
}
console.log("\n=== index.html 배경 렌더링 로직 ===");
console.log(bgLogic.join("\n"));
