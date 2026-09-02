const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// I will just use regex to replace the specific inline styles for cover
html = html.replace(/<p style="font-family: var\(--font-display, 'SF Pro Display', sans-serif\); font-size: 14px; font-weight: 600; color: var\(--primary-on-dark, #2997ff\); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">\$\{part\}<\/p>/g,
    `<p style="font-family: var(--font-display, 'SF Pro Display', sans-serif); font-size: 16px; font-weight: 700; color: #6db6ff; letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase; text-shadow: 0 2px 12px rgba(0,0,0,0.9), 0 1px 4px rgba(0,0,0,0.8);">\${part}</p>`);

html = html.replace(/<h1 class="book-title" style="font-family: var\(--font-display, 'SF Pro Display', sans-serif\); font-size: clamp\(28px, 6vw, 44px\); font-weight: 700; color: #ffffff; margin: 0 0 24px 0; line-height: 1.25; letter-spacing: -0.02em; word-break: keep-all;">\$\{mainTitle\}<\/h1>/g,
    `<h1 class="book-title" style="font-family: var(--font-display, 'SF Pro Display', sans-serif); font-size: clamp(28px, 6vw, 44px); font-weight: 800; color: #ffffff; margin: 0 0 24px 0; line-height: 1.25; letter-spacing: -0.02em; word-break: keep-all; text-shadow: 0 4px 24px rgba(0,0,0,0.9), 0 2px 8px rgba(0,0,0,0.8);">\${mainTitle}</h1>`);

html = html.replace(/<p style="font-family: var\(--font-body, 'SF Pro Text', sans-serif\); font-size: 18px; font-weight: 300; color: #a0a0a0; margin: 0; word-break: keep-all; line-height: 1.5;">\$\{subtitle\}<\/p>/g,
    `<p style="font-family: var(--font-body, 'SF Pro Text', sans-serif); font-size: 20px; font-weight: 400; color: #f0f0f0; margin: 0; word-break: keep-all; line-height: 1.5; text-shadow: 0 2px 12px rgba(0,0,0,0.9), 0 1px 4px rgba(0,0,0,0.8);">\${subtitle}</p>`);

fs.writeFileSync('index.html', html, 'utf8');
