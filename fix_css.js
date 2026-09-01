const fs = require('fs');
const indexPath = 'index.html';

let content = fs.readFileSync(indexPath, 'utf8');

// Replace the max-width and aspect-ratio logic
let cssAdd = `
        /* ===== Mobile Responsive Adjustments ===== */
        @media (max-width: 768px) {
            .book-container {
                max-width: 100vw !important;
                aspect-ratio: auto !important;
                height: 100dvh !important;
                border-radius: 0 !important;
            }
            .page-content {
                padding: 15% 6% 25% 6% !important; /* more padding bottom for nav */
            }
            p.body-text {
                font-size: 16px !important;
                line-height: 1.7 !important;
            }
            .page-content.philosophy-mode p.body-text {
                font-size: 16px !important;
                line-height: 1.8 !important;
            }
            /* When landscape on mobile */
            @media (orientation: landscape) {
                .book-container {
                    height: 100dvh !important;
                }
                .page-content {
                    padding: 5% 5% 15% 5% !important;
                    column-count: 2;
                    column-gap: 40px;
                }
                .page-text-flow {
                    column-count: 2 !important;
                }
                p.body-text {
                    font-size: 15px !important;
                }
            }
        }
        
        /* Adjust for landscape orientation in general (tablets) */
        @media (max-height: 500px) and (orientation: landscape) {
            .book-container {
                max-width: 100vw !important;
                aspect-ratio: auto !important;
                height: 100dvh !important;
            }
            .page-content {
                padding: 5% 8% 15% 8% !important;
                column-count: 2;
                column-gap: 40px;
            }
        }
`;

// Insert before </style> in the head
content = content.replace(/(<\/style>\s*<\/head>)/i, cssAdd + "\n$1");

// Also make the default book-container a bit more readable on desktop
content = content.replace(/max-width: 90vh;/g, 'max-width: min(90vh, 800px);');

fs.writeFileSync(indexPath, content, 'utf8');
console.log("CSS injected.");
