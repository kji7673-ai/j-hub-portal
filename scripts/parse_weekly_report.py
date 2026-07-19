#!/usr/bin/env python3
"""
parse_weekly_report.py
주간 업무 보고서(HTML)를 파싱하여 workspace.json에 구조화된 데이터를 주입하는 스크립트.

■ 추출 항목:
  1. section2.departments — 본부별 프로젝트 목록 (디자인/도시개발/도시재생/삼정건축/도시계획/QC팀 등)
  2. section2.bidding    — 전략 기획 본부 입찰·수주 현황
  3. section3            — 향후 2주 주요 일정 (향후 진행방향·비고 열에서 날짜 추출)
  4. section1.siteUpdates— 금주 핵심 변동사항 (diff-highlight 태그 기반)

■ 사용법:
  python3 parse_weekly_report.py                        # reports/ 에서 최신 파일 자동 탐색
  python3 parse_weekly_report.py <보고서_파일_경로>      # 특정 파일 지정

작성일: 2026-07-19
"""

import json
import os
import re
import sys
import glob
from datetime import datetime
from typing import Optional

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("\n" + "=" * 60)
    print("🚨 [CRITICAL] BeautifulSoup4가 설치되어 있지 않습니다!")
    print("   💡 해결: pip install beautifulsoup4")
    print("=" * 60 + "\n")
    sys.exit(1)

# ── 경로 설정 ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
WORKSPACE_JSON = os.path.join(PROJECT_ROOT, 'src', 'data', 'workspace.json')

# ── 본부 매핑 (page-header title → 출력 본부명) ───────────
DEPT_MAP = {
    '디자인 본부': '디자인 본부',
    '도시 개발 본부': '도시개발 & 재생 본부',
    '도시 재생 본부': '도시 재생 본부',
    '삼정건축': '삼정건축',
    '도시 계획 본부': '도시계획 본부',
    'QC팀': 'QC팀',
    '전략 계획 본부': '전략 계획 본부',
    '경영 관리 본부': '경영 관리 본부',
    'CM/감리 본부': 'CM/감리 본부',
}

# 전략 기획 본부는 별도 처리 (bidding)
BIDDING_DEPT_KEY = '전략 기획 본부'

# ── 날짜 패턴 ─────────────────────────────────────────────
# MM/DD, M/DD, MM/D 형태 + 선택적 (요일)
DATE_PATTERN = re.compile(
    r'(?:0?)(\d{1,2})/(\d{1,2})\s*(?:\(([월화수목금토일])\w*\))?'
)
# "8월중", "8월 초", "7월 말" 등
MONTH_APPROX_PATTERN = re.compile(
    r'(\d{1,2})월\s*(중|초|말|중순|하순|상순)'
)

WEEKDAY_MAP = {
    '월': '월요일', '화': '화요일', '수': '수요일',
    '목': '목요일', '금': '금요일', '토': '토요일', '일': '일요일',
}


# ═══════════════════════════════════════════════════════════
# 1. 파일 탐색
# ═══════════════════════════════════════════════════════════

def find_latest_report(reports_dir: str) -> Optional[str]:
    """reports/ 디렉토리에서 '주간 보고.html' 패턴의 최신 파일을 찾는다."""
    pattern = os.path.join(reports_dir, '*주간*보고*.html')
    files = glob.glob(pattern)
    if not files:
        return None
    # 파일명 기준 역순 정렬 → 최신 파일
    files.sort(reverse=True)
    return files[0]


# ═══════════════════════════════════════════════════════════
# 2. 본부별 세부 업무 현황 파싱
# ═══════════════════════════════════════════════════════════

def _extract_dept_name_from_title(title_text: str) -> Optional[str]:
    """
    page-header .title 텍스트에서 본부명 추출.
    예: '디자인 본부 - 세부 업무 현황' → '디자인 본부'
    """
    if '세부 업무 현황' not in title_text:
        return None
    name = title_text.replace('- 세부 업무 현황', '').strip()
    return name


def _get_project_name_from_row(row: Tag) -> Optional[str]:
    """프로젝트명 셀 (font-weight: 600) 에서 텍스트 추출."""
    for td in row.find_all('td'):
        style = td.get('style', '')
        if 'font-weight' in style and '600' in style:
            return td.get_text(strip=True)
    return None


def _row_has_highlight(row: Tag) -> bool:
    """해당 행에 diff-highlight ins 태그가 존재하는지 확인."""
    return bool(row.find('ins', class_='diff-highlight'))


