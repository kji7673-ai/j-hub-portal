import json

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

# 1. Fix typos
for item in data:
    if 'text' in item:
        text = item['text']
        if isinstance(text, list):
            text = '\n'.join(text)
        
        # 30년 -> 26년
        text = text.replace('30년 전', '26년 전')
        text = text.replace('30년이 지난', '26년이 지난')
        text = text.replace('30년 건축 인생', '26년 건축 인생')
        text = text.replace('30년 차 소장', '26년 차 소장')
        text = text.replace('30년 차 대표', '26년 차 대표')
        text = text.replace('30년의 경험치', '26년의 경험치')
        text = text.replace('30년 차 경영자', '26년 차 경영자')
        
        # UI -> AI
        text = text.replace('숏폼 UI', '숏폼 AI')
        
        # Remove leftover comments
        text = text.replace('<br>*(첨부해주신 용역원실 이미지가 이곳에 어울립니다.)*', '')
        text = text.replace('*(첨부해주신 용역원실 이미지가 이곳에 어울립니다.)*', '')
        
        if isinstance(item['text'], list):
            item['text'] = text.split('\n')
        else:
            item['text'] = text

# 2. Add images
out_data = []
for item in data:
    title = item.get('title', '')
    
    if title == '02. 찢어진 운동화':
        out_data.append({"type": "image_full", "image": "static/images/sketch_essay_sneakers_1786666695957.jpg"})
    elif title == '18. 삼켜낸 말과 술 한 잔':
        out_data.append({"type": "image_full", "image": "static/images/sketch_essay_drinks_1786666913149.jpg"})
    elif title == '32. 외로움':
        out_data.append({"type": "image_full", "image": "static/images/solitary_architect_desk.jpg"})
    
    out_data.append(item)
    
    # Sisyphus is not in the title, it's in the text. Let's check text
    if 'text' in item:
        t = item['text']
        if isinstance(t, list): t = '\n'.join(t)
        if '시지프스' in t and '물방울' in t:
            out_data.append({"type": "image_full", "image": "static/images/sketch_sisyphus_1786667026066.jpg"})

new_json_str = json.dumps(out_data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)
