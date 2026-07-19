#!/usr/bin/env python3
"""
inject_approved_text.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
승인 완료된 OCR 텍스트를 주간 보고서 HTML 및 workspace.json에 주입하는 스크립트.

■ 역할 (파이프라인 ④번 다리):
  manifest.json (status=approved) → 주간 보고서 HTML에 본부별 섹션 주입
                                   → workspace.json에 본부별 일정/회의록 데이터 병합

■ 사용법:
  python3 inject_approved_text.py              # 자동 실행
  python3 inject_approved_text.py --dry-run    # 실제 저장 없이 미리보기만

작성일: 2026-07-19
"""

import json
import os
import re
import sys
import glob
from datetime import datetime
from typing import Optional

# ── 경로 설정 ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..')
MANIFEST_FILE = os.path.join(PROJECT_ROOT, 'reports', 'weekly', 'uploads', 'manifest.json')
WORKSPACE_JSON = os.path.join(PROJECT_ROOT, 'src', 'data', 'workspace.json')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')

# ── 업로더(본부장) → 본부명 매핑 ──────────────────────────
# app.py에서 session['user_name']이 업로더로 기록되므로,
# 업로더 이름에 포함된 키워드로 본부를 추론한다.
UPLOADER_TO_DEPT = {
    '디자인': '디자인 본부',
    '도시개발': '도시개발 & 재생 본부',
    '도시재생': '도시 재생 본부',
    '삼정': '삼정건축',
    '도시계획': '도시계획 본부',
    'QC': 'QC팀',
    '전략': '전략 계획 본부',
    '경영': '경영 관리 본부',
    'CM': 'CM/감리 본부',
    '감리': 'CM/감리 본부',
}


def guess_dept_from_uploader(uploader: str) -> str:
    """업로더 이름에서 본부명을 추론. 매칭 안 되면 '기타' 반환."""
    for keyword, dept in UPLOADER_TO_DEPT.items():
        if keyword in uploader:
            return dept
    return f'기타 ({uploader})'


# ═══════════════════════════════════════════════════════════
# 1. manifest.json에서 승인 완료된 항목 수집
# ═══════════════════════════════════════════════════════════

def load_approved_items() -> list:
    """manifest.json에서 status=approved이고 ocr_text가 있는 항목만 반환."""
    if not os.path.exists(MANIFEST_FILE):
        print("⚠️  manifest.json이 존재하지 않습니다.")
        return []

    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  manifest.json 파싱 실패.")
            return []

    approved = [
        item for item in manifest
        if item.get('status') == 'approved'
        and item.get('ocr_text')
        and item.get('ocr_text', '').strip()
    ]

    print(f"📋 승인 완료 항목: {len(approved)}건 / 전체 {len(manifest)}건")
    return approved


# ═══════════════════════════════════════════════════════════
# 2. 승인 텍스트를 본부별로 그룹핑
# ═══════════════════════════════════════════════════════════

def group_by_department(items: list) -> dict:
    """승인 항목들을 본부별로 그룹핑."""
    groups = {}
    for item in items:
        dept = guess_dept_from_uploader(item.get('uploader', ''))
        if dept not in groups:
            groups[dept] = []
        groups[dept].append({
            'filename': item.get('original_name', item.get('filename', '')),
            'uploader': item.get('uploader', ''),
            'text': item.get('ocr_text', ''),
            'timestamp': item.get('timestamp', ''),
            'approved_at': item.get('approved_at', ''),
            'week': item.get('week', ''),
        })
    return groups


# ═══════════════════════════════════════════════════════════
# 3. 주간 보고서 HTML에 승인 텍스트 섹션 주입
# ═══════════════════════════════════════════════════════════

def find_latest_report() -> Optional[str]:
    """reports/ 디렉토리에서 최신 주간 보고서 HTML을 찾는다."""
    pattern = os.path.join(REPORTS_DIR, '*주간*보고*.html')
    files = glob.glob(pattern)
    if not files:
        return None
    files.sort(reverse=True)
    return files[0]


def build_injection_html(dept_groups: dict) -> str:
    """본부별 그룹 데이터로 주입할 HTML 블록을 생성."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""
<!-- ═══════════════════════════════════════════════════════════ -->
<!-- 📷 OCR 승인 텍스트 자동 주입 섹션 (inject_approved_text.py) -->
<!-- 주입 시각: {now} -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div class="page-break"></div>
<section id="ocr-approved-section" style="page-break-before: always;">
    <div class="page-header" style="border-bottom: 3px solid #0066cc;">
        <div class="title" style="color: #0066cc;">📷 본부별 주간일정 · 회의록 (OCR 승인 반영분)</div>
        <div class="date">{now} 자동 주입</div>
    </div>
"""

    for dept_name, items in dept_groups.items():
        html += f"""
    <div style="margin-top: 24px; margin-bottom: 16px;">
        <h3 style="font-size: 16px; font-weight: 600; color: #1d1d1f; border-left: 4px solid #0066cc; padding-left: 12px;">
            {dept_name}
        </h3>
"""
        for item in items:
            # 텍스트를 줄바꿈 기준으로 HTML 포맷
            text_html = item['text'].replace('\n', '<br>')

            html += f"""
        <div style="background: #fafafc; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 13px; font-weight: 600; color: #333;">📄 {item['filename']}</span>
                <span style="font-size: 11px; color: #999;">업로더: {item['uploader']} | 승인: {item['approved_at']}</span>
            </div>
            <div style="font-size: 14px; line-height: 1.7; color: #1d1d1f; white-space: pre-wrap;">
{text_html}
            </div>
        </div>
"""
        html += "    </div>\n"

    html += "</section>\n"
    return html


