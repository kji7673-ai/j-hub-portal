import os
from pathlib import Path
from playwright.sync_api import sync_playwright

html_path = '/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/docs_apple/index.html'
output_image = '/Users/joongilkim/.gemini/antigravity/brain/308a47f0-c18d-4944-a763-42deecc6afd7/scratch/index_screenshot_new.png'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(f'file://{html_path}', wait_until='networkidle')
    page.screenshot(path=output_image, full_page=True)
    browser.close()
print('Screenshot saved to', output_image)
