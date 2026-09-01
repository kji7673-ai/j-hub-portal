const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldResize = `window.addEventListener('resize', () => {
            updateControls();
        });`;

const newResize = `let _windowWidth = window.innerWidth;
        let _resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(_resizeTimer);
            _resizeTimer = setTimeout(() => {
                if (window.innerWidth !== _windowWidth) {
                    _windowWidth = window.innerWidth;
                    updateControls();
                }
            }, 100);
        });`;

html = html.replace(oldResize, newResize);
fs.writeFileSync('index.html', html, 'utf8');
console.log("Replaced resize handler.");
