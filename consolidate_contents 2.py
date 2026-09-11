import os
import shutil
import re

base_dir = "/Users/joongilkim/Desktop/03_업무자료/법규관련/생성 자료/2026-07-14/웹_매뉴얼_플랫폼/content"
new_track_dir = os.path.join(base_dir, "01_진양_AI_통합_매뉴얼")
archive_dir = os.path.join(base_dir, "archive_old_contents")

os.makedirs(new_track_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

# 병합 계획
merge_plan = {
    "01_진양_AI_마인드셋_및_보안규정.md": [
        "AI_입문_경영자의사결정자/001_통합본_진양_AI_여정과_7대_비전.md",
        "AI_실무_활용_설계자실무자/003_문서_3_AI를_다루는_16가지_핵심_사고방식.md",
        "AI_입문_경영자의사결정자/004_문서_4_1인_1플랫폼의_명암_코어는_하나로_엣지는_개.md",
        "AI_입문_경영자의사결정자/005_문서_5_매뉴얼을_넘어_실전으로_우리가_마주할_4가지_.md",
        "보안_및_데이터_거버넌스/007_문서_7_전사_보안_규정_및_데이터_해시화.md"
    ],
    "02_실전_SOP_프롬프트_템플릿_총망라.md": [
        "AI_실무_활용_설계자실무자/009_문서_9_통합_사업성_검토_플랫폼_활용_가이드.md",
        "AI_실무_활용_설계자실무자/011_문서_11_실전_튜토리얼_가상의_대상지_사업성_검토_따.md",
        "AI_실무_활용_설계자실무자/013_문서_13_즉시_복사해서_쓰는_마법의_프롬프트_템플릿.md",
        "AI_실무_활용_설계자실무자/014_문서_14_AI_배치_실전_SOP_계산값프롬프트체크리스.md"
    ],
    "03_K_제너러티브_배치_및_용어해설.md": [
        "AI_실무_활용_설계자실무자/006_문서_6_K_제너러티브_배치_알고리즘_V2_데크_우선주.md",
        "공통_모듈/016_문서_15_핵심_용어_해설집_배치지하법규_편.md"
    ],
    "04_AI_환각_방지_및_교차_검증_매뉴얼.md": [
        "AI_실무_활용_설계자실무자/008_문서_8_AI_환각_방지_및_교차_검증_매뉴얼.md"
    ],
    "05_진양저널_주간보고_및_밴드연동_가이드.md": [
        "공통_모듈/010_문서_10_진양_저널_사내_소통과_게이미피케이션.md",
        "보안_및_데이터_거버넌스/017_네이버_밴드_진양저널_주간회의록_안전_연동_가이드.md"
    ]
}

def strip_frontmatter_and_extract_title(content):
    if content.startswith("```json"):
        end_idx = content.find("```", 7)
        if end_idx != -1:
            return content[end_idx+3:].strip()
    return content.strip()

for new_filename, src_files in merge_plan.items():
    combined_content = ""
    # Create frontmatter for the new file
    title = new_filename.replace(".md", "").replace("_", " ")
    combined_content += f"```json\n{{\n  \"title\": \"{title}\"\n}}\n```\n\n"
    
    for src in src_files:
        src_path = os.path.join(base_dir, src)
        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
                cleaned_content = strip_frontmatter_and_extract_title(content)
                combined_content += cleaned_content + "\n\n---\n\n"
            
            # Archive the file
            archive_subdir = os.path.join(archive_dir, os.path.dirname(src))
            os.makedirs(archive_subdir, exist_ok=True)
            shutil.move(src_path, os.path.join(archive_subdir, os.path.basename(src)))
        else:
            print(f"Warning: {src_path} not found.")
            
    # Write the new combined file
    with open(os.path.join(new_track_dir, new_filename), 'w', encoding='utf-8') as f:
        f.write(combined_content)
    print(f"✅ Created {new_filename}")

# Remove empty directories
for root, dirs, files in os.walk(base_dir, topdown=False):
    if root == base_dir or root.startswith(archive_dir) or root.startswith(new_track_dir):
        continue
    if root.endswith("부록_플랫폼_개발일지"):
        continue
    try:
        os.rmdir(root)
        print(f"Removed empty directory: {root}")
    except OSError:
        pass
