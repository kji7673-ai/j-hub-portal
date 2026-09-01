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
                    const pages = dom.window.document.querySelectorAll('.page-content');
                    console.log("Total pages rendered:", pages.length);
                    const active = dom.window.document.querySelectorAll('.page-content.active');
                    console.log("Active pages:", active.length);
                    
                    if (active.length > 0) {
                        console.log("First active page classes:", active[0].className);
                        console.log("First active page HTML:", active[0].innerHTML.substring(0, 100));
                    }
                    process.exit(0);
                }, 1000);
            });
        });
    });
});
