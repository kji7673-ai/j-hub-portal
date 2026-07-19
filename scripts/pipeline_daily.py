#!/usr/bin/env python3
"""
pipeline_daily.py — J-Hub 일일 100선 뉴스 크롤러
Google News RSS를 활용하여 건축·부동산·정비사업 관련 실제 뉴스를 수집합니다.
"""

import json
import random
import datetime
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
import re

# Google News RSS 피드 목록 (카테고리별)
RSS_FEEDS = [
    {
        "url": "https://news.google.com/rss/search?q=%EB%B6%80%EB%8F%99%EC%82%B0+%EA%B1%B4%EC%B6%95+%EC%9E%AC%EA%B0%9C%EB%B0%9C&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "부동산 · 경제",
        "name": "부동산·건축·재개발"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EC%A0%95%EB%B9%84%EC%82%AC%EC%97%85+%EC%9E%AC%EA%B1%B4%EC%B6%95+%EB%AA%A8%EC%95%84%ED%83%80%EC%9A%B4&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "정책 · 인허가",
        "name": "정비·재건축·모아타운"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EA%B1%B4%EC%B6%95+ESG+%EC%B9%9C%ED%99%98%EA%B2%BD+%EC%A0%9C%EB%A1%9C%EC%97%90%EB%84%88%EC%A7%80&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "ESG · 친환경",
        "name": "건축ESG·친환경"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EC%8A%A4%EB%A7%88%ED%8A%B8%EC%8B%9C%ED%8B%B0+%EB%8F%84%EC%8B%9C%EC%9E%AC%EC%83%9D+%ED%94%84%EB%A1%AD%ED%85%8C%ED%81%AC&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "미래 도시",
        "name": "스마트시티·도시재생·프롭테크"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EA%B1%B4%EC%84%A4%EA%B2%BD%EC%A0%9C+%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85+%EC%A3%BC%ED%83%9D%EC%8B%9C%EC%9E%A5&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "부동산 · 경제",
        "name": "건설경제·주택시장"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EA%B1%B4%EC%B6%95%EB%AC%B8%ED%99%94+%EA%B3%B5%EA%B3%B5%EB%AF%B8%EC%88%A0+%EA%B1%B4%EC%B6%95%EB%94%94%EC%9E%90%EC%9D%B8&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "건축과 미술",
        "name": "건축문화·디자인"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EB%8F%84%EC%8B%9C%EA%B3%84%ED%9A%8D+%EC%9D%B8%ED%97%88%EA%B0%80+%EA%B1%B4%EC%B6%95%EC%8B%AC%EC%9D%98&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "정책 · 인허가",
        "name": "도시계획·인허가·건축심의"
    },
    {
        "url": "https://news.google.com/rss/search?q=%ED%95%B4%EC%99%B8%EA%B1%B4%EC%84%A4+%EA%B8%80%EB%A1%9C%EB%B2%8C%EB%B6%80%EB%8F%99%EC%82%B0&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "해외 동향",
        "name": "해외건설·글로벌부동산"
    },
    {
        "url": "https://news.google.com/rss/search?q=%EC%A3%BC%EA%B1%B0%ED%8A%B8%EB%A0%8C%EB%93%9C+%EB%9D%BC%EC%9D%B4%ED%94%84%EC%8A%A4%ED%83%80%EC%9D%BC+1%EC%9D%B8%EA%B0%80%EA%B5%AC&hl=ko&gl=KR&ceid=KR:ko",
        "default_cat": "사회 트렌드",
        "name": "주거트렌드·라이프스타일"
    },
]

# 카테고리 키워드 매핑 (제목 기반 자동 분류)
CATEGORY_KEYWORDS = {
    "ESG · 친환경": ["ESG", "친환경", "탄소", "ZEB", "제로에너지", "녹색", "그린", "탄소중립", "넷제로"],
    "테크 · 프롭테크": ["AI", "프롭테크", "스마트홈", "디지털트윈", "자동화", "메타버스", "로봇", "BIM", "DX"],
    "미래 도시": ["도시재생", "스마트시티", "미래도시", "혁신도시", "뉴타운", "TOD", "MaaS"],
    "해외 동향": ["미국", "중국", "일본", "유럽", "해외", "글로벌", "두바이", "싱가포르"],
    "정책 · 인허가": ["조례", "시행령", "입법예고", "인허가", "의무화", "규제", "건축심의", "도시계획"],
    "건축과 미술": ["디자인", "공공미술", "건축상", "프리츠커", "전시", "비엔날레", "미술관"],
    "사회 트렌드": ["MZ세대", "1인가구", "고령화", "라이프스타일", "주거복지", "공유주택", "청년주택"],
    "부동산 · 경제": ["분양", "매매", "시세", "금리", "PF", "착공", "공급", "재건축", "재개발"],
    "도시 인문학": ["역사", "문화유산", "지역", "마을", "커뮤니티", "보존", "골목"],
}

def classify_category(title, default_cat):
    """제목에서 키워드를 탐색하여 가장 적합한 카테고리 반환"""
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in title for kw in keywords):
            return cat
    return default_cat

