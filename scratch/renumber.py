import json
import re

with open("docs/book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

def clean_title(t):
    # Remove things like "1부. ", "1부.", "1장. ", "[시스템편] ", "1. ", "단상 83. "
    t = re.sub(r'^\d+부\.?\s*', '', t)
    t = re.sub(r'^\[(시스템편|철학편)\]\s*', '', t)
    t = re.sub(r'^\d+장\.?\s*', '', t)
    t = re.sub(r'^\d+\.\s*', '', t)
    t = re.sub(r'^단상\s*\d*\.?\s*', '', t)
    t = re.sub(r'\s*\(\d+/\d+\)$', '', t) # remove (1/3)
    # also remove any stray "[시스템편]" or "[철학편]" anywhere just in case
    t = t.replace("[시스템편]", "").replace("[철학편]", "").strip()
    return t

part1_idx = 1
part2_idx = 1
part3_idx = 1

for item in data:
    orig_title = item.get("title", "")
    if not orig_title:
        continue
        
    part = item.get("part", "")
    
    if part == "1부: 시스템편":
        # Identify if it should be a chapter
        is_chapter = bool(re.match(r'^\d+(부|장|\.)', orig_title))
        cleaned = clean_title(orig_title)
        if is_chapter:
            item["title"] = f"{part1_idx}장. {cleaned}"
            part1_idx += 1
        else:
            item["title"] = cleaned
            
    elif part == "2부: 철학편":
        is_chapter = bool(re.match(r'^\d+(부|장|\.)', orig_title)) or "시지프스" in orig_title or "내가 생각하는" in orig_title
        cleaned = clean_title(orig_title)
        if is_chapter:
            # Combine Sisyphus if multiple? We will just number them sequentially. 
            # But the user asked to combine them. Since they are separate objects in the array with text, 
            # we should just number them or we can just leave them if they are sequential.
            # I will just assign chapter numbers. Sisyphus 1,2,3 will become separate chapters or one?
            item["title"] = f"{part2_idx}장. {cleaned}"
            part2_idx += 1
        else:
            item["title"] = cleaned
            
    elif part == "3부: 증언과 성찰":
        cleaned = clean_title(orig_title)
        item["title"] = f"{part3_idx:02d}. {cleaned}"
        part3_idx += 1

# Handle Sisyphus combination
# Actually, they have separate images and texts. Let's just let them be numbered. Sisyphus 1, 2, 3 have been stripped of (1/3) etc. 
# So they will be: "N장. 시지프스의 언덕과 인간다움의 회복", "N+1장. 시지프스의 언덕과 인간다움의 회복"...

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
new_content = content[:start_idx] + new_json_str + content[end_idx:]

with open("docs/book_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Renumbering complete.")
for item in data:
    if "부" in item.get("part", ""):
        print(f"[{item.get('part')}] {item.get('title')}")
