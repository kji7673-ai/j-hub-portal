import os
import shutil
import json

base_dir = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/content"
new_track_dir = os.path.join(base_dir, "01_진양_AI_통합_매뉴얼")

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 두 가지 종류의 프론트매터 모두 제거
    if content.startswith("---json"):
        end_idx = content.find("---", 7)
        if end_idx != -1:
            content = content[end_idx+3:].strip()
    elif content.startswith("```json"):
        end_idx = content.find("```", 7)
        if end_idx != -1:
            content = content[end_idx+3:].strip()
            
    return content

files = os.listdir(new_track_dir)
for i, filename in enumerate(sorted(files)):
    if not filename.endswith(".md"): continue
    
    filepath = os.path.join(new_track_dir, filename)
    content = clean_file(filepath)
    
    # 제대로 된 프론트매터 생성
    title = filename.replace(".md", "").replace("_", " ")
    # ID 부여 (1부터 순서대로)
    frontmatter = {
        "id": i + 1,
        "title": title,
        "category": "📘 실전 가이드",
        "level": 1,
        "is_internal": False,
        "date": "2026-07-25",
        "summary": f"{title} 통합 매뉴얼입니다."
    }
    
    frontmatter_str = "```json\n" + json.dumps(frontmatter, ensure_ascii=False, indent=2) + "\n```\n\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter_str + content)

print("✅ 프론트매터 수정 완료")
