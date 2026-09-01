import re
import json

js_path = "book_data.js"

with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the text_only page with author_profile
text = re.sub(
    r'\{\s*"type":\s*"text_only",\s*"title":\s*"저자 소개[^}]*\}',
    """{
            "type": "author_profile"
        }""",
    text,
    flags=re.DOTALL
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(text)
    
html_path = "book_studio.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update the description in the UI
new_desc = "정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 가까이서 마주해 온 건축가의 진심 어린 조언이자 따뜻한 혁신의 기록."

# We need to replace the old description in the template if it exists
html = re.sub(
    r'<div class="author-desc">.*?</div>',
    f'<div class="author-desc">\\n                            "{new_desc}"\\n                        </div>',
    html,
    flags=re.DOTALL
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
