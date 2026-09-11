import os
import json
import re

OLD_DIR = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-13/정비사업_통합검토_매뉴얼/scratch/chapters"
NEW_DIR = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/data"

db = []

for i in range(0, 7):
    path = os.path.join(OLD_DIR, f"page_{i:03d}.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Extract a sensible title based on h2 or h3
            title_match = re.search(r'<h[12].*?>(.*?)</h[12]>', content)
            title = title_match.group(1).replace('<br>', ' ').strip() if title_match else f"페이지 {i}"
            
            db.append({
                "id": str(i),
                "title": title,
                "content": content,
                "ai_instruction": "",
                "ceo_thoughts": "",
                "whiteboard_data": ""
            })

os.makedirs(NEW_DIR, exist_ok=True)
db_path = os.path.join(NEW_DIR, "manual_db.json")
with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=4)

print(f"Successfully migrated {len(db)} pages into manual_db.json.")
