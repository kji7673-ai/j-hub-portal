const fs = require("fs");
const vm = require("vm");

const data = fs.readFileSync("book_data.js", "utf8");
const sandbox = {};
vm.runInNewContext(data, sandbox);
const bookData = sandbox.bookData;

bookData.forEach((page) => {
  if (page.image) {
    let imgName = page.image.toLowerCase();

    // 1. 조각상/입체 조형물 판단
    if (
      imgName.match(
        /sculpture|clay|wire|sphere|face|relief|carry_mass|dancing|falling|hunched|running|reaching/i,
      )
    ) {
      page.caption = "오리지널 입체 조형물 (Original Sculpture)";
    }
    // 2. 평면 도면/스케치/프레임 판단
    else if (
      imgName.match(/frame|arch|sketch|bighands|flat|heart|leaning|bowl/i)
    ) {
      page.caption = "오리지널 스케치 도면 (Original Sketch Drawing)";
    }
  }

  // 표지의 경우 캡션을 비우는 것이 나을 수 있음
  if (page.type === "cover" || page.type === "author_profile") {
    delete page.caption; // 표지와 프로필은 이미지가 백그라운드거나 특별한 배치이므로 캡션 불필요
  }
});

const output = "var bookData = " + JSON.stringify(bookData, null, 4) + ";";
fs.writeFileSync("book_data.js", output);
console.log("Captions fixed successfully.");
