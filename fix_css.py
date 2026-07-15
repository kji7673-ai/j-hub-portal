import re

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the chip CSS
old_chip_css = """
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
"""

new_chip_css = """
.tag-row {
    margin-bottom: 8px; /* Fixes overlap with report-title */
}
.chip {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    text-transform: uppercase;
    border: 1px solid var(--accent);
    background: transparent;
    color: var(--accent);
}
.chip.red {
    border-color: var(--text-primary);
    color: var(--surface);
    background: var(--text-primary); /* Swiss Grid high contrast instead of raw red */
}
.chip.blue, .chip.green {
    border-color: var(--text-secondary);
    color: var(--text-secondary);
    background: transparent;
}
"""

content = content.replace(old_chip_css.strip(), new_chip_css.strip())

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS Fixed")
