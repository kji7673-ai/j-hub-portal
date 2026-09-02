const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

html = html.replace(/<h1 class="book-title" style="color:#1d1d1f; font-size:clamp\(32px, 6vw, 56px\); margin-bottom:20px; font-weight:800; letter-spacing: -0\.03em; line-height: 1\.2; word-break: keep-all; text-shadow: 0 4px 20px rgba\(0,0,0,0\.9\);">/g, 
    '<h1 class="book-title" style="color:#1d1d1f; font-size:clamp(32px, 6vw, 56px); margin-bottom:20px; font-weight:800; letter-spacing: -0.03em; line-height: 1.2; word-break: keep-all;">');
    
html = html.replace(/<p style="color:rgba\(255,255,255,0\.9\); font-size:clamp\(18px, 3vw, 24px\); font-weight:500; word-break: keep-all; margin:0; text-shadow: 0 4px 15px rgba\(0,0,0,0\.8\);">/g,
    '<p style="color:rgba(29,29,31,0.9); font-size:clamp(18px, 3vw, 24px); font-weight:500; word-break: keep-all; margin:0;">');

fs.writeFileSync('index.html', html, 'utf8');
