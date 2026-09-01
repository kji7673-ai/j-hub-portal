const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldRender = `function renderBook() {
            const container = document.getElementById('book-container');`;
const newRender = `function renderBook() {
            try {
            const container = document.getElementById('book-container');`;

const oldRenderEnd = `container.insertBefore(pageEl, container.querySelector('.controls'));
            });`;
const newRenderEnd = `container.insertBefore(pageEl, container.querySelector('.controls'));
            });
            } catch (error) {
                alert("렌더링 오류 발생: " + error.message);
                console.error(error);
            }`;

html = html.replace(oldRender, newRender).replace(oldRenderEnd, newRenderEnd);
fs.writeFileSync('index.html', html, 'utf8');
console.log("Added try-catch to renderBook.");
