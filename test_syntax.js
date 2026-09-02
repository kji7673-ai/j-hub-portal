const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
let match;
const regex = /<script.*?>([\s\S]*?)<\/script>/g;
let i = 0;
while ((match = regex.exec(html)) !== null) {
    if (match[1].trim()) {
        fs.writeFileSync(`temp_script_${i}.js`, match[1], 'utf8');
        i++;
    }
}
