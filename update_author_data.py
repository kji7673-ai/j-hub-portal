import re

js_path = "book_data.js"

with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the specific text_only page that has the author info
old_block = """        {
            "type": "text_only",
            "title": "저자 소개: 현장의 최전선에서 정책을 조율하는 건축가",
            "text": "<li>**현(現) 서울시 건축심의위원**</li>\\n<li>**현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원**</li>\\n<li>**현(現) 강동구, 양천구 건축심의위원**</li>\\n<li>**현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원**</li>\\n\\n정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 뼈저리게 목도하고 있는 건축가의 현장 고발이자 생존 전략."
        },"""

new_block = """        {
            "type": "author_profile",
            "title": "저자 소개: (주)진양엔지니어링건축사사무소 김중일 건축사"
        },"""

if old_block in text:
    text = text.replace(old_block, new_block)
else:
    # Let's try regex if exact match fails
    text = re.sub(r'{\s*"type": "text_only",\s*"title": "저자 소개[^}]*}', new_block.strip(), text)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(text)
