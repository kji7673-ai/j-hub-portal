---json
{
  "id": 2,
  "title": "02 실전 SOP: 수작업 3일에서 AI 3분으로",
  "category": "📘 실전 가이드",
  "level": 1,
  "is_internal": false,
  "date": "2026-07-28",
  "summary": "AI를 활용한 5단계 사업성 검토 워크플로우와 교차 검증(Cross-Check) 실전 교본"
}
---

<h3>AI 전투 교본: 수작업의 종말과 '검증'의 시작</h3>

<figure style="text-align: center; margin: 40px 0;">
  <img src="static/images/illustrations/prompt.jpg" alt="터미널에서 정교한 블루프린트가 생성되는 모습" style="max-width: 100%; border-radius: 12px; box-shadow: rgba(0,0,0,0.1) 0 4px 24px;">
  <figcaption style="font-size: 13px; color: #7a7a7a; margin-top: 12px;">[삽도] 완벽한 프롬프트(명령어)가 수작업 3일의 도면을 3분 만에 생성합니다.</figcaption>
</figure>

<p>과거 우리는 VWorld를 열어 지적도를 확인하고, 디스코(Disco)에서 실거래가를 검색하며, 국가법령정보센터에서 조례를 뒤적이는 데 <strong>꼬박 3일</strong>을 썼습니다. 이제 J-Hub AI 플랫폼은 지번 하나만으로 이 모든 데이터를 <strong>단 3분</strong> 만에 긁어옵니다.</p>

<p>본 매뉴얼은 '어떻게 검색하는가'를 가르치지 않습니다. 대신 <strong>'AI가 3분 만에 가져온 데이터를 어떻게 의심하고, 어떤 치트키로 교차 검증(Cross-Check)할 것인가'</strong>를 가르치는 전투 교본입니다.</p>

<div class="mermaid" style="background: var(--canvas-parchment); padding: 24px; border-radius: 18px; margin-bottom: 30px;">
graph LR
  A[STEP 1. 대지 확보] --> B[STEP 2. 시장 조사]
  B --> C[STEP 3. 타당성 검증]
  C --> D[STEP 4. 법규 및 개요]
  D --> E[STEP 5. 최종 의사결정]
</div>

---

<h4>STEP 1. 대지 자료의 확보 (VWorld 수작업의 종말)</h4>
<p>과거에는 VWorld에 접속해 API 키를 발급받고 레이어를 설정해야 했습니다. 이제는 AI에게 지번만 던지면 됩니다. 하지만 AI가 가져온 데이터는 완벽할까요?</p>

<div class="mermaid" style="background: var(--canvas-parchment); padding: 24px; border-radius: 18px; margin: 20px 0;">
graph TD
  A[건축사: 지번 입력] --> B(AI: VWorld 지적 데이터 크롤링)
  B --> C[면적, 지목, 용도지역 도출]
  C -.-> D{건축사의 팩트체크}
  D -->|물리적 제약| E[경사도, 암반, 진입로 폭원 보정]
</div>

<div class="episode ep-fail" style="background-color: var(--surface-tile-1); color: var(--on-dark); padding: 32px; border-radius: 18px; margin-bottom: 24px;">
  <h4 style="font-family: 'SF Pro Display', sans-serif; font-weight: 600; font-size: 24px; color: #fff; margin-bottom: 12px;">⚠️ 검증 포인트: AI는 3D 지형을 모른다</h4>
  <p style="font-family: 'SF Pro Text', sans-serif; font-size: 17px; line-height: 1.47; color: var(--body-muted); margin-bottom: 0;">
    AI가 "면적 2,000㎡, 정형화된 평탄지"라고 대답했더라도 절대 맹신하지 마십시오. AI는 도면 위의 선만 읽을 뿐 현장의 숨결을 알지 못합니다. 로드뷰나 현장 답사를 통해 <strong>실제 대지의 가파른 경사도와 비좁은 진입로 폭원</strong>을 건축사의 눈으로 직접 확인하고, 그 '현장의 진실'을 수동으로 보정(Override)하여 다시 시스템에 주입해야 합니다.
  </p>
