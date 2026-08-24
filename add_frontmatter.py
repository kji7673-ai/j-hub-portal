import os

target_dir = "/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/content/02_건축자료실"

files = [
    "01_한눈에_보는_핵심숫자.md",
    "02_세대수별_적용_매트릭스_및_법적근거.md",
    "03_서울시_녹색건축물_및_추가요구사항.md",
    "04_친환경_인센티브_및_영향평가.md",
    "05_인증의_역설과_대안.md"
]

for idx, file in enumerate(files):
    path = os.path.join(target_dir, file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = content.split('\n')[0].replace('# ', '').strip()
    
    frontmatter = f"""---json
{{
  "id": {100 + idx},
  "title": "{title}",
  "category": "🏛️ 건축 실무 가이드",
  "level": 2,
  "is_internal": false,
  "date": "2026-08-04",
  "summary": "{title} 요약본",
  "track": "arch"
}}
---

"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
