import json
import os

DB_PATH = "data/manual_db.json"

def get_summary(title):
    if "프롤로그" in title:
        return "정비사업 통합 검토 플랫폼의 철학과 원칙"
    elif "제1장" in title:
        return "구역계 및 토지대장 기반 데이터 수집 원리"
    elif "제2장" in title:
        return "용적률 계산, 상가 제척 및 기부채납 연산"
    elif "제3장" in title:
        return "KPI 대시보드 및 마스터 PDF 자동 생성"
    elif "부록" in title:
        return "에러 복구 스크립트 및 시스템 유지보수 지침"
    return "기본 내용"

def update_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    for p in db:
        cat = p.get("category", "")
        if cat == "기타":
            p["category"] = "목차" # Or just place it properly
            
        # Give page 0 a specific category
        if p["id"] == "0":
            p["category"] = "도입부"
        if p["id"] == "6":
            p["category"] = "부록"
            
        p["summary"] = get_summary(p["title"])
            
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_db()
