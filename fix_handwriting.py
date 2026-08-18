import re

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix pattern 1:
# <div style=\"background-color: var(--canvas-parchment); ... border-left: 4px solid var(--primary);\">
pattern1 = r'(<div style=\\"background-color: var\(--canvas-parchment\);[^>]*?border-left: 4px solid var\(--primary\);\\")>'
replacement1 = r'\1 class=\"handwriting\">'
content = re.sub(pattern1, replacement1, content)

# Fix pattern 2: 
# <div class=\"handwriting\" style=\"margin-top: 10px;\">[AI와의 대화]</h4>
# Change it to <h4>[AI와의 대화]</h4>
pattern2 = r'<div class=\\"handwriting\\" style=\\"margin-top: 10px;\\">(\[AI와의 대화\])</h4>'
replacement2 = r'\1</h4>'
content = re.sub(pattern2, replacement2, content)

# Fix pattern 3:
# <b><div class=\"handwriting\" style=\"margin-top: 10px;\">[AI와의 대화]</b><br>
# Change it to <div class=\"handwriting\" style=\"margin-top: 10px;\"><b>[AI와의 대화]</b><br>
pattern3 = r'<b><div class=\\"handwriting\\" style=\\"margin-top: 10px;\\">(\[AI와의 대화\])</b><br>'
replacement3 = r'<div class=\"handwriting\" style=\"margin-top: 10px;\"><b>\1</b><br>'
content = re.sub(pattern3, replacement3, content)

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied handwriting fixes.")
