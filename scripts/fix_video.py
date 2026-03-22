"""
iframe 태그에 allow/referrerpolicy 속성 추가 및 로컬 파일 동영상 로드 버그 수정.
또한 study-plan-video-area 렌더링 코드를 개선하여 YouTube 링크 fallback 버튼 추가.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix all iframe tags: add allow and referrerpolicy
old_iframe = '<iframe src="https://www.youtube.com/embed/${data.videoId}" allowfullscreen></iframe>'
new_iframe = '<iframe src="https://www.youtube.com/embed/${data.videoId}?rel=0&modestbranding=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
html = html.replace(old_iframe, new_iframe)

# 2. Fix verbs/preps/phrasal video iframes (use v.videoId pattern)
old_iframe2 = '<iframe src="https://www.youtube.com/embed/${v.videoId}" allowfullscreen></iframe>'
new_iframe2 = '<iframe src="https://www.youtube.com/embed/${v.videoId}?rel=0&modestbranding=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
html = html.replace(old_iframe2, new_iframe2)

count = html.count('allowfullscreen referrerpolicy="strict-origin-when-cross-origin"')
print(f"Fixed {count} iframe(s)")

# 3. Replace video rendering section in loadDay to add fallback button
old_video_block = '''    // Update Video Area
    const videoArea = document.getElementById('study-plan-video-area');
    if (videoArea && data.videoId) {
      videoArea.innerHTML = `
        <div class="video-master-card container fade-in" style="margin-bottom: 40px; padding:0;">
          <div class="video-container" style="padding-bottom: 50%;">
            <iframe src="https://www.youtube.com/embed/${data.videoId}?rel=0&modestbranding=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>
          </div>
          <div style="padding: 24px;">
            <p class="section-title">Master Class</p>
            <h3 style="font-size: 20px; margin-bottom: 8px;">🎬 Day ${day} 마스터 클래스</h3>
            <p style="font-size: 14px; color: var(--text-dim);">${data.title}의 품격을 높여주는 마스터 영상입니다.</p>
          </div>
        </div>
      `;
    }'''

new_video_block = '''    // Update Video Area
    const videoArea = document.getElementById('study-plan-video-area');
    if (videoArea && data.videoId) {
      videoArea.innerHTML = `
        <div class="video-master-card container fade-in" style="margin-bottom: 40px; padding:0;">
          <div class="video-container" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; background:#000;">
            <iframe
              src="https://www.youtube.com/embed/${data.videoId}?rel=0&modestbranding=1&enablejsapi=1"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
              referrerpolicy="strict-origin-when-cross-origin"
              style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
            ></iframe>
          </div>
          <div style="padding: 24px;">
            <p class="section-title">Master Class</p>
            <h3 style="font-size: 20px; margin-bottom: 8px;">🎬 Day ${day} 마스터 클래스</h3>
            <p style="font-size: 14px; color: var(--text-dim); margin-bottom: 12px;">${data.title}의 품격을 높여주는 마스터 영상입니다.</p>
            <a href="https://www.youtube.com/watch?v=${data.videoId}" target="_blank" rel="noopener noreferrer"
               style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:var(--accent);color:#fff;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;">
              ▶ YouTube에서 열기
            </a>
          </div>
        </div>
      `;
    }'''

if old_video_block in html:
    html = html.replace(old_video_block, new_video_block)
    print("Fixed study-plan video block")
else:
    # try without the fixed iframe (in case the first replacement already applied)
    print("WARNING: video block not found exactly. Trying partial match...")
    # Find and fix just the videoArea assignment using line marker
    import re
    # Replace the key iframe line inside the video block
    html = re.sub(
        r'videoArea\.innerHTML = `([\s\S]*?)`\s*;',
        lambda m: fix_video_inner(m.group(0), data_videoId_var='data.videoId'),
        html,
        count=1
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done. index.html saved.")
