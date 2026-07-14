import re

def fix_html():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Rename master-view to curriculum-view
    html = html.replace('<div id="master-view" style="display:flex; max-width: 1400px; margin: 0 auto;">', '<div id="curriculum-view" style="display:none; max-width: 1400px; margin: 0 auto;">')

    # 2. Remove the sidebar
    html = re.sub(r'<!-- Left Sidebar: Months -->\s*<div class="sidebar">.*?</div>\s*</div>', '', html, flags=re.DOTALL)
    
    # 3. Add TOC View HTML right before curriculum-view (if not already there)
    if '<div id="toc-view"' not in html:
        toc_html = """
<div id="toc-view" class="fade-in" style="display: block;">
  <div class="toc-container">
    <h1 class="toc-header">Table of Contents</h1>
    <div id="toc-content"></div>
  </div>
</div>
"""
        html = html.replace('<div id="curriculum-view"', toc_html + '\n<div id="curriculum-view"')

    # 4. Insert back button in curriculum-view (above Header)
    if 'back-to-toc' not in html:
        back_btn_html = """
    <!-- Back to TOC -->
    <div style="padding: 20px 30px 0;">
      <div class="back-to-toc" onclick="showView('study')">
        <span style="font-size: 16px;">←</span> 전체 목차로 돌아가기
      </div>
    </div>
"""
        html = html.replace('<!-- Month & Day Header -->', back_btn_html + '\n    <!-- Month & Day Header -->')

    # 5. Fix Javascript functions
    # openDayFromTOC
    html = re.sub(r'function openDayFromTOC\(day\) \{.*?\}', """function openDayFromTOC(day) {
        document.getElementById('toc-view').style.display = 'none';
        document.getElementById('curriculum-view').style.display = 'flex';
        loadDay(day);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }""", html, flags=re.DOTALL)
    
    # showView
    # In showView we need to make sure 'study' shows toc-view and hides curriculum-view
    # First, let's fix the array of views to include curriculum-view
    html = html.replace("[mainContent, trainingView, kiwiView, reviewView, masterView]", "[document.getElementById('curriculum-view'), document.getElementById('toc-view'), mainContent, trainingView, kiwiView, reviewView]")
    
    # Replace 'study' logic
    html = re.sub(r'if \(view === \'study\'\) \{.*?\} else if', """if (view === 'study') {
      document.getElementById('toc-view').style.display = 'block';
      document.getElementById('curriculum-view').style.display = 'none';
      if(document.getElementById('nav-master')) document.getElementById('nav-master').classList.add('active');
      renderTOC();
    } else if""", html, flags=re.DOTALL)
    
    # 6. Replace `masterView` in JS if it still exists
    html = html.replace("const masterView = document.getElementById('master-view');", "")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    fix_html()
