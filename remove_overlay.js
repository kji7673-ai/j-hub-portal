const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldOverlay = 'contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box; background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6));">`;';
const newOverlay = 'contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box; padding: 20px;">`;';

html = html.replace(oldOverlay, newOverlay);

fs.writeFileSync('index.html', html, 'utf8');
console.log("Removed gradient overlay");
