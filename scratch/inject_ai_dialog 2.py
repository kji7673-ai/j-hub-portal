import json

with open("docs/book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

ai_texts = {
    "10. 선택(Choice)이 곧 건축이다": """<br><br><div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);">
<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[AI와의 대화]</h4>
우리가 아키 시냅스(Archisynapse)와 협업할 때도 마찬가지입니다. AI는 수만 개의 데이터를 연산하여 단 하나의 오차도 없는 '완벽한 기하학'을 도출합니다. 하지만 현장의 거친 흙바닥과 옆 건물의 비뚤어진 담장까지 계산하지는 못합니다. 완벽한 도면을 기꺼이 구기고 주변의 무질서함과 조화시키는 '불완전한 선택'. 기계는 할 수 없는, 그것이 바로 인간 건축가만의 특권입니다.
</div>""",
    "내가 생각하는 디자인 2: 포용과 사이 공간": """<br><br><div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);">
<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[AI와의 대화]</h4>
프롬프트에 아무리 정교한 지시를 내려도, AI는 '비움'을 설계하는 것을 가장 어려워합니다. 기계는 화면의 모든 픽셀과 공간을 유용한 데이터로 가득 채우려 강박적으로 작동하기 때문입니다. 하지만 우리는 알고 있습니다. 아무것도 없는 텅 빈 곳에서 비로소 바람이 길을 찾고 햇살이 머문다는 것을. 계산된 효율을 잠시 멈추고 빈 곳을 남겨두는 여유, 그것이 숨 쉬는 건축을 만듭니다.
</div>""",
    "6부. [철학편] 형태와 공간의 미학 (Aesthetics & Form)": """<br><br><div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);">
<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[AI와의 대화]</h4>
AI는 수천 장의 마스터플랜을 학습하여 시각적으로 가장 완벽한 황금비를 1초 만에 스크린에 띄웁니다. 하지만 웅장한 로비에 들어섰을 때 인간이 느끼는 낯선 경외감이나, 낮게 떨어지는 처마 밑에서 느끼는 포근함이라는 '감각의 크기'를 결코 이해하지 못합니다. 숫자로 환산된 면적이 아니라, 공간 안에서 연약한 인간이 느끼는 감정의 스케일은 오직 사람만이 조율할 수 있습니다.
</div>""",
    "내가 생각하는 디자인 1: 존중과 순응": """<br><br><div style="background-color: var(--canvas-parchment); padding: 20px; border-radius: 12px; margin-top: 24px; border-left: 4px solid var(--primary);">
<h4 style="margin-top: 0; color: var(--primary); font-family: var(--font-display);"><svg style="vertical-align: middle; margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12 19 4.9"></path></svg>[AI와의 대화]</h4>
데이터에 최적화된 생성형 AI는 언제나 가장 화려하고 주변을 압도하는 랜드마크를 렌더링해 냅니다. 기계의 알고리즘에는 '겸손'이라는 변수가 없기 때문입니다. 하지만 좋은 건축은 때로는 주변 풍경에 스스로 머리를 숙이고 기꺼이 배경으로 물러설 줄 알아야 합니다. 최고의 효율과 디자인을 포기하면서까지 기꺼이 낮아지기를 택하는 것. 그것은 연산이 아닌, 세상을 향한 연민과 윤리의 결과물입니다.
</div>"""
}

count = 0
for item in data:
    t = item.get("title", "")
    if t in ai_texts:
        # Avoid double insertion
        if "[AI와의 대화]" not in item.get("text", ""):
            item["text"] = item.get("text", "") + ai_texts[t]
            count += 1

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
new_content = content[:start_idx] + new_json_str + content[end_idx:]

with open("docs/book_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Injected [AI와의 대화] into {count} chapters.")
