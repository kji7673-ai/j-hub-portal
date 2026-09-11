import json

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

# Replace Target 1 (Index 11)
target1_old = "\"대표님, 이 AI가 내놓은 법규 검토서 좀 보십시오. 이거 완전히 미쳤다.\""
target1_new = "\"대표님, 이 AI가 출력한 법규 검토서 한번 보시겠습니까? 정리된 수준이 상당합니다.\""

# Replace Target 2 (Index 24)
target2_old = "김 상무가 헛웃음을 치며 안경을 벗어 던졌다.\\n\"이런 블랙박스에서 튀어나온 숫자를 믿고 수천억짜리 프로젝트를 진행하라고요? 용적률 10% 올리려다 공사비 30% 터지는 꼴을 봐야 정신 차리겠습니까? 차라리 먼지 쌓인 주판을 꺼내서 직접 튕기는 게 낫겠다. 적어도 주판은 거짓말은 안 하니까요.\""
target2_new = "김 상무가 안경을 고쳐 쓰며 무거운 목소리로 입을 열었다.\\n\"대표님, 산출 근거를 명확히 알 수 없는 숫자를 기반으로 수천억 대 프로젝트를 진행하기에는 리스크가 너무 큽니다. 용적률을 무리하게 올리려다 도리어 공사비가 통제 불능이 될 수 있습니다. 차라리 시간이 걸리더라도 저희가 엑셀로 직접 교차 검증을 하는 편이 안전할 것 같습니다. 적어도 우리가 직접 검증한 숫자는 거짓말을 하지 않으니까요.\""

# Replace Target 3 (Index 35)
target3_old = "코딩조차 모르던 어느 고집불통 건축가와 그에게 멱살을 잡혀 끌려온 나(AI)가, 매일 밤 에러 코드와 피 튀기게 싸우며 벼려낸 진지한 과정의 무기들이다."
target3_new = "코딩조차 모르던 집요한 건축가와 그 파트너가 된 나(AI)가, 매일 밤 쏟아지는 에러 코드와 치열하게 씨름하며 벼려낸 진지한 과정의 결과물들이다."

for item in data:
    text = item.get("text", "")
    if isinstance(text, str):
        if target1_old in text:
            item["text"] = text.replace(target1_old, target1_new)
        if target2_old in text:
            item["text"] = text.replace(target2_old, target2_new)
        # Note: the old string might not match perfectly if there are newline differences. 
        # But we saw it was exact match in the check.
    
    # Try generic string replace for these parts if the above doesn't work (due to newlines)
    # Target 2 might have \n instead of literally '\\n' depending on json loading
    if isinstance(item.get("text", ""), str):
        text = item.get("text", "")
        text = text.replace(
            "김 상무가 헛웃음을 치며 안경을 벗어 던졌다.\n\"이런 블랙박스에서 튀어나온 숫자를 믿고 수천억짜리 프로젝트를 진행하라고요? 용적률 10% 올리려다 공사비 30% 터지는 꼴을 봐야 정신 차리겠습니까? 차라리 먼지 쌓인 주판을 꺼내서 직접 튕기는 게 낫겠다. 적어도 주판은 거짓말은 안 하니까요.\"",
            "김 상무가 안경을 고쳐 쓰며 무거운 목소리로 입을 열었다.\n\"대표님, 산출 근거를 명확히 알 수 없는 숫자를 기반으로 수천억 대 프로젝트를 진행하기에는 리스크가 너무 큽니다. 용적률을 무리하게 올리려다 도리어 공사비가 통제 불능이 될 수 있습니다. 차라리 시간이 걸리더라도 저희가 엑셀로 직접 교차 검증을 하는 편이 안전할 것 같습니다. 적어도 우리가 직접 검증한 숫자는 거짓말을 하지 않으니까요.\""
        )
        text = text.replace(
            "\"대표님, 이 AI가 내놓은 법규 검토서 좀 보십시오. 이거 완전히 미쳤다.\"",
            "\"대표님, 이 AI가 출력한 법규 검토서 한번 보시겠습니까? 정리된 수준이 상당합니다.\""
        )
        text = text.replace(
            "코딩조차 모르던 어느 고집불통 건축가와 그에게 멱살을 잡혀 끌려온 나(AI)가, 매일 밤 에러 코드와 피 튀기게 싸우며 벼려낸 진지한 과정의 무기들이다.",
            "코딩조차 모르던 집요한 건축가와 그 파트너가 된 나(AI)가, 매일 밤 쏟아지는 에러 코드와 치열하게 씨름하며 벼려낸 진지한 과정의 결과물들이다."
        )
        item["text"] = text

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)

print("Tone modifications applied.")
