const fs = require('fs');
let content = fs.readFileSync('book_data.js', 'utf8');

// The original style for the tables is inline. Let's just do a regex replace to insert our scroll rules.
content = content.replace(/class="custom-table"\s+style="/g, 'class="custom-table" style="max-height: 60vh; overflow-y: auto; display: block; ');

fs.writeFileSync('book_data.js', content, 'utf8');
console.log("Table styles fixed!");
