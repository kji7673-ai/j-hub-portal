import sys
import re

html_path = "book_studio.html"
js_path = "book_data.js"

with open(html_path, 'r', encoding='utf-8') as f:
    html_text = f.read()

# 1. Update CSS in book_studio.html
# Find the CSS block and inject custom styles

css_injections = """
        /* -- Custom Scrollbar for pages -- */
        .page-content {
            flex: 1;
            padding: 10% 12% 15% 12%; /* Increased bottom padding to avoid controls overlap */
            display: block;
            opacity: 0;
            transition: opacity 0.3s ease;
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            overflow-y: auto;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }

        .page-content::-webkit-scrollbar {
            width: 6px;
        }
        .page-content::-webkit-scrollbar-track {
            background: transparent;
        }
        .page-content::-webkit-scrollbar-thumb {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }

        /* -- Cover Design (Dark Mode) -- */
        .page-content.bg-dark {
            background-color: var(--surface-tile-1, #272729);
            color: var(--canvas, #ffffff);
        }
        .page-content.bg-dark h1.book-title,
        .page-content.bg-dark p {
            color: var(--canvas, #ffffff) !important;
        }

        /* -- Chapter Title Redesign -- */
        h2.chapter-title {
            font-family: var(--font-display);
            font-size: clamp(20px, 4cqw, 28px);
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 24px;
            color: var(--ink);
            border-left: 4px solid var(--primary);
            padding-left: 14px;
            line-height: 1.3;
        }

        /* -- Table Redesign -- */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            font-size: 14px;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .custom-table th, .custom-table td {
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid var(--hairline);
        }
        .custom-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        .custom-table tr:last-child td {
            border-bottom: none;
        }
"""

# Replace original page-content CSS block with the new one.
# First, remove the old page-content block to avoid duplicates.
old_page_content_pattern = re.compile(r'\.page-content\s*\{[^}]*\}', re.MULTILINE)
html_text = old_page_content_pattern.sub("", html_text)

# Also remove old chapter-title CSS
old_chapter_title_pattern = re.compile(r'h2\.chapter-title\s*\{[^}]*\}', re.MULTILINE)
html_text = old_chapter_title_pattern.sub("", html_text)

# Inject the new CSS before </style>
html_text = html_text.replace("</style>", css_injections + "\n    </style>")

# 2. Update JS Logic in book_studio.html
# Add bg-dark to cover pages
old_cover_js = """                if (page.type === 'cover') {
                    contentHTML += `<div class="cover-content">`;
                    contentHTML += `<h1 class="book-title" style="text-align:center;">${page.title}</h1>`;
                    if(page.subtitle) contentHTML += `<p style="text-align:center; color:#666;">${page.subtitle}</p>`;
                    contentHTML += `</div>`;
                } """
new_cover_js = """                if (page.type === 'cover') {
                    pageEl.className += ' bg-dark';
                    contentHTML += `<div class="cover-content">`;
                    contentHTML += `<h1 class="book-title" style="text-align:center;">${page.title}</h1>`;
                    if(page.subtitle) contentHTML += `<p style="text-align:center; color:#a0a0a0; font-weight: 300;">${page.subtitle}</p>`;
                    contentHTML += `</div>`;
                } """
html_text = html_text.replace(old_cover_js, new_cover_js)

# Modify paragraph wrapping logic so it doesn't wrap <table> elements in <p>
old_p_wrap_1 = """                    if(page.text) {
                        const paragraphs = page.text.split('\\n\\n');
                        paragraphs.forEach(p => {
                            contentHTML += `<p class="body-text">${p}</p>`;
                        });
                    }"""
new_p_wrap_1 = """                    if(page.text) {
                        const paragraphs = page.text.split('\\n\\n');
                        paragraphs.forEach(p => {
                            if (p.trim().startsWith('<table') || p.trim().startsWith('<div class="custom-table"')) {
                                contentHTML += p;
                            } else {
                                contentHTML += `<p class="body-text">${p}</p>`;
                            }
                        });
                    }"""
# Need to replace this in multiple places (image_top, text_only)
html_text = html_text.replace(old_p_wrap_1, new_p_wrap_1)

# Write HTML back
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_text)

# 3. Update book_data.js Tables to HTML
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# Replace 7 Steps table
table1_md = """| 스텝 (Step) | AI의 역할 (데이터 수집 및 단순 연산) | 인간의 통제 (필터링 및 철학적 결정) |\\n| :--- | :--- | :--- |\\n| **1. 대지 분석** | 지적도, 공시지가 등 공공 데이터 스크래핑 | 대상지 경계 확정 및 오류 필지 필터링 |\\n| **2. 규제 검토** | 지자체 조례/법규 텍스트 매칭 및 제시 | 모호한 규제 해석 및 적용 여부 최종 승인 |\\n| **3. 3D 환경** | 지형 고저차 및 일조권 시뮬레이션 데이터 제공 | 주변 건물과의 관계를 고려한 주동 배치 방향성 결정 |\\n| **4. 규모 시뮬레이션** | 용적률에 맞춘 평형별 세대수 경우의 수 도출 | 지역 수요와 분양성을 통찰하여 최적의 세대 믹스 선택 |\\n| **5. 사업성 분석** | 공사비/보정계수를 대입한 예상 분담금 계산 | 클라이언트 설득을 위한 보수적/공격적 숫자 튜닝 |\\n| **6. 공간 성격 부여** | 텅 빈 공용공간 면적 및 법정 조경 면적 산출 | 거주자 소통 공간(접촉점) 여부 등 철학적 가치 부여 |\\n| **7. 통합 리포트** | 결정된 데이터를 디자인된 리포트로 자동 조립 | 최종 도장을 찍으며 전문가로서의 권위와 책임 보증 |"""

