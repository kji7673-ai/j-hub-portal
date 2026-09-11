import json
import re

with open("book_data.js", "r") as f:
    content = f.read()

# Extract the JSON object correctly
match = re.search(r"const bookData = (\{.*\});", content, re.DOTALL)
if match:
    json_str = match.group(1)
    # The JSON might have trailing commas or JS-specific syntax that json.loads doesn't like,
    # but let's try to parse it.
    try:
        data = json.loads(json_str)
        seen = {}
        duplicates = []
        pages = data.get("pages", [])

        for idx, page in enumerate(pages):
            text = page.get("text", "").strip()
            if not text: continue
            # Normalize text for comparison
            norm = re.sub(r"\s+", " ", text)[:100]
            if norm in seen:
                duplicates.append((seen[norm], idx, norm))
            else:
                seen[norm] = idx

        if duplicates:
            print(f"Found {len(duplicates)} duplicates:")
            for d in duplicates:
                print(f" - Duplicate found at page {d[1]} (first seen at page {d[0]}):\n   Text: {d[2]}...\n")
        else:
            print(f"No exact duplicates found across {len(pages)} pages.")
    except Exception as e:
        print(f"JSON parsing error: {e}")
else:
    print("Could not find bookData object")
