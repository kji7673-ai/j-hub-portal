import json

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

front = data[:28]
body = data[28:84]
tail = data[84:]

out = []
for item in front:
    out.append(item)
    t = item.get('title', '')
    if t is None:
        t = ''
    if '2장. 엑셀과 서류에 짓눌린 건축가들' in t:
        out.extend(body[0:5])
    elif '4장. "어디서 이렇게 불완전한 데이터를 가져왔어?"' in t:
        out.extend(body[5:9])
    elif '7장. 통찰력을 시스템화하다' in t:
        out.extend(body[9:25])
    elif '8장. [Case 1]' in t:
        out.append(body[55])
        out.extend(body[25:40])
    elif '9장. [Case 2]' in t:
        out.extend(body[40:45])
    elif '10장. [Case 3]' in t:
        out.extend(body[45:47])
    elif '회의록 자동화와 노이즈 필터링' in t:
        out.append(body[47])
    elif '11장. 엔터프라이즈 엘레강스' in t:
        out.extend(body[48:55])

out.extend(tail)

if len(out) != len(data):
    print(f"Error: Length mismatch! Expected {len(data)}, got {len(out)}")
else:
    print(f"Success! Length matched: {len(out)}")

new_json_str = json.dumps(out, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)
