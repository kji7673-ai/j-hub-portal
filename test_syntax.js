const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scripts = [...html.matchAll(/<script.*?>([\s\S]*?)<\/script>/g)];
let all_ok = true;
scripts.forEach((match, i) => {
    try {
        require('vm').createScript(match[1]);
        console.log(`Script ${i} is OK`);
    } catch (e) {
        console.error(`Script ${i} Error:`, e.message);
        all_ok = false;
    }
});
if(!all_ok) process.exit(1);
