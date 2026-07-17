const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/const allowedUsers = {[\s\S]*?};/);
if (scriptMatch) {
    eval(scriptMatch[0]);
    if (allowedUsers["김중일"] === "0000") {
        console.log("LOGIN OK");
    } else {
        console.log("LOGIN FAIL", allowedUsers["김중일"]);
    }
} else {
    console.log("SCRIPT NOT FOUND");
}
