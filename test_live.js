const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const https = require('https');

https.get('https://kji7673-ai.github.io/j-hub-portal/', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        // Mock bookData since it's external
        data = data.replace('</head>', '<script>const bookData = {pages:[]};</script></head>');
        const dom = new JSDOM(data, { runScripts: "dangerously" });
        setTimeout(() => {
            console.log("Done checking live html");
            process.exit(0);
        }, 1000);
    });
});