def extract_publisher(title):
    """Google News 제목에서 ' - 매체명' 추출"""
    match = re.search(r'\s-\s(.+)$', title)
    if match:
        return match.group(1).strip()
    return "뉴스"

def clean_title(title):
    """Google News 제목에서 ' - 매체명' 부분 제거"""
    cleaned = re.sub(r'\s-\s[^-]+$', '', title)
    return cleaned.strip()

def parse_google_news_date(pub_date_str):
    """Google News의 pubDate를 한국어 날짜로 변환"""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(pub_date_str)
        return dt.strftime("%Y.%m.%d")
    except:
        return datetime.datetime.now().strftime("%Y.%m.%d")

def run_pipeline():
    print("🚀 뉴스 크롤링 파이프라인 시작...")
    print(f"   대상 RSS 피드: {len(RSS_FEEDS)}개")
    
    articles = []
    seen_titles = set()  # 중복 제거용
    
    for feed_info in RSS_FEEDS:
        feed_url = feed_info["url"]
        default_cat = feed_info["default_cat"]
        feed_name = feed_info["name"]
        
        # 피드별 최대 15건으로 제한 — 9개 카테고리 균형 분배
        MAX_PER_FEED = 15
        
        try:
            req = urllib.request.Request(feed_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            items = root.findall('.//item')
            feed_count = 0
            
            for item in items:
                raw_title = item.find('title').text if item.find('title') is not None else ""
                if not raw_title:
                    continue
                
                # 중복 제거
                title_key = clean_title(raw_title)[:40]
                if title_key in seen_titles:
                    continue
                seen_titles.add(title_key)
                
                publisher = extract_publisher(raw_title)
                title = clean_title(raw_title)
                
                desc = item.find('description').text if item.find('description') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                date_str = parse_google_news_date(pub_date)
                
                # description에서 HTML 제거
                excerpt = re.sub(r'<[^>]+>', '', desc).strip()[:200] if desc else f"{title}에 대한 최신 뉴스입니다."
                
                category = classify_category(title, default_cat)
                
                articles.append({
                    "category": category,
                    "title": title,
                    "excerpt": excerpt if excerpt else f"{title} — {publisher} 보도",
                    "meta": f"{publisher} | {date_str}"
                })
                feed_count += 1
                
                if feed_count >= MAX_PER_FEED or len(articles) >= 100:
                    break
            
            print(f"   ✅ [{feed_name}] {feed_count}건 수집 (누적: {len(articles)}건)")
            
        except Exception as e:
            print(f"   ⚠️ [{feed_name}] 실패: {str(e)[:80]}")
            continue
        
        if len(articles) >= 100:
            break
    
    print(f"\n📊 크롤링 결과: 실제 기사 {len(articles)}건 수집")
    
    # 100건 미만이면 나머지를 다른 카테고리 검색으로 보충
    if len(articles) < 100:
        shortfall = 100 - len(articles)
        print(f"   ⚠️ {shortfall}건 부족 — 추가 검색 시도")
        
        extra_queries = [
            ("%EA%B1%B4%EC%B6%95%EC%82%AC+%EC%84%A4%EA%B3%84+%EC%82%AC%EB%AC%B4%EC%86%8C", "건축사·설계", "도시 인문학"),
            ("%EC%95%84%ED%8C%8C%ED%8A%B8+%EC%8B%9C%EC%84%B8+%EB%B6%84%EC%96%91", "아파트·분양", "부동산 · 경제"),
        ]
        for query, name, cat in extra_queries:
            if len(articles) >= 100:
                break
            try:
                extra_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
                req = urllib.request.Request(extra_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                root = ET.fromstring(data)
                for item in root.findall('.//item'):
                    raw_title = item.find('title').text or ""
                    title_key = clean_title(raw_title)[:40]
                    if title_key in seen_titles:
                        continue
                    seen_titles.add(title_key)
                    
                    publisher = extract_publisher(raw_title)
                    pub_date = item.find('pubDate').text or ""
                    articles.append({
                        "category": classify_category(clean_title(raw_title), cat),
                        "title": clean_title(raw_title),
                        "excerpt": f"{clean_title(raw_title)} — {publisher} 보도",
                        "meta": f"{publisher} | {parse_google_news_date(pub_date)}"
                    })
                    if len(articles) >= 100:
                        break
                print(f"   ✅ [보충: {name}] 누적 {len(articles)}건")
            except Exception as e:
                print(f"   ⚠️ [보충: {name}] 실패: {e}")
    
    # 최종 100건으로 잘라내기 + 셔플
    articles = articles[:100]
    random.shuffle(articles)
    
    # 카테고리별 통계 출력
    cat_stats = {}
    for a in articles:
        c = a["category"]
        cat_stats[c] = cat_stats.get(c, 0) + 1
    print(f"\n📋 카테고리 분포:")
    for c, n in sorted(cat_stats.items(), key=lambda x: -x[1]):
        print(f"   {c}: {n}건")
    
    # 저장
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    out_path = os.path.join(data_dir, 'daily_articles.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ {len(articles)}건 저장 완료: {out_path}")

if __name__ == "__main__":
    run_pipeline()
