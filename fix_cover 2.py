import json
import os

DB_PATH = "data/manual_db.json"

def fix_cover():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    for p in db:
        if p["id"] == "0":
            content = p["content"]
            # Change the heavy black overlay to a light white overlay
            content = content.replace("background:rgba(0,0,0,0.85);", "background:rgba(255,255,255,0.85);")
            
            # Change specific text colors
            content = content.replace("color: var(--primary-on-dark);", "color: var(--primary);")
            content = content.replace("color: var(--on-dark);", "color: var(--ink);")
            
            # Change specific borders
            content = content.replace("border-top: 1px solid rgba(255,255,255,0.2);", "border-top: 1px solid rgba(0,0,0,0.1);")
            
            p["content"] = content
            
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    fix_cover()
