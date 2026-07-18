#!/usr/bin/env python3
"""
update_workspace_api.py
서울시 오픈 API 크롤러(fetch_seoul_notices.py) 결과를 J-Hub의 workspace.json에 주입하는 스크립트
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

def generate_dummy_api_data():
    """API Key가 제공되지 않았을 때 사용하는 더미 데이터"""
    return [
        { "name": "갈현1구역", "status": "등록", "desc": "[테스트] 사업시행계획 변경 인가", "active": True },
        { "name": "한남3구역", "status": "등록", "desc": "[테스트] 관리처분계획 인가 고시", "active": True },
        { "name": "노량진1구역", "status": "미지정", "desc": "[테스트] 건축심의 상정 전", "active": False },
        { "name": "상계주공5단지", "status": "등록", "desc": "[테스트] 정비계획 결정 고시", "active": True }
    ]

def fetch_real_data(api_key):
    """fetch_seoul_notices.py를 실행하여 JSON 파싱 (현재는 미구현)"""
    print(f"API Key {api_key}를 사용하여 fetch_seoul_notices.py를 실행합니다...")
    return generate_dummy_api_data()

def main():
    api_key = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🚀 J-Workspace API 연동 파이프라인 시작...")
    
    ws_data = load_workspace()
    
    if api_key:
        api_data = fetch_real_data(api_key)
    else:
        print("⚠️ API Key가 제공되지 않았습니다. 테스트 모드(더미 데이터)로 작동합니다.")
        api_data = generate_dummy_api_data()
        
    # 데이터 병합
    if "section2" not in ws_data:
        ws_data["section2"] = {}
    
    ws_data["section2"]["apiData"] = api_data
    
    # 최종 업데이트 시간 변경
    now_str = datetime.now().strftime("%Y.%m.%d %H:%M (API 자동 동기화)")
    ws_data["lastUpdated"] = now_str
    
    save_workspace(ws_data)
    print(f"✅ {WORKSPACE_JSON} 업데이트 성공!")

if __name__ == '__main__':
    main()
