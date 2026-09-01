const fs = require('fs');
const bookDataPath = 'book_data.js';

let content = fs.readFileSync(bookDataPath, 'utf8');
const match = content.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const data = eval('(' + match[2] + ')');

let newPages = [];

// Helper to split text into chunks roughly matching max length, breaking at newlines
function splitText(text, maxLen) {
    if(!text) return [];
    let paragraphs = text.split('\n\n');
    let chunks = [];
    let currentChunk = '';

    for(let i = 0; i < paragraphs.length; i++) {
        let p = paragraphs[i].trim();
        if(!p) continue;
        
        if(currentChunk.length + p.length > maxLen && currentChunk.length > 0) {
            chunks.push(currentChunk.trim());
            currentChunk = p;
        } else {
            currentChunk += (currentChunk ? '\n\n' : '') + p;
        }
    }
    if(currentChunk) chunks.push(currentChunk.trim());
    return chunks;
}

data.pages.forEach((p, idx) => {
    if(p.text) {
        // Image_top pages have less space, so maxLen is smaller. Pure text pages have more.
        let maxLen = (p.type === 'image_top' || p.type === 'cover' || p.type === 'interlude') ? 600 : 1000;
        
        // Some pages like author_profile shouldn't be split usually, but let's be safe
        if(p.text.length > maxLen) {
            let chunks = splitText(p.text, maxLen);
            
            chunks.forEach((chunk, i) => {
                let newP = { ...p }; // copy
                newP.text = chunk;
                // Only show title on the first chunk, or append (계속)
                if(i > 0) {
                    if(newP.title) newP.title = newP.title + ' (계속)';
                    // If it was image_top, maybe change to text for subsequent pages to give more room?
                    // Let's keep the same type, but remove image to give room, or keep it.
                    if(newP.type === 'image_top') newP.type = 'text';
                }
                newPages.push(newP);
            });
        } else {
            newPages.push(p);
        }
    } else {
        newPages.push(p);
    }
});

data.pages = newPages;

const newContent = match[1] + JSON.stringify(data, null, 4) + ";\n";
fs.writeFileSync(bookDataPath, newContent, 'utf8');
console.log("Pages split. New total pages: " + newPages.length);
