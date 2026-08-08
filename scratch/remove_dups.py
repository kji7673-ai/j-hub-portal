import json
import re

with open("book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(const bookData = )(\[.*\]);", content, re.DOTALL)
if match:
    prefix = match.group(1)
    json_str = match.group(2)
    
    data = json.loads(json_str)
    
    seen = {}
    
    for chapter in data:
        # Keep track of unique pages in this chapter
        unique_pages = []
        for page in chapter.get("pages", []):
            text = page.get("text", "").strip()
            
            # If no text, keep it (might be an image-only page)
            if not text:
                unique_pages.append(page)
                continue
                
            norm = re.sub(r"\s+", " ", text)[:100]
            if norm not in seen:
                seen[norm] = True
                unique_pages.append(page)
            else:
                # Duplicate! Skip it.
                pass
                
        chapter["pages"] = unique_pages

    # Write back
    new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
    new_content = content[:match.start()] + prefix + new_json_str + ";" + content[match.end():]
    
    with open("book_data.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Duplicates removed and book_data.js updated.")
else:
    print("Could not find array structure in book_data.js. Let's try object structure...")
    match2 = re.search(r"(const bookData = )(\{.*\});", content, re.DOTALL)
    if match2:
        prefix = match2.group(1)
        json_str = match2.group(2)
        
        data = json.loads(json_str)
        seen = {}
        unique_pages = []
        
        for page in data.get("pages", []):
            text = page.get("text", "").strip()
            if not text:
                unique_pages.append(page)
                continue
            
            norm = re.sub(r"\s+", " ", text)[:100]
            if norm not in seen:
                seen[norm] = True
                unique_pages.append(page)
            else:
                # Skip duplicate
                pass
                
        data["pages"] = unique_pages
        
        new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
        new_content = content[:match2.start()] + prefix + new_json_str + ";" + content[match2.end():]
        
        with open("book_data.js", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Duplicates removed from object structure and book_data.js updated.")
    else:
        print("Could not parse JSON structure.")
