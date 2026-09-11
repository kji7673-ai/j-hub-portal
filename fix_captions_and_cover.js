const fs = require("fs");
const vm = require("vm");

const data = fs.readFileSync("book_data.js", "utf8");
const sandbox = {};
vm.runInNewContext(data, sandbox);
const bookData = sandbox.bookData;

bookData.pages.forEach((page) => {
  // 1. 표지 부제 간격 넓히기 (margin-top:-20px -> margin-top:24px)
  if (page.type === "cover" && page.text) {
    page.text = page.text.replace("margin-top:-20px;", "margin-top:24px;");
  }

  // 2. 캡션 자동 분류
  if (page.image) {
    let imgName = page.image.toLowerCase();

    // 조각상/입체 조형물 판단
    if (
      imgName.match(
        /sculpture|clay|wire|sphere|face|relief|carry|dancing|falling|hunched|running|reaching/i,
      )
    ) {
      page.caption = "오리지널 입체 조형물 (Original Sculpture)";
    }
    // 평면 도면/스케치/프레임 판단
    else if (
      imgName.match(/frame|arch|sketch|bighands|flat|heart|leaning|bowl/i)
    ) {
      page.caption = "오리지널 스케치 도면 (Original Sketch Drawing)";
    }
  }

  // 표지와 저자 소개 등은 별도의 캡션(도면/조형물) 표시 불필요하므로 깔끔하게 제거
  if (page.type === "cover" || page.partCategory === "저자 소개") {
    delete page.caption;
  }
});

const output = "var bookData = " + JSON.stringify(bookData, null, 4) + ";";
fs.writeFileSync("book_data.js", output);
console.log("Captions and cover spacing fixed successfully.");
