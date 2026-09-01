const fs = require('fs');
const vm = require('vm');

let content = fs.readFileSync('book_data.js', 'utf8');
const script = new vm.Script(content + '; bookData;');
const bookData = script.runInNewContext({});

// 1. Find indices
let part3Index = bookData.pages.findIndex(p => p.title && p.title.includes('3부. 정비나침반 실행 로드맵'));
let part4Index = bookData.pages.findIndex(p => p.title && p.title.includes('4부. 건축가, 인간을 짓다'));

// 2. Rename Part 4 to Part 3
if (part4Index !== -1) {
    bookData.pages[part4Index].title = bookData.pages[part4Index].title.replace('4부', '3부');
    bookData.pages[part4Index].part = '3부: 증언과 성찰';
}
// Update any part category names in following pages
for (let i = part4Index + 1; i < bookData.pages.length; i++) {
    if (bookData.pages[i].partCategory === "4부: 증언과 성찰") {
        bookData.pages[i].partCategory = "3부: 증언과 성찰";
    }
}

// 3. Extract Part 3 (Interlude + The massive text page)
let appendixPages = [];
if (part3Index !== -1) {
    let interlude = bookData.pages[part3Index];
    let massivePage = bookData.pages[part3Index + 1];
    
    // Remove them from array
    bookData.pages.splice(part3Index, 2);
    
    // Convert Interlude to Appendix
    interlude.title = "[부록] J-Hub 플랫폼 마스터플랜 원본 (SRD)";
    interlude.part = "부록";
    appendixPages.push(interlude);
    
    // Split the massive text page by "## Part "
    let parts = massivePage.text.split(/(?=## Part [A-Z]\. )/);
    
    parts.forEach((partText, idx) => {
        let titleMatch = partText.match(/## (Part [A-Z]\. [^\n]+)/);
        let pageTitle = titleMatch ? titleMatch[1] : `부록 세부항목 ${idx + 1}`;
        
        appendixPages.push({
            type: "text_only",
            title: pageTitle,
            text: partText.trim(),
            partCategory: "부록"
        });
    });
}

// 4. Append Appendix pages to the end
bookData.pages = bookData.pages.concat(appendixPages);

let newBookData = `const bookData = {\n    pages: ${JSON.stringify(bookData.pages, null, 4)}\n};`;
fs.writeFileSync('book_data.js', newBookData, 'utf8');
console.log("Restructured to Appendix successfully. Total pages:", bookData.pages.length);
