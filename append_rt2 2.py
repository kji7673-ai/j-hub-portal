import json

path = '/Users/joongilkim/Desktop/03_업무자료/법규관련/.agents/지식베이스/redteam_insights.json'
with open(path, 'r', encoding='utf-8') as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        data = []

data.append({
    'id': 'RT-2026-0725-002',
    'timestamp': '2026-07-25T10:50:00Z',
    'chat_id': '583085b5',
    'chat_name': 'J-journal RAG 복구 및 레드팀 평가',
    'type': '레드팀 의견',
    'category': 'UX/UI',
    'severity': 'high',
    'title': '교육자료 플랫폼의 사용자 관점 UI/UX 한계',
    'problem': '교육 플랫폼이 장문의 텍스트와 선형적 목차로 구성되어 현업 실무자들의 인지 과부하 유발 및 실천(Action) 부재',
    'redteam_opinion': '개발 과정이나 이론 설명에 치우쳐, 당장 실무에 써먹어야 하는 상황별 템플릿을 직관적으로 찾기 힘듦.',
    'resolution': 'RAG 챗봇 렌더링 오류 수정 후 배포. 목적 지향적 대시보드 개편 및 원클릭 복사 버튼 도입 제안.',
    'lesson': '사용자는 교과서가 아니라 당장 쓸 수 있는 도구를 원한다.',
    'is_public': True,
    'tags': ['UX/UI', 'RAG'],
    'track': ['education'],
    'is_safe_for_employees': True,
    'story_arc': '실패→극복→완성',
    'episode_title': '가르치려다 이탈하게 만든 플랫폼',
    'evidence_uri': None,
    'aftermath': 'RAG 기능 복구'
})

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Redteam insight appended.")