def inject_into_report(report_path: str, injection_html: str, dry_run: bool = False) -> bool:
    """주간 보고서 HTML 파일 끝(</body> 앞)에 승인 텍스트를 주입."""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 기존 주입 블록이 있으면 제거 (멱등성 보장)
    content = re.sub(
        r'<!-- ═+\s*-->\s*<!-- 📷 OCR 승인 텍스트 자동 주입 섹션.*?</section>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # </body> 직전에 삽입
    if '</body>' in content:
        content = content.replace('</body>', injection_html + '\n</body>')
    else:
        # </body>가 없는 경우 맨 끝에 추가
        content += '\n' + injection_html

    if dry_run:
        print(f"\n[DRY-RUN] 주입 HTML 미리보기 (처음 500자):")
        print(injection_html[:500])
        return True

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 주간 보고서에 승인 텍스트 주입 완료: {os.path.basename(report_path)}")
    return True


# ═══════════════════════════════════════════════════════════
# 4. workspace.json에 승인 데이터 병합
# ═══════════════════════════════════════════════════════════

def update_workspace(dept_groups: dict, dry_run: bool = False) -> bool:
    """workspace.json에 승인된 OCR 텍스트 데이터를 병합."""
    ws_data = {}
    if os.path.exists(WORKSPACE_JSON):
        try:
            with open(WORKSPACE_JSON, 'r', encoding='utf-8') as f:
                ws_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            ws_data = {}

    # ocr_approved 섹션 추가/갱신
    ocr_section = []
    for dept_name, items in dept_groups.items():
        dept_entry = {
            'department': dept_name,
            'items': []
        }
        for item in items:
            dept_entry['items'].append({
                'filename': item['filename'],
                'uploader': item['uploader'],
                'text_preview': item['text'][:200] + ('...' if len(item['text']) > 200 else ''),
                'full_text': item['text'],
                'approved_at': item['approved_at'],
                'week': item['week'],
            })
        ocr_section.append(dept_entry)

    ws_data['ocr_approved'] = ocr_section
    ws_data['ocr_last_injected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 본부별 제출 현황도 갱신
    submission_status = {}
    for dept_name, items in dept_groups.items():
        submission_status[dept_name] = {
            'submitted': True,
            'count': len(items),
            'latest': max(item['approved_at'] for item in items) if items else '',
        }
    ws_data['weekly_submission'] = submission_status

    if dry_run:
        print(f"\n[DRY-RUN] workspace.json 갱신 미리보기:")
        print(f"  ocr_approved: {len(ocr_section)}개 본부")
        return True

    os.makedirs(os.path.dirname(WORKSPACE_JSON), exist_ok=True)
    with open(WORKSPACE_JSON, 'w', encoding='utf-8') as f:
        json.dump(ws_data, f, ensure_ascii=False, indent=2)

    print(f"✅ workspace.json 갱신 완료: {len(ocr_section)}개 본부 데이터 병합")
    return True


# ═══════════════════════════════════════════════════════════
# 5. 메인
# ═══════════════════════════════════════════════════════════

def main():
    dry_run = '--dry-run' in sys.argv

    print("=" * 60)
    print("📷 OCR 승인 텍스트 → 주간 보고서/workspace.json 주입 스크립트")
    print("=" * 60)

    # 1) 승인 항목 수집
    approved_items = load_approved_items()
    if not approved_items:
        print("\n⏭️  승인 완료된 항목이 없습니다. 건너뜁니다.")
        return

    # 2) 본부별 그룹핑
    dept_groups = group_by_department(approved_items)
    print(f"\n📁 본부별 분류:")
    for dept, items in dept_groups.items():
        print(f"   • {dept}: {len(items)}건")

    # 3) 주간 보고서 HTML 주입
    report_path = find_latest_report()
    if report_path:
        print(f"\n📄 대상 보고서: {os.path.basename(report_path)}")
        injection_html = build_injection_html(dept_groups)
        inject_into_report(report_path, injection_html, dry_run)
    else:
        print("\n⚠️  주간 보고서 HTML 파일을 찾지 못했습니다. HTML 주입은 건너뜁니다.")

    # 4) workspace.json 갱신
    update_workspace(dept_groups, dry_run)

    print()
    print("=" * 60)
    if dry_run:
        print("🔍 [DRY-RUN 모드] 실제 파일 변경은 없었습니다.")
    else:
        print("✨ 승인 텍스트 주입 파이프라인 완료!")
    print("=" * 60)


if __name__ == '__main__':
    main()
