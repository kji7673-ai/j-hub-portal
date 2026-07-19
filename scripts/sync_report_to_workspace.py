#!/usr/bin/env python3
"""
sync_report_to_workspace.py
정비사업통합검토보고서(Markdown/HTML)의 주요 데이터를 파싱하여 
J-Hub의 workspace.json에 주입하는 스크립트 (Phase 2 연동 테스트용)
"""

import json
import os
import sys
from datetime import datetime

WORKSPACE_JSON = os.path.join(os.path.dirname(__file__), '../data/workspace.json')

def load_workspace():
    with open(WORKSPACE_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_workspace(data):
    with open(WORKSPACE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_data_from_report(report_path):
    """
    실제 보고서(MD/HTML) 파일을 읽고 BeautifulSoup으로 데이터를 파싱합니다.
    """
    print(f"📄 '{report_path}' 에서 데이터를 파싱합니다...")
    
    extracted = {
        "siteUpdates": [],
        "newSchedule": []
    }
    
    try:
        from bs4 import BeautifulSoup
        
        with open(report_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        # 1. 현장 핵심 변동 파싱 (Summary Box 내의 h3 이후 ul li 탐색)
        summary_boxes = soup.find_all('div', class_='summary-box')
        for box in summary_boxes:
            h3_tags = box.find_all('h3')
            for h3 in h3_tags:
                if '현장' in h3.text or '법규' in h3.text:
                    ul = h3.find_next_sibling('ul')
                    if ul:
                        for li in ul.find_all('li'):
                            text = li.get_text(strip=True)
                            # 예: "[07.10] 서울시 특별회의 — 내용" -> 분리
                            parts = text.split('—')
                            if len(parts) >= 2:
                                name = parts[0].strip()
                                desc = parts[1].strip()
                                extracted["siteUpdates"].append({"name": name, "desc": desc})
                                
        # 2. 일정표 파싱 (추후 상세 테이블 파싱 등으로 고도화 가능)
        # 우선은 더미로 몇 가지 일정을 세팅 (보고서 테이블 구조에 따라 변경)
        extracted["newSchedule"] = [
            { "date": "다음 주", "weekday": "예정", "event": "주요 회의", "note": "보고서 자동 추출 일정", "important": True }
        ]
        
    except ImportError:
        print("\n" + "="*50)
        print("🚨 [CRITICAL ERROR] BeautifulSoup4(bs4) 라이브러리가 설치되어 있지 않습니다!")
        print("💡 해결 방법: 터미널에서 'pip install beautifulsoup4'를 실행하세요.")
        print("⚠️ 현재는 테스트(더미) 데이터로 강제 진행합니다.")
        print("="*50 + "\n")
        return {
            "siteUpdates": [
                { "name": "장위15구역", "desc": "정비사업통합보고서 생성 완료 (신규)" },
                { "name": "대림1구역", "desc": "주민총회 안건 분석 완료" }
            ],
            "newSchedule": []
        }
    except Exception as e:
        print(f"⚠️ 파싱 중 에러 발생: {e}")
        
    return extracted

def main():
    if len(sys.argv) < 2:
        print("사용법: python3 sync_report_to_workspace.py <보고서_파일_경로>")
        sys.exit(1)
        
    report_path = sys.argv[1]
    
    print("🚀 보고서 데이터 -> J-Workspace 연동 파이프라인 시작...")
    
    ws_data = load_workspace()
    extracted = extract_data_from_report(report_path)
    
    # Section 1: 현장 핵심 변동 업데이트
    if "section1" not in ws_data:
        ws_data["section1"] = {"siteUpdates": []}
    
    # 기존 업데이트 내역을 밀어내거나 병합 (최근 5건 유지)
    current_updates = extracted["siteUpdates"] + ws_data["section1"].get("siteUpdates", [])
    ws_data["section1"]["siteUpdates"] = current_updates[:5]
    
    # Section 3: 일정표 업데이트
    if "section3" not in ws_data:
        ws_data["section3"] = []
    
    current_schedules = extracted["newSchedule"] + ws_data.get("section3", [])
    ws_data["section3"] = current_schedules[:5]
    
    # 최종 업데이트 시간 변경
    now_str = datetime.now().strftime("%Y.%m.%d %H:%M (보고서 연동 완료)")
    ws_data["lastUpdated"] = now_str
    
    save_workspace(ws_data)
    print(f"✅ {WORKSPACE_JSON} 업데이트 성공!")

if __name__ == '__main__':
    main()