def _get_column_text(row: Tag, col_idx: int) -> str:
    """행에서 특정 열(0-indexed)의 텍스트를 반환."""
    tds = row.find_all('td')
    if col_idx < len(tds):
        return tds[col_idx].get_text(separator=' ', strip=True)
    return ''


def _build_status_text(row: Tag, header_cols: list) -> str:
    """
    '주요 업무 내용'(col 4) + '향후 진행방향'(col 6) 에서 간결한 상태 문자열 생성.
    diff-highlight 텍스트를 우선 사용.
    """
    tds = row.find_all('td')
    status_parts = []

    # 향후 진행방향 열 (index 6 for standard 8-col table, or find by header)
    future_col_idx = _find_col_index(header_cols, '향후 진행방향', '예정사항')
    main_col_idx = _find_col_index(header_cols, '주요 업무 내용', '진행사항')

    # diff-highlight된 텍스트를 우선 수집
    for idx in [future_col_idx, main_col_idx]:
        if idx is not None and idx < len(tds):
            ins_tags = tds[idx].find_all('ins', class_='diff-highlight')
            for ins in ins_tags:
                text = ins.get_text(strip=True).lstrip('> ·')
                if text and len(text) > 2:
                    status_parts.append(text)

    # diff-highlight가 없으면 향후 진행방향 전체 텍스트 사용
    if not status_parts and future_col_idx is not None and future_col_idx < len(tds):
        text = tds[future_col_idx].get_text(separator=' ', strip=True)
        text = re.sub(r'^[>·\s]+', '', text)
        if text:
            status_parts.append(text)

    # 80자 제한
    result = '; '.join(status_parts)
    if len(result) > 120:
        result = result[:117] + '...'
    return result


def _find_col_index(header_cols: list, *keywords) -> Optional[int]:
    """헤더 목록에서 키워드를 포함하는 열의 인덱스를 반환."""
    for i, col in enumerate(header_cols):
        for kw in keywords:
            if kw in col:
                return i
    return None


def parse_department_tables(soup: BeautifulSoup) -> list:
    """
    '세부 업무 현황' 페이지에서 각 본부의 프로젝트 테이블을 파싱.
    전략 기획 본부는 bidding으로 별도 처리하므로 제외.
    """
    departments = []
    seen_depts = set()

    # 모든 page-header에서 '세부 업무 현황' 페이지를 찾는다
    page_headers = soup.find_all('div', class_='page-header')

    for ph in page_headers:
        title_span = ph.find('span', class_='title')
        if not title_span:
            continue
        title_text = title_span.get_text(strip=True)
        dept_name = _extract_dept_name_from_title(title_text)

        if not dept_name:
            continue
        if dept_name == BIDDING_DEPT_KEY:
            continue  # 전략 기획 본부는 bidding에서 처리

        # 출력용 이름 매핑
        display_name = DEPT_MAP.get(dept_name, dept_name)

        # 이미 처리된 본부 → 프로젝트 병합
        existing_dept = None
        for d in departments:
            if d['name'] == display_name:
                existing_dept = d
                break

        if not existing_dept:
            existing_dept = {'name': display_name, 'projects': []}
            departments.append(existing_dept)

        # page-header가 속한 .page div 안의 table들을 탐색
        page_div = ph.find_parent('div', class_='page')
        if not page_div:
            continue

        tables = page_div.find_all('table')
        for table in tables:
            thead = table.find('thead')
            if not thead:
                continue

            # 헤더 열 이름 수집
            header_cols = [th.get_text(strip=True) for th in thead.find_all('th')]

            # 프로젝트명 열이 있는지 확인
            project_col_idx = _find_col_index(header_cols, '프로젝트명')
            if project_col_idx is None:
                continue

            tbody = table.find('tbody')
            if not tbody:
                continue

            for row in tbody.find_all('tr'):
                project_name = _get_project_name_from_row(row)
                if not project_name:
                    continue

                # 이미 추가된 프로젝트 중복 방지
                if any(p['name'] == project_name for p in existing_dept['projects']):
                    continue

                has_highlight = _row_has_highlight(row)
                status = _build_status_text(row, header_cols)

                existing_dept['projects'].append({
                    'name': project_name,
                    'status': status if status else '업무 진행 중',
                    'highlight': has_highlight,
                })

    return departments


# ═══════════════════════════════════════════════════════════
# 3. 전략 기획 본부 → 입찰/수주 현황 (bidding)
# ═══════════════════════════════════════════════════════════

