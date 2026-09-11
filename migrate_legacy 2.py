import os
import glob
import json
from bs4 import BeautifulSoup

LEGACY_DIR = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-12/교육자료_매뉴얼/scratch/chapters"
DB_PATH = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/data/manual_db.json"

def categorize_title(title):
    t = title.lower()
    if "용어" in t or "해설" in t or "glossary" in t or "개념" in t:
        return "기초 지식 및 용어 해설"
    elif "프롬프트" in t or "에러" in t or "환각" in t:
        return "프롬프트 및 에러 대처 실무"
    elif "모아타운" in t or "도심복합" in t or "공동주택" in t or "용적률" in t or "lisp" in t:
        return "실무 자동화 가이드 (건축 특화)"
    elif "튜토리얼" in t or "통합보고서" in t or "동향" in t or "주간회의록" in t or "창신" in t or "용문동" in t or "파이프라인" in t:
        return "프로젝트 실전 튜토리얼"
    elif "시스템" in t or "아키텍처" in t or "동기화" in t or "api" in t:
        return "시스템 아키텍처 및 확장"
    elif "부록" in t or "갤러리" in t:
        return "부록"
    else:
        return "상세 교육 매뉴얼 (V1)"

def clean_html(html_str):
    """Convert dark theme to light theme"""
    s = html_str.replace("tile-dark", "tile-light")
    s = s.replace("background-color: var(--surface-tile-1);", "")
    s = s.replace("background: #1d1d1f;", "")
    s = s.replace("color: #ffffff;", "")
    s = s.replace("color: rgba(255, 255, 255, 0.7);", "color: rgba(0, 0, 0, 0.6);")
    s = s.replace("border-color: rgba(255, 255, 255, 0.1);", "border-color: rgba(0, 0, 0, 0.1);")
    s = s.replace("color: var(--on-dark);", "color: var(--ink);")
    return s

def migrate():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    # We want to skip pages we already have? 
    # Actually, the 37 pages are from July 12. The current 7 pages are from July 13 (V2).
    # We will just append all 37 pages to the DB.
    
    files = sorted(glob.glob(os.path.join(LEGACY_DIR, "page_*.html")))
    
    current_id = len(db)
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            raw_html = f.read()
            
        soup = BeautifulSoup(raw_html, "html.parser")
        h2 = soup.find("h2")
        h1 = soup.find("h1")
        title = h2.text.strip() if h2 else (h1.text.strip() if h1 else "No Title")
        title = title.replace("\n", " ")
        
        category = categorize_title(title)
        
        # Clean HTML
        cleaned_html = clean_html(raw_html)
        
        new_page = {
            "id": str(current_id),
            "title": title,
            "content": cleaned_html,
            "ai_instruction": "",
            "ceo_thoughts": "",
            "whiteboard_data": "",
            "category": category,
            "summary": "26.07.12 상세 매뉴얼 데이터"
        }
        
        db.append(new_page)
        current_id += 1
        
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
        
    print(f"Migration complete. Added {len(files)} pages. Total pages: {len(db)}")

if __name__ == "__main__":
    migrate()
