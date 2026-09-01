const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

data.pages.forEach(p => {
    if (p.type === 'interlude' || p.type === 'cover') {
        if (p.title.includes('1부')) p.image = 'static/images/12.jpg';
        else if (p.title.includes('2부')) p.image = 'static/images/14.jpg';
        else if (p.title.includes('3부')) p.image = 'static/images/60.jpg';
        else if (p.title.includes('부록')) p.image = 'static/images/61.jpg';
        else if (p.title.includes('테마 1')) p.image = 'static/images/22.jpg';
        else if (p.title.includes('테마 2')) p.image = 'static/images/23.jpg';
        else if (p.title.includes('테마 3')) p.image = 'static/images/24.jpg';
        else if (p.title.includes('테마 4')) p.image = 'static/images/25.jpg';
        
        // Ensure text is at least an empty string so UI doesn't break
        p.text = p.text || '';
    }
});

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Images fixed.");
