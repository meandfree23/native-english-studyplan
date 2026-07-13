import re

def update_layout():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # We need to replace the grid gap
    old_grid = 'display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px;'
    new_grid = 'display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px;'
    
    html = html.replace(old_grid, new_grid)
    
    # We need to replace the sentence card layout
    old_card = """              <div class="sentence-card" style="padding: 20px 24px; background: var(--surface); border-radius: 16px; border: 1px solid var(--border); position: relative; transition: transform 0.2s, box-shadow 0.2s; display: flex; flex-direction: column;">
                  <div style="font-size: 12px; font-weight: 800; color: var(--accent); margin-bottom: 6px; letter-spacing: 0.05em;">${s.n} : ${s.s}</div>
                  <div style="font-size: 20px; font-weight: 800; color: var(--text); margin-bottom: 6px; padding-right: 40px; letter-spacing: -0.01em;">${s.txt}</div>
                  <div style="font-size: 14px; color: var(--text-dim); margin-bottom: 16px; flex-grow: 1;">${s.t}</div>
                  <div style="padding: 10px 14px; background: rgba(255,255,255,0.03); border-radius: 8px; font-size: 13px; color: var(--text-dim); line-height: 1.4; border: 1px solid rgba(255,255,255,0.05);">
                      <strong style="color: var(--text); font-weight: 700;">Essence:</strong> ${s.eD || ''}
                  </div>
                  <button class="voice-btn" style="position: absolute; top: 20px; right: 20px; background:none; border:none; font-size:22px; cursor:pointer; opacity:0.4; transition: opacity 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.4" onclick="speakText('${s.txt.replace(/'/g, "\\\\'")}')" title="듣기">🔊</button>
              </div>"""

    new_card = """              <div class="sentence-card" style="padding: 16px 20px; background: var(--surface); border-radius: 14px; border: 1px solid var(--border); position: relative; transition: transform 0.2s, box-shadow 0.2s; display: flex; flex-direction: column;">
                  <div style="font-size: 11px; font-weight: 800; color: var(--accent); margin-bottom: 4px; letter-spacing: 0.05em;">${s.n} : ${s.s}</div>
                  <div style="font-size: 18px; font-weight: 800; color: var(--text); margin-bottom: 4px; padding-right: 36px; letter-spacing: -0.01em;">${s.txt}</div>
                  <div style="font-size: 13px; color: var(--text-dim); margin-bottom: 12px; flex-grow: 1;">${s.t}</div>
                  <div style="padding: 8px 12px; background: rgba(255,255,255,0.03); border-radius: 8px; font-size: 12px; color: var(--text-dim); line-height: 1.4; border: 1px solid rgba(255,255,255,0.05);">
                      <strong style="color: var(--text); font-weight: 700;">Essence:</strong> ${s.eD || ''}
                  </div>
                  <button class="voice-btn" style="position: absolute; top: 16px; right: 16px; background:none; border:none; font-size:20px; cursor:pointer; opacity:0.4; transition: opacity 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.4" onclick="speakText('${s.txt.replace(/'/g, "\\\\'")}')" title="듣기">🔊</button>
              </div>"""
              
    html = html.replace(old_card, new_card)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    update_layout()
