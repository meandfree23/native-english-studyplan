import re

def refactor_chapter_nuance():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    new_js_code = """
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
      
      let sectionIndex = 1;
      
      // Loop through days in this chapter
      for(let d = start; d <= end; d++) {
          const data = window.dayData[d];
          if(!data || !data.sentences || data.sentences.length === 0) continue;
          
          // Clean the title by removing "Day 8: [Get] " format
          let cleanTitle = data.governing.replace(/Day \\d+: \\[[^\\]]+\\] /, '');
          
          // Generate Nuance Map
          // Extract unique situations (s) from sentences
          let situations = data.sentences.map(s => s.s).filter((v, i, a) => v && a.indexOf(v) === i);
          let tagHtml = situations.map(sit => `<span style="display: inline-block; padding: 6px 12px; background: rgba(82, 183, 136, 0.1); color: var(--accent); border-radius: 6px; font-size: 13px; font-weight: 700; margin-right: 8px; margin-bottom: 8px;">#${sit}</span>`).join('');
          
          html += `
          <div style="margin-bottom: 100px;">
              <div style="margin-bottom: 30px; border-bottom: 2px solid var(--border); padding-bottom: 20px;">
                  <div style="font-size: 13px; font-weight: 800; color: var(--accent); opacity: 0.8; margin-bottom: 8px; letter-spacing: 0.05em;">SECTION 0${sectionIndex}</div>
                  <h2 style="font-size: 28px; font-weight: 800; color: var(--text); letter-spacing: -0.02em; margin-bottom: 16px;">${cleanTitle}</h2>
                  
                  <!-- Nuance Map Box -->
                  <div style="padding: 16px 20px; background: rgba(255,255,255,0.02); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                      <div style="margin-bottom: 10px;">${tagHtml}</div>
                      <p style="font-size: 14px; color: var(--text-dim); line-height: 1.5; margin: 0; font-weight: 400;">
                          아래 예시들은 단일한 개념이 <strong>${situations.slice(0, 3).join(', ')}${situations.length > 3 ? ' 등' : ''}</strong>의 다채로운 상황에서 어떻게 세밀한 뉘앙스 차이로 변주되는지 보여줍니다.
                      </p>
                  </div>
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
          sectionIndex++;
      }
      
      renderArea.innerHTML = html;
  }
"""

    # We need to replace the entire `function loadChapter(start, end) { ... }` block.
    # We will use regex to find it.
    pattern = r"function loadChapter\(start, end\) \{.*?\s{6}renderArea\.innerHTML = html;\n\s{2}\}"
    
    html = re.sub(pattern, lambda m: new_js_code.strip(), html, flags=re.DOTALL)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    refactor_chapter_nuance()
