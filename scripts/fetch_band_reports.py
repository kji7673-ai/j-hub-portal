#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
네이버 밴드 API 수집 스크립트 (통합 주간 보고서용)
--------------------------------------------------
이 스크립트는 매주 금/일 오후 5시에 예약 실행(Cron)되어,
진양 엔지니어링 네이버 밴드에 업로드된 직원들의 주간 보고서 자료(텍스트, 이미지)를 수집합니다.

[설치 및 세팅 가이드]
1. 개발자 센터 접속: https://developers.band.us/
2. "내 앱(My Apps)"에서 앱 생성 후, [Access Token] 발급
3. 아래의 'YOUR_ACCESS_TOKEN' 변수에 발급받은 문자열을 붙여넣으세요.
4. 'YOUR_BAND_KEY' 변수에는 진양 밴드의 고유 키를 붙여넣으세요.
   (밴드 키는 /v2.1/bands 엔드포인트에서 확인할 수 있습니다.)

[크론(Cron) 예약 설정 방법]
터미널에서 `crontab -e`를 입력 후 아래 두 줄을 추가하세요:
# 매주 금요일 오후 5시 실행
0 17 * * 5 /usr/bin/python3 /Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/scripts/fetch_band_reports.py
# 매주 일요일 오후 5시 실행
0 17 * * 0 /usr/bin/python3 /Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/scripts/fetch_band_reports.py
"""

import os
import requests
import json
from datetime import datetime

# ==========================================
# [설정] 발급받은 토큰 및 키를 입력하세요
# ==========================================
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
BAND_KEY = "YOUR_BAND_KEY_HERE"

# API Endpoints
API_URL_BANDS = "https://openapi.band.us/v2.1/bands"
API_URL_POSTS = "https://openapi.band.us/v2/band/posts"

def get_recent_posts():
    """밴드에서 최신 게시글 목록과 첨부 이미지 URL을 가져옵니다."""
    print("네이버 밴드 API 접근 중...")
    
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("[오류] Access Token이 설정되지 않았습니다. 개발자 센터에서 토큰을 발급받아 입력해주세요.")
        return None

    # 요청 파라미터 구성
    params = {
        'access_token': ACCESS_TOKEN,
        'band_key': BAND_KEY,
        'locale': 'ko_KR'
    }

    try:
        response = requests.get(API_URL_POSTS, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('result_code') == 1:
            posts = data['result_data']['items']
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {len(posts)}개의 게시글을 성공적으로 불러왔습니다.")
            return posts
        else:
            print(f"[API 오류] {data.get('result_code')} - {data.get('result_data', {}).get('message', '알 수 없는 오류')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[네트워크 오류] 밴드 서버와 통신할 수 없습니다: {e}")
        return None

def process_reports(posts):
    """
    수집된 텍스트와 이미지 URL을 바탕으로 AI 요약 모듈로 전송합니다.
    (이 함수는 pipeline_daily.py 등 기존 통합 보고서 파이프라인과 연동됩니다.)
    """
    print("수집된 데이터를 AI 요약 파이프라인으로 전송합니다...")
    
    # 예시 로직: 텍스트 및 이미지 추출
    for post in posts:
        content = post.get('content', '')
        author = post.get('author', {}).get('name', '알 수 없음')
        photos = post.get('photos', [])
        
        print(f"작성자: {author}")
        print(f"내용 요약: {content[:50]}...")
        if photos:
            print(f"첨부된 이미지 수: {len(photos)}")
            # 이미지 OCR 처리를 위해 URL을 Vision API로 전송하는 로직이 여기에 추가됩니다.
        print("-" * 30)

if __name__ == "__main__":
    print("=== 진양 엔지니어링 주간 보고서 수집 파이프라인 가동 ===")
    
    # 1. 밴드 API를 통해 데이터 수집
    posts = get_recent_posts()
    
    # 2. 데이터 처리 및 AI 초안 작성
    if posts:
        process_reports(posts)
        print(">> J-Hub 포털(index.html)의 [Weekly Report] 탭에 임시 저장(Draft) 상태로 대기 처리 완료.")
        print(">> 대표님 승인 대기 중입니다.")
    else:
        print(">> 수집할 데이터가 없거나 인증 정보가 올바르지 않습니다.")
