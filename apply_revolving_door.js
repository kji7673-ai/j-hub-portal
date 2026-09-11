const fs = require("fs");
const vm = require("vm");
const path = require("path");

const code = fs.readFileSync("book_data.js", "utf8");
const script = new vm.Script(code);
const context = {};
vm.createContext(context);
script.runInContext(context);

let pages = context.bookData.pages;

// 1. Enhance Case Studies with Titles and Explicit Intro
let p1 = pages.find((p) => p.title && p.title.includes("서계동 현상설계"));
if (p1 && !p1.title.includes("[물리적")) {
  p1.title = "[물리적 공유결합의 실증] 서계동 현상설계";
  p1.text =
    "<div style='padding:16px; background:#eef4fa; border-left:4px solid #0066cc; margin-bottom:24px;'><strong>이것은 '공유결합의 4가지 층위' 중 첫 번째, 지형의 약점과 주민의 편의가 상호 보완하는 '물리적 공유결합'에 관한 기록입니다.</strong></div>" +
    p1.text;
}

let p2 = pages.find((p) => p.title && p.title.includes("100년의 기억"));
if (p2 && !p2.title.includes("[시간적")) {
  p2.title = "[시간적 공유결합의 실증] 100년의 기억을 덮는다는 것";
  p2.text =
    "<div style='padding:16px; background:#eef4fa; border-left:4px solid #0066cc; margin-bottom:24px;'><strong>이것은 '공유결합의 4가지 층위' 중 두 번째, 과거의 흔적과 현대적 개발이 공존하는 '시간적 공유결합'에 관한 기록입니다.</strong></div>" +
    p2.text;
}

let p3 = pages.find((p) => p.title && p.title.includes("용역원실에서"));
if (p3 && !p3.title.includes("[인간적")) {
  p3.title = "[인간적 공유결합의 실증] 용역원실에서 노동 쉼터로";
  p3.text =
    "<div style='padding:16px; background:#eef4fa; border-left:4px solid #0066cc; margin-bottom:24px;'><strong>이것은 '공유결합의 4가지 층위' 중 세 번째, 공간의 위계를 허물고 노동자의 존엄을 지켜내는 '인간적 공유결합'에 관한 기록입니다.</strong></div>" +
    p3.text;
}

let p4 = pages.find((p) => p.title && p.title.includes("어느 심의 날의 기록"));
if (p4 && !p4.title.includes("[제도적")) {
  p4.title = "[제도적 공유결합의 실증] 어느 심의 날의 기록";
  p4.partCategory = "제1막: 공유결합 디자인 방법론"; // 2막에서 1막으로 이동
  p4.text =
    "<div style='padding:16px; background:#eef4fa; border-left:4px solid #0066cc; margin-bottom:24px;'><strong>이것은 '공유결합의 4가지 층위' 중 네 번째, 자본과 공공의 규제, 그리고 주민의 이해관계가 조율되는 '제도적 공유결합'에 관한 기록입니다.</strong></div>" +
    p4.text;
}

// 2. Add Bridge to Act 2
let act2Intro = pages.find(
  (p) => p.title === "여는 글: 제2막: 나라는 개체의 독립과 생존",
);
if (act2Intro && !act2Intro.text.includes("뼈아픈 기록")) {
  act2Intro.text +=
    "<br><br>1막에서 도면 위의 물리적, 시간적, 인간적, 제도적 공유결합을 이야기했다면, 2막은 이 거대한 결합을 감당해내기 위해 건축가 개인이 현장과 도시에서 겪어내야 했던 '내면의 생존과 독립'에 대한 뼈아픈 기록입니다.";
}

// 3. Add Bridge to Act 3
let act3Intro = pages.find(
  (p) => p.title === "여는 글: 제3막: 사람을 알아가는 관계성",
);
if (act3Intro && !act3Intro.text.includes("사회적 실천")) {
  act3Intro.text +=
    "<br><br>결국 모든 공유결합의 완성은 '사회적 실천'으로 이어집니다. 물리적, 제도적 결합을 넘어, 3막은 타인과 부딪히며 다름을 이해하고 마침내 더 큰 사회적 결합(공동체)으로 나아가는 가장 따뜻한 관계의 이야기입니다.";
}

// 4. Reorder to ensure Act groupings and correct case study sequence in Act 1
let frontMatter = pages.filter(
  (p) =>
    !p.partCategory ||
    (!p.partCategory.includes("1막") &&
      !p.partCategory.includes("2막") &&
      !p.partCategory.includes("3막") &&
      !p.title.includes("에필로그")),
);
let act1 = pages.filter(
  (p) => p.partCategory && p.partCategory.includes("1막"),
);
let act2 = pages.filter(
  (p) => p.partCategory && p.partCategory.includes("2막"),
);
let act3 = pages.filter(
  (p) => p.partCategory && p.partCategory.includes("3막"),
);
let epilogue = pages.filter((p) => p.title && p.title.includes("에필로그"));

// Ensure p4 is right after p3 in Act 1
let p3Index = act1.findIndex((p) =>
  p.title.includes("용역원실에서 노동 쉼터로"),
);
let p4Index = act1.findIndex((p) => p.title.includes("어느 심의 날의 기록"));
if (p3Index !== -1 && p4Index !== -1 && p4Index !== p3Index + 1) {
  let p4Obj = act1.splice(p4Index, 1)[0];
  // Re-find p3 index after removal just in case
  p3Index = act1.findIndex((p) => p.title.includes("용역원실에서 노동 쉼터로"));
  act1.splice(p3Index + 1, 0, p4Obj);
}

