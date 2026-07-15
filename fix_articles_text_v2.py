import json
import re
import random

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/articles.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract JSON data
match = re.search(r'const articlesData = (\[.*?\]);', content, re.DOTALL)
if match:
    data_str = match.group(1)
    
    # Simple eval replacing logic to parse the js object since it's just JSON-like
    # It might have unquoted keys or trailing commas. Fortunately, the previous script generated clean JSON.
    try:
        articles = json.loads(data_str)
    except json.JSONDecodeError:
        print("Could not parse JSON. Attempting manual replacement.")
        articles = []
        
    if articles:
        # Generate some mock "main content" sentences
        mock_contents = {
            "건축": [
                "최근 서울시 건축심의 위원회에서는 입면의 다양화와 공공 보행통로 확보를 조건으로 용적률 인센티브를 부여하는 방안을 적극 검토 중입니다.",
                "특히, 지하 주차장 램프 구간의 유효폭원 산정 시, 곡선부의 추가 확폭을 엄격히 적용하는 사례가 늘고 있어 초기 계획 단계에서 각별한 주의가 요구됩니다."
            ],
            "도시": [
                "모아타운 및 소규모 정비사업 지침에 따르면, 노후도 산정 방식이 일부 완화되어 그동안 사업 추진이 지연되었던 2종 일반주거지역의 활로가 열릴 것으로 기대됩니다.",
                "다만, 기반시설 확보 비율에 따른 기부채납 산정 공식이 지자체별로 상이하게 적용되고 있어, 사업지 관할 구역의 조례를 최우선으로 교차 검증해야 합니다."
            ],
            "법규": [
                "개정된 주택법 시행령에 따라, 리모델링 조합 설립 시 필요한 동의율 요건이 세분화되었으며, 안전진단 등급 산정 기준 역시 구조 안전성 비중이 조정되었습니다.",
                "교육환경평가와 관련하여, 일조권 시뮬레이션의 기준일과 시간대가 동지 기준으로 명확히 고정됨에 따라, 배치안 작성 시 인접 학교와의 이격 거리를 재산정해야 할 수 있습니다."
            ],
            "ESG": [
                "제로에너지건축물(ZEB) 인증 의무화 로드맵이 민간 아파트로 확대 적용됨에 따라, 패시브 설계 기법 도입과 신재생 에너지 설비 비율 맞추기가 공사비 상승의 주요 원인으로 지목되고 있습니다.",
                "친환경 자재 사용 비율에 따른 취득세 감면 혜택이 연장될 가능성이 높으나, 증빙 서류의 요건이 한층 강화되어 시공사와의 긴밀한 데이터 공유가 필수적입니다."
            ]
        }
        
        default_contents = [
            "사업성 분석 시, 최근 급격히 상승한 건설 공사비 지수를 반영하여 예비비를 기존 대비 15% 이상 보수적으로 책정하는 가이드라인이 배포되었습니다.",
            "이와 함께, 도급 계약서 작성 시 물가 변동으로 인한 계약 금액 조정(Escalation) 조항을 발주처와 시공사 양측이 명확히 합의하는 것이 분쟁 예방의 핵심입니다."
        ]
        
        for article in articles:
            cat = article.get("category", "")
            
            # Select 2 random sentences based on category
            pool = default_contents
            if "건축" in cat or "설계" in cat: pool = mock_contents["건축"]
            elif "도시" in cat or "정비" in cat or "복합" in cat: pool = mock_contents["도시"]
            elif "정책" in cat or "법규" in cat or "인허가" in cat: pool = mock_contents["법규"]
            elif "ESG" in cat or "친환경" in cat: pool = mock_contents["ESG"]
            
            added_content = random.choice(pool) + " " + random.choice(default_contents)
            
            # If excerpt ends with <br><br>, append directly, else add <br><br>
            excerpt = article.get("excerpt", "")
            if "<br><br>" not in excerpt:
                excerpt += "<br><br>"
            else:
                excerpt += "<br><br>"
                
            article["excerpt"] = excerpt + added_content
            
        new_data_str = json.dumps(articles, ensure_ascii=False, indent=4)
        new_content = content.replace(data_str, new_data_str)
        
        with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/articles.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated articles with richer main content.")
