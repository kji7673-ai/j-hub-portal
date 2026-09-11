import re

for filename in ['index.html', 'reader_index.html']:
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
        bad_pattern = r"currentChapter = parseInt\(savedChapter, 10\);\n\s*currentColumn = parseInt\(savedColumn, 10\);"
        good_pattern = "const parsedChap = parseInt(savedChapter, 10);\n                const parsedCol = parseInt(savedColumn, 10);\n                if(!isNaN(parsedChap) && !isNaN(parsedCol)) {\n                    currentChapter = parsedChap;\n                    currentColumn = parsedCol;\n                }"
        
        content = re.sub(bad_pattern, good_pattern, content)
        
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Fixed {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")
