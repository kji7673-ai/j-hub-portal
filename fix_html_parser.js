const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// Replace the parser condition to allow raw HTML blocks
html = html.replace(
    /\} else if \(trimmed\.startsWith\('&gt;'\) \|\| trimmed\.startsWith\('>'\)\) \{/g,
    `} else if (trimmed.startsWith('<h') || trimmed.startsWith('<ul') || trimmed.startsWith('<ol') || trimmed.startsWith('<div')) {
                                contentHTML += trimmed;
                            } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {`
);

fs.writeFileSync('index.html', html, 'utf8');
