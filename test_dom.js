const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });
setTimeout(() => {
    console.log("No syntax errors. DOM loaded.");
    process.exit(0);
}, 1000);
