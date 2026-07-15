import re

with open('index_old.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

# Load all new page files
pages = ['dashboard.html', 'projects.html', 'calendar.html', 'laws.html']
new_content = ""
for page in pages:
    with open(f'src/pages/{page}', 'r', encoding='utf-8') as f:
        new_content += f.read()

# Clean up HTML tags and whitespace to compare raw text content
def extract_text(html_str):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html_str)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Extract the relevant sections from old HTML
start_marker = "<!-- TAB 1: 일일보고 (Dashboard) -->"
end_marker = "<!-- TAB 5: 오늘의 읽을거리 (Today's Reading) -->"
old_section = old_html[old_html.find(start_marker):old_html.find(end_marker)]

old_text = extract_text(old_section)
new_text = extract_text(new_content)

# Check for specific key content items to ensure they are present in new_text
keywords_to_check = [
    "장대B구역",
    "사업시행인가 완료",
    "장안1구역",
    "당산1구역",
    "특별 공정촉진회의",
    "주택법 시행령 개정",
    "수택동 재개발",
    "마천5구역",
    "화성 남양 지역주택",
    "갈현1구역",
    "범일3구역",
    "장위13구역",
    "삼선동 1·2구역",
    "증산5구역",
    "불광8",
    "상봉7구역",
    "은마아파트",
    "종로2·3가",
    "신월곡제1구역",
    "대림1구역",
    "창신10구역",
    "중계본동 재개발",
    "신정동 922",
    "면목역 1차 모아주택",
    "석관초 관리계획",
    "하계 현대우성"
]

missing_items = []
for keyword in keywords_to_check:
    if keyword not in new_text:
        missing_items.append(keyword)

if not missing_items:
    print("SUCCESS: All key content items from the old index are present in the new modular structure.")
else:
    print("WARNING: The following items are missing in the new structure:")
    for item in missing_items:
        print(f" - {item}")

# Also compare the number of table rows or li items as a sanity check
old_li_count = old_section.count('<li>')
new_li_count = new_content.count('<li>')

old_tr_count = old_section.count('<tr>')
new_tr_count = new_content.count('<tr>')

print(f"List items (<li>) count: Old={old_li_count}, New={new_li_count}")
print(f"Table rows (<tr>) count: Old={old_tr_count}, New={new_tr_count}")

