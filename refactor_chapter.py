import re

def refactor_chapter():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update TOC rendering to pass start and end to openChapterFromTOC
    html = html.replace('onclick="openDayFromTOC(${g.start})"', 'onclick="openChapterFromTOC(${g.start}, ${g.end})"')

    # 2. Replace curriculum-view HTML
    # We find curriculum-view and replace its ENTIRE content up to <div class="progress-float">
    new_curriculum_html = """
<div id="curriculum-view" style="display:none; max-width: 1000px; margin: 0 auto; flex-direction: column; padding-bottom: 100px;">
  <!-- Back to TOC -->
  <div style="padding: 40px 20px 0;">
    <div class="back-to-toc" onclick="showView('study')">
      <span style="font-size: 16px;">←</span> 전체 목차로 돌아가기
    </div>
  </div>
  
  <div id="chapter-render-area" style="padding: 20px; width: 100%;">
      <!-- dynamically injected -->
  </div>
</div>
"""
    # Regex to replace curriculum-view
    html = re.sub(r'<div id="curriculum-view".*?</div>\s*</section>\s*</div>\s*(?=<div class="progress-float">)', new_curriculum_html, html, flags=re.DOTALL)
    
    # If the above failed because </section> is not there or something, let's try a safer replace
    if 'chapter-render-area' not in html:
        # Let's find exactly what to replace. curriculum-view up to the end of its div.
        # Actually it's safer to just replace the `<div id="curriculum-view" ...` until `<div class="progress-float">`
        html = re.sub(r'<div id="curriculum-view".*?(?=<div class="progress-float">)', new_curriculum_html + '\n', html, flags=re.DOTALL)

    # 3. Add JS functions
    js_code = """
  function openChapterFromTOC(start, end) {
      document.getElementById('toc-view').style.display = 'none';
      document.getElementById('curriculum-view').style.display = 'flex';
      loadChapter(start, end);
      window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function loadChapter(start, end) {
      const renderArea = document.getElementById('chapter-render-area');
      if (!renderArea) return;
      
      let html = '';
      const firstDay = window.dayData[start];
      
      if (!firstDay) {
          renderArea.innerHTML = '<p>데이터를 불러올 수 없습니다.</p>';
          return;
      }
      
      // Chapter Header
      html += `
      <div style="text-align: center; margin-bottom: 80px; margin-top: 40px;">
          <div style="font-size: 14px; font-weight: 800; color: var(--ember); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">CHAPTER</div>
          <h1 style="font-size: 56px; font-weight: 900; color: var(--text); margin-bottom: 24px; letter-spacing: -0.02em;">${firstDay.core} <span style="color: var(--text-dim); font-weight: 300;">|</span> ${firstDay.vT}</h1>
          <p style="font-size: 18px; color: var(--text-dim); max-width: 600px; margin: 0 auto; line-height: 1.6; word-break: keep-all;">${firstDay.vD || ''}</p>
      </div>
      `;
      
      // Loop through days in this chapter
      for(let d = start; d <= end; d++) {
          const data = window.dayData[d];
          if(!data || !data.sentences) continue;
          
          html += `
          <div style="margin-bottom: 100px;">
              <div style="margin-bottom: 40px; border-bottom: 2px solid var(--border); padding-bottom: 16px;">
                  <h2 style="font-size: 26px; font-weight: 800; color: var(--text); letter-spacing: -0.02em;">${data.governing}</h2>
              </div>
              <div style="display: flex; flex-direction: column; gap: 20px;">
          `;
          
          data.sentences.forEach((s, idx) => {
              html += `
              <div class="sentence-card" style="padding: 30px; background: var(--surface); border-radius: 20px; border: 1px solid var(--border); position: relative; transition: transform 0.2s, box-shadow 0.2s;">
                  <div style="font-size: 13px; font-weight: 800; color: var(--accent); margin-bottom: 12px; letter-spacing: 0.05em;">${s.n} : ${s.s}</div>
                  <div style="font-size: 24px; font-weight: 800; color: var(--text); margin-bottom: 12px; padding-right: 50px; letter-spacing: -0.01em;">${s.txt}</div>
                  <div style="font-size: 16px; color: var(--text-dim); margin-bottom: 20px;">${s.t}</div>
                  <div style="padding: 16px 20px; background: rgba(255,255,255,0.03); border-radius: 12px; font-size: 14px; color: var(--text-dim); line-height: 1.5; border: 1px solid rgba(255,255,255,0.05);">
                      <strong style="color: var(--text); font-weight: 700;">Essence:</strong> ${s.eD || ''}
                  </div>
                  <button class="voice-btn" style="position: absolute; top: 30px; right: 30px; background:none; border:none; font-size:24px; cursor:pointer; opacity:0.4; transition: opacity 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.4" onclick="speakText('${s.txt.replace(/'/g, "\\'")}')" title="듣기">🔊</button>
              </div>
              `;
          });
          
          html += `</div></div>`;
      }
      
      renderArea.innerHTML = html;
  }
"""
    # Replace openDayFromTOC function with the new functions
    html = re.sub(r'function openDayFromTOC\(day\) \{.*?\}', js_code, html, flags=re.DOTALL)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    refactor_chapter()
