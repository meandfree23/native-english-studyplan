import re

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add <script src="master/data/core_insights.js"></script>
    if "core_insights.js" not in html:
        script_tag = '<script src="master/data/core_insights.js"></script>\n'
        # Insert before the closing </head>
        html = html.replace('</head>', script_tag + '</head>')
        
    # Replace the short <p> in Chapter Header with the Core Insight Article rendering logic
    old_chapter_header = """      // Chapter Header
      html += `
      <div style="text-align: center; margin-bottom: 80px; margin-top: 40px;">
          <div style="font-size: 14px; font-weight: 800; color: var(--ember); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">CHAPTER</div>
          <h1 style="font-size: 56px; font-weight: 900; color: var(--text); margin-bottom: 24px; letter-spacing: -0.02em;">${firstDay.core} <span style="color: var(--text-dim); font-weight: 300;">|</span> ${firstDay.vT}</h1>
          <p style="font-size: 18px; color: var(--text-dim); max-width: 600px; margin: 0 auto; line-height: 1.6; word-break: keep-all;">${firstDay.vD || ''}</p>
      </div>
      `;"""
      
    new_chapter_header = """      // Chapter Header
      let insightHTML = '';
      if (window.coreInsights && window.coreInsights[firstDay.core]) {
          insightHTML = window.coreInsights[firstDay.core];
      } else {
          // Fallback if no deep insight exists yet
          insightHTML = `<p style="font-size: 18px; color: var(--text-dim); max-width: 600px; margin: 0 auto; line-height: 1.6; word-break: keep-all; text-align: center;">${firstDay.vD || ''}</p>`;
      }

      html += `
      <div style="margin-bottom: 100px; margin-top: 40px;">
          <div style="text-align: center; margin-bottom: 60px;">
              <div style="font-size: 14px; font-weight: 800; color: var(--ember); letter-spacing: 0.1em; margin-bottom: 16px; text-transform: uppercase;">CHAPTER</div>
              <h1 style="font-size: 56px; font-weight: 900; color: var(--text); margin-bottom: 24px; letter-spacing: -0.02em;">${firstDay.core} <span style="color: var(--text-dim); font-weight: 300;">|</span> ${firstDay.vT}</h1>
          </div>
          ${insightHTML}
      </div>
      `;"""
      
    html = html.replace(old_chapter_header, new_chapter_header)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    update_index_html()
