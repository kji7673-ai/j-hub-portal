const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

let count = 0;
for (let i = 0; i < data.pages.length; i++) {
    let p = data.pages[i];
    if (p.text) {
        let old = p.text;
        // Fix 40px 20px -> 40px 0
        p.text = p.text.replace(/padding:\s*40px\s+20px\s*;/g, 'padding: 40px 0;');
        // Fix 20px -> 20px 0
        p.text = p.text.replace(/padding:\s*20px\s*;/g, 'padding: 20px 0;');
        
        if (old !== p.text) count++;
    }
}

fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
console.log("Pages fixed for padding:", count);
