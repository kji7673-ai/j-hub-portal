#!/usr/bin/env python3
"""
ocr_extract.py
macOS 내장 Vision 프레임워크를 사용하여 이미지에서 텍스트를 추출하는 스크립트.

사용법:
  python3 ocr_extract.py <이미지_경로>
"""

import sys
import os
import subprocess
import json

SWIFT_SCRIPT = """
import Foundation
import Vision

let args = CommandLine.arguments
if args.count < 2 {
    print("Error: No image path provided")
    exit(1)
}

let imagePath = args[1]
guard let imageURL = URL(string: "file://" + imagePath) else {
    print("Error: Invalid URL")
    exit(1)
}

let requestHandler = VNImageRequestHandler(url: imageURL, options: [:])
let request = VNRecognizeTextRequest { (request, error) in
    if let error = error {
        print("Error: \\(error.localizedDescription)")
        return
    }
    
    guard let observations = request.results as? [VNRecognizedTextObservation] else {
        return
    }
    
    var extractedText = ""
    for observation in observations {
        guard let topCandidate = observation.topCandidates(1).first else { continue }
        extractedText += topCandidate.string + "\\n"
    }
    
    print(extractedText)
}

// 한국어와 영어 인식
request.recognitionLanguages = ["ko-KR", "en-US"]
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

do {
    try requestHandler.perform([request])
} catch {
    print("Error: \\(error.localizedDescription)")
}
"""

def extract_text_vision(image_path: str) -> str:
    """macOS Vision 프레임워크를 사용하여 텍스트 추출"""
    # 임시 Swift 스크립트 파일 생성
    script_path = "/tmp/vision_ocr.swift"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(SWIFT_SCRIPT)
    
    try:
        # Swift 스크립트 실행
        result = subprocess.run(
            ["swift", script_path, os.path.abspath(image_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"OCR 실패: {e.stderr}", file=sys.stderr)
        return ""
    finally:
        # 임시 파일 삭제
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 ocr_extract.py <이미지_경로>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"파일을 찾을 수 없습니다: {image_path}")
        sys.exit(1)
    
    # PDF는 향후 변환 로직 추가 필요, 현재는 이미지 위주
    if image_path.lower().endswith('.pdf'):
        print("[PDF 지원 안됨] 현재 버전에서는 이미지 파일만 지원합니다.")
        sys.exit(1)
        
    text = extract_text_vision(image_path)
    print(text)