pages = [...frontMatter, ...act1, ...act2, ...act3, ...epilogue];

const outputString = "var bookData = " + JSON.stringify(pages, null, 4) + ";";
fs.writeFileSync("book_data.js", outputString, "utf8");

// Generate HTML
let html = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>도면 위의 공유결합 - 출판 투고용 최종 원고</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        body { font-family: 'Pretendard', sans-serif; line-height: 1.8; color: #1d1d1f; max-width: 860px; margin: 0 auto; padding: 40px 20px; background-color: #f5f5f7; word-break: keep-all; }
        .page { background: #ffffff; padding: 60px 80px; margin-bottom: 40px; border-radius: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.04); }
        @media (max-width: 768px) { .page { padding: 40px 30px; } }
        h1.book-title { font-size: 2.5em; color: #1d1d1f; margin-bottom: 20px; text-align: center; font-weight: 800; letter-spacing: -0.03em; }
        h1.book-title span { display: block; font-size: 0.45em; color: #7a7a7a; font-weight: 400; margin-top: 15px; }
        h2.episode-title { font-size: 1.8em; color: #1d1d1f; margin-top: 0; margin-bottom: 30px; font-weight: 700; letter-spacing: -0.02em; }
        .category { display: inline-block; font-size: 0.9em; color: #0066cc; font-weight: 600; margin-bottom: 15px; padding: 4px 12px; background-color: rgba(0, 102, 204, 0.08); border-radius: 999px; }
        img { max-width: 100%; height: auto; border-radius: 12px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .content { font-size: 1.1em; color: #333333; }
        blockquote { padding: 24px; background: #fafafc; border-left: 4px solid #0066cc; border-radius: 0 12px 12px 0; margin: 32px 0; color: #1d1d1f; }
        hr { border: 0; height: 1px; background: #e0e0e0; margin: 40px 0; }
    </style>
</head>
<body>
    <div class="page" style="text-align: center; padding: 120px 40px;">
        <h1 class="book-title">도면 위의 공유결합<br><span>건축과 사람, 그리고 삶을 잇는 단단한 흔적들</span></h1>
        <p style="color: #7a7a7a; font-size: 1.2em; margin-top: 40px;">저자 : 김중일</p>
    </div>`;

function embedBase64(htmlContent) {
  return htmlContent.replace(
    /src="(static\/images\/[^"]+)"/g,
    (match, imagePath) => {
      try {
        let fullPath = path.join(__dirname, imagePath);
        if (fs.existsSync(fullPath)) {
          let ext = path.extname(fullPath).substring(1);
          if (ext === "jpg") ext = "jpeg";
          let base64 = fs.readFileSync(fullPath, "base64");
          return `src="data:image/${ext};base64,${base64}"`;
        }
      } catch (e) {}
      return match;
    },
  );
}

pages.forEach((page) => {
  if (!page.title && !page.text && !page.image) return;
  html += `<div class="page">`;
  if (page.partCategory)
    html += `<div class="category">${page.partCategory}</div>`;
  if (page.title) html += `<h2 class="episode-title">${page.title}</h2>`;
  let contentHtml = "";
  if (page.image) contentHtml += `<img src="${page.image}"><br>`;
  if (page.text) contentHtml += page.text;
  html += `<div class="content">${embedBase64(contentHtml)}</div>`;
  html += `</div>`;
});
html += `</body></html>`;
fs.writeFileSync("도면위의공유결합_출판투고용_최종본.html", html, "utf8");

// Generate MD
let md = "# 도면 위의 공유결합 (최종본)\n\n";
let currentCategory = "";
pages.forEach((page) => {
  if (page.partCategory && page.partCategory !== currentCategory) {
    currentCategory = page.partCategory;
    md += `---\n\n# ${currentCategory}\n\n`;
  }
  if (page.title) md += `## ${page.title}\n\n`;
  let contentHtml = "";
  if (page.image) contentHtml += `<img src="${page.image}">\n\n`;
  if (page.text) contentHtml += page.text;
  if (contentHtml) {
    let text = contentHtml;
    text = text.replace(/<br\s*\/?>/gi, "\n");
    text = text.replace(/<\/p>/gi, "\n\n");
    text = text.replace(/<p[^>]*>/gi, "");
    text = text.replace(/<blockquote[^>]*>/gi, "\n> ");
    text = text.replace(/<\/blockquote>/gi, "\n\n");
    text = text.replace(/<div[^>]*>/gi, "\n> ");
    text = text.replace(/<\/div>/gi, "\n\n");
    text = text.replace(/<span[^>]*>/gi, "");
    text = text.replace(/<\/span>/gi, "");
    text = text.replace(/<strong[^>]*>/gi, "**");
    text = text.replace(/<\/strong>/gi, "**");
    text = text.replace(/<b[^>]*>/gi, "**");
    text = text.replace(/<\/b>/gi, "**");
    text = text.replace(/<em[^>]*>/gi, "*");
    text = text.replace(/<\/em>/gi, "*");
    text = text.replace(/<img[^>]*>/gi, "\n\n[이미지 첨부됨]\n\n");
    text = text.replace(
      /<svg[^>]*>.*<\/svg>/gi,
      "\n\n[공유결합 다이어그램 SVG]\n\n",
    );
    text = text.replace(/\n{3,}/g, "\n\n");
    md += text.trim() + "\n\n";
  }
});
fs.writeFileSync(
  "/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/도면위의공유결합_최종본.md",
  md,
  "utf8",
);
