import re
import os

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/index_old.html', 'r', encoding='utf-8') as f:
    html = f.read()

def extract_block(text, start_str, end_str):
    try:
        start_idx = text.index(start_str)
        end_idx = text.index(end_str) if end_str else len(text)
        return text[start_idx:end_idx]
    except ValueError as e:
        print(f"Error extracting from {start_str} to {end_str}")
        return ""

tab_dashboard = extract_block(html, '<!-- TAB 1: 일일보고 (Dashboard) -->', '<!-- TAB 2: 프로젝트 현황 (Projects) -->')
tab_projects = extract_block(html, '<!-- TAB 2: 프로젝트 현황 (Projects) -->', '<!-- TAB 3: 통합 캘린더 (Calendar) -->')
tab_calendar = extract_block(html, '<!-- TAB 3: 통합 캘린더 (Calendar) -->', '<!-- TAB 4: 법규 아카이브 (Laws) -->')
tab_laws = extract_block(html, '<!-- TAB 4: 법규 아카이브 (Laws) -->', '<!-- TAB 5: 오늘의 읽을거리 (Today\'s Reading) -->')

# Write to src/pages
with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/src/pages/dashboard.html', 'w', encoding='utf-8') as f: f.write(tab_dashboard)
with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/src/pages/projects.html', 'w', encoding='utf-8') as f: f.write(tab_projects)
with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/src/pages/calendar.html', 'w', encoding='utf-8') as f: f.write(tab_calendar)
with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/src/pages/laws.html', 'w', encoding='utf-8') as f: f.write(tab_laws)

print("Extraction successful.")
