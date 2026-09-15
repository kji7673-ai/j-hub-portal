const fs = require('fs');
let data = JSON.parse(fs.readFileSync('book_data.json', 'utf8'));

// The text is split across index 156.
let text156 = data.pages[156].text;
let replaced = text156.replace(/static\/images\/sketches\/sculpture_bond_(\d)\.jpg/g, 'static/images/user_sculpture_$1.jpg');

if (text156 !== replaced) {
    data.pages[156].text = replaced;
    fs.writeFileSync('book_data.json', JSON.stringify(data, null, 2));
    console.log("Updated image paths on index 156.");
} else {
    console.log("No replacement made.");
}
