import json
import os

DB_PATH = "data/manual_db.json"

def clean_dark_theme():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    for p in db:
        if p["id"] == "0":
            # Remove any specific inline dark styles from page 0
            p["content"] = p["content"].replace("background-color: var(--surface-tile-1);", "background-color: #ffffff;")
            p["content"] = p["content"].replace("background: #1d1d1f;", "background: #ffffff;")
            p["content"] = p["content"].replace("color: #ffffff;", "color: #1d1d1f;")
            p["content"] = p["content"].replace("color:#ffffff;", "color:#1d1d1f;")
            p["content"] = p["content"].replace("tile-dark", "tile-light")
            p["content"] = p["content"].replace("color: rgba(255, 255, 255, 0.7);", "color: rgba(0, 0, 0, 0.6);")
            p["content"] = p["content"].replace("border-color: rgba(255, 255, 255, 0.1);", "border-color: rgba(0, 0, 0, 0.1);")
            
        elif p["id"] == "1":
            # Also clean up the bottom quote box in page 1
            p["content"] = p["content"].replace("background:#1d1d1f; color:#ffffff;", "background:#f5f5f7; color:#1d1d1f;")
            p["content"] = p["content"].replace("color:#ffffff;", "color:#1d1d1f;")

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    clean_dark_theme()
