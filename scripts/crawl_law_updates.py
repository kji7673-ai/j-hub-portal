#!/usr/bin/env python3
"""
crawl_law_updates.py
Google News RSS를 통해 건축·정비사업 관련 법규/규정 업데이트를 크롤링하여
J-Hub workspace.json의 section4 및 section1.policyUpdates를 자동 갱신합니다.

검색 쿼리:
  1. 법령+개정+건축        (건축 관련 법령 개정)
  2. 시행령+도시정비+정비사업 (정비사업 시행령)
  3. 입법예고+국토교통부     (국토부 입법예고)
  4. 조례+서울시+건축       (서울시 조례)

사용법:
  python3 crawl_law_updates.py
  python3 crawl_law_updates.py --days 7      # 최근 7일 이내만 필터
  python3 crawl_law_updates.py --dry-run     # workspace.json 수정 없이 결과만 출력
"""

import argparse
import json
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from html import unescape
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote

# ═══════════════════════════════════════════════════════════════
# 경로 설정
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_JSON = os.path.join(SCRIPT_DIR, '..', 'data', 'workspace.json')

# ═══════════════════════════════════════════════════════════════
# 로거 설정
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# Google News RSS 검색 쿼리 정의
# ═══════════════════════════════════════════════════════════════

SEARCH_QUERIES = [
    {
        "query": "법령+개정+건축",
        "label": "건축 관련 법령 개정",
        "default_category": "신규시행",
    },
    {
        "query": "시행령+도시정비+정비사업",
        "label": "정비사업 시행령",
        "default_category": "신규시행",
    },
    {
        "query": "입법예고+국토교통부",
        "label": "국토부 입법예고",
        "default_category": "입법예고",
    },
    {
        "query": "조례+서울시+건축",
        "label": "서울시 조례",
        "default_category": "지자체고시",
    },
]

GOOGLE_NEWS_RSS_BASE = (
    "https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
)

# ═══════════════════════════════════════════════════════════════
# 카테고리 분류 키워드 매핑
# ═══════════════════════════════════════════════════════════════

CATEGORY_KEYWORDS = {
    "신규시행": [
        "시행", "개정 시행", "공포", "시행령", "시행규칙",
        "신규 시행", "개정안 시행", "즉시 시행",
    ],
    "입법예고": [
        "입법예고", "입법 예고", "의견 수렴", "공청회",
        "규제심사", "법제처", "국민참여", "의견조회",
    ],
    "정책발표": [
        "정책", "대책", "발표", "방안", "계획 발표",
        "로드맵", "혁신방안", "종합계획", "추진계획",
        "국토부", "국토교통부", "장관", "차관",
    ],
    "지자체고시": [
        "조례", "고시", "공고", "서울시", "광역시",
        "자치구", "지자체", "지방자치", "구청",
        "시청", "도시계획위원회", "건축위원회",
    ],
}

# 정책 업데이트 뱃지 매핑
CATEGORY_BADGE_MAP = {
    "신규시행": {"badge": "신규시행", "badgeClass": "green"},
    "입법예고": {"badge": "입법예고", "badgeClass": "blue"},
    "정책발표": {"badge": "정책발표", "badgeClass": "red"},
    "지자체고시": {"badge": "지자체고시", "badgeClass": "orange"},
}


# ═══════════════════════════════════════════════════════════════
# HTML 정리 유틸
# ═══════════════════════════════════════════════════════════════

def clean_html(text: str) -> str:
    """HTML 태그 제거 및 엔티티 디코딩."""
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_source(title: str) -> tuple[str, str]:
    """Google News 제목에서 ' - 매체명' 패턴을 분리합니다.
    Returns: (순수 제목, 매체명)
    """
    # Google News RSS 제목 형식: "기사 제목 - 매체명"
    match = re.match(r'^(.+?)\s*-\s*([^-]+)$', title)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return title, "미확인"


# ═══════════════════════════════════════════════════════════════
# Google News RSS pubDate 파싱
# ═══════════════════════════════════════════════════════════════

