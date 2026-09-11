import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

# 1. 암묵지의 자산화 (Add J-사전 box after the paragraph in Chapter 6)
target_md_1 = "직원 개개인의 역량이나 도덕성에만 의존하는 회사는 반드시 무너진다. 행동을 강제하고, 깔때기(AI)로 스크리닝하여, 회의장에서 뱉는 말 한마디조차 정제된 회사의 '공식 입장'으로 만드는 것. 이것이 15년짜리 지뢰밭에서 설계사무소의 네임 밸류를 지켜내는 우리의 진짜 생존 방식이다."

glossary_1 = """

> **💡 [친절한 J-사전] 암묵지(Tacit Knowledge)의 자산화란?**
> 글이나 매뉴얼로 명확하게 표현하기 힘든, 현장 경험으로 체득한 개인의 직관이나 '감(암묵지)'을 누구나 볼 수 있는 회사의 시스템과 데이터로 바꾸어 영구적으로 보존(자산화)하는 것을 말합니다. J-Hub는 개인의 머릿속에 갇혀 사라질 뻔한 노하우를 회사의 영구적인 지식 자산으로 탈바꿈시켰습니다."""

md_text = md_text.replace(target_md_1, target_md_1 + glossary_1)

# 2. 신통기획 (Add J-사전 box in Interlude)
target_md_2 = "또한 그 틀을 만드는 과정에서 공적인 이익과 사적 이익이 충돌되는 부분을 조율하고, 도시 전체의 흐름과 관리를 하겠다는 뜻이 분명히 느껴지고 있다."

glossary_2 = """

> **💡 [친절한 J-사전] 신통기획(신속통합기획)이란?**
> 서울시가 정비계획 수립 단계에서 공공성과 사업성의 균형을 맞춘 가이드라인을 제시하고, 신속한 사업 추진을 지원하는 공공지원 계획입니다. 복잡한 정비사업을 서울시라는 거대한 플랫폼 안에 녹여내어 관리하겠다는 의지가 담겨 있습니다."""

md_text = md_text.replace(target_md_2, target_md_2 + glossary_2)

# 3. 주동, 일조 사선, 대안(Alts) - Inline replace
md_text = md_text.replace("주동 하나를", "아파트 건물 덩어리(주동) 하나를")
md_text = md_text.replace("북측 일조 사선 제한", "북측 일조 사선(햇빛을 가리지 않기 위해 건물을 깎아내야 하는 건축법적 제한)")
md_text = md_text.replace("일조 사선을 통과", "일조 사선(햇빛을 가리지 않게 건물을 깎는 규제)을 통과")
md_text = md_text.replace("대안(Alts)", "수많은 설계 대안(Alts)")
md_text = md_text.replace("용적률 2% 추가", "용적률(사업성의 핵심이 되는 건축물 총면적 비율) 2% 추가")

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)


with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

js_text = js_text.replace(
    "우리의 진짜 생존 방식이다.",
    "우리의 진짜 생존 방식이다.\\n\\n> **💡 [친절한 J-사전] 암묵지(Tacit Knowledge)의 자산화란?**\\n> 글이나 매뉴얼로 명확하게 표현하기 힘든, 현장 경험으로 체득한 개인의 직관이나 '감(암묵지)'을 누구나 볼 수 있는 회사의 시스템과 데이터로 바꾸어 영구적으로 보존(자산화)하는 것을 말합니다. J-Hub는 개인의 머릿속에 갇혀 사라질 뻔한 노하우를 회사의 영구적인 지식 자산으로 탈바꿈시켰습니다."
)

js_text = js_text.replace(
    "도시 전체의 흐름과 관리를 하겠다는 뜻이 분명히 느껴지고 있다.",
    "도시 전체의 흐름과 관리를 하겠다는 뜻이 분명히 느껴지고 있다.\\n\\n> **💡 [친절한 J-사전] 신통기획(신속통합기획)이란?**\\n> 서울시가 정비계획 수립 단계에서 공공성과 사업성의 균형을 맞춘 가이드라인을 제시하고, 신속한 사업 추진을 지원하는 공공지원 계획입니다. 복잡한 정비사업을 서울시라는 거대한 플랫폼 안에 녹여내어 관리하겠다는 의지가 담겨 있습니다."
)

js_text = js_text.replace("주동 하나를", "아파트 건물 덩어리(주동) 하나를")
js_text = js_text.replace("북측 일조 사선 제한", "북측 일조 사선(햇빛을 가리지 않기 위해 건물을 깎아내야 하는 건축법적 제한)")
js_text = js_text.replace("일조 사선을 통과", "일조 사선(햇빛을 가리지 않게 건물을 깎는 규제)을 통과")
js_text = js_text.replace("대안(Alts)", "수많은 설계 대안(Alts)")
js_text = js_text.replace("용적률 2% 추가", "용적률(사업성의 핵심이 되는 건축물 총면적 비율) 2% 추가")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Glossary injection successful.")
