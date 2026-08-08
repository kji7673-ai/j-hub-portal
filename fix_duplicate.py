import json

with open('book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# The array assignment starts with: const bookPages = [
# We can parse the json if we strip the prefix and suffix.
prefix = "const bookPages = "
if content.startswith(prefix):
    json_str = content[len(prefix):].strip()
    if json_str.endswith(";"):
        json_str = json_str[:-1]
    
    pages = json.loads(json_str)

    # Pages are 0-indexed. 
    # Let's find the ones with "용문동" in Chapter 5.
    for i, page in enumerate(pages):
        if i < 80: # Chapter 5 is around pages 39-42 (index 38-41)
            if 'text' in page and '용문동' in page['text']:
                if i == 38: # Page 39 (image 39.jpg)
                    page['text'] = page['text'].replace('[용문동 프로젝트: 116개 필지의 데이터를 장악하다]', '[연남동 프로젝트: 복잡한 규제를 데이터로 장악하다]')
                elif i == 39: # Page 40
                    page['text'] = "2026년 3월, 마포구 연남동 239-1번지 일원의 상업용 빌딩 신축 타당성 검토를 의뢰받았다. 대지면적은 작았지만 지구단위계획과 사선제한이 복잡하게 얽혀 있는 구역이었다. 클라이언트는 산전수전을 다 겪은 깐깐한 자산가였다. 어설픈 한 장짜리 개요서로는 결코 그의 마음을 움직일 수 없었다.\n\n우리는 즉시 아키 시냅스 기반의 '통합 보고서 마법사'를 가동했다.\n\n> **[그림 삽입: 연남동 타당성 검토 보고서 표지]**\n> *단순한 텍스트 쪼가리가 아닌, '엔터프라이즈 엘레강스'가 적용된 보고서의 첫인상*\n\n과거라면 일주일 내내 야근하며 규제를 분석해야 했을 작업이 마법사 플랫폼 위에서는 압도적인 속도로 전개되었다.\n\n단순히 도면 그리기가 아니었다. 플랫폼은 즉각적으로 해당 필지의 건축 한계선, 주차 대수, 그리고 **주변 임대료 데이터를 1초 만에 전수조사**하여 12장짜리 묵직한 데이터 리포트로 뱉어냈다.\n\n> **[그림 삽입: 연남동 규제 및 임대료 전수조사 데이터 테이블 (보고서 본문)]**\n> *사람의 손으로는 며칠이 걸릴 데이터가 단 1초 만에 도출되어 표로 정리된다.*\n\n[250%의 용적률과 7.8%의 수익률을 증명하다]"
                elif i == 40: # Page 41
                    page['text'] = "가장 강력한 한 방은 '건축 한계선과 층수 제한의 심층 비교'였다. \n클라이언트는 항상 불안하다. \"1층을 상가로 전부 빼는 게 맞나? 주차장을 지하로 넣어야 하나?\" 마법사는 3가지 매스(Mass) 시나리오를 동시에 시뮬레이션했다. 주차 대수, 임대 면적, 공사비를 알고리즘이 교차 검증한 결과, **'1층 필로티 주차장과 상층부 테라스 특화 방식'이 수익성을 극대화할 수 있는 유일한 해답**임을 논리적으로 도출해 냈다.\n\n결과는 소름 돋을 정도로 정밀했다.\n* **최종 용적률:** 250% (일조권 사선제한 완벽 반영)\n* **총 임대 면적:** 980㎡\n* **최종 수익률:** 7.8% (층별 임대료 시나리오별 손익분기 완벽 제시)\n\n> **[그림 삽입: 수익률 7.8% 시뮬레이션 요약 대시보드 (보고서 본문)]**\n> *3가지 건축 방식을 비교하고 최적의 수익성(7.8%)을 증명한 핵심 페이지*\n\n과거처럼 고연차 소장이 며칠 밤을 새우며 엑셀을 두드린 결과가 아니다. 입사 한 달 차 신입사원이라도, 플랫폼이 묻는 질문에 정확한 팩트만 입력하면 30년 차 대표 수준의 완벽한 재무적 타당성(Feasibility) 분석이 쏟아져 나오는 '지식의 상향 평준화'가 이루어진 것이다.\n\n[결과가 아닌 '과정'이 신뢰를 만든다, 그리고 얻어낸 승리]"
                elif i == 41: # Page 42
                    page['text'] = "이 압도적인 12장짜리 <연남동 타당성 검토 보고서>를 받아 든 클라이언트의 반응은 굳이 설명할 필요가 없었다.\n\n단순히 결과(면적)만 덜렁 적힌 것이 아니라, 어떤 규제를 근거로 볼륨을 뽑아냈는지, 지하 주차장 시나리오와 지상 주차장 방안 중 왜 후자가 압도적으로 유리한지 그 **'도출 과정(Process)' 전체가 투명하게 증명**되어 있었기 때문이다. 클라이언트는 이 보고서를 통해 자신의 수백억 원대 자산이 가장 안전하고 완벽하게 분석되고 있음을 확인했다. 의심은 무한한 신뢰로 바뀌었다.\n\n결국 플랫폼이 곧 회사의 경쟁력이다. 정비 사업 통합 보고서 마법사는 우리에게 야근 없는 저녁을 선물한 것을 넘어, 철저한 숫자의 증명으로 수십억 원의 설계 계약을 성사시키는 우리의 가장 강력한 최전방 공격수가 되었다.\n\n---"

    new_content = prefix + json.dumps(pages, indent=4, ensure_ascii=False) + ";\n"
    with open('book_data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced successfully in book_data.js")
