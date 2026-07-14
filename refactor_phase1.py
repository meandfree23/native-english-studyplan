import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update TTS Rate to 0.85
html = re.sub(r'utterance\.rate = 1\.0;', 'utterance.rate = 0.85;', html)

# 2. Add Search UI to Navbar
search_ui = """
    <!-- Search Bar -->
    <div style="position: relative; margin-left: 15px; display: inline-block;">
      <input type="text" id="global-search" placeholder="단어, 뜻 검색..." 
             style="padding: 6px 30px 6px 15px; border-radius: 20px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); font-family: inherit; font-size: 13px; width: 140px; transition: width 0.3s; outline: none;" 
             onfocus="this.style.width='200px'" 
             onblur="if(!this.value) this.style.width='140px'" 
             onkeyup="if(event.key==='Enter') executeSearch()">
      <span style="position: absolute; right: 12px; top: 7px; font-size: 13px; color: var(--text-dim); cursor: pointer;" onclick="executeSearch()">🔍</span>
    </div>
"""

# Find the end of nav-links and insert search UI before theme-toggle
if 'id="global-search"' not in html:
    html = html.replace('<button id="theme-toggle"', search_ui + '\n    <button id="theme-toggle"')

# 3. Enhance Theme Toggle (Show Moon/Sun)
theme_logic_old = """function toggleTheme() {
    const html = document.documentElement;
    const current = html.classList.contains('theme-dark') ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    html.classList.remove(`theme-${current}`);
    html.classList.add(`theme-${next}`);
    localStorage.setItem('study_theme', next);
  }"""

theme_logic_new = """function toggleTheme() {
    const html = document.documentElement;
    const current = html.classList.contains('theme-dark') ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    html.classList.remove(`theme-${current}`);
    html.classList.add(`theme-${next}`);
    localStorage.setItem('study_theme', next);
    
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.innerHTML = next === 'dark' ? '🌙 다크 모드' : '☀️ 라이트 모드';
  }"""

if theme_logic_old in html:
    html = html.replace(theme_logic_old, theme_logic_new)

# Add search logic script
search_script = """
  // --- Global Search Logic ---
  function executeSearch() {
    const query = document.getElementById('global-search').value.trim().toLowerCase();
    if (!query) {
      alert("검색어를 입력해주세요.");
      return;
    }
    
    let foundDay = null;
    let foundType = null;
    let fallbackDay = null;
    
    // First, look for exact match in core expressions
    for (let day in window.dayData) {
      const data = window.dayData[day];
      if (data.core && data.core.toLowerCase() === query) {
        foundDay = parseInt(day);
        foundType = 'core';
        break;
      }
      if (data.sentences) {
        for (let s of data.sentences) {
          if (s.txt.toLowerCase().includes(query) || s.t.includes(query)) {
            fallbackDay = parseInt(day);
          }
        }
      }
    }
    
    if (!foundDay && fallbackDay) {
        foundDay = fallbackDay;
        foundType = 'sentence';
    }
    
    if (foundDay) {
        showView('study');
        
        // Find which month contains this day
        let targetMonth = Math.ceil(foundDay / 30);
        if (targetMonth < 1) targetMonth = 1;
        
        // Close current modal if any
        const modal = document.getElementById('insight-modal');
        if (modal) modal.classList.remove('show');
        
        // Select the day in the UI
        loadDay(foundDay);
        alert("Day " + foundDay + " 에서 검색 결과를 찾았습니다.");
    } else {
        alert("'" + query + "' 에 대한 검색 결과가 없습니다.");
    }
  }
"""

if 'function executeSearch()' not in html:
    html = html.replace('// --- TOC Logic ---', search_script + '\n  // --- TOC Logic ---')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Phase 1 refactoring applied.")