table1_html = """<table class=\\"custom-table\\">
  <thead>
    <tr>
      <th>스텝 (Step)</th>
      <th>AI의 역할 (데이터 수집 및 단순 연산)</th>
      <th>인간의 통제 (필터링 및 철학적 결정)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>1. 대지 분석</strong></td><td>지적도, 공시지가 등 공공 데이터 스크래핑</td><td>대상지 경계 확정 및 오류 필지 필터링</td></tr>
    <tr><td><strong>2. 규제 검토</strong></td><td>지자체 조례/법규 텍스트 매칭 및 제시</td><td>모호한 규제 해석 및 적용 여부 최종 승인</td></tr>
    <tr><td><strong>3. 3D 환경</strong></td><td>지형 고저차 및 일조권 시뮬레이션 데이터 제공</td><td>주변 건물과의 관계를 고려한 주동 배치 방향성 결정</td></tr>
    <tr><td><strong>4. 규모 시뮬레이션</strong></td><td>용적률에 맞춘 평형별 세대수 경우의 수 도출</td><td>지역 수요와 분양성을 통찰하여 최적의 세대 믹스 선택</td></tr>
    <tr><td><strong>5. 사업성 분석</strong></td><td>공사비/보정계수를 대입한 예상 분담금 계산</td><td>클라이언트 설득을 위한 보수적/공격적 숫자 튜닝</td></tr>
    <tr><td><strong>6. 공간 성격 부여</strong></td><td>텅 빈 공용공간 면적 및 법정 조경 면적 산출</td><td>거주자 소통 공간(접촉점) 여부 등 철학적 가치 부여</td></tr>
    <tr><td><strong>7. 통합 리포트</strong></td><td>결정된 데이터를 디자인된 리포트로 자동 조립</td><td>최종 도장을 찍으며 전문가로서의 권위와 책임 보증</td></tr>
  </tbody>
</table>"""
# We must format string for JSON escaping in JS
table1_html = table1_html.replace('\\n', '').replace('\\"', '\\\"').replace('\n', '')

js_text = js_text.replace(table1_md, table1_html)

# Replace Before & After table
table2_md = """| 구분 | 엑셀 기반의 기존 업무 (Before) | J-Hub 기반의 혁신 (After) |\\n| :--- | :--- | :--- |\\n| **소요 시간** | 며칠 밤을 새우며 수작업 데이터 입력 | **단 3초 만에** 법규 및 지형 데이터 스캔 완료 |\\n| **신뢰도** | 휴먼 에러 발생 시 수십억 단위 사고 위험 | **레드팀 로직**으로 AI 환각 교차 검증 |\\n| **클라이언트 설득** | \\\"글쎄요, 대충 이 정도 나올 겁니다\\\" | **권위 있는 시각화 데이터**로 완벽한 논리 제시 |\\n| **건축가의 역할** | 숫자 맞추기에 급급한 '엑셀 오퍼레이터' | 딜레마를 통제하고 철학을 불어넣는 **'진짜 지휘자'** |"""

table2_html = """<table class=\\"custom-table\\">
  <thead>
    <tr>
      <th>구분</th>
      <th>엑셀 기반의 기존 업무 (Before)</th>
      <th>J-Hub 기반의 혁신 (After)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>소요 시간</strong></td><td>며칠 밤을 새우며 수작업 데이터 입력</td><td><strong>단 3초 만에</strong> 법규 및 지형 데이터 스캔 완료</td></tr>
    <tr><td><strong>신뢰도</strong></td><td>휴먼 에러 발생 시 수십억 단위 사고 위험</td><td><strong>레드팀 로직</strong>으로 AI 환각 교차 검증</td></tr>
    <tr><td><strong>클라이언트 설득</strong></td><td>"글쎄요, 대충 이 정도 나올 겁니다"</td><td><strong>권위 있는 시각화 데이터</strong>로 완벽한 논리 제시</td></tr>
    <tr><td><strong>건축가의 역할</strong></td><td>숫자 맞추기에 급급한 '엑셀 오퍼레이터'</td><td>딜레마를 통제하고 철학을 불어넣는 <strong>'진짜 지휘자'</strong></td></tr>
  </tbody>
</table>"""
table2_html = table2_html.replace('\\n', '').replace('"', '\\"').replace('\n', '')

js_text = js_text.replace(table2_md, table2_html)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("UI updates applied successfully.")
