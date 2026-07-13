import re

def update_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add dictionary.js script
    if "dictionary.js" not in html:
        script_tag = '<script src="master/data/dictionary.js"></script>\n'
        html = html.replace('</head>', script_tag + '</head>')
        
    # 2. Modify loadChapter to extract vocabulary and render
    # Find the end of the `loadChapter` loop.
    # The loop currently ends with:
    #       html += `
    #           <div style="margin-bottom: 24px; ...">
    #               ...
    #               <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px;">
    #       `;
    #       ... sentences ...
    #       html += `</div></div>`;
    #   }
    #   
    #   renderArea.innerHTML = html;

    # Wait, the end of the loadChapter loop looks like this:
    old_end = """        html += `</div></div>`;
      }
      
      renderArea.innerHTML = html;
  }"""

    new_end = """        html += `</div>`;
          
          // Generate Vocabulary Footnotes for this section
          let dayText = data.sentences.map(s => s.txt).join(' ').toLowerCase();
          // Remove punctuation
          dayText = dayText.replace(/[.,?!;:()'"]/g, '');
          let words = dayText.split(/\\s+/);
          let uniqueWords = [...new Set(words)];
          
          let foundVocab = [];
          if (window.globalDictionary) {
              uniqueWords.forEach(w => {
                  if (window.globalDictionary[w]) {
                      foundVocab.push({ word: w, meaning: window.globalDictionary[w] });
                  }
              });
          }
          
          if (foundVocab.length > 0) {
              let vocabItems = foundVocab.map(v => `<li><strong>${v.word}</strong>: ${v.meaning}</li>`).join('');
              html += `
              <div class="vocab-notes">
                  <div class="vocab-title">💡 핵심 단어 및 표현 (Vocabulary)</div>
                  <ul class="vocab-list">
                      ${vocabItems}
                  </ul>
              </div>
              `;
          }
          
          html += `</div>`;
      }
      
      renderArea.innerHTML = html;
  }"""
  
    html = html.replace(old_end, new_end)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    update_index()
