#!/usr/bin/env python3
"""
서울시 열린데이터광장 ListNewsTender API 크롤러
- 정비사업/건축 관련 공고만 필터링
- 중복 BOARD_ID 제거 (첨부파일별 중복 row 통합)
- 일일 동향 보고서용 JSON/마크다운 출력

사용법:
  python3 fetch_seoul_notices.py --key YOUR_API_KEY
  python3 fetch_seoul_notices.py --key YOUR_API_KEY --days 7
  python3 fetch_seoul_notices.py --xml input.xml   # 로컬 XML 파싱
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from html import unescape
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# 1. 필터링 키워드 (당사 관련 정비사업/건축 공고)
# ═══════════════════════════════════════════════════════════════

INCLUDE_KEYWORDS = [
    # 정비사업 유형
    "재개발", "재건축", "정비사업", "정비구역", "정비계획",
    "도시정비", "주거환경개선", "주거정비",
    # 소규모정비
    "모아타운", "모아주택", "가로주택", "소규모정비", "소규모재건축",
    "자율주택", "빈집정비",
    # 도시계획
    "지구단위계획", "도시관리계획", "용도지역", "종상향",
    "도심복합", "역세권개발", "공공재개발",
    # 건축 인허가
    "건축심의", "건축위원회", "도시계획위원회", "통합심의",
    "사업시행인가", "관리처분", "조합설립",
    # 입찰/용역
    "설계용역", "건축설계", "정비계획수립", "건축사",
    "엔지니어링", "도시계획용역", "MP용역",
    # 법규/조례
    "도정법", "도시정비법", "소규모주택정비법", "주택법",
    "건축법", "국토계획법",
    # 기타 관련
    "안전진단", "리모델링", "공공주택", "임대주택",
]

EXCLUDE_KEYWORDS = [
    # 비관련 분야 제외
    "청소년", "위탁운영", "체육시설", "문화시설",
    "환경미화", "쓰레기", "급식", "의료",
    "소방", "경찰", "교통신호", "버스노선",
]

# ═══════════════════════════════════════════════════════════════
# 2. HTML → 평문 변환
# ═══════════════════════════════════════════════════════════════

def strip_html(html_str):
    """HTML 태그 제거 및 평문 추출"""
    if not html_str:
        return ""
    text = unescape(html_str)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ═══════════════════════════════════════════════════════════════
# 3. XML 파싱 + 중복 제거 + 필터링
# ═══════════════════════════════════════════════════════════════

def parse_xml(xml_content):
    """XML 응답을 파싱하여 고유 공고 목록 반환 (중복 BOARD_ID 통합)"""
    root = ET.fromstring(xml_content)
    
    # 에러 체크
    result = root.find('RESULT')
    if result is not None:
        code = result.findtext('CODE', '')
        if code != 'INFO-000':
            msg = result.findtext('MESSAGE', '')
            print(f"❌ API 에러: {code} - {msg}", file=sys.stderr)
            return []
    
    total = root.findtext('list_total_count', '0')
    print(f"📊 전체 공고 수: {total}건", file=sys.stderr)
    
    # 중복 BOARD_ID 통합 (첨부파일만 합침)
    notices = {}
    for row in root.findall('row'):
        board_id = row.findtext('BOARD_ID', '')
        if not board_id:
            continue
        
        if board_id not in notices:
            notices[board_id] = {
                'board_id': board_id,
                'title': row.findtext('TITLE', ''),
                'author': row.findtext('KOR_NAME', ''),
                'create_date': row.findtext('CREATE_DATE', ''),
                'update_date': row.findtext('UPDATE_DATE', ''),
                'organ': row.findtext('ORGAN', ''),
                'position': row.findtext('POSITION', ''),
                'tel': row.findtext('TEL', ''),
                'email': row.findtext('EMAIL', ''),
                'contents_html': row.findtext('CONTENTS', ''),
                'contents_text': strip_html(row.findtext('CONTENTS', '')),
                'read_cnt': int(row.findtext('READ_CNT', '0')),
                'start_date': row.findtext('START_DATE', ''),
                'end_date': row.findtext('END_DATE', ''),
                'date_check': row.findtext('DATE_CHECK', ''),
                'file_count': int(row.findtext('FILE_COUNT', '0')),
                'files': [],
                'trackback': row.findtext('TRACKBACK', ''),
            }
        
        # 첨부파일 추가
        file_name = row.findtext('APPD_FILE_NAME', '')
        file_url = row.findtext('FILE_URL', '')
        if file_name:
            notices[board_id]['files'].append({
                'name': file_name,
                'url': file_url,
                'size': int(row.findtext('FILE_SIZE', '0')),
            })
    
    print(f"📋 중복 제거 후 고유 공고: {len(notices)}건", file=sys.stderr)
    return list(notices.values())


def filter_notices(notices, days=None):
    """정비사업/건축 관련 공고만 필터링"""
    filtered = []
    
    for notice in notices:
        search_text = f"{notice['title']} {notice['contents_text']} {notice['position']}"
        
        # 제외 키워드 체크
        if any(kw in search_text for kw in EXCLUDE_KEYWORDS):
            continue
        
        # 포함 키워드 체크
        matched_keywords = [kw for kw in INCLUDE_KEYWORDS if kw in search_text]
        if not matched_keywords:
            continue
        
        # 날짜 필터 (선택적)
        if days and notice['create_date']:
            try:
                created = datetime.strptime(notice['create_date'][:8], '%Y%m%d')
                cutoff = datetime.now() - timedelta(days=days)
                if created < cutoff:
                    continue
            except ValueError:
                pass
        
        notice['matched_keywords'] = matched_keywords
        notice['relevance_score'] = len(matched_keywords)
        filtered.append(notice)
    
    # 관련도 높은 순 정렬
    filtered.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"🎯 정비사업 관련 필터링 결과: {len(filtered)}건", file=sys.stderr)
    return filtered


# ═══════════════════════════════════════════════════════════════
# 4. 보고서용 마크다운 출력
# ═══════════════════════════════════════════════════════════════

def format_date(date_str):
    """'20260716095524' → '2026-07-16'"""
    if not date_str or len(date_str) < 8:
        return "N/A"
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"


def to_report_markdown(notices):
    """일일 동향 보고서 섹션용 마크다운 생성"""
    if not notices:
        return "해당 기간 내 정비사업 관련 서울시 공고/입찰 없음.\n"
    
    lines = []
    lines.append(f"### 서울시 공고/입찰 동향 (자동 수집 {len(notices)}건)\n")
    lines.append(f"> 📎 출처: 서울 열린데이터광장 ListNewsTender API | 수집일: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    lines.append("| # | 공고명 | 부서 | 게시일 | 키워드 | 조회수 |")
    lines.append("|---|--------|------|--------|--------|--------|")
    
    for i, n in enumerate(notices, 1):
        title = n['title'][:40] + ('...' if len(n['title']) > 40 else '')
        keywords = ', '.join(n.get('matched_keywords', [])[:3])
        lines.append(
            f"| {i} | {title} | {n['position']} | {format_date(n['create_date'])} | {keywords} | {n['read_cnt']} |"
        )
    
    lines.append("")
    
    # 상세 내용 (상위 5건)
    for i, n in enumerate(notices[:5], 1):
        lines.append(f"#### {i}. {n['title']}")
        lines.append(f"- **기관**: {n['organ']} {n['position']}")
        lines.append(f"- **게시일**: {format_date(n['create_date'])}")
        lines.append(f"- **담당자**: {n['author']} ({n['tel']})")
        
        # 내용 요약 (첫 200자)
        summary = n['contents_text'][:200]
        if len(n['contents_text']) > 200:
            summary += "..."
        lines.append(f"- **요약**: {summary}")
        
        if n['files']:
            lines.append(f"- **첨부파일**: {', '.join(f['name'] for f in n['files'])}")
        
        lines.append("")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 5. API 호출 (온라인 모드)
# ═══════════════════════════════════════════════════════════════

def fetch_from_api(api_key, start=1, end=100):
    """서울시 Open API 호출"""
    import urllib.request
    
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/xml/ListNewsTender/{start}/{end}/"
    print(f"🌐 API 호출: {url}", file=sys.stderr)
    
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


# ═══════════════════════════════════════════════════════════════
# 6. 메인
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='서울시 공고/입찰 정비사업 필터링')
    parser.add_argument('--key', help='서울시 Open API 인증키')
    parser.add_argument('--xml', help='로컬 XML 파일 경로 (오프라인 모드)')
    parser.add_argument('--days', type=int, default=7, help='최근 N일 이내 공고만 (기본: 7)')
    parser.add_argument('--count', type=int, default=1000, help='API 호출 시 가져올 건수 (기본: 1000)')
    parser.add_argument('--format', choices=['json', 'markdown', 'both'], default='both',
                        help='출력 형식 (기본: both)')
    parser.add_argument('--output', help='출력 파일 경로 (기본: stdout)')
    
    args = parser.parse_args()
    
    # XML 데이터 획득
    if args.xml:
        xml_content = Path(args.xml).read_text(encoding='utf-8')
    elif args.key:
        xml_content = fetch_from_api(args.key, 1, args.count)
    else:
        print("❌ --key 또는 --xml 중 하나를 지정해주세요.", file=sys.stderr)
        sys.exit(1)
    
    # 파싱 → 필터링
    notices = parse_xml(xml_content)
    filtered = filter_notices(notices, days=args.days)
    
    # 출력
    output_parts = []
    
    if args.format in ('json', 'both'):
        # JSON 출력 (contents_html 제거하여 용량 절감)
        json_data = []
        for n in filtered:
            clean = {k: v for k, v in n.items() if k != 'contents_html'}
            json_data.append(clean)
        
        json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
        
        if args.format == 'json':
            output_parts.append(json_str)
        else:
            # JSON 파일 별도 저장
            json_path = args.output.replace('.md', '.json') if args.output else None
            if json_path:
                Path(json_path).write_text(json_str, encoding='utf-8')
                print(f"💾 JSON 저장: {json_path}", file=sys.stderr)
    
    if args.format in ('markdown', 'both'):
        md = to_report_markdown(filtered)
        output_parts.append(md)
    
    result = "\n\n".join(output_parts)
    
    if args.output:
        Path(args.output).write_text(result, encoding='utf-8')
        print(f"💾 저장 완료: {args.output}", file=sys.stderr)
    else:
        print(result)
    
    # 요약 통계
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"📊 처리 요약:", file=sys.stderr)
    print(f"   - 전체 수신: {len(notices)}건 (중복 제거 후)", file=sys.stderr)
    print(f"   - 정비사업 관련: {len(filtered)}건", file=sys.stderr)
    print(f"   - 필터 통과율: {len(filtered)/max(len(notices),1)*100:.1f}%", file=sys.stderr)
    if filtered:
        all_kws = {}
        for n in filtered:
            for kw in n.get('matched_keywords', []):
                all_kws[kw] = all_kws.get(kw, 0) + 1
        top_kws = sorted(all_kws.items(), key=lambda x: -x[1])[:10]
        print(f"   - 상위 키워드: {', '.join(f'{k}({v})' for k,v in top_kws)}", file=sys.stderr)


if __name__ == '__main__':
    main()
