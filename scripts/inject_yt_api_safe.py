import os

index_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

if 'iframe_api' not in html:
    html = html.replace('</head>', '  <script src="https://www.youtube.com/iframe_api"></script>\n</head>')

# Add class and enablejsapi to iframes
old_iframe1 = '<iframe src="https://www.youtube.com/embed/${data.videoId}" allowfullscreen></iframe>'
new_iframe1 = '<iframe class="yt-video-player" src="https://www.youtube.com/embed/${data.videoId}?enablejsapi=1" allowfullscreen></iframe>'
html = html.replace(old_iframe1, new_iframe1)

old_iframe2 = '<iframe src="https://www.youtube.com/embed/${v.videoId}" allowfullscreen></iframe>'
new_iframe2 = '<iframe class="yt-video-player" src="https://www.youtube.com/embed/${v.videoId}?enablejsapi=1" allowfullscreen></iframe>'
html = html.replace(old_iframe2, new_iframe2)

old_render1 = "videoArea.innerHTML = `\n        <div class=\"video-master-card container fade-in\""
new_render1 = "videoArea.innerHTML = `\n        <div class=\"video-master-card container fade-in\"\n        `;\n        setTimeout(window.initYTVideos, 300);\n        videoArea.innerHTML = `\n        <div class=\"video-master-card container fade-in\""
# Wait, replacing videoArea.innerHTML like that is tricky because of backticks
old_res1 = "videoArea.innerHTML = `"
new_res1 = "setTimeout(window.initYTVideos, 300);\n      videoArea.innerHTML = `"
html = html.replace(old_res1, new_res1)

html = html.replace("verbsGrid.innerHTML = htmlContent;\n  }", "verbsGrid.innerHTML = htmlContent;\n    setTimeout(window.initYTVideos, 300);\n  }")
html = html.replace("prepsGrid.innerHTML = htmlContent;\n  }", "prepsGrid.innerHTML = htmlContent;\n    setTimeout(window.initYTVideos, 300);\n  }")
html = html.replace("phrasalGrid.innerHTML = htmlContent;\n  }", "phrasalGrid.innerHTML = htmlContent;\n    setTimeout(window.initYTVideos, 300);\n  }")

err_handler = """
  <!-- YouTube Error Handler -->
  <script>
    window.onYouTubePlayerError = function(event) {
      if (!event || !event.target || !event.target.getIframe) return;
      const iframe = event.target.getIframe();
      if (!iframe) return;
      
      const container = iframe.parentNode;
      const originalSrc = iframe.src;
      const videoIdMatch = originalSrc.match(/embed\\/([a-zA-Z0-9_\\-]{11})/);
      const vid = videoIdMatch ? videoIdMatch[1] : '';
      
      container.style.position = 'relative';
      
      container.innerHTML = `
        <div style="background:#1e1e1e; position:absolute; top:0; left:0; right:0; bottom:0; padding:40px; text-align:center; color:#fff; display:flex; flex-direction:column; justify-content:center; align-items:center; border-radius:12px; z-index:10;">
          <span style="font-size:40px; margin-bottom:16px;">⚠️</span>
          <h3 style="margin-bottom:8px; font-weight:600; font-size:18px;">영상을 불러올 수 없습니다</h3>
          <p style="color:#aaa; font-size:14px; margin-bottom:20px;">원작자에 의해 삭제되었거나 퍼가기가 금지된 영상입니다.</p>
          <a href="https://www.youtube.com/watch?v=${vid}" target="_blank" style="display:inline-flex;align-items:center;gap:8px;padding:8px 16px;background:var(--accent);color:#fff;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;">
            YouTube에서 직접 확인하기
          </a>
        </div>
      `;
    };

    window.initYTVideos = function() {
      if (typeof YT === 'undefined' || !YT.Player) return;
      const iframes = document.querySelectorAll('iframe.yt-video-player');
      iframes.forEach(ifr => {
        if (!ifr.id) {
          ifr.id = 'yt-' + Math.random().toString(36).substr(2, 9);
          new YT.Player(ifr.id, {
            events: {
              'onError': window.onYouTubePlayerError
            }
          });
        }
      });
    };
  </script>
</body>
"""
html = html.replace('</body>', err_handler)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Safe UI injection complete.")
