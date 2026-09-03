const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// The missing logic that toggleBookmark relies on:
const missingCode = `
        let bookmarks = JSON.parse(localStorage.getItem('JJournal_bookmarks_v2') || '[]');
        
        function saveProgress() {
            localStorage.setItem('JJournal_savedChapter', currentChapter);
            localStorage.setItem('JJournal_savedColumn', currentColumn);
        }
        
        function openTOC() {
            document.getElementById('toc-modal').style.display = 'flex';
        }
        function closeTOC() {
            document.getElementById('toc-modal').style.display = 'none';
        }
`;

// Replace window.onload = renderBook; with window.onload = renderBook; + missingCode
html = html.replace('window.onload = renderBook;', 'window.onload = renderBook;\n' + missingCode);

html = html.replace(/v=20241107/g, 'v=20241108');

fs.writeFileSync('index.html', html, 'utf8');
