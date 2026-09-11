import json
import re

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

# 1. Find and extract Epilogue, 마치는 글, and 에피소드 cover
epilogue = None
closing = None

for i, item in enumerate(data):
    title = item.get("title", "")
    if "에필로그" in title:
        epilogue = item
    elif "마치는 글" in title:
        closing = item

# Remove them from array
data = [item for item in data if item is not epilogue and item is not closing and item.get("title") != "에피소드:  쟁이의 마음"]

# 2. Merge 시지프스의 언덕
sisyphus_indices = []
for i, item in enumerate(data):
    if "시지프스의 언덕과 인간다움의 회복" in item.get("title", ""):
        sisyphus_indices.append(i)

if len(sisyphus_indices) >= 3:
    idx1, idx2, idx3 = sisyphus_indices[:3]
    merged_text = (data[idx1].get("text", "") + "\n\n" + 
                   data[idx2].get("text", "") + "\n\n" + 
                   data[idx3].get("text", ""))
    data[idx1]["text"] = merged_text
    # Remove parts 2 and 3
    data.pop(idx3)
    data.pop(idx2)

# 3. Renumber Part 2
part2_chapter = 1
for item in data:
    if item.get("part") == "2부: 철학편":
        title = item.get("title", "")
        # Replace X장. with N장.
        if re.match(r'^\d+장\.', title):
            new_title = re.sub(r'^\d+장\.', f'{part2_chapter}장.', title)
            item["title"] = new_title
            part2_chapter += 1
            
# 4. Append 마치는 글 and 에필로그 to the end
if closing:
    closing["part"] = "에필로그"
    closing["partTitle"] = "여정을 마치며"
    data.append(closing)
if epilogue:
    epilogue["part"] = "에필로그"
    epilogue["partTitle"] = "여정을 마치며"
    data.append(epilogue)

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)

print("Reorder successful!")
