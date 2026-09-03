const fs = require('fs');
const text = fs.readFileSync('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_text_final_v4.md', 'utf8');
const charsWithSpaces = text.length;
const charsWithoutSpaces = text.replace(/\s/g, '').length;
console.log('공백 포함 글자수:', charsWithSpaces);
console.log('공백 제외 글자수:', charsWithoutSpaces);
