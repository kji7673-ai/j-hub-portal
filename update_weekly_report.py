import os
import sys
import re
import argparse

def update_weekly_report(input_file, output_file, old_week_str, new_week_str, old_date_str, new_date_str):
    """
    주간 보고서 HTML을 복사하며, 주차 및 날짜 텍스트를 일괄 치환하여 휴먼 에러를 방지합니다.
    """
    if not os.path.exists(input_file):
        print(f"Error: 입력 파일 {input_file} 이(가) 존재하지 않습니다.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 일괄 치환 진행
    updated_content = content.replace(old_week_str, new_week_str)
    updated_content = updated_content.replace(old_date_str, new_date_str)

    # 출력 폴더가 없다면 생성
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"[완료] {output_file} 파일이 성공적으로 자동 생성/치환 되었습니다!")
    print(f" - {old_week_str} -> {new_week_str}")
    print(f" - {old_date_str} -> {new_date_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="주간 보고서 주차 및 날짜 일괄 자동 치환기")
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
