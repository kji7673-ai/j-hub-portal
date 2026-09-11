const fs = require("fs");

let css = fs.readFileSync("style.css", "utf8");

// 본문 문단 스타일 보완 (마진 추가)
if (!css.includes("margin-bottom: 24px")) {
  css = css.replace(
    "p.body-text {",
    "p.body-text {\n        margin-bottom: 24px;",
  );
}

fs.writeFileSync("style.css", css);

let html = fs.readFileSync("index.html", "utf8");

// 표지 간격 수정
// cover 제목 부분 간격 넓히기
html = html.replace(
  "font-size: 2.8em; color: #1d1d1f; margin-bottom: 10px; font-weight: 800;",
  "font-size: 2.8em; color: #1d1d1f; margin-bottom: 24px; font-weight: 800;",
);
html = html.replace("margin-top:-20px;", "margin-top: 16px;");
// 본문 단락 간격
html = html.replace(/<p>/g, '<p class="body-text">');
fs.writeFileSync("index.html", html);

console.log("Styles fixed.");
