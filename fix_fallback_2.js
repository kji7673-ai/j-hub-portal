const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldUpdate = `function updateControls() {
            const pageEls = document.querySelectorAll('.page-content');`;
const newUpdate = `function updateControls() {
            try {
            const pageEls = document.querySelectorAll('.page-content');`;

const oldUpdateEnd = `document.getElementById('page-num').innerText = \`[\${currentChapter + 1}/\${totalChapters}] \${currentColumn + 1} / \${maxCols}\`;
            if(typeof saveProgress === 'function') saveProgress();
        }`;
const newUpdateEnd = `document.getElementById('page-num').innerText = \`[\${currentChapter + 1}/\${totalChapters}] \${currentColumn + 1} / \${maxCols}\`;
            if(typeof saveProgress === 'function') saveProgress();
            } catch (error) {
                alert("컨트롤 업데이트 오류: " + error.message);
                console.error(error);
            }
        }`;

html = html.replace(oldUpdate, newUpdate).replace(oldUpdateEnd, newUpdateEnd);

const oldDomLoad = `window.addEventListener('DOMContentLoaded', () => {`;
const newDomLoad = `window.addEventListener('DOMContentLoaded', () => {
    try {`;

const oldDomLoadEnd = `renderBook();
            renderTOC();
        });`;
const newDomLoadEnd = `renderBook();
            renderTOC();
    } catch (e) { alert("초기화 오류: " + e.message); }
        });`;

html = html.replace(oldDomLoad, newDomLoad).replace(oldDomLoadEnd, newDomLoadEnd);
fs.writeFileSync('index.html', html, 'utf8');
