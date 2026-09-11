import re
import json

html_path = "book_studio.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for author_profile (if not already added)
author_css = """
        /* Author Profile Styles */
        .author-page {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 40px;
            text-align: center;
            background: linear-gradient(135deg, var(--canvas) 0%, var(--canvas-parchment) 100%);
        }
        .author-header {
            margin-bottom: 32px;
        }
        .author-name {
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 600;
            color: var(--ink);
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        }
        .author-title {
            font-family: var(--font-body);
            font-size: 16px;
            color: var(--primary);
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        .author-divider {
            width: 40px;
            height: 3px;
            background-color: var(--primary);
            margin: 0 auto 32px auto;
            border-radius: 2px;
        }
        .author-list {
            list-style: none;
            padding: 0;
            margin: 0 0 32px 0;
            text-align: left;
            width: 100%;
            max-width: 440px;
        }
        .author-list li {
            position: relative;
            padding-left: 24px;
            margin-bottom: 16px;
            font-size: 15px;
            color: var(--ink-muted-80, #333333);
            line-height: 1.4;
        }
        .author-list li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-size: 20px;
            line-height: 1;
            top: -2px;
        }
        .author-desc {
            font-size: 15px;
            color: var(--ink);
            line-height: 1.6;
            font-style: italic;
            max-width: 450px;
        }
"""
if ".author-page" not in html:
    html = html.replace('</style>', author_css + '\n    </style>')

# Replace any existing JS render logic for author_profile
author_js = """
            } else if (page.type === 'author_profile') {
                pageEl.innerHTML = `
                    <div class="author-page">
                        <div class="author-header">
                            <div class="author-name">김중일 건축사</div>
                            <div class="author-title">(주)진양엔지니어링건축사사무소 대표이사</div>
                        </div>
                        <div class="author-divider"></div>
                        <ul class="author-list">
                            <li>현(現) 서울시 건축심의위원</li>
                            <li>현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원</li>
                            <li>현(現) 강동구, 양천구 건축심의위원</li>
                            <li>현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원</li>
                        </ul>
                        <div class="author-desc">
                            "정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 가까이서 마주해 온 건축가의 진심 어린 조언이자 따뜻한 혁신의 기록."
                        </div>
                    </div>
                `;
            }
"""

if "page.type === 'author_profile'" in html:
    # We need to replace the old block with the new one
    html = re.sub(r"\} else if \(page.type === 'author_profile'\) \{.*?(?=\} else if|\}$)", author_js.strip() + " ", html, flags=re.DOTALL)
else:
    html = html.replace("} else if (page.type === 'text_only')", author_js.strip() + " else if (page.type === 'text_only')")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
