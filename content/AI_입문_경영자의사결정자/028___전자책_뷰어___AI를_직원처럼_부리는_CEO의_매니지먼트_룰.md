---json
{
  "id": 28,
  "title": "📙 AI를 직원처럼 부리는 CEO의 매니지먼트 룰 (전자책 뷰어)",
  "category": "🌱 AI 입문 (경영자/의사결정자)",
  "level": 1,
  "is_internal": false,
  "date": "2026-07-20",
  "summary": "코드를 한 줄도 모르는 50대 건축사의 AI 실전 기록. Canva 시각화 완성본을 책처럼 넘겨보세요.",
  "track": "ceo"
}
---

<style>
.book-viewer-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0;
}
.book-viewer-header {
  text-align: center;
  padding: 32px 20px 24px;
  background: linear-gradient(135deg, #1d1d1f 0%, #2a2a2c 100%);
  border-radius: 18px;
  margin-bottom: 24px;
  color: #fff;
}
.book-viewer-header h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  letter-spacing: -0.3px;
  color: #fff;
}
.book-viewer-header p {
  font-size: 15px;
  color: #cccccc;
  margin: 0 0 16px 0;
  line-height: 1.5;
}
.book-viewer-header .author-badge {
  display: inline-block;
  background: rgba(255,255,255,0.12);
  padding: 6px 16px;
  border-radius: 9999px;
  font-size: 13px;
  color: #fff;
  font-weight: 500;
}
.pdf-viewer-wrap {
  position: relative;
  width: 100%;
  height: 75vh;
  background: #2a2a2c;
  border-radius: 12px;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  box-shadow: rgba(0,0,0,0.12) 0 4px 24px;
}
.viewer-controls {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.viewer-controls a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 12px 24px;
  border-radius: 9999px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  font-family: -apple-system, sans-serif;
  transition: all 0.2s;
}
.btn-download {
  background: #0066cc;
  color: #fff !important;
}
.btn-download:hover {
  background: #0071e3;
}
.btn-fullscreen {
  background: #1d1d1f;
  color: #fff !important;
}
.btn-fullscreen:hover {
  background: #333;
}
.viewer-note {
  text-align: center;
  margin-top: 16px;
  font-size: 13px;
  color: #7a7a7a;
  line-height: 1.5;
}
@media (max-width: 768px) {
  .book-viewer-header h2 { font-size: 20px; }
  .book-viewer-header p { font-size: 14px; }
  .viewer-controls a { padding: 10px 18px; font-size: 14px; }
}
</style>

<div class="book-viewer-container">

<div class="book-viewer-header">
  <h2>AI를 직원처럼 부리는<br>CEO의 매니지먼트 룰</h2>
  <p>코드를 한 줄도 모르는 50대 중반 건축사가<br>AI로 업무 시스템을 바꾼 현장 기록</p>
  <span class="author-badge">✍️ 김중일 저 · (주)진양엔지니어링건축사사무소</span>
</div>

<div class="pdf-viewer-wrap" id="pdf-viewer-wrap">
  <div id="pdf-container" style="display: flex; flex-direction: column; align-items: center; padding: 20px;">
     <p id="pdf-loading-msg" style="padding: 40px; font-weight: bold; color: #fff; font-size: 16px;">📚 뷰어 엔진 로딩 중... 잠시만 기다려주세요.</p>
  </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
<script>
  (function() {
    var url = 'data/AI_JI.pdf';
    var pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';

    var loadingTask = pdfjsLib.getDocument(url);
    loadingTask.promise.then(function(pdf) {
      var container = document.getElementById('pdf-container');
      container.innerHTML = '';
      
      var canvases = [];
      for (var i = 1; i <= pdf.numPages; i++) {
          var canvas = document.createElement('canvas');
          canvas.style.display = "block";
          canvas.style.margin = "0 auto 20px auto";
          canvas.style.maxWidth = "100%";
          canvas.style.width = "100%";
          canvas.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
          container.appendChild(canvas);
          canvases.push(canvas);
      }
      
      for (var i = 1; i <= pdf.numPages; i++) {
        (function(pageNum, canvasElement) {
          pdf.getPage(pageNum).then(function(page) {
            var scale = 2.0; 
            var viewport = page.getViewport({scale: scale});
            var context = canvasElement.getContext('2d');
            canvasElement.height = viewport.height;
            canvasElement.width = viewport.width;
            var renderContext = { canvasContext: context, viewport: viewport };
            page.render(renderContext);
          });
        })(i, canvases[i-1]);
      }
    }, function (reason) {
      console.error(reason);
      var loadingMsg = document.getElementById('pdf-loading-msg');
      if (loadingMsg) loadingMsg.innerText = "PDF를 불러오는데 실패했습니다.";
    });
  })();
</script>

<div class="viewer-controls">
  <a href="data/AI_JI.pdf" download="AI를_직원처럼_부리는_CEO의_매니지먼트룰_v1.pdf" class="btn-download">📥 PDF 다운로드</a>
  <a href="data/AI_JI.pdf" target="_blank" class="btn-fullscreen">🔲 새 탭에서 전체화면</a>
</div>

<p class="viewer-note">
  💡 모바일에서는 [새 탭에서 전체화면] 버튼을 눌러 읽으시면 더 편합니다.<br>
  본 전자책은 v1 (2026.07.20)입니다. 향후 업데이트된 버전이 자동 반영됩니다.
</p>

</div>