def parse_pub_date(date_str: str) -> datetime | None:
    """Google News RSS pubDate를 datetime으로 변환.
    형식 예: 'Sat, 19 Jul 2026 00:47:00 GMT'
    """
    if not date_str:
        return None

    try:
        # RFC 2822 형식 파싱 (email.utils 표준 라이브러리)
        return parsedate_to_datetime(date_str)
    except (ValueError, TypeError):
        pass

    # 폴백: 수동 파싱 시도
    date_formats = [
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    logger.warning(f"날짜 파싱 실패: '{date_str}'")
    return None


# ═══════════════════════════════════════════════════════════════
# 카테고리 자동 분류
# ═══════════════════════════════════════════════════════════════

def classify_category(title: str, description: str, default_category: str) -> str:
    """제목과 설명을 기반으로 법규 카테고리를 분류합니다."""
    combined = f"{title} {description}".lower()

    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > 0:
            scores[category] = score

    if scores:
        return max(scores, key=scores.get)

    return default_category


# ═══════════════════════════════════════════════════════════════
# RSS 크롤링
# ═══════════════════════════════════════════════════════════════

def fetch_rss(query: str, timeout: int = 15) -> list[dict]:
    """Google News RSS에서 기사 목록을 가져옵니다."""
    url = GOOGLE_NEWS_RSS_BASE.format(query=quote(query, safe='+'))
    logger.info(f"📡 RSS 요청: {query}")
    logger.debug(f"   URL: {url}")

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': 'application/rss+xml, application/xml, text/xml',
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            xml_data = response.read()
    except HTTPError as e:
        logger.error(f"HTTP 에러 {e.code}: {query} — {e.reason}")
        return []
    except URLError as e:
        logger.error(f"URL 에러: {query} — {e.reason}")
        return []
    except Exception as e:
        logger.error(f"네트워크 에러: {query} — {e}")
        return []

    # XML 파싱
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        logger.error(f"XML 파싱 에러: {query} — {e}")
        return []

    items = []
    for item_el in root.iter('item'):
        title_el = item_el.find('title')
        pub_date_el = item_el.find('pubDate')
        desc_el = item_el.find('description')
        link_el = item_el.find('link')
        source_el = item_el.find('source')

        raw_title = clean_html(title_el.text if title_el is not None else "")
        title, source_from_title = extract_source(raw_title)

        # source 태그가 있으면 우선, 없으면 제목에서 추출
        if source_el is not None and source_el.text:
            source = source_el.text.strip()
        else:
            source = source_from_title

        description = clean_html(desc_el.text if desc_el is not None else "")
        pub_date_str = pub_date_el.text if pub_date_el is not None else ""
        link = link_el.text.strip() if link_el is not None else ""

        parsed_date = parse_pub_date(pub_date_str)

        items.append({
            "title": title,
            "date": parsed_date,
            "date_str": pub_date_str,
            "source": source,
            "description": description,
            "link": link,
        })

    logger.info(f"   → {len(items)}건 수신")
    return items


def crawl_all_queries(days_filter: int = 14) -> list[dict]:
    """모든 검색 쿼리를 실행하고 결과를 통합합니다.

    Args:
        days_filter: 최근 N일 이내의 기사만 포함 (기본 14일)

    Returns:
        분류된 기사 리스트
    """
    cutoff_date = datetime.now() - timedelta(days=days_filter)
    all_articles = []
    seen_titles = set()  # 중복 제거용

    for q in SEARCH_QUERIES:
        items = fetch_rss(q["query"])

        for item in items:
            # 날짜 필터
            if item["date"] and item["date"].replace(tzinfo=None) < cutoff_date:
                continue

            # 중복 제거 (제목 기반)
            title_key = re.sub(r'\s+', '', item["title"])[:40]
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

            # 카테고리 분류
            category = classify_category(
                item["title"],
                item["description"],
                q["default_category"],
            )

            all_articles.append({
                "title": item["title"],
                "date": item["date"],
                "date_formatted": (
                    item["date"].strftime("%m.%d") if item["date"] else "미확인"
                ),
                "source": item["source"],
                "category": category,
                "description": item["description"],
                "link": item["link"],
                "query_label": q["label"],
            })

    # 최신순 정렬
    all_articles.sort(key=lambda x: x["date"] or datetime.min, reverse=True)

    logger.info(f"\n📊 총 {len(all_articles)}건 수집 완료")
    for cat in ["신규시행", "입법예고", "정책발표", "지자체고시"]:
        count = sum(1 for a in all_articles if a["category"] == cat)
        if count:
            logger.info(f"   [{cat}] {count}건")

    return all_articles


# ═══════════════════════════════════════════════════════════════
# workspace.json 변환
# ═══════════════════════════════════════════════════════════════

def build_section4_data(articles: list[dict], existing_section4: dict) -> dict:
    """크롤링 결과를 section4 형식으로 변환합니다.
    기존 section4의 suggestions10 등 다른 키는 보존합니다.

    section4 형식:
      newLaws: [{date, name, desc}]
      localNotices: [string]
    """
    section4 = dict(existing_section4)  # 기존 데이터 복사

    # --- newLaws: 신규시행 + 입법예고 + 정책발표 ---
    new_laws = []
    for article in articles:
        if article["category"] in ("신규시행", "입법예고", "정책발표"):
            desc = article["description"]
            if len(desc) > 60:
                desc = desc[:57] + "..."

            new_laws.append({
                "date": article["date_formatted"],
                "name": article["title"][:30] if len(article["title"]) > 30 else article["title"],
                "desc": desc if desc else f"({article['source']})",
            })

    # 기존 newLaws와 병합 (크롤링 결과 우선, 최대 10건)
    if new_laws:
        existing_laws = existing_section4.get("newLaws", [])
        # 기존 항목 중 중복되지 않는 것만 유지
        existing_names = {law["name"][:15] for law in new_laws}
        for law in existing_laws:
            if law["name"][:15] not in existing_names:
                new_laws.append(law)
        section4["newLaws"] = new_laws[:10]

    # --- localNotices: 지자체고시 ---
    new_notices = []
    for article in articles:
        if article["category"] == "지자체고시":
            title = article["title"]
            if len(title) > 60:
                title = title[:57] + "..."
            notice = f"[{article['source']}] {title}"
            new_notices.append(notice)

    # 기존 localNotices와 병합
    if new_notices:
        existing_notices = existing_section4.get("localNotices", [])
        existing_set = {n[:30] for n in existing_notices}
        for notice in existing_notices:
            if notice[:30] not in {n[:30] for n in new_notices}:
                new_notices.append(notice)
        section4["localNotices"] = new_notices[:10]

    return section4


def build_policy_updates(articles: list[dict], existing_updates: list) -> list:
    """크롤링 결과를 section1.policyUpdates 형식으로 변환합니다.

    형식: [{badge, badgeClass, title, desc}]
    """
    new_updates = []

    for article in articles[:5]:  # 최근 5건만
        badge_info = CATEGORY_BADGE_MAP.get(
            article["category"],
            {"badge": article["category"], "badgeClass": "gray"},
        )

        desc = article["description"]
        if len(desc) > 80:
            desc = desc[:77] + "..."
        if not desc:
            desc = f"{article['source']} 보도"

        # 날짜 정보 뱃지에 추가
        date_suffix = f" ({article['date_formatted']})" if article['date_formatted'] != "미확인" else ""

        new_updates.append({
            "badge": badge_info["badge"] + date_suffix,
            "badgeClass": badge_info["badgeClass"],
            "title": article["title"],
            "desc": desc,
        })

    # 기존 policyUpdates 중 '기 보고' 항목 보존
    for update in existing_updates:
        if update.get("badge", "").startswith("기 보고") or update.get("badge", "").startswith("기보고"):
            new_updates.append(update)

    return new_updates[:8]  # 최대 8건


# ═══════════════════════════════════════════════════════════════
# workspace.json 읽기 / 쓰기
# ═══════════════════════════════════════════════════════════════

def load_workspace() -> dict:
    """workspace.json을 읽어 dict로 반환합니다."""
    path = os.path.normpath(WORKSPACE_JSON)

    if not os.path.exists(path):
        logger.error(f"workspace.json이 존재하지 않습니다: {path}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info(f"📂 workspace.json 로드 완료 (lastUpdated: {data.get('lastUpdated', 'N/A')})")
    return data


def save_workspace(data: dict) -> None:
    """workspace.json에 저장합니다. 기존 파일은 .bak으로 백업합니다."""
    path = os.path.normpath(WORKSPACE_JSON)

    # 백업 생성
    bak_path = path + '.bak'
    if os.path.exists(path):
        import shutil
        shutil.copy2(path, bak_path)
        logger.info(f"💾 백업 생성: {bak_path}")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ workspace.json 저장 완료: {path}")


# ═══════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Google News RSS 기반 법규 업데이트 크롤러 → workspace.json 갱신',
    )
    parser.add_argument(
        '--days', type=int, default=14,
        help='최근 N일 이내 기사만 필터링 (기본: 14)',
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='workspace.json을 수정하지 않고 결과만 출력',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='상세 로그 출력',
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=" * 60)
    logger.info("🚀 법규 업데이트 크롤러 시작")
    logger.info(f"   필터: 최근 {args.days}일 이내")
    logger.info(f"   모드: {'DRY-RUN (미저장)' if args.dry_run else '실행 (저장)'}")
    logger.info("=" * 60)

    # 1. 크롤링 실행
    articles = crawl_all_queries(days_filter=args.days)

    if not articles:
        logger.warning("⚠️ 수집된 기사가 없습니다. workspace.json을 변경하지 않습니다.")
        return

    # 2. 결과 요약 출력
    logger.info("\n" + "─" * 60)
    logger.info("📋 수집 결과 요약:")
    logger.info("─" * 60)
    for i, article in enumerate(articles[:15], 1):
        logger.info(
            f"  {i:2d}. [{article['category']}] {article['date_formatted']} "
            f"| {article['title'][:45]}"
        )
        if args.verbose:
            logger.debug(f"      출처: {article['source']} | 쿼리: {article['query_label']}")

    if len(articles) > 15:
        logger.info(f"  ... 외 {len(articles) - 15}건")

    # 3. workspace.json 업데이트
    if args.dry_run:
        logger.info("\n🏁 DRY-RUN 모드: workspace.json 수정을 건너뜁니다.")

        # dry-run에서도 변환 결과를 보여줌
        sample_section4 = build_section4_data(articles, {})
        logger.info("\n[section4.newLaws 미리보기]")
        for law in sample_section4.get("newLaws", [])[:5]:
            logger.info(f"  • {law['date']} | {law['name']} — {law['desc']}")
        logger.info("\n[section4.localNotices 미리보기]")
        for notice in sample_section4.get("localNotices", [])[:5]:
            logger.info(f"  • {notice}")
        return

    # 기존 데이터 로드
    ws_data = load_workspace()

    # section4 업데이트 (기존 데이터 보존)
    existing_section4 = ws_data.get("section4", {})
    ws_data["section4"] = build_section4_data(articles, existing_section4)

    # section1.policyUpdates 업데이트
    if "section1" not in ws_data:
        ws_data["section1"] = {}
    existing_policy = ws_data["section1"].get("policyUpdates", [])
    ws_data["section1"]["policyUpdates"] = build_policy_updates(articles, existing_policy)

    # lastUpdated 타임스탬프 갱신
    now_str = datetime.now().strftime("%Y.%m.%d %H:%M (법규 크롤링 반영)")
    ws_data["lastUpdated"] = now_str

    # 저장
    save_workspace(ws_data)

    logger.info("\n" + "=" * 60)
    logger.info("🎉 법규 업데이트 크롤링 및 workspace.json 갱신 완료!")
    logger.info(f"   section4.newLaws: {len(ws_data['section4'].get('newLaws', []))}건")
    logger.info(f"   section4.localNotices: {len(ws_data['section4'].get('localNotices', []))}건")
    logger.info(f"   section1.policyUpdates: {len(ws_data['section1'].get('policyUpdates', []))}건")
    logger.info(f"   lastUpdated: {now_str}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
