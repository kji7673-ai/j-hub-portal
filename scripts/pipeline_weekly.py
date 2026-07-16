import json
import random
import datetime
import os

categories = ["주간 회의록", "통합 일정표"]
topics = ["전략기획본부 주간회의 요약", "설계1본부 주요 안건", "인허가 리스크 점검 회의"]
perspectives = ["핵심 결정사항", "차주 계획", "주요 이슈"]
publishers = ["진양 저널 편집부", "전략기획본부", "사무국"]
subjects = [
    "이번 주 주간회의에서는 신규 수주 프로젝트의 초기 인허가 일정 단축 방안이 중점적으로 논의되었습니다.",
    "차주 주요 마일스톤 및 마감 일정을 공유합니다.",
    "현장 답사 결과 및 리스크 요인 분석 결과가 새롭게 업데이트되었습니다.",
    "설계1본부의 주요 안건으로 대안 설계안에 대한 치열한 토론이 있었습니다.",
    "인허가 리스크 점검 회의에서 지자체 협의 지연 문제가 안건으로 상정되었습니다."
]
contexts = [
    "특히 수요일 예정된 사전협상위원회 준비에 만전을 기해 주십시오.",
    "각 본부별 협조 사항을 숙지하고, 업무 혼선이 없도록 일정표를 재확인 바랍니다.",
    "본부장급 이상은 반드시 첨부된 상세 보고서를 확인하고 피드백을 남겨야 합니다.",
    "발주처의 요구사항이 일부 변경되었으니, 관련 팀은 즉각적인 대응 플랜을 가동해 주십시오.",
    "최근 법규 개정안이 실무에 미치는 영향을 분석하여 내부 가이드라인을 수정 중입니다."
]
conclusions = [
    "차주 월요일 오전까지 각 팀별 세부 실행 계획을 제출해 주시기 바랍니다.",
    "추가적인 문의사항이나 일정 조율이 필요하신 분은 기획팀으로 연락 바랍니다.",
    "성공적인 프로젝트 완수를 위해 전 직원의 유기적인 협업을 당부드립니다.",
    "이슈 사항 발생 시 즉각적으로 이슈 트래커에 등록하고 공유해 주십시오.",
    "관련 부서 간 긴밀한 소통을 통해 리스크를 사전에 완벽히 차단합시다."
]

def run_pipeline():
    today = datetime.datetime.now()
    articles = []
    
    # Generate 20 weekly articles
    for _ in range(20):
        cat = random.choice(categories)
        title = f"[주간 브리핑] {random.choice(topics)}: {random.choice(perspectives)}"
        
        # Weekly items usually correspond to recent days
        days_ago = random.randint(0, 3)
        pub_date = today - datetime.timedelta(days=days_ago)
        date_str = pub_date.strftime("%Y.%m.%d")
        
        meta = f"{random.choice(publishers)} | {date_str}"
        
        # 3단락으로 구성된 긴 요약문 생성 (최소 10줄 이상 분량 확보)
        excerpt_p1 = f"<b>[회의 주요 안건 및 배경]</b><br>{random.choice(subjects)} {random.choice(contexts)} {random.choice(conclusions)}"
        excerpt_p2 = f"<b>[논의 사항 상세]</b><br>이와 관련하여 각 팀별로 심도 깊은 논의가 진행되었습니다. {random.choice(subjects)} {random.choice(contexts)} {random.choice(conclusions)} 진행 과정에서 누락되는 부분이 없도록 더블 체크가 반드시 필요합니다."
        excerpt_p3 = f"<b>[향후 액션 아이템]</b><br>결정된 사안에 대한 후속 조치로서, {random.choice(subjects)} {random.choice(contexts)} {random.choice(conclusions)} 다음 회의 전까지 부여된 태스크의 진척 상황을 전산망에 필히 업데이트해주시기 바랍니다."
        
        excerpt = f"{excerpt_p1}<br><br>{excerpt_p2}<br><br>{excerpt_p3}"
        
        articles.append({
            "category": cat,
            "title": title,
            "excerpt": excerpt,
            "meta": meta
        })
        
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    out_path = os.path.join(data_dir, 'weekly_articles.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        
    print(f"Generated {len(articles)} weekly articles at {out_path}")

if __name__ == "__main__":
    run_pipeline()
