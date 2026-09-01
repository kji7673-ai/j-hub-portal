import json
import re

with open('book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Instead of parsing the whole JSON (which might be complicated by the JS variable declaration),
# I can just use basic string replacement since the strings are very specific.

# 1. Prologue Rewrite
old_prologue = "우리는 '진짜 설계'를 잃어버리고 있었다."
new_prologue = "우리는 '진짜 설계'를 잃어버리고 있었다. 아니, 솔직해지자. 대한민국의 수많은 건축사사무소들은 거대한 착각에 빠져 있다. '건축은 장인정신'이라는 낭만적인 이름표를 달고, 정작 19세기의 아날로그 방식으로 21세기의 클라이언트를 상대하려 든다. 우리는 왜 수백억 원의 자산을 다루는 '전략적 비즈니스 파트너'에서, 관청의 서류를 대행해 주는 '을(乙)'로 스스로를 전락시켰는가?"

# 2. Chapter 5 Rewrite
old_ch5 = """건축주나 조합장 입장에서는 답답할 노릇이다. 내 재산이 어떻게 쪼개지고 어떤 방식으로 개발해야 가장 이득인지 정확한 데이터(Data)를 원하는데, 돌아오는 대답은 \\\"일단 설계 계약부터 하시면 자세히 풀어드리겠습니다\\\"라는 식의 막연한 구애뿐이었다. 신뢰가 생길 리 만무했다."""
new_ch5 = """건축주나 조합장 입장에서는 기가 찰 노릇이다. 수천억 원의 자산이 걸린 의사결정을 '감'과 '엑셀'에 의존하는 것은 클라이언트에 대한 기만이다. 수주를 위해 무료 서비스로 던져주는 한 장짜리 개요서 관행이 결국 우리 건축가들의 권위와 단가를 어떻게 스스로 갉아먹고 있는지 직시해야 한다. 데이터 없는 제안에 신뢰가 생길 리 만무했다."""

# 3. Chapter 6 Rewrite
old_ch6 = """우리는 지식의 '병목 현상'을 깨부숴야만 했다. 고연차 소장의 머릿속에만 존재하는 파편화된 실무 지식을 밖으로 끄집어내어, 신입사원도 즉각적으로 활용할 수 있는 '회사의 자산'으로 만들어야 했다."""
new_ch6 = """에이스 직원이 퇴사할 때마다 회사의 20년 치 경쟁력도 함께 리셋되는 참담한 현실을 언제까지 방관할 것인가? 도제식 교육을 핑계로 고연차 소장의 머릿속에만 갇혀 있는 암묵적 경험은 결코 회사의 자산이 될 수 없다. 지식을 시스템에 귀속시키지 못하는 조직에게 미래는 없다. 우리는 지식의 '병목 현상'을 깨부수고, 신입사원도 즉각적으로 활용할 수 있는 '영구적인 자산'으로 만들어야 했다."""

# 4. Epilogue Rewrite
old_epilogue = "거창한 개발비나 막막함에 주저할 필요는 없다."
new_epilogue = "이 책은 단순한 진양건축의 성공담이 아니다. 아날로그의 낭만에 취해 데이터와 기술(IT)을 내재화하지 못한 설계사무소는, 결국 거대 플랫폼과 테크 기업의 도면을 대신 그려주는 하청업체로 전락하고 말 것이라는 서늘한 경고장이자 생존의 로드맵이다. 거창한 개발비나 막막함에 주저할 시간이 없다."

content = content.replace(old_prologue, new_prologue)
content = content.replace(old_ch5, new_ch5)
content = content.replace(old_ch6, new_ch6)
content = content.replace(old_epilogue, new_epilogue)

with open('book_data.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced strings successfully using text replacement.")
