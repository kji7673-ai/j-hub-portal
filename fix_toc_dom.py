import re

html_path = "book_studio.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract TOC Modal HTML
modal_start = html.find('<!-- TOC Modal -->')
modal_end = html.find('</body>')

if modal_start != -1 and modal_end != -1:
    modal_html = html[modal_start:modal_end]
    # Remove from bottom
    html = html[:modal_start] + html[modal_end:]
    
    # Insert before scripts
    script_start = html.find('<script src="book_data.js"></script>')
    if script_start != -1:
        html = html[:script_start] + modal_html + '\n    ' + html[script_start:]
        
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        print("Successfully moved TOC Modal above scripts.")
else:
    print("Could not find TOC Modal HTML.")
