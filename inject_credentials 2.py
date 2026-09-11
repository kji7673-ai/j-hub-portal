import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

# 1. Update MD with Author Profile and modified Interlude

with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

# Add Author Profile right after the title
author_profile_md = """

## 저자 소개: 현장의 최전선에서 정책을 조율하는 건축가

- **현(現) 서울시 건축심의위원**
- **현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원**
- **현(現) 강동구, 양천구 건축심의위원**
- **현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원**

정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 뼈저리게 목도하고 있는 건축가의 현장 고발이자 생존 전략.
"""
md_text = md_text.replace("## 프롤로그: 우리는 왜 '진짜 설계'를 잃어버렸는가?", author_profile_md + "\n## 프롤로그: 우리는 왜 '진짜 설계'를 잃어버렸는가?")

# Modify Interlude
old_interlude_part = """수주에 눈이 먼 일부 설계사무소들은 "무조건 용적률 최대, 사업성 최대"라는 허황된 청사진으로 조합원들을 현혹한다. 하지만 진정한 전문가의 길은 다르다. 서울시의 행정 기조를 정확히 꿰뚫고, 해당 사업지의 현실적인 사업 방향과 방식을 냉철하게 검토해야 한다."""

new_interlude_part = """나는 현재 서울시 건축심의위원이자 각 구의 모아타운 MP(Master Planner)로서, 이 거대한 '행정의 깔때기'가 어떻게 작동하는지 심의장 최전선에서 매일 목도하고 있다. 그렇기에 수주에 눈이 멀어 "무조건 용적률 최대, 사업성 최대"라는 허황된 청사진으로 조합원들을 현혹하는 것이 얼마나 무책임하고 위험한 일인지 누구보다 잘 안다. 진정한 전문가의 길은 다르다. 서울시의 행정 기조를 정확히 꿰뚫고, 해당 사업지의 현실적인 사업 방향과 방식을 냉철하게 검토해야 한다."""

md_text = md_text.replace(old_interlude_part, new_interlude_part)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)


# 2. Update JS with Author Profile and modified Interlude

with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# Add Author Profile page (index 1)
author_profile_js = """        {
            "type": "text_only",
            "title": "저자 소개: 현장의 최전선에서 정책을 조율하는 건축가",
            "text": "<li>**현(現) 서울시 건축심의위원**</li>\\n<li>**현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원**</li>\\n<li>**현(現) 강동구, 양천구 건축심의위원**</li>\\n<li>**현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원**</li>\\n\\n정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 뼈저리게 목도하고 있는 건축가의 현장 고발이자 생존 전략."
        },
"""

prologue_target = """        {
            "type": "image_full",
            "title": "프롤로그: 우리는 왜 '진짜 설계'를 잃어버렸는가?","""

js_text = js_text.replace(prologue_target, author_profile_js + prologue_target)

# Modify Interlude in JS
old_interlude_part_js = """수주에 눈이 먼 일부 설계사무소들은 \\\"무조건 용적률 최대, 사업성 최대\\\"라는 허황된 청사진으로 조합원들을 현혹한다. 하지만 진정한 전문가의 길은 다르다. 서울시의 행정 기조를 정확히 꿰뚫고, 해당 사업지의 현실적인 사업 방향과 방식을 냉철하게 검토해야 한다."""

new_interlude_part_js = """나는 현재 서울시 건축심의위원이자 각 구의 모아타운 MP(Master Planner)로서, 이 거대한 '행정의 깔때기'가 어떻게 작동하는지 심의장 최전선에서 매일 목도하고 있다. 그렇기에 수주에 눈이 멀어 \\\"무조건 용적률 최대, 사업성 최대\\\"라는 허황된 청사진으로 조합원들을 현혹하는 것이 얼마나 무책임하고 위험한 일인지 누구보다 잘 안다. 진정한 전문가의 길은 다르다. 서울시의 행정 기조를 정확히 꿰뚫고, 해당 사업지의 현실적인 사업 방향과 방식을 냉철하게 검토해야 한다."""

js_text = js_text.replace(old_interlude_part_js, new_interlude_part_js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Author credentials updated successfully.")
