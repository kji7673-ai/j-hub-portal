import os

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()
    
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# 1. Fix the quote about '구청 행정실'
# MD
md_old_quote = '"대표님, 제가 건축을 하러 온 건지, 구청 행정실에 취업을 한 건지 모르겠습니다. 건축이 언제부터 이렇게 지독한 행정 서류 작업이 되었습니까?"'
md_new_quote = '"대표님, 제가 건축을 하러 온 건지, ppt 작업과 실현되지도 않는 계획안만 만들러 온 건지 모르겠습니다. 내가 건축을 하고 있다는 이유 하나만으로 존중받기보다는 그저 \'을\'로 취급받는 현실이 너무나도 어렵습니다."'
md_text = md_text.replace(md_old_quote, md_new_quote)

# JS
js_old_quote = '"대표님, 제가 건축을 하러 온 건지, 구청 행정실에 취업을 한 건지 모르겠습니다. 하루 종일 서류만 만지다 보니 연차는 쌓여가는데, 정작 제 손으로 도면 한 장 제대로 쳐본 적이 없습니다. 실현되지도 않을 서류 더미 속에서, 영원히 종이 위에서만 건물을 짓는 \'페이퍼 아키텍트\'로 남을까 봐 두렵습니다."'
js_new_quote = '"대표님, 제가 건축을 하러 온 건지, ppt 작업과 실현되지도 않는 계획안만 만들러 온 건지 모르겠습니다. 내가 건축을 하고 있다는 이유 하나만으로 존중받기보다는 그저 \'을\'로 취급받는 현실이 너무나도 어렵습니다. 영원히 종이 위에서만 건물을 짓는 \'페이퍼 아키텍트\'로 남을까 봐 두렵습니다."'
js_text = js_text.replace(js_old_quote, js_new_quote)

# 2. Fix spelling '결괏값' -> '결과값'
md_text = md_text.replace('결괏값', '결과값')
js_text = js_text.replace('결괏값', '결과값')

# 3. Change title "우리의 '잘생김'은 매혹적인 도면과 보고서다"
old_title = "우리의 '잘생김'은 매혹적인 도면과 보고서다"
new_title = "전문가의 자존심은 완벽한 도면과 데이터에서 나온다"
md_text = md_text.replace(old_title, new_title)
js_text = js_text.replace(old_title, new_title)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Text replacements completed.")
