const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

function updatePageTitle(oldTitle, newTitle, newText, isBridge) {
    for (let p of bookData.pages) {
        if (p.title && p.title.includes(oldTitle)) {
            p.title = newTitle;
            p.text = newText;
            if (isBridge) {
                // remove image if it's a bridge, or keep it.
            }
            return true;
        }
    }
    return false;
}

// But wait, there are currently no "bridges" in book_data.js!
// I need to INSERT bridges at the right index.

// First let's find the indices of the themes.
for (let i = 0; i < bookData.pages.length; i++) {
    let p = bookData.pages[i];
    if (p.partTitle && p.partTitle.includes('테마 1: 내가 무엇인가')) {
        console.log("Theme 1 starts at index", i);
        break;
    }
}
