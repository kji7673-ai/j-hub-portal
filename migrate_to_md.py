#!/usr/bin/env python3
import json
import os
import re

DB_PATH = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/data/manual_db.json"
CONTENT_DIR = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/content"

def sanitize_filename(name):
    # 특수문자 제거 및 공백을 언더스코어로
    s = re.sub(r'[^\w\s가-힣-]', '', name)
    return re.sub(r'[-\s]+', '_', s).strip('_')

def main():
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)

    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    for doc in db:
        cat = doc.get("category", "미분류")
        cat_dir_name = sanitize_filename(cat)
        cat_dir = os.path.join(CONTENT_DIR, cat_dir_name)
        
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)
            
        doc_id = doc.get("id", 0)
        title = doc.get("title", "제목없음")
        file_name = f"{doc_id:03d}_{sanitize_filename(title)[:30]}.md"
        file_path = os.path.join(cat_dir, file_name)
        
        # 메타데이터 분리
        meta = {
            "id": doc_id,
            "title": title,
            "category": cat,
            "level": doc.get("level", 1),
            "is_internal": doc.get("is_internal", False),
            "date": doc.get("date", ""),
            "summary": doc.get("summary", "")
        }
        
        # Markdown 컨텐츠 (html 필드에 마크다운이 변환된 상태로 저장되어 있을 수도 있고 content 필드에 마크다운 원본이 있을 수도 있음)
        # J-Hub의 기존 manual_db.json 구조: 'content'에 Markdown 저장, 'html'에 렌더링된 HTML 저장.
        # Markdown 원본만 저장하고, HTML 렌더링은 빌드 스크립트로 이관.
        content_md = doc.get("content", "")
        
        with open(file_path, "w", encoding="utf-8") as out_f:
            out_f.write("---json\n")
            json.dump(meta, out_f, ensure_ascii=False, indent=2)
            out_f.write("\n---\n")
            out_f.write(content_md)
            
        print(f"Created: {file_path}")

if __name__ == "__main__":
    main()
