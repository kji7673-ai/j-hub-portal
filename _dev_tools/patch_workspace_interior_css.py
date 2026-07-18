import re

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'r', encoding='utf-8') as f:
    content = f.read()

additional_css = """
/* Workspace Interior Elements (Swiss Grid Adaptation) */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 24px;
}
@media (max-width: 768px) {
    .grid-2 { grid-template-columns: 1fr; }
}

.hero {
    background: transparent;
    border-bottom: 4px solid var(--accent);
    padding: 0 0 16px 0;
    margin-bottom: 32px;
}
.hero h1 {
    font-size: 32px;
    margin: 0 0 8px 0;
    text-transform: uppercase;
    letter-spacing: -1px;
}
.hero p {
    font-size: 16px;
    color: var(--text-secondary);
    margin: 0;
}

.card {
    background: var(--surface);
    border: 1px solid var(--accent); /* Brutalism strict borders */
    padding: 24px;
    box-shadow: none;
    border-radius: 0;
    display: flex;
    flex-direction: column;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}

.chip {
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    text-transform: uppercase;
    border: 1px solid var(--accent);
    background: transparent;
    color: var(--accent);
}
.chip.red {
    border-color: #e30000;
    color: #e30000;
    background: rgba(227, 0, 0, 0.05);
}
.chip.blue {
    border-color: #0066cc;
    color: #0066cc;
    background: rgba(0, 102, 204, 0.05);
}

ul {
    list-style-type: square; /* Swiss modernism list style */
    padding-left: 20px;
}
li {
    margin-bottom: 8px;
    font-size: 14px;
    color: var(--text-primary);
}
.highlight {
    font-weight: 700;
    background: rgba(0,0,0,0.05);
    padding: 2px 4px;
}
"""

if "/* Workspace Interior Elements" not in content:
    content = content.replace("</style>", additional_css + "\n</style>")

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Interior CSS added.")