</div>

---

<h4>STEP 2. 지역 및 시장 조사 (데이터 크롤링의 함정 피하기)</h4>
<p>AI는 주변 분양가, 세대수, 상권 데이터를 1분 만에 크롤링합니다. 하지만 AI는 '숫자'만 볼 뿐, 그 이면의 '맥락'은 읽지 못합니다.</p>

<pre style="background:#2d3748;color:#e2e8f0;padding:12px;border-radius:6px;font-size:13px;overflow-x:auto;">
[AI 크롤링 지시 프롬프트]
대상지 반경 500m 이내, 최근 3년 이내 입주한 아파트의 전용 84㎡ 기준 실거래가 평균과 
주력 평형대(세대 배분)를 마크다운 표로 정리해 줘. 
비정상적인 이상치(특수거래 등)는 제외할 것.
</pre>

<div class="alert alert-secondary" style="background-color: var(--canvas-parchment); color: var(--ink); padding: 32px; border-radius: 18px; border: 1px solid var(--hairline); margin: 24px 0;">
  <h4 style="font-family: 'SF Pro Display', sans-serif; font-weight: 600; font-size: 21px; color: var(--primary); margin-bottom: 12px;">💡 건축사의 교차 검증 (Cross-Check)</h4>
  <p style="font-family: 'SF Pro Text', sans-serif; font-size: 17px; line-height: 1.47; color: var(--ink-muted-80); margin-bottom: 0;">
    AI가 "주변 시세 10억, 분양성 양호"라는 숫자를 내놓았다고 안심할 수 있을까요? 대상지 바로 옆에 철도 소음이 끊이지 않거나 상권이 단절된 이면도로가 있다면 그 분양성은 즉시 폭락합니다. AI가 놓치는 <strong>'정성적인 환경 제약'</strong>을 인간의 직관으로 짚어내어, 프롬프트에 추가 조건으로 통제하는 것. 그것이 게이트키퍼로서 건축사가 존재하는 이유입니다.
  </p>
</div>

---

<h4>STEP 3. 사업 방식 타당성 검증 (AI의 제안 vs 건축사의 직관)</h4>
<p>AI는 면적과 간선도로 접근성 등의 정량 데이터를 바탕으로 "모아타운이 적합하다"고 제안할 수 있습니다. 이를 곧바로 믿어서는 안 됩니다.</p>

<div class="mermaid" style="background: var(--canvas-parchment); padding: 24px; border-radius: 18px; margin: 20px 0;">
graph LR
  A[AI 제안: 모아타운] --> B{건축사 직관 필터링}
  B -->|Pass| C[상세 개요 작성]
  B -->|Reject| D[정치/사회적 리스크 (상가 반대 등)]
  D --> E[가로주택정비사업으로 선회]
</div>

<p><strong>반려(Reject) 프롬프트 예시:</strong><br>
"네가 제안한 모아타운 방식은 물리적으로는 가능하지만, 대상지 남측의 상가 소유주 반발 리스크가 너무 커서 사업 지연이 예상돼. 상가 구역을 제척(제외)하고 가로주택정비사업으로 진행할 때의 대안을 다시 분석해 줘."</p>

---

<h4>STEP 4. 용적률 체계 확인 및 개요 작성 (치명적 환각 방어)</h4>
<p>가장 위험한 단계입니다. AI는 서울시 조례나 국가 법령을 그럴싸하게 지어내는 <strong>환각(Hallucination)</strong>을 자주 일으킵니다.</p>

