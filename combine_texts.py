import os
import re

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/master_manuscript_v2.md', 'r', encoding='utf-8') as f:
    v2_text = f.read()

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/new_text.md', 'r', encoding='utf-8') as f:
    new_text = f.read()

# In v2_text, we change:
# "# 1부." -> "# 1부. [시스템편]"
v2_text = v2_text.replace('# 1부. 우리는 왜 설계하지 못하는가?', '# 1부. [시스템편] 우리는 왜 설계하지 못하는가?')
v2_text = v2_text.replace('# 2부. AI라는 환각의 숲을 지나다', '# 2부. [시스템편] AI라는 환각의 숲을 지나다')
v2_text = v2_text.replace('# 3부. [구축과 증명]', '# 3부. [시스템편]')
v2_text = v2_text.replace('# 4부. [완성]', '# 4부. [시스템편]')
v2_text = v2_text.replace('## 10장. 에필로그', '## [시스템편] 에필로그')

# In new_text, we change:
# "# 제1부:" -> "# 5부. [철학편]"
new_text = new_text.replace('# 제1부: 설계를 대하는 우리의 태도', '# 5부. [철학편] 설계를 대하는 우리의 태도')
new_text = new_text.replace('# 제2부: 형태와 공간의 미학', '# 6부. [철학편] 형태와 공간의 미학')
new_text = new_text.replace('# 제3부: 건축이 세상과 관계 맺는 법', '# 7부. [철학편] 건축이 세상과 관계 맺는 법')
new_text = new_text.replace('# 에필로그 (Epilogue)', '# [철학편] 에필로그 (Epilogue)')

# Also, the new text has its own prologue. 
# We can change it to: "# [철학편] 프롤로그"
new_text = new_text.replace('# 프롤로그 (Prologue)', '# [철학편] 프롤로그 (Prologue)')

combined_text = v2_text + "\n\n---\n\n" + new_text

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/master_manuscript_v3.md', 'w', encoding='utf-8') as f:
    f.write(combined_text)

print("Combined successfully to master_manuscript_v3.md")