def parse_bidding_section(soup: BeautifulSoup) -> list:
    """전략 기획 본부 세부 업무 현황에서 입찰/수주 데이터를 추출."""
    bidding = []
    page_headers = soup.find_all('div', class_='page-header')

    for ph in page_headers:
        title_span = ph.find('span', class_='title')
        if not title_span:
            continue
        title_text = title_span.get_text(strip=True)
        dept_name = _extract_dept_name_from_title(title_text)
        if dept_name != BIDDING_DEPT_KEY:
            continue

        page_div = ph.find_parent('div', class_='page')
        if not page_div:
            continue

        tables = page_div.find_all('table')
        for table in tables:
            thead = table.find('thead')
            if not thead:
                continue

            header_cols = [th.get_text(strip=True) for th in thead.find_all('th')]
            project_col_idx = _find_col_index(header_cols, '프로젝트명')
            if project_col_idx is None:
                continue

            schedule_col_idx = _find_col_index(header_cols, '예정사항', '향후 진행방향')
            progress_col_idx = _find_col_index(header_cols, '진행사항', '주요 업무 내용')
            note_col_idx = _find_col_index(header_cols, '비고')

            tbody = table.find('tbody')
            if not tbody:
                continue

            for row in tbody.find_all('tr'):
                project_name = _get_project_name_from_row(row)
                if not project_name:
                    continue

                # 이미 추가된 중복 방지
                if any(b['name'] == project_name for b in bidding):
                    continue

                tds = row.find_all('td')

                # 예정사항 열 텍스트
                schedule = ''
                if schedule_col_idx is not None and schedule_col_idx < len(tds):
                    schedule = tds[schedule_col_idx].get_text(separator=' ', strip=True)
                    schedule = re.sub(r'^[>·\s]+', '', schedule)

                # position: 비고 열 또는 구분 열의 텍스트
                position = ''
                if note_col_idx is not None and note_col_idx < len(tds):
                    position = tds[note_col_idx].get_text(strip=True)

                has_highlight = _row_has_highlight(row)

                bidding.append({
                    'name': project_name,
                    'schedule': schedule[:80] if schedule else '',
                    'position': position[:60] if position else '',
                    'highlight': has_highlight,
                })

    return bidding


# ═══════════════════════════════════════════════════════════
# 4. diff-highlight → siteUpdates (핵심 변동사항)
# ═══════════════════════════════════════════════════════════

def parse_site_updates(soup: BeautifulSoup) -> list:
    """
    diff-highlight(ins 태그)가 있는 행에서 '프로젝트명 — 변경내용' 형태로 추출.
    중복 제거 후 최대 8건.
    """
    updates = []
    seen = set()

    # '세부 업무 현황' 페이지의 테이블 행들에서만 추출
    page_headers = soup.find_all('div', class_='page-header')

    for ph in page_headers:
        title_span = ph.find('span', class_='title')
        if not title_span:
            continue
        title_text = title_span.get_text(strip=True)
        if '세부 업무 현황' not in title_text:
            continue

        page_div = ph.find_parent('div', class_='page')
        if not page_div:
            continue

        # 이 페이지 내 모든 테이블 행
        for table in page_div.find_all('table'):
            tbody = table.find('tbody')
            if not tbody:
                continue
            for row in tbody.find_all('tr'):
                ins_tags = row.find_all('ins', class_='diff-highlight')
                if not ins_tags:
                    continue

                project_name = _get_project_name_from_row(row)
                if not project_name:
                    continue

                # 가장 의미 있는 diff-highlight 텍스트 추출
                highlight_texts = []
                for ins in ins_tags:
                    text = ins.get_text(strip=True).lstrip('> ·')
                    # 너무 짧거나 일반적인 것은 제외
                    if text and len(text) > 3 and text not in ('건축업무지원', '건축업무 지원'):
                        highlight_texts.append(text)

                if not highlight_texts:
                    continue

                desc = highlight_texts[0]
                if len(desc) > 80:
                    desc = desc[:77] + '...'

                key = f"{project_name}|{desc}"
                if key in seen:
                    continue
                seen.add(key)

                updates.append({
                    'name': project_name,
                    'desc': desc,
                })

    # 최대 8건
    return updates[:8]


# ═══════════════════════════════════════════════════════════
# 5. 향후 일정 추출 → section3
# ═══════════════════════════════════════════════════════════

