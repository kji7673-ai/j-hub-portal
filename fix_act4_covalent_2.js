const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

function removeFootnote(index, keyword) {
    if (data.pages[index] && data.pages[index].text) {
        let regex = new RegExp('<div class="footnote-box">[\\s\\S]*?\\* ' + keyword + '[\\s\\S]*?<\\/div>\\n?', 'g');
        if(regex.test(data.pages[index].text)) {
            data.pages[index].text = data.pages[index].text.replace(regex, "");
            console.log(`Removed footnote ${keyword} from index ${index}`);
        } else {
            console.log(`Failed to remove footnote ${keyword} from index ${index}`);
        }
    }
}

removeFootnote(205, "공유결합 \\(건축적 의미\\)");
removeFootnote(210, "공유결합 \\(일상적 의미\\)");
removeFootnote(225, "공유결합 \\(공간적 의미\\)");
removeFootnote(235, "공유결합 \\(사회적 의미\\)");

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
