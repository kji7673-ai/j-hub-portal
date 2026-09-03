const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Fix .page-text-flow overflow: hidden;
html = html.replace(/\.page-text-flow\s*\{\s*display:\s*block;\s*overflow:\s*hidden;\s*\}/, '.page-text-flow { display: block; overflow-y: auto; overflow-x: hidden; -webkit-overflow-scrolling: touch; }');

// Make sure .page-content can scroll
html = html.replace(/\.page-content\s*\{\s*overflow-y:\s*auto;\s*overflow-x:\s*hidden;\s*\}/, '.page-content { overflow-y: auto; overflow-x: hidden; -webkit-overflow-scrolling: touch; }');

// Force version bump again
html = html.replace(/v=20241100/g, 'v=20241101');

fs.writeFileSync('index.html', html, 'utf8');
