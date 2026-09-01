const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

let count = 0;
// We'll use a pool of known generic images (1 to 60)
const imagePool = Array.from({length: 60}, (_, i) => i + 1);

data.pages.forEach((p) => {
    // Only insert if it's a text page or a long text and we haven't done too many
    if(p.text && p.text.length > 300 && p.type !== 'cover' && p.type !== 'interlude' && Math.random() > 0.6) {
        let paragraphs = p.text.split('\n\n');
        if (paragraphs.length >= 3) {
            // Insert after the first or second paragraph
            let insertPos = Math.floor(paragraphs.length / 2);
            let imgId = imagePool[Math.floor(Math.random() * imagePool.length)];
            paragraphs.splice(insertPos, 0, `![현장 스케치](static/images/${imgId}.jpg)`);
            p.text = paragraphs.join('\n\n');
            count++;
        }
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log(`Inserted ${count} random inline images.`);
