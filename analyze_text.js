const fs = require("fs");
const vm = require("vm");
const code = fs.readFileSync("book_data.js", "utf8");
const script = new vm.Script(code);
const context = {};
vm.createContext(context);
script.runInContext(context);

const pages = context.bookData.pages;

console.log("=== 1. TONE INCONSISTENCIES (해요체/합쇼체 어긋난 부분) ===");
const casualRegex = /[^입습니]다[.\s]/g;

pages.forEach((page, i) => {
  if (!page.text) return;
  let text = page.text.replace(/<[^>]+>/g, ""); // strip HTML

  // Split by sentences
  let sentences = text.split(/(?<=[.!?])\s+/);
  sentences.forEach((s) => {
    // Exclude quotes (e.g. "이다.", '하다.')
    if (s.includes('"') || s.includes("'")) return;

    // Find sentences ending in casual '다'
    if (
      /[^입습니]다\.$/.test(s) &&
      !s.includes("바랍니다.") &&
      !s.includes("않습니다.") &&
      !s.includes("있습니다.")
    ) {
      // Wait, 바랍니다, 않습니다, 있습니다 ending in 다. are caught if we don't handle them well.
      // Let's use a better check:
      // Ends with 다. but NOT [입습합니]다.
      if (/[^입습합니]다\.$/.test(s)) {
        console.log(`[Page ${i} / ${page.title || "No Title"}] ${s}`);
      }
    }
  });
});

console.log("\n=== 2. DUPLICATE PHRASES (중복 내용 의심 구간) ===");
let phrases = [
  "공유결합(Covalent Bond)",
  "찢어진 운동화",
  "조은 슈퍼",
  "유현준",
  "면목동",
  "사람과 사람을 연결하는 선",
  "이 시대에 필요한",
];

phrases.forEach((phrase) => {
  let matches = [];
  pages.forEach((page, i) => {
    if (page.text && page.text.includes(phrase)) {
      matches.push(`Page ${i}: ${page.title}`);
    }
  });
  if (matches.length > 1) {
    console.log(`- '${phrase}' is mentioned in ${matches.length} places:`);
    matches.forEach((m) => console.log(`  ${m}`));
  }
});
