import json
import re

with open('book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

episode_3_text_1 = """"정비사업통합검토 마법사."
이 거창한 이름의 시스템을 기획한 지 벌써 한 달이 훌쩍 넘었지만, 시스템은 여전히 먹통이거나 엉뚱한 결론을 내뱉고 있다.

아래 화면처럼 'Step 1. 토지 현황' 단계에서는 Vworld의 공간정보 API를 끌어와 우리가 설정한 구역계 폴리곤을 성공적으로 추출하고 지적 매핑을 완료했다. 여기까지는 완벽해 보였다."""

episode_3_text_2 = """하지만 문제는 그다음이었다.
'Step 2. 시장 분석' 단계로 넘어가 인접지의 데이터를 불러오고 공간 연산을 시도하는 순간, 화면은 하얗게 얼어붙고 개발자 콘솔에는 새빨간 에러 메시지가 폭포수처럼 쏟아졌다.

모니터 앞에서 에러 메시지와 한 달째 씨름하는 개발자와 실무자들을 보고 있노라면, 내 마음속 깊은 곳에서 거대한 의심과 유혹이 스멀스멀 피어오른다.

'아, 이거 그냥 내가 다음지도(카카오맵) 켜서 지적편집도 누르고 5분만 훑어보면 견적 다 나오는 건데. 굳이 이 엄청난 돈과 시간을 들여서 시스템을 가르치고 있어야 하나? 차라리 그 시간에 내가 현장 하나라도 더 검토하는 게 이득 아닐까?'"""

episode_3_text_3 = """솔직히 말해, 20년의 짬바(경력)를 가진 내 직관과 속도를 이 시스템이 당장 이길 확률은 제로에 가깝다. 실제로도 내가 지도를 한 번 쓱 훑어보는 게 지금 당장은 시간도 절약되고 가장 정확한 정답일지도 모른다.

하지만 나는 마우스로 향하던 손을 거둔다.
내가 다음지도를 열어 5분 만에 문제를 해결하는 순간, 시스템의 발전은 거기서 멈춘다. 그리고 내 직관에 의존하는 낡은 방식이 유지되는 한, 회사의 현장이 70개에서 100개로 늘어날 때 누군가는 또다시 새벽 3시의 모니터 앞에서 영혼을 갈아 넣어야 한다. 

지금 우리가 겪는 이 지독한 에러와 실패는, 20년 차의 직관을 1년 차의 신입사원도 클릭 한 번으로 복제해 낼 수 있게 만드는 '죽음의 계곡(Valley of Death)'이다. 이 계곡을 건너지 못하면 진양건축의 미래는 없다. 나는 다시 모니터 앞의 실무자들에게 돌아가 말했다.

"실패해도 좋습니다. 당장 제가 지도 보는 것보다 느려도 좋습니다. 어떻게든 돌파해 냅시다."

우리는 기어이 이 마법사를 완성할 것이다. 내가 다음지도를 켜지 않아도 되는 그날까지."""


new_page_json = f"""        {{
            "type": "chapter",
            "title": "[Episode 3] 다음지도 5분의 유혹",
            "subtitle": "죽음의 계곡(Valley of Death)을 건너며"
        }},
        {{
            "type": "image_top",
            "title": "Step 1: 구역계 추출의 성공",
            "text": {json.dumps(episode_3_text_1, ensure_ascii=False)},
            "image": "static/images/step1_success.png"
        }},
        {{
            "type": "image_top",
            "title": "Step 2: 에러와 의심의 늪",
            "text": {json.dumps(episode_3_text_2, ensure_ascii=False)},
            "image": "static/images/step2_error.png"
        }},
        {{
            "type": "text_only",
            "text": {json.dumps(episode_3_text_3, ensure_ascii=False)}
        }},"""

# We want to insert this at the very end of the bookPages array.
# The array ends with:
#         }
#     ];
# We will replace `    ];` with our new pages followed by `    ];`

match = re.search(r'}\s*];\s*$', content)
if match:
    # Need to add a comma to the previous object
    content = re.sub(r'}(\s*];\s*)$', r'},\1', content)
    
    # Now replace the array end
    new_content = content.replace('];', new_page_json + '\n    ];')
    with open('book_data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success")
else:
    print("Failed to find end of array")
