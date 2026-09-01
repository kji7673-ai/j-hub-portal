const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const https = require('https');

https.get('https://kji7673-ai.github.io/j-hub-portal/book_data.js', (res) => {
    let jsData = '';
    res.on('data', chunk => jsData += chunk);
    res.on('end', () => {
        https.get('https://kji7673-ai.github.io/j-hub-portal/', (res2) => {
            let htmlData = '';
            res2.on('data', chunk => htmlData += chunk);
            res2.on('end', () => {
                htmlData = htmlData.replace('</head>', '<script>' + jsData + '</script></head>');
                const dom = new JSDOM(htmlData, { runScripts: "dangerously" });
                setTimeout(() => {
                    console.log("Done checking live html");
                    process.exit(0);
                }, 1000);
            });
        });
    });
});
