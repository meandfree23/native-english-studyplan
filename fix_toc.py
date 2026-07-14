import re

def fix_html():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Insert toc-view HTML if missing
    if '<div id="toc-view"' not in html:
        toc_html = """
<div id="toc-view" class="fade-in" style="display: none;">
  <div class="toc-container">
    <h1 class="toc-header">Table of Contents</h1>
    <div id="toc-content"></div>
  </div>
</div>
"""
        html = re.sub(r'(<div id="curriculum-view")', toc_html + r'\n\1', html)

    # 2. Insert back button if missing
    if 'back-to-toc' not in html:
        back_btn_html = """
    <div class="container" style="margin-top: 20px; display:flex; justify-content:flex-start;">
      <div class="back-to-toc" onclick="showView('study')">
        <span style="font-size: 16px;">←</span> 전체 목차로 돌아가기
      </div>
    </div>
"""
        html = re.sub(r'(<div id="study-plan-view">)', back_btn_html + r'\n    \1', html)

    # 3. Fix openDayFromTOC
    html = html.replace("document.getElementById('toc-view').style.display = 'block'; document.getElementById('curriculum-view').style.display = 'none'; renderTOC();\n        loadDay(day);", "document.getElementById('curriculum-view').style.display = 'flex';\n        loadDay(day);")

    # 4. Fix showView to actually show toc-view initially instead of curriculum-view
    # Wait, earlier I did:
    # html = html.replace("document.getElementById('curriculum-view').style.display = 'flex';", "document.getElementById('toc-view').style.display = 'block'; document.getElementById('curriculum-view').style.display = 'none'; renderTOC();")
    # This was wrong, because showView is called on click. But openDayFromTOC also got messed up because it contained "document.getElementById('curriculum-view').style.display = 'flex';".
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    fix_html()