<div class="alert alert-danger" style="background-color: var(--surface-tile-1); color: var(--on-dark); padding: 32px; border-radius: 18px; margin-bottom: 32px;">
  <h4 style="font-family: 'SF Pro Display', sans-serif; font-weight: 600; font-size: 24px; color: #fff; margin-bottom: 16px;">🚨 치명적 환각 TOP 3 방어선</h4>
  <p style="font-family: 'SF Pro Text', sans-serif; font-size: 17px; line-height: 1.47; color: var(--body-muted); margin-bottom: 16px;">
    AI가 산출한 그럴싸한 건축 개요를 마주했을 때, 다음 3가지 핵심 지표만큼은 <strong>반드시 법제처(law.go.kr) 원문과 직접 대조</strong>해야 합니다. 이 3가지에서 발생하는 환각은 프로젝트의 존폐를 가릅니다.
  </p>
  <ul style="font-family: 'SF Pro Text', sans-serif; font-size: 17px; line-height: 1.6; color: var(--body-muted);">
    <li><strong>임대주택 완화 비율:</strong> 제2종일반주거지역 임대주택 건립 시 용적률 완화 산식이 최신 법령에 맞게 적용되었는가?</li>
    <li><strong>노후도 조건:</strong> 지자체별로 시시각각 변하는 노후도 충족 비율(예: 67% vs 57%)이 최신 고시 기준으로 정확히 반영되었는가?</li>
    <li><strong>주차 대수 산정:</strong> 서울시 주차장 조례의 기점(세대당 1대 vs 1.2대)이 평형대별로 오차 없이 쪼개어져 계산되었는가?</li>
  </ul>
</div>

<pre style="background:#2d3748;color:#e2e8f0;padding:12px;border-radius:6px;font-size:13px;overflow-x:auto;">
[교차 검증 프롬프트]
위에서 계산한 '최대 용적률 250%'의 산출 근거를 
'서울특별시 도시계획 조례'의 정확한 조(제OO조)와 항을 명시하여 다시 설명해. 
만약 2026년 최신 개정본을 확인하지 못했다면 "확인 불가"라고 정직하게 답해.
</pre>

---

<h4>STEP 5. 대안 비교표 및 최종 의사결정 (건축사의 Final Touch)</h4>
<p>AI가 뽑아낸 기계적인 비교 개요표(Alt 1 vs Alt 2)에 <strong>'생명력'</strong>을 불어넣는 것은 오직 건축사의 종합 의견뿐입니다.</p>

<div class="mermaid" style="background: var(--canvas-parchment); padding: 24px; border-radius: 18px; margin: 20px 0;">
graph TD
  A(정량적 데이터: AI 산출) --> C{최종 의사결정 보고서}
  B(정성적 통찰: 건축사 판단) --> C
</div>

<div class="episode ep-solve" style="background-color: var(--canvas-parchment); color: var(--ink); padding: 32px; border-radius: 18px; border: 1px solid var(--hairline); margin: 24px 0;">
  <h4 style="font-family: 'SF Pro Display', sans-serif; font-weight: 600; font-size: 21px; color: var(--primary); margin-bottom: 12px;">💡 건축사의 Final Touch: 생명력을 불어넣는 프롬프트</h4>
  <p style="font-family: 'SF Pro Text', sans-serif; font-size: 17px; line-height: 1.47; color: var(--ink-muted-80); margin-bottom: 0;">
    "위 비교표 밑에 나의 종합 의견을 다음과 같이 추가해서 최종 보고서를 포맷팅해 줘.<br><br>
    <strong>[건축사 통찰]</strong> Alt 1이 세대수는 많지만, 북측 경사지로 인한 흙막이 토목 공사비의 막대한 증가분과 최근 하이엔드 분양 시장 트렌드를 감안할 때, 조경과 펜트하우스를 특화한 Alt 2 방식이 조합원 분담금 최소화와 사업성 확보에 압도적으로 유리할 것으로 판단됨."
  </p>
</div>

<hr style="margin: 40px 0; border: 0; border-top: 1px solid var(--hairline);">

<h3>결론: AI는 조수일 뿐, 책임은 건축사에게 있다</h3>
<p>수작업 3일의 고통이 AI를 통해 3분으로 줄어들었습니다. 하지만 그 3분 만에 나온 결과물이 수백억 단위의 정비사업 향방을 결정짓습니다. <strong>AI가 주는 데이터를 100% 맹신하지 말고, 끊임없이 의심하고 집요하게 검증하는 것.</strong> 그것이 진양의 J-Hub를 지배하는 '마스터 건축사'의 길입니다.</p>
