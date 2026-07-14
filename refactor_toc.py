import re
import json

def apply_refactoring():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Remove master-view entirely
    html = re.sub(r'<div id="master-view".*?<!-- Right Content Area -->.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    
    # Also just in case, find master-view manually if regex fails
    if 'id="master-view"' in html:
        # Regex might be too strict, let's try a simpler one
        html = re.sub(r'<div id="master-view".*?(<div id="curriculum-view"|<div id="review-view")', r'\1', html, flags=re.DOTALL)
        
    # 2. Add TOC View CSS
    toc_css = """
  /* --- TOC Style --- */
  .toc-container { max-width: 900px; margin: 40px auto; padding: 0 20px; font-family: 'Pretendard', sans-serif; }
  .toc-header { font-size: 32px; font-weight: 900; margin-bottom: 50px; text-align: center; color: var(--text); letter-spacing: -0.02em; }
  .toc-lesson { display: flex; margin-bottom: 60px; border-bottom: 1px solid var(--border); padding-bottom: 40px; page-break-inside: avoid; }
  .toc-lesson-number { font-size: 90px; font-weight: 900; color: #E63946; line-height: 0.8; width: 130px; flex-shrink: 0; margin-top: -5px; text-align: right; padding-right: 30px; letter-spacing: -0.05em; font-family: serif; }
  .toc-lesson-content { flex: 1; }
  .toc-lesson-title { font-size: 18px; font-weight: 800; color: var(--text); margin-bottom: 24px; text-transform: uppercase; letter-spacing: -0.01em; }
  .toc-topic-list { display: flex; flex-direction: column; gap: 14px; }
  .toc-topic-item { display: flex; justify-content: space-between; align-items: baseline; font-size: 15px; color: var(--text-dim); cursor: pointer; transition: color 0.2s; position: relative; line-height: 1.4; letter-spacing: -0.01em; }
  .toc-topic-item:hover { color: var(--accent); }
  .toc-topic-item::after { content: ''; flex: 1; border-bottom: 2px dotted rgba(0,0,0,0.1); margin: 0 16px; position: relative; top: -4px; transition: border-color 0.2s; }
  body.dark-mode .toc-topic-item::after { border-bottom: 2px dotted rgba(255,255,255,0.2); }
  .toc-topic-item:hover::after { border-color: var(--accent); opacity: 0.5; }
  .toc-topic-day { font-size: 14px; font-weight: 700; color: var(--text-dim); white-space: nowrap; font-family: monospace; letter-spacing: 0; }
  .toc-topic-item:hover .toc-topic-day { color: var(--accent); }
  .toc-topic-title { font-weight: 700; color: var(--text); }
  
  .back-to-toc { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; color: var(--text-dim); cursor: pointer; margin-bottom: 30px; padding: 8px 16px; border-radius: 8px; background: var(--surface2); transition: all 0.2s; }
  .back-to-toc:hover { color: var(--accent); background: rgba(82, 183, 136, 0.1); }
"""
    if '/* --- TOC Style --- */' not in html:
        html = html.replace('</style>', toc_css + '\n</style>')
        
    # 3. Insert TOC View HTML
    toc_html = """
<div id="toc-view" class="fade-in" style="display: none;">
  <div class="toc-container">
    <h1 class="toc-header">Table of Contents</h1>
    <div id="toc-content"></div>
  </div>
</div>
"""
    if '<div id="toc-view"' not in html:
        html = html.replace('<div id="curriculum-view"', toc_html + '\n<div id="curriculum-view"')
        
    # 4. Insert Back button in curriculum-view
    back_btn_html = """
    <div class="container" style="margin-top: 20px;">
      <div class="back-to-toc" onclick="showView('study')">
        <span style="font-size: 16px;">←</span> 목차로 돌아가기
      </div>
    </div>
"""
    if 'back-to-toc' not in html:
        html = html.replace('<div id="study-plan-view">', back_btn_html + '\n    <div id="study-plan-view">')
        
    # 5. Add JS to render TOC
    toc_js = """
    // --- TOC Logic ---
    function renderTOC() {
        const tocContent = document.getElementById('toc-content');
        if (!tocContent) return;
        
        let html = '';
        
        // Use monthInfo to define Lessons/Parts
        const parts = monthInfo;
        
        parts.forEach((part, index) => {
            html += `<div class="toc-lesson">
                <div class="toc-lesson-number">${index + 1}</div>
                <div class="toc-lesson-content">
                    <div class="toc-lesson-title">${part.theme}</div>
                    <div class="toc-topic-list">`;
            
            // Group days in this part by 'core' (Verb or Concept)
            // Assuming part 1 is day 1-30, part 2 is 31-60... wait, let's just find days that match this part dynamically, or hardcode the ranges if we don't have the mapping.
            // Actually, we don't have a mapping of day to month in dayData!
            // Let's use the known ranges: month 1 = 1-30, month 2 = 31-60...
            // But wait, there are 8 months. 8 * 30 = 240 days? Or 8 * 30 = 240. Where are the other days?
            // If we don't know the exact range, let's group all days in dayData into ranges of 30 for now, or just iterate through dayData.
            // Let's create an array of day chunks.
            const startDay = (part.id - 1) * 30 + 1;
            const endDay = startDay + 29;
            
            let currentCore = null;
            let currentSubTheme = null;
            let groupStart = -1;
            
            let groups = [];
            
            for (let d = startDay; d <= endDay; d++) {
                const data = window.dayData[d];
                if (!data) continue;
                
                let core = data.core || 'Concept';
                let vT = data.vT || '';
                
                if (core !== currentCore) {
                    if (currentCore !== null) {
                        groups.push({ core: currentCore, vT: currentSubTheme, start: groupStart, end: d - 1 });
                    }
                    currentCore = core;
                    currentSubTheme = vT;
                    groupStart = d;
                }
            }
            if (currentCore !== null) {
                groups.push({ core: currentCore, vT: currentSubTheme, start: groupStart, end: endDay });
            }
            
            groups.forEach(g => {
                const label = g.vT ? `${g.core} \\\\ ${g.vT}` : g.core;
                const range = g.start === g.end ? `Day ${g.start}` : `Day ${g.start}-${g.end}`;
                html += `
                    <div class="toc-topic-item" onclick="openDayFromTOC(${g.start})">
                        <span class="toc-topic-title">${label}</span>
                        <span class="toc-topic-day">${range}</span>
                    </div>
                `;
            });
            
            html += `</div></div></div>`;
        });
        
        tocContent.innerHTML = html;
    }
    
    function openDayFromTOC(day) {
        document.getElementById('toc-view').style.display = 'none';
        document.getElementById('curriculum-view').style.display = 'flex';
        loadDay(day);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
"""
    if 'renderTOC()' not in html:
        html = html.replace('function showView(view) {', toc_js + '\n  function showView(view) {')
        
    # 6. Update showView to toggle toc-view and curriculum-view appropriately
    # The default view 'study' should now show toc-view instead of curriculum-view
    # Wait, the nav-master points to showView('study'). Let's change showView('study') to show toc-view.
    html = html.replace("document.getElementById('curriculum-view').style.display = 'flex';", "document.getElementById('toc-view').style.display = 'block'; document.getElementById('curriculum-view').style.display = 'none'; renderTOC();")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    # Update test_puppeteer.js
    with open("test_puppeteer.js", "r", encoding="utf-8") as f:
        js = f.read()
    js = js.replace("return document.getElementById('curriculum-view') !== null;", "return document.getElementById('toc-view') !== null;")
    js = js.replace("return mw && window.getComputedStyle(mw).display !== 'none';", "const tv = document.getElementById('toc-view'); return tv && window.getComputedStyle(tv).display !== 'none';")
    with open("test_puppeteer.js", "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == "__main__":
    apply_refactoring()
    print("Refactoring applied successfully.")
