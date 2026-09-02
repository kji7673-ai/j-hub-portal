const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldCss = `.page-inner {
            /* Fix for vertical overflow: column-width doesn't accept percentages! */
             
             
            height: 100%;
            width: 100%;
            transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
            padding-bottom: 120px; /* Spacer for bottom nav controls */
        }`;

const newCss = `.page-inner {
            width: 100%;
            min-height: 100%;
            transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
            padding-bottom: 120px; /* Spacer for bottom nav controls */
        }`;

html = html.replace(oldCss, newCss);
fs.writeFileSync('index.html', html, 'utf8');
console.log("Fixed page-inner height!");
