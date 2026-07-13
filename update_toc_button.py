import re

def update_toc_button():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS
    old_css = """.back-to-toc { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; color: var(--text-dim); cursor: pointer; margin-bottom: 30px; padding: 8px 16px; border-radius: 8px; background: var(--surface2); transition: all 0.2s; }
  .back-to-toc:hover { color: var(--accent); background: rgba(82, 183, 136, 0.1); }"""
    
    new_css = """.back-to-toc {
    position: fixed;
    bottom: 40px;
    right: 40px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 4px 12px rgba(82, 183, 136, 0.4);
    cursor: pointer;
    z-index: 9999;
    transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
  }
  .back-to-toc:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(82, 183, 136, 0.6);
    background: #40a072;
  }
  @media (max-width: 600px) {
    .back-to-toc {
      bottom: 24px;
      right: 24px;
      width: 48px;
      height: 48px;
      font-size: 20px;
    }
  }"""
    html = html.replace(old_css, new_css)
    
    # 2. Update HTML Element
    old_html = """<div id="curriculum-view" style="display:none; max-width: 1000px; margin: 0 auto; flex-direction: column; padding-bottom: 100px;">
  <!-- Back to TOC -->
  <div style="padding: 40px 20px 0;">
    <div class="back-to-toc" onclick="showView('study')">
      <span style="font-size: 16px;">←</span> 전체 목차로 돌아가기
    </div>
  </div>
  
  <div id="chapter-render-area" style="padding: 20px; width: 100%;">"""
  
    new_html = """<div id="curriculum-view" style="display:none; max-width: 1000px; margin: 0 auto; flex-direction: column; padding-bottom: 100px;">
  <!-- Floating Back to TOC -->
  <div class="back-to-toc" onclick="showView('study')" title="목차로 돌아가기">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
  </div>
  
  <div id="chapter-render-area" style="padding: 20px; width: 100%;">"""
    
    html = html.replace(old_html, new_html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    update_toc_button()
