const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// The faulty functions:
// function openTOC() {
//     document.getElementById('toc-modal').style.display = 'flex';
// }
// function closeTOC() {
//     document.getElementById('toc-modal').style.display = 'none';
// }

const newTOC = `
        function openTOC() {
            const modal = document.querySelector('.toc-modal');
            const overlay = document.querySelector('.toc-overlay');
            if(modal) modal.classList.add('active');
            if(overlay) overlay.classList.add('active');
        }
        function closeTOC() {
            const modal = document.querySelector('.toc-modal');
            const overlay = document.querySelector('.toc-overlay');
            if(modal) modal.classList.remove('active');
            if(overlay) overlay.classList.remove('active');
        }
`;

html = html.replace(/function openTOC\(\) \{[\s\S]*?function closeTOC\(\) \{[\s\S]*?\}/, newTOC.trim());

// Also, the item click in renderTOC uses `document.getElementById('toc-modal').style.display = 'none';`
// Let's fix that to call closeTOC()
html = html.replace("document.getElementById('toc-modal').style.display = 'none';", "closeTOC();");

html = html.replace(/v=20241109/g, 'v=20241110');

fs.writeFileSync('index.html', html, 'utf8');
