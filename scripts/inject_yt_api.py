import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(base_dir, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add YT Iframe API script at the top if not present
yt_script = '<script src="https://www.youtube.com/iframe_api"></script>'
if yt_script not in html:
    html = html.replace('</head>', f'  {yt_script}\n</head>')

# 2. Add global error handler
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
      
      container.innerHTML = `
        <div style="background:#1e1e1e; position:absolute; top:0; left:0; right:0; bottom:0; padding:40px; text-align:center; color:#fff; display:flex; flex-direction:column; justify-content:center; align-items:center; border-radius:12px;">
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
"""
if 'window.onYouTubePlayerError' not in html:
    html = html.replace('</body>', f'{err_handler}\n</body>')

# 3. Add class "yt-video-player" and enablejsapi=1 to all iframes
# Also make sure the parent container has position:relative for the absolute fallback div
import re

def fix_iframe(match):
    full_str = match.group(0)
    # Ensure enablejsapi=1
    if 'enablejsapi=1' not in full_str:
        full_str = re.sub(r'src="https://www.youtube.com/embed/([^"?]+)([^"]*)"', r'src="https://www.youtube.com/embed/\1\2&enablejsapi=1"', full_str)
        # remove doubled && or ?&
        full_str = full_str.replace('?&', '?').replace('&&', '&')
    
    # Add class
    if 'class="yt-video-player"' not in full_str:
        full_str = full_str.replace('<iframe ', '<iframe class="yt-video-player" ')
    
    return full_str

# We want to replace all iframes in the static HTML and generating templates
# But wait, index.html contains javascript templates making the iframes!
# e.g., `<iframe src="https://www.youtube.com/embed/${v.videoId}" allowfullscreen></iframe>`
# So we just run our regex over the entire file
html = re.sub(r'<iframe\s+[^>]*src="https://www.youtube.com/embed/[^>]*></iframe>', fix_iframe, html)

# 4. We need to call `window.initYTVideos()` after rendering any view.
# In `showView()`, `renderVerbs()`, `renderPreps()`, `renderPhrasal()`, and `loadDay()`
def add_init_call(match):
    block = match.group(0)
    return block + '\\n    setTimeout(window.initYTVideos, 300);'

# Render functions
html = re.sub(r'function renderVerbs\(\)\s*\{[^\}]+innerHTML = [^;]+;', add_init_call, html)
html = re.sub(r'function renderPreps\(\)\s*\{[^\}]+innerHTML = [^;]+;', add_init_call, html)
html = re.sub(r'function renderPhrasal\(\)\s*\{[^\}]+innerHTML = [^;]+;', add_init_call, html)
html = re.sub(r'videoArea\.innerHTML = [^;]+;', add_init_call, html)

# Also ensure video-container has position: relative if not already
html = html.replace('class="video-container" style="padding-bottom:50%;"', 'class="video-container" style="position:relative; padding-bottom:50%;"')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("YT Iframe API integration injected.")