def parse_schedule_items(soup: BeautifulSoup) -> list:
    """
    '향후 진행방향' 및 '예정사항' 열에서 구체적 날짜(M/DD)가 언급된 항목을 추출.
    important-highlight span이 포함된 것은 important=True.
    """
    schedule_items = []
    seen = set()

    page_headers = soup.find_all('div', class_='page-header')

    for ph in page_headers:
        title_span = ph.find('span', class_='title')
        if not title_span:
            continue
        title_text = title_span.get_text(strip=True)
        if '세부 업무 현황' not in title_text:
            continue

        page_div = ph.find_parent('div', class_='page')
        if not page_div:
            continue

        for table in page_div.find_all('table'):
            thead = table.find('thead')
            if not thead:
                continue

            header_cols = [th.get_text(strip=True) for th in thead.find_all('th')]
            future_col_idx = _find_col_index(header_cols, '향후 진행방향', '예정사항')

            if future_col_idx is None:
                continue

            tbody = table.find('tbody')
            if not tbody:
                continue

            for row in tbody.find_all('tr'):
                project_name = _get_project_name_from_row(row)
                if not project_name:
                    continue

                tds = row.find_all('td')
                if future_col_idx >= len(tds):
                    continue

                future_td = tds[future_col_idx]
                future_text = future_td.get_text(separator='\n', strip=False)
                has_important = bool(future_td.find('span', class_='important-highlight'))
                has_new_change = bool(future_td.find('ins', class_='diff-highlight'))

                # 날짜 패턴 매칭
                for match in DATE_PATTERN.finditer(future_text):
                    month = match.group(1)
                    day = match.group(2)
                    weekday_short = match.group(3)

                    date_str = f"{month}/{day}"
                    weekday_str = WEEKDAY_MAP.get(weekday_short, '') if weekday_short else ''

                    # 날짜 주변의 이벤트 설명 추출
                    # 매치된 날짜가 포함된 줄 전체를 가져옴
                    full_match_start = match.start()
                    lines = future_text.split('\n')
                    event_note = ''
                    for line in lines:
                        if date_str in line or (weekday_short and f'({weekday_short})' in line):
                            event_note = line.strip().lstrip('> ·')
                            # 날짜 부분을 제거하고 설명만 남김
                            event_note = re.sub(
                                r'0?\d{1,2}/\d{1,2}\s*\([월화수목금토일]\w*\)\s*',
                                '', event_note
                            ).strip()
                            break

                    if not event_note:
                        event_note = '일정'

                    key = f"{date_str}|{project_name}"
                    if key in seen:
                        continue
                    seen.add(key)

                    important = has_important or has_new_change

                    schedule_items.append({
                        'date': date_str,
                        'weekday': weekday_str,
                        'event': project_name,
                        'note': event_note[:80] if event_note else '',
                        'important': important,
                    })

    # 날짜순 정렬 (월/일 기준)
    def sort_key(item):
        parts = item['date'].split('/')
        try:
            return (int(parts[0]), int(parts[1]))
        except (ValueError, IndexError):
            return (99, 99)

    schedule_items.sort(key=sort_key)

    # 향후 2주 내 일정만 필터 (현재 월/일 기준, 최대 10건)
    from datetime import datetime
    today = datetime.now()
    current_month = today.month
    current_day = today.day
    
    filtered_items = []
    for item in schedule_items:
        parts = item['date'].split('/')
        try:
            m = int(parts[0])
            d = int(parts[1])
            # Filter dates that are in the past (before today minus 3 days for slight leeway)
            # Roughly: if the date is earlier than today, skip it.
            if m < current_month or (m == current_month and d < current_day - 3):
                continue
            filtered_items.append(item)
        except (ValueError, IndexError):
            pass
            
    return filtered_items[:10]


# ═══════════════════════════════════════════════════════════
# 6. workspace.json 로드/저장/병합
# ═══════════════════════════════════════════════════════════

def load_workspace(path: str) -> dict:
    """workspace.json 로드. 파일이 없으면 빈 구조 반환."""
    if not os.path.exists(path):
        print(f"⚠️  workspace.json이 존재하지 않습니다: {path}")
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  workspace.json 로드 실패: {e}")
        return {}


