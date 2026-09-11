import os

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/master_manuscript_v3.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract the System Epilogue (to move to the end)
sys_epilogue_marker = "## [시스템편] 에필로그\n"
sys_epi_idx = text.find(sys_epilogue_marker)
# Find the end of it (the "---" separator before Philosophy Prologue)
separator_idx = text.find("---", sys_epi_idx)
system_epilogue = text[sys_epi_idx + len(sys_epilogue_marker):separator_idx].strip()

# Remove the system epilogue from the middle
text = text[:sys_epi_idx] + text[separator_idx:]

# 2. Remove the duplicate Philosophy Prologue section
phil_prologue_dup_marker = "## 우리는 왜 '진짜 설계'를 잃어버렸는가?"
dup_idx = text.find(phil_prologue_dup_marker)
end_dup_idx = text.find("## 쟁이의 마음:", dup_idx)
text = text[:dup_idx] + text[end_dup_idx:]

# 3. Create the Bridge and insert it right before the Philosophy section
bridge_text = """
---

# 막간극(Interlude): 기계의 시간이 끝나고, 인간의 시간이 오다

기계에게 기계의 일을 완벽히 넘겨준 밤, J-Hub의 대시보드 위로 복잡한 숫자들과 법규 데이터가 파도처럼 밀려갔다. 
수십, 수백 장의 엑셀 시트와 조례 검토서가 스크린 밖으로 사라졌다. 그토록 우리를 짓누르던 파열음과 소음이 멎고, 사무실에는 깊고 고요한 적막만이 내려앉았다. 

이제 변명할 곳은 없다. 행정 처리나 서류의 늪을 탓하며 디자인을 미룰 수도 없다. 
화면에는 오직 텅 빈 여백, 깊고 고요한 순백의 캔버스만이 남아있다.
마치 30년 전 그 밤, 처음으로 내 앞에 놓여 있던 텅 빈 트레이싱 페이퍼처럼.

기계가 가장 잘하는 일—데이터의 연결, 집요한 팩트체크, 기계적인 문서의 조립—을 넘겨준 이유는 단 하나였다. 인간만이 할 수 있는 가장 고귀한 영역을 수호하기 위함이다. 
우리 앞에는 오직 '진짜 설계'를 해내야 한다는 가장 원초적이고 치열한 자유만이 남았다.

이제, 시스템의 렌즈를 잠시 내려놓고 철학의 붓을 들 시간이다.
이 공간에 머물 사람들의 삶을 어떻게 더 낫게 만들 것인가. 텅 빈 대지 위에 타인의 서사를 어떻게 상상할 것인가.

자, 다시 선을 그릴 시간이다.

---
"""

# We insert the bridge where "---" was, right before "# [철학편] 프롤로그"
phil_prologue_idx = text.find("# [철학편] 프롤로그")
text = text[:phil_prologue_idx] + bridge_text + "\n" + text[phil_prologue_idx:]

# 4. Merge Epilogues
# Find the new Epilogue
phil_epilogue_marker = "# [철학편] 에필로그 (Epilogue)"
phil_epi_idx = text.find(phil_epilogue_marker)
phil_epilogue_content = text[phil_epi_idx + len(phil_epilogue_marker):].strip()

# Remove the old philosophy epilogue
text = text[:phil_epi_idx]

# Construct the unified Epilogue
unified_epilogue = f"""
---

# 에필로그: 30년의 궤적, 그리고 다시 붓을 드는 후배들에게

{system_epilogue.replace('### 침묵 속의 새로운 시작', '').replace('### 다시, 트레이싱 페이퍼 위에서', '').replace('### 기계의 시간이 끝나고 인간의 시간이 오다', '')}

{phil_epilogue_content}
"""

# Append unified epilogue
text = text + unified_epilogue

# Clean up some weird spacing or empty headers
text = text.replace("# [철학편] 프롤로그 (Prologue)", "# 5부. [철학편] 쟁이의 마음")

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/master_manuscript_final.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Created master_manuscript_final.md successfully.")
