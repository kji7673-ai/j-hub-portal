import re

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'r', encoding='utf-8') as f:
    content = f.read()

calendar_css = """
/* Calendar & Day Block Styling */
.day-block {
    border-bottom: 1px solid var(--accent); /* Clear separation lines between days */
    padding: 16px 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.day-block:last-child {
    border-bottom: none;
}
.day-header {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
}
.day-date {
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -1px;
}
.day-weekday {
    font-size: 14px;
    color: var(--text-secondary);
    text-transform: uppercase;
}
.event-card {
    background: #fafafc;
    border: 1px solid #e5e5ea;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.event-card.important {
    border-left: 4px solid var(--accent);
    background: var(--surface);
}
.event-name {
    font-weight: 700;
    font-size: 15px;
}
.event-note {
    font-size: 13px;
    color: var(--text-secondary);
}
.event-time {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 2px;
}

/* Strict Box Alignment & Spacing Overrides */
.workspace-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px; /* Uniform larger gap between major blocks */
}
.card {
    height: 100%; /* Force equal heights where possible */
    margin-bottom: 0 !important; /* Controlled by grid gap */
}
.grid-2 {
    gap: 32px; /* Uniform gap matching workspace-grid */
    margin-bottom: 32px;
    align-items: start;
}
"""

# Insert right before </style>
content = content.replace("</style>", calendar_css + "\n</style>")

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/build_jhub.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Calendar CSS added.")
