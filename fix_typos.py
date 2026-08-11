import json

replacements = [
  {
    "target": "완벽히 숙지해야 가깝다.",
    "replacement": "완벽히 숙지해야 한다."
  },
  {
    "target": "대안이 유리한다.",
    "replacement": "대안이 유리하다."
  },
  {
    "target": "생존을 도모하기 위한 모두를 보호하기 위한",
    "replacement": "생존을 도모하고 모두를 보호하기 위한"
  },
  {
    "target": "깊이 있는 효율성.",
    "replacement": "압도적인 효율성."
  },
  {
    "target": "사업성을 낫게 하고,",
    "replacement": "사업성을 높이고,"
  },
  {
    "target": "깊이 있는 속도로 전개되었다.",
    "replacement": "압도적인 속도로 전개되었다."
  },
  {
    "target": "깊이 있으로 유리한지",
    "replacement": "압도적으로 유리한지"
  },
  {
    "target": "깊이 있이고 실질적인 가치가",
    "replacement": "압도적이고 실질적인 가치가"
  },
  {
    "target": "깊이 있는 속도로 전문가로 성장한다.",
    "replacement": "압도적인 속도로 전문가로 성장한다."
  },
  {
    "target": "깊이 있는 속도로 보여주기 때문이다.",
    "replacement": "압도적인 속도로 보여주기 때문이다."
  },
  {
    "target": "신입 도 마찬가지겠지요.",
    "replacement": "신입도 마찬가지겠지요."
  },
  {
    "target": "세상에 내어놓다. 발가벗겨진",
    "replacement": "세상에 내어놓는다. 발가벗겨진"
  }
]

for filename in ["book_data.js", "docs/book_data.js", "docs_apple/book_data.js", "docs_internal/book_data.js"]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        for item in replacements:
            content = content.replace(item["target"], item["replacement"])
            
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Applied fixes to {filename}")
    except FileNotFoundError:
        print(f"{filename} not found, skipping.")
