#!/usr/bin/env python3
"""
validate_build.py — J-Hub 빌드 후 Smoke Test
빌드된 index.html의 필수 요소를 검증하여 Weekly Report 소실을 방지합니다.
"""
import os, sys

INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
BACKUP_PATH = INDEX_PATH + '.bak'

REQUIRED_MARKERS = [
    ('view-weekly', 1, 'Weekly Report 탭'),
    ('view-master', 1, 'Master 제안함 탭'),
    ('view-workspace', 1, 'Workspace 뷰'),
    ('view-journal', 1, 'Journal 뷰'),
    ('iframe', 3, 'Weekly Report + 법규동향 + Workspace iframe'),
    ('wa-container', 4, 'Workspace 아코디언 섹션'),
    ('mode-btn', 4, '모드 전환 버튼'),
]

MIN_FILE_SIZE = 50000  # 50KB 미만이면 비정상

def validate():
    if not os.path.exists(INDEX_PATH):
        print("🚨 FAIL: index.html이 존재하지 않습니다!")
        return False

    size = os.path.getsize(INDEX_PATH)
    if size < MIN_FILE_SIZE:
        print(f"🚨 FAIL: index.html 크기 비정상 ({size:,} bytes < {MIN_FILE_SIZE:,} bytes)")
        return False

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    all_passed = True
    for marker, min_count, desc in REQUIRED_MARKERS:
        count = html.count(marker)
        if count < min_count:
            print(f"🚨 FAIL: {desc} — 기대 ≥{min_count}, 실제 {count}")
            all_passed = False
        else:
            print(f"  ✅ {desc}: {count}개 확인")

    if all_passed:
        print(f"\n✅ SMOKE TEST PASSED — index.html ({size:,} bytes)")
    else:
        print(f"\n🚨 SMOKE TEST FAILED — 롤백이 필요합니다!")
        if os.path.exists(BACKUP_PATH):
            print(f"   💡 백업 파일 존재: {BACKUP_PATH}")

    return all_passed

if __name__ == '__main__':
    success = validate()
    sys.exit(0 if success else 1)
