import os
import shutil

base_dir = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/content"
appendix_dir = os.path.join(base_dir, "부록_플랫폼_개발일지")

os.makedirs(appendix_dir, exist_ok=True)

# 이동할 폴더 통째로
folders_to_move = [
    "플랫폼_개발_개발자DX"
]

# 이동할 개별 파일들 (경로)
files_to_move = [
    "보안_및_데이터_거버넌스/018_일반_서버_vs_클라우드_서버_진양저널이_클라우드를_선.md",
    "보안_및_데이터_거버넌스/022_통합문서관리_플랫폼_기술_및_교육_가이드_RAG와_클라.md",
    "보안_및_데이터_거버넌스/027_레드팀_데일리_인사이트_2026_07_19.md",
    "보안_및_데이터_거버넌스/028_레드팀_데일리_인사이트_2026_07_18.md",
    "AI_입문_경영자의사결정자/023_1_4_진양_AI_철학_아키_시냅스와_플랫폼_그리고_레.md"
]

for folder in folders_to_move:
    src_folder = os.path.join(base_dir, folder)
    if os.path.exists(src_folder):
        for filename in os.listdir(src_folder):
            src_file = os.path.join(src_folder, filename)
            if os.path.isfile(src_file):
                dst_file = os.path.join(appendix_dir, filename)
                shutil.move(src_file, dst_file)
                print(f"Moved: {filename}")
        # 폴더 내 파일 모두 이동 후 빈 폴더 삭제
        os.rmdir(src_folder)
        print(f"Removed empty folder: {folder}")

for file_rel in files_to_move:
    src_file = os.path.join(base_dir, file_rel)
    if os.path.exists(src_file):
        filename = os.path.basename(src_file)
        dst_file = os.path.join(appendix_dir, filename)
        shutil.move(src_file, dst_file)
        print(f"Moved: {filename}")

print("✅ 개발 관련 문서들을 [부록] 폴더로 모두 분리했습니다.")
