import re

for filename in ['index.html', 'reader_index.html']:
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
        bad_pattern = r"\}\n            if\(typeof saveProgress === 'function'\) saveProgress\(\);\n\n        function prevPage\(\) \{"
        good_pattern = "    if(typeof saveProgress === 'function') saveProgress();\n        }\n\n        function prevPage() {"
        
        content = re.sub(bad_pattern, good_pattern, content)
        
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Fixed {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")
