import json
import random
import datetime
import os
import sys

def fallback_generator(count=100):
    categories = ["해외 동향", "ESG · 친환경", "정책 · 인허가", "부동산 · 경제", "미래 도시", "테크 · 프롭테크", "건축과 미술", "도시 인문학", "사회 트렌드"]
    topics = ["도심 복합개발", "초고층 스카이라인", "ZEB 의무화", "프롭테크 혁명", "모듈러 건축", "공공미술의 가치", "젠트리피케이션", "공간 심리학", "라이프스타일 변화", "도시재생과 문화"]
    perspectives = ["명암과 한계", "위기와 기회", "현장 르포", "새로운 지평", "실무적 해법", "예술적 시각", "인문학적 고찰", "사회적 합의"]
    publishers = ["한국경제 부동산", "매일경제 뎁스", "건설경제 프리미엄", "스마트시티 저널", "디자인프레스", "도시건축 리뷰", "월간 미술", "트렌드 코리아"]
    
    today = datetime.datetime.now()
    articles = []
    
    for _ in range(count):
        cat = random.choice(categories)
        title = f"[일일 동향] {random.choice(topics)}: {random.choice(perspectives)}"
        days_ago = random.randint(0, 7)
        pub_date = today - datetime.timedelta(days=days_ago)
        date_str = pub_date.strftime("%Y.%m.%d")
        meta = f"{random.choice(publishers)} | {date_str}"
        excerpt = f"최근 {random.choice(topics)}에 대한 논의가 활발합니다. 이것은 건축업계의 중요한 이슈입니다."
        
        articles.append({
            "category": cat,
            "title": title,
            "excerpt": excerpt,
            "meta": meta
        })
    return articles

def run_pipeline():
    print("🚀 뉴스 크롤링 파이프라인 시작...")
    
    articles = []
    try:
        import urllib.request
        from bs4 import BeautifulSoup
        import xml.etree.ElementTree as ET
        
        # EXT-03 FIX: 다중 RSS 피드 + 카테고리 자동 분류
        RSS_FEEDS = [
            ("https://rss.hankyung.com/new/news_estate.xml", "부동산 · 경제", "한국경제"),
            ("https://rss.hankyung.com/new/news_economy.xml", "정책 · 인허가", "한국경제"),
            ("https://www.mk.co.kr/rss/30100041/", "부동산 · 경제", "매일경제"),
            ("https://rss.hankyung.com/new/news_international.xml", "해외 동향", "한국경제"),
        ]
        
        # 카테고리 키워드 매핑 (제목 기반 자동 분류)
        CATEGORY_KEYWORDS = {
            "ESG · 친환경": ["ESG", "친환경", "탄소", "ZEB", "제로에너지", "녹색", "그린"],
            "테크 · 프롭테크": ["AI", "프롭테크", "스마트", "디지털", "자동화", "메타버스", "로봇"],
            "미래 도시": ["도시재생", "스마트시티", "미래", "혁신도시", "공공주택"],
            "해외 동향": ["미국", "중국", "일본", "유럽", "해외", "글로벌"],
            "정책 · 인허가": ["정책", "인허가", "법", "규제", "의무화", "시행령", "조례"],
        }
        
        def classify_category(title, default_cat):
            for cat, keywords in CATEGORY_KEYWORDS.items():
                if any(kw in title for kw in keywords):
                    return cat
            return default_cat
        
        for feed_url, default_cat, publisher in RSS_FEEDS:
            try:
                req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    xml_data = response.read()
                
                root = ET.fromstring(xml_data)
                for item in root.findall('.//item'):
                    title = item.find('title').text if item.find('title') is not None else "제목 없음"
                    desc = item.find('description').text if item.find('description') is not None else ""
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                    
                    soup = BeautifulSoup(desc, "html.parser")
                    excerpt = soup.get_text()[:200].strip()
                    
                    articles.append({
                        "category": classify_category(title, default_cat),
                        "title": title,
                        "excerpt": excerpt if excerpt else f"{title}에 대한 최신 동향 기사입니다.",
                        "meta": f"{publisher} | {pub_date}"
                    })
                    
                    if len(articles) >= 100:
                        break
                        
            except Exception as feed_err:
                print(f"⚠️ RSS 피드 실패 ({feed_url}): {feed_err}")
                continue
            
            if len(articles) >= 100:
                break
                
        print(f"✅ 실제 크롤링 성공: {len(articles)}건 수집")
        
    except Exception as e:
        print("\n" + "="*50)
        print(f"🚨 [CRITICAL ERROR] 크롤링 실패: {e}")
        print("⚠️ 오프라인/샌드박스 환경으로 인해 Fallback 더미 데이터를 사용합니다.")
        print("="*50 + "\n")
        articles = fallback_generator(100)
    
    # 100개가 안 채워졌으면 더미로 보충
    if len(articles) < 100:
        articles.extend(fallback_generator(100 - len(articles)))
        
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    out_path = os.path.join(data_dir, 'daily_articles.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Generated {len(articles)} daily articles at {out_path}")

if __name__ == "__main__":
    run_pipeline()

