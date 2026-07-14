import re
import sys

def main():
    file_path = "index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. CSS Updates: Tighter typography (density)
    if "letter-spacing: -0.02em;" not in html:
        html = html.replace("body {", "body {\n      letter-spacing: -0.02em;\n      line-height: 1.45;")
        
    # Make sentence cards denser
    html = html.replace("padding: 24px;", "padding: 16px 20px;")
    html = html.replace("margin-bottom: 20px;", "margin-bottom: 12px;")
    
    # 2. Extract Master Sidebar
    sidebar_match = re.search(r'(<aside class="master-sidebar">.*?</aside>)', html, re.DOTALL)
    if sidebar_match:
        sidebar_html = sidebar_match.group(1)
        # Remove master-view completely since we extract its sidebar
        html = re.sub(r'<div id="master-view".*?</div>\s*<!-- \/Master Dashboard View -->', '', html, flags=re.DOTALL)
    else:
        sidebar_html = ""

    # 3. Create the new curriculum container and wrap study-plan-view & main-content
    # Find study-plan-view
    study_plan_match = re.search(r'(<div id="study-plan-view">.*?</div>)', html, re.DOTALL)
    # Find main-content
    main_content_match = re.search(r'(<div id="main-content" class="fade-in">.*?</div>\n\n\n\n)', html, re.DOTALL)
    
    if study_plan_match and main_content_match:
        old_study = study_plan_match.group(1)
        old_main = main_content_match.group(1)
        
        # Remove old ones
        html = html.replace(old_study, "")
        html = html.replace(old_main, "")
        
        # Build new curriculum view
        new_curriculum_view = f"""
<div id="curriculum-view" style="display:flex; max-width: 1400px; margin: 0 auto; gap: 30px;">
  {sidebar_html}
  <div style="flex: 1; min-width: 0;">
    {old_study}
    {old_main}
  </div>
</div>
"""
        # Insert before review-view
        html = html.replace('<div id="review-view"', new_curriculum_view + '\n<div id="review-view"')

    # 4. Remove quiz functions
    html = re.sub(r'function startQuiz\(\) \{.*?\}\s*function checkAns\(isCorrect\) \{.*?\}\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<div id="quiz-content">.*?</div>', '', html, flags=re.DOTALL)

    # 5. Fix JS view routing to show curriculum-view
    html = html.replace("studyView.style.display = 'block';", "document.getElementById('curriculum-view').style.display = 'flex';")
    html = html.replace("const studyView = document.getElementById('study-plan-view');", "const studyView = document.getElementById('study-plan-view');\n    const curriculumView = document.getElementById('curriculum-view');")
    html = html.replace("[studyView, mainContent", "[curriculumView, studyView, mainContent")
    
    # Let's write the modified HTML back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Refactor complete.")

if __name__ == "__main__":
    main()
