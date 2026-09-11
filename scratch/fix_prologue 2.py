import json

with open("docs/book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

for item in data:
    if "프롤로그" in item.get("title", ""):
        # Change type from image_full to split (half image, half text)
        item["type"] = "split"
        # We can also add a nice title inside the text or just let it render.
        # Let's add paragraph tags for better formatting and readability.
        
        text = """<p style="font-size: 1.1em; line-height: 1.8; margin-bottom: 24px;">안녕하세요. 도면 위에서, 그리고 거친 현장에서 26년째 구르고 있는 평범한 건축 쟁이입니다.</p>

<p style="margin-bottom: 24px;">처음 이 기록을 엮기로 마음먹었을 때, 참 많은 망설임이 있었습니다. 시중에는 이미 AI와 혁신을 다루는 훌륭한 전문가들의 책이 차고 넘치기 때문입니다. 하지만 용기를 내어 이 부끄러운 기록을 세상에 꺼내놓는 이유는 단 하나입니다. 이 책은 'AI로 이렇게 성공했다'를 자랑하기 위한 매뉴얼이 아니라, <strong style="color: var(--primary);">서류 더미에 파묻혀 '진짜 설계'를 잃어버릴 뻔했던 한 건축가의 처절한 생존기</strong>이기 때문입니다.</p>

<p style="margin-bottom: 24px;">언제부터인가 우리는 선을 긋고 공간을 상상하는 시간보다, 엑셀 칸을 채우고 심의 서류를 넘기며 해명하는 데 더 많은 밤을 지새우게 되었습니다. 이러다가는 정말 건축이 서류로만 남는 '페이퍼 아키텍처'가 되어버릴 것 같다는 두려움이 엄습했습니다.</p>

<p style="margin-bottom: 24px;">제가 '아키 시냅스(Archisynapse)'와 같은 AI 시스템을 필사적으로 구축했던 이유는 기술이 좋아서가 아니었습니다. 기계가 할 수 있는 차가운 일들은 기계에게 모두 넘겨주고, <strong style="color: var(--primary);">우리 인간만이 할 수 있는 '따뜻한 본질'로 다시 돌아가기 위한 몸부림</strong>이었습니다.</p>

<p style="margin-bottom: 24px;">이 책은 다소 불친절하고 이질적인 세 가지 이야기로 구성되어 있습니다.<br>독자 여러분께 이 책을 어떻게 읽어주십사 하는 작은 <strong>안내(Guide)</strong>를 덧붙입니다.</p>

<ul style="margin-bottom: 24px; padding-left: 20px; line-height: 1.7;">
  <li style="margin-bottom: 12px;"><strong>1부 [시스템편]</strong> 은 쏟아지는 업무의 과부하 속에서 살아남기 위해 발버둥 치며 만들어낸 '도구'에 대한 기록입니다. 행정적 늪에 빠져 허우적대는 실무자나 경영진이 계신다면, 이 파트가 작은 돌파구가 되기를 바랍니다.</li>
  <li style="margin-bottom: 12px;"><strong>2부 [철학편]</strong> 은 그렇게 얻어낸 귀중한 시간 동안, 다시 도면 앞에 앉아 치열하게 고민했던 '건축의 본질'에 대한 이야기입니다. 완벽한 AI의 연산 앞에서도, 결국 여백을 남기고 주변에 순응하는 '불완전한 선택'은 우리 인간의 몫이어야 함을 담았습니다.</li>
  <li style="margin-bottom: 12px;"><strong>3부 [증언과 성찰]</strong> 은 화려한 시스템과 거창한 철학 뒤에 숨겨진, 한 명의 쟁이로서 느꼈던 찌질하고도 솔직한 감정의 파편들입니다. 찢어진 운동화, 억지스러운 타협, 텅 빈 도면 앞에서의 외로움 등 날것의 일기를 그대로 남겨두었습니다.</li>
</ul>

<p style="margin-bottom: 24px;">기술 서적을 기대하셨다면 3부의 감정이 낯설게 느껴지실 수도, 에세이를 기대하셨다면 1부의 시스템이 딱딱하게 느껴지실 수도 있습니다. 하지만 이 모든 모순된 파편들이 모여야만 '건축'이라는 거대한 유기체가 굴러간다는 사실을, 현장에 계신 분들이라면 깊이 공감해 주시리라 믿습니다.</p>

<p style="margin-bottom: 24px;">단 한 분에게라도, 이 부족하고 투박한 기록이 무거운 일상을 버텨내는 작은 위로이자 내일을 그릴 수 있는 실용적인 도구가 되기를 진심으로 바랍니다.</p>

<p style="font-weight: 600; text-align: right; margin-top: 40px; font-size: 1.1em; color: var(--primary);">도면 위에 머무는 우리의 시간이 다시 온전히 우리의 것이 되기를 기원하며.</p>"""
        
        item["text"] = text
        break

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
new_content = content[:start_idx] + new_json_str + content[end_idx:]

with open("docs/book_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated prologue formatting and layout type in book_data.js")
