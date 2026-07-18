import re

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/articles.js', 'r', encoding='utf-8') as f:
    content = f.read()

# The specific string to remove
target_str = "결과적으로, 이 사안을 어떻게 선제적으로 실무에 적용하고 기회로 만드느냐가 향후 업계에서의 독보적인 위치를 점하는 열쇠가 될 것입니다. 본 원문에서는 이와 관련된 세부적인 통계 지표와 구체적인 대응 가이드라인, 그리고 전문가들의 다각적인 시각을 10가지 항목으로 정리하여 제공합니다."

# Replace it with something more natural, or just remove it.
# The user said: "오히려 이 문장을 삭제하고 본문의 내용을 조금 더 보여주는 게 나을 것 같습니다."
# Let's replace it with a more diverse set of concluding thoughts or just strip it.
# Actually, since it's mock data, let's just strip it, and if it becomes too short, add a generic but context-aware mock sentence.
# Or better, just strip it for now.

new_content = content.replace("<br><br>" + target_str, "")
new_content = new_content.replace(target_str, "")

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/articles.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Removed repetitive sentence.")
