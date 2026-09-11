with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

leftover = """         else {
                menu.style.display = 'none';
            }
        }"""
        
html = html.replace(leftover, "")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
