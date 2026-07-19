import os
import sys
import argparse
from bs4 import BeautifulSoup

def update_weekly_report(input_file, output_file, old_week_str, new_week_str, old_date_str, new_date_str):
    """
    FUNC-03 FIX: BeautifulSoup을 사용하여 특정 HTML 요소(제목, 헤더)만 선별 교체.
    본문 기사 내의 동일 문자열은 변경하지 않음.
    """
    if not os.path.exists(input_file):
        print(f"Error: 입력 파일 {input_file} 이(가) 존재하지 않습니다.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # 제목(title), h1~h3 헤더, .report-header 등 구조적 요소만 선별 교체
    SAFE_TAGS = ['title', 'h1', 'h2', 'h3', 'h4']
    SAFE_CLASSES = ['report-header', 'report-title', 'week-label', 'date-range', 'header-subtitle']
    
    changed_count = 0
    
    # 1. 안전 태그 내에서만 주차 텍스트 교체
    for tag_name in SAFE_TAGS:
        for tag in soup.find_all(tag_name):
            if old_week_str in tag.get_text():
                original_html = str(tag)
                tag.string = tag.get_text().replace(old_week_str, new_week_str).replace(old_date_str, new_date_str)
                changed_count += 1
    
    # 2. 안전 클래스를 가진 요소 내에서도 교체
    for cls in SAFE_CLASSES:
        for el in soup.find_all(class_=cls):
            if old_week_str in el.get_text() or old_date_str in el.get_text():
                for text_node in el.find_all(string=True):
                    if old_week_str in text_node:
                        text_node.replace_with(text_node.replace(old_week_str, new_week_str))
                        changed_count += 1
                    if old_date_str in text_node:
                        text_node.replace_with(text_node.replace(old_date_str, new_date_str))
                        changed_count += 1
    
    # 3. meta 태그 등 문서 메타데이터도 교체
    for meta in soup.find_all('meta'):
        if meta.get('content') and (old_week_str in meta['content'] or old_date_str in meta['content']):
            meta['content'] = meta['content'].replace(old_week_str, new_week_str).replace(old_date_str, new_date_str)
            changed_count += 1
    
    # 출력 폴더가 없다면 생성
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"[완료] {output_file} 파일이 성공적으로 자동 생성/치환 되었습니다!")
    print(f" - {old_week_str} -> {new_week_str}")
    print(f" - {old_date_str} -> {new_date_str}")
    print(f" - 변경된 요소: {changed_count}개 (구조적 태그만 선별 교체, 본문 기사 보호)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="주간 보고서 주차 및 날짜 선별 자동 치환기 (BS4)")
    parser.add_argument("--input", required=True, help="이전 주차 HTML 원본 파일 경로")
    parser.add_argument("--output", required=True, help="새 주차 HTML 저장 파일 경로")
    parser.add_argument("--old-week", required=True, help="기존 주차 텍스트 (예: '7월 4주차')")
    parser.add_argument("--new-week", required=True, help="신규 주차 텍스트 (예: '8월 1주차')")
    parser.add_argument("--old-date", required=True, help="기존 날짜 범위 (예: '7.20 ~ 7.26')")
    parser.add_argument("--new-date", required=True, help="신규 날짜 범위 (예: '7.27 ~ 8.2')")
    
    args = parser.parse_args()
    
    update_weekly_report(
        args.input, 
        args.output, 
        args.old_week, 
        args.new_week, 
        args.old_date, 
        args.new_date
    )
