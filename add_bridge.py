import re

with open('index.html', 'r') as f:
    html = f.read()

bridge_html = """
                else if (page.type === 'bridge') {
                    pageEl.style.backgroundColor = '#1d1d1f';
                    pageEl.style.color = '#ffffff';
                    pageEl.style.padding = '0';
                    let rawTitle = page.title || "";
                    let pText = page.text || "";
                    
                    // Add text-shadow to any paragraphs in the text
                    pText = pText.replace(/<p style='(.*?)'>/g, "<p style='$1 text-shadow: 0 4px 15px rgba(0,0,0,0.8); color: rgba(255,255,255,0.9); font-weight: 300;'>");

                    contentHTML = `
                    <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; width:100%; height:100%; padding:40px; box-sizing:border-box; text-align:center; background: radial-gradient(circle at center, #2a2a2c 0%, #1d1d1f 100%);">
                        <h2 style="font-family:'SF Pro Display', sans-serif; font-size:clamp(20px, 4vw, 24px); font-weight:600; color:rgba(255,255,255,0.5); margin-bottom: 40px; letter-spacing:2px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">${rawTitle}</h2>
                        <div style="font-family:'SF Pro Text', sans-serif; font-size:clamp(16px, 3.5vw, 18px); line-height:2.0; color:#ffffff; word-break:keep-all; max-width: 90%;">
                            ${pText}
                        </div>
                    </div>`;
                }
"""

# Insert before `else if (page.type === 'image_full')`
html = html.replace("else if (page.type === 'image_full') {", bridge_html.strip() + "\n                else if (page.type === 'image_full') {")

with open('index.html', 'w') as f:
    f.write(html)
