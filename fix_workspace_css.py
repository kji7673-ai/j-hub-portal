import re

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS for workspace tables to the swiss_css block
workspace_css = """
/* Workspace Tables & Typography (Readable Design) */
.workspace-card h2, .workspace-card h3 {
    font-size: 20px;
    letter-spacing: -0.5px;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 16px;
    text-transform: uppercase;
}

.card-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px; /* Global rule minimum for 50-60 age group */
    line-height: 1.6;
    margin-bottom: 24px;
}

.table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.card-table th {
    text-align: left;
    font-weight: 600;
    color: var(--text-secondary);
    padding: 12px;
    border-bottom: 1px solid #e0e0e0; /* Apple hairline border */
}

.card-table td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0; /* Apple hairline border */
    color: var(--text-primary);
}

.card-table tr:nth-child(even) td {
    background-color: #fafafc; /* Apple pure parchment/even row color */
}

.card-table tr:hover td {
    background-color: #f0f0f5;
    transition: background-color 0.2s;
}

/* Badge and specific highlighting */
.highlight-red {
    color: #e30000;
    font-weight: 600;
}
.highlight-blue {
    color: #0066cc;
    font-weight: 600;
}
"""

if "/* Workspace Tables" not in content:
    # Insert right before </style>
    content = content.replace("</style>", workspace_css + "\n</style>")

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS updated.")
