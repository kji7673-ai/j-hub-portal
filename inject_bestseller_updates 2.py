import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# 1. Update Titles in MD
old_md_title = "# 📘 프롤로그: 우리는 왜 '진짜 설계'를 잃어버렸는가?"
new_md_title = """# 📖 《여백을 설계하는 자가 살아남는다》
### 기계의 연산이 끝난 곳에서 시작되는 인간의 위대한 통찰

---

# 📘 프롤로그: 우리는 왜 '진짜 설계'를 잃어버렸는가?"""
md_text = md_text.replace(old_md_title, new_md_title)

# 2. Add Checklist to MD
md_checklist = """
---

### 4. 독자를 위한 실전 가이드: 내 조직에 '투명한 유리상자' 도입하기 (자가 진단 체크리스트)

이 책의 철학을 건축사사무소뿐만 아니라 법률, 의료, 회계, 기획 등 모든 지식 서비스 조직에 적용하기 위한 5가지 핵심 체크리스트입니다. 우리 조직은 AI의 블랙박스에 잡아먹히고 있습니까, 아니면 AI를 지휘하고 있습니까?

1. **[  ] 프로세스의 분해**: 현재 직원들이 챗GPT 등 대화형 AI에 던지는 질문을, 단계별(Step-by-step) 모듈로 분해할 수 있는가?
2. **[  ] 인간의 통제권 (유리상자)**: AI가 도출한 데이터(결과값)를 인간 전문가가 중간에 개입하여 '필터링'하고 '승인'하는 교차 검증(Red Team) 단계가 존재하는가?
3. **[  ] 암묵지의 자산화**: 에이스 직원의 퇴사와 함께 사라지는 노하우를, 누구나 접근할 수 있는 사내 플랫폼(J-Edu 형태)에 영구적인 자산으로 쌓아두고 있는가?
4. **[  ] 권위의 시각화**: 기계가 찾아낸 완벽한 데이터를 클라이언트나 경영진에게 제시할 때, 조악한 엑셀이 아닌 직관적이고 아름다운 UI/UX로 포장하여 신뢰를 얻어내고 있는가?
5. **[  ] 전문가의 철학**: 기계적인 연산과 서류 작업을 AI에게 넘긴 후, 우리의 직원들은 '가치 판단'과 '철학적 고민'이라는 본연의 임무로 돌아갔는가?
"""

# Append to the very end of MD
md_text = md_text + md_checklist

# 3. Update Titles in JS
js_text = js_text.replace('"title": "공유결합"', '"title": "여백을 설계하는 자가 살아남는다"')
js_text = js_text.replace('"subtitle": "아키 시냅스, 건축과 AI가 연결되는 순간"', '"subtitle": "기계의 연산이 끝난 곳에서 시작되는 인간의 위대한 통찰"')

# 4. Add Checklist Page to JS
js_checklist_page = """        },
        {
            "type": "text_only",
            "title": "[부록] 자가 진단 체크리스트",
            "text": "이 책의 철학을 건축사사무소뿐만 아니라 법률, 의료, 회계, 기획 등 모든 지식 서비스 조직에 적용하기 위한 5가지 핵심 체크리스트입니다. 우리 조직은 AI의 블랙박스에 잡아먹히고 있습니까, 아니면 AI를 지휘하고 있습니까?\\n\\n1. **프로세스의 분해**: 현재 직원들이 챗GPT 등 대화형 AI에 던지는 질문을, 단계별(Step-by-step) 모듈로 분해할 수 있는가?\\n2. **인간의 통제권 (유리상자)**: AI가 도출한 데이터(결과값)를 인간 전문가가 중간에 개입하여 '필터링'하고 '승인'하는 교차 검증(Red Team) 단계가 존재하는가?\\n3. **암묵지의 자산화**: 에이스 직원의 퇴사와 함께 사라지는 노하우를, 누구나 접근할 수 있는 사내 플랫폼(J-Edu 형태)에 영구적인 자산으로 쌓아두고 있는가?\\n4. **권위의 시각화**: 기계가 찾아낸 완벽한 데이터를 클라이언트나 경영진에게 제시할 때, 조악한 엑셀이 아닌 직관적이고 아름다운 UI/UX로 포장하여 신뢰를 얻어내고 있는가?\\n5. **전문가의 철학**: 기계적인 연산과 서류 작업을 AI에게 넘긴 후, 우리의 직원들은 '가치 판단'과 '철학적 고민'이라는 본연의 임무로 돌아갔는가?"
        }
    ]
};"""

# Replace the closing brackets of JS array with the new checklist page
js_text = js_text.replace("""        }
    ]
};""", js_checklist_page)
# Just in case there is a trailing newline
js_text = js_text.replace("""        }
    ]
};
""", js_checklist_page + "\n")

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Insertion of title and checklist successful.")
