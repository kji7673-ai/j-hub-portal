const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldOverlay = 'contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box;">`;';
const newOverlay = 'contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box; background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6));">`;';

const oldPart = 'contentHTML += `<p style="font-family: var(--font-display, \\\'SF Pro Display\\\', sans-serif); font-size: 14px; font-weight: 600; color: var(--primary-on-dark, #2997ff); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">${part}</p>`;';
const newPart = 'contentHTML += `<p style="font-family: var(--font-display, \\\'SF Pro Display\\\', sans-serif); font-size: 16px; font-weight: 700; color: #4ba3e3; letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase; text-shadow: 0 2px 12px rgba(0,0,0,0.9), 0 1px 4px rgba(0,0,0,0.8);">${part}</p>`;';

const oldTitle = 'contentHTML += `<h1 class="book-title" style="font-family: var(--font-display, \\\'SF Pro Display\\\', sans-serif); font-size: clamp(28px, 6vw, 44px); font-weight: 700; color: #ffffff; margin: 0 0 24px 0; line-height: 1.25; letter-spacing: -0.02em; word-break: keep-all;">${mainTitle}</h1>`;';
const newTitle = 'contentHTML += `<h1 class="book-title" style="font-family: var(--font-display, \\\'SF Pro Display\\\', sans-serif); font-size: clamp(28px, 6vw, 44px); font-weight: 800; color: #ffffff; margin: 0 0 24px 0; line-height: 1.25; letter-spacing: -0.02em; word-break: keep-all; text-shadow: 0 4px 24px rgba(0,0,0,0.9), 0 2px 8px rgba(0,0,0,0.8);">${mainTitle}</h1>`;';

const oldSub = 'contentHTML += `<p style="font-family: var(--font-body, \\\'SF Pro Text\\\', sans-serif); font-size: 18px; font-weight: 300; color: #a0a0a0; margin: 0; word-break: keep-all; line-height: 1.5;">${subtitle}</p>`;';
const newSub = 'contentHTML += `<p style="font-family: var(--font-body, \\\'SF Pro Text\\\', sans-serif); font-size: 20px; font-weight: 400; color: #e0e0e0; margin: 0; word-break: keep-all; line-height: 1.5; text-shadow: 0 2px 12px rgba(0,0,0,0.9), 0 1px 4px rgba(0,0,0,0.8);">${subtitle}</p>`;';

html = html.replace(oldOverlay, newOverlay);
html = html.replace(oldPart, newPart);
html = html.replace(oldTitle, newTitle);
html = html.replace(oldSub, newSub);

fs.writeFileSync('index.html', html, 'utf8');
console.log("Updated shadows in index.html");