def save_workspace(data: dict, path: str):
    """workspace.json 저장."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def merge_into_workspace(ws_data: dict,
                         departments: list,
                         bidding: list,
                         schedule: list,
                         site_updates: list) -> dict:
    """추출 데이터를 기존 workspace.json에 병합. 건드리지 않는 필드는 보존."""

    # v2 JSON 형식 적용
    if 'dashboard' not in ws_data:
        ws_data['dashboard'] = {}
    if site_updates:
        ws_data['dashboard']['field_updates'] = [
            {"name": su['name'], "content": su['desc']} for su in site_updates
        ]

    if 'projects' not in ws_data:
        ws_data['projects'] = {}
    if departments:
        # 본부별 매핑
        design = []
        urban_dev = []
        urban_plan = []
        for d in departments:
            if '디자인' in d['name']: design.extend(d['projects'])
            elif '개발' in d['name'] or '재생' in d['name']: urban_dev.extend(d['projects'])
            elif '계획' in d['name']: urban_plan.extend(d['projects'])
        
        if design: ws_data['projects']['design_dept'] = design
        if urban_dev: ws_data['projects']['urban_dev_dept'] = urban_dev
        if urban_plan: ws_data['projects']['urban_plan_dept'] = urban_plan

    if bidding:
        ws_data['projects']['strategy_bids'] = [
            {"name": b['name'], "date": b['schedule'], "status": b['position'], "highlight": b.get('highlight', False)}
            for b in bidding
        ]

    if schedule:
        # 플랫 리스트를 date 기준으로 그룹화하여 calendar 형식으로 변환
        cal_dict = {}
        for s in schedule:
            dt = s['date']
            if dt not in cal_dict:
                # 임의의 요일 할당 또는 파싱 로직 추가 가능, 우선 기본 형태 유지
                cal_dict[dt] = {"date": dt, "weekday": "", "events": []}
            cal_dict[dt]['events'].append({
                "time": s.get('time', ''),
                "name": s['event'],
                "note": s.get('note', ''),
                "important": s.get('important', False)
            })
        ws_data['calendar'] = list(cal_dict.values())

    # lastUpdated
    now_str = datetime.now().strftime("%Y.%m.%d %H:%M (실시간 동기화 완료)")
    ws_data['updated_at'] = now_str

    return ws_data


# ═══════════════════════════════════════════════════════════
# 7. 메인
# ═══════════════════════════════════════════════════════════

def main():
    # CLI 인자로 보고서 경로 지정 가능
    if len(sys.argv) >= 2:
        report_path = sys.argv[1]
    else:
        report_path = find_latest_report(REPORTS_DIR)

    if not report_path or not os.path.exists(report_path):
        print(f"🚨 보고서 파일을 찾을 수 없습니다.")
        if report_path:
            print(f"   지정 경로: {report_path}")
        print(f"   탐색 경로: {REPORTS_DIR}")
        sys.exit(1)

    print(f"📄 파싱 대상: {os.path.basename(report_path)}")
    print(f"   경로: {report_path}")
    print()

    # HTML 로드
    with open(report_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # ── 1) 본부별 프로젝트 추출 ──
    print("🔍 [1/4] 본부별 세부 업무 현황 파싱...")
    departments = parse_department_tables(soup)
    total_projects = sum(len(d['projects']) for d in departments)
    print(f"   ✅ {len(departments)}개 본부, 총 {total_projects}개 프로젝트 추출")
    for dept in departments:
        highlighted = sum(1 for p in dept['projects'] if p.get('highlight'))
        print(f"      • {dept['name']}: {len(dept['projects'])}건 (변경 {highlighted}건)")

    # ── 2) 전략 기획 본부 입찰 현황 ──
    print("\n🔍 [2/4] 전략 기획 본부 입찰/수주 현황 파싱...")
    bidding = parse_bidding_section(soup)
    print(f"   ✅ {len(bidding)}개 입찰 프로젝트 추출")
    for b in bidding:
        marker = '🔴 ' if b.get('highlight') else '   '
        print(f"      {marker}{b['name']} — {b['schedule'][:40]}")

    # ── 3) 핵심 변동사항 (diff-highlight) ──
    print("\n🔍 [3/4] 금주 핵심 변동사항(diff-highlight) 추출...")
    site_updates = parse_site_updates(soup)
    print(f"   ✅ {len(site_updates)}개 변동사항 추출")
    for su in site_updates:
        print(f"      • {su['name']}: {su['desc'][:50]}")

    # ── 4) 향후 일정 ──
    print("\n🔍 [4/4] 향후 일정 추출...")
    schedule = parse_schedule_items(soup)
    print(f"   ✅ {len(schedule)}개 일정 항목 추출")
    for s in schedule:
        marker = '⭐ ' if s.get('important') else '   '
        print(f"      {marker}{s['date']} {s['event']} — {s['note'][:40]}")

    # ── workspace.json 병합 ──
    print(f"\n💾 workspace.json 병합 중...")
    ws_data = load_workspace(WORKSPACE_JSON)
    ws_data = merge_into_workspace(ws_data, departments, bidding, schedule, site_updates)
    save_workspace(ws_data, WORKSPACE_JSON)
    print(f"   ✅ 저장 완료: {WORKSPACE_JSON}")
    print(f"   📅 updated_at: {ws_data['updated_at']}")
    print()
    print("=" * 60)
    print("✨ 주간 보고서 파싱 → workspace.json 연동 완료!")
    print("=" * 60)


if __name__ == '__main__':
    main()
