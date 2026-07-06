import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Isolate the master JS block
match = re.search(r'(// --- MASTER DASHBOARD JS ---.*?// ---------------------------)', html, re.DOTALL)
if match:
    js = match.group(1)
    
    # Rename functions
    renames = [
        ('loadDay', 'masterLoadDay'),
        ('renderDays', 'masterRenderDays'),
        ('renderMonths', 'masterRenderMonths'),
        ('saveProgress', 'masterSaveProgress'),
        ('escapeHTML', 'masterEscapeHTML'),
        ('showBriefing', 'masterShowBriefing'),
        ('closeBriefing', 'masterCloseBriefing'),
        ('pickVoice', 'masterPickVoice'),
        ('loadVoices', 'masterLoadVoices'),
        ('speakSentence', 'masterSpeakSentence')
    ]
    
    for old, new in renames:
        # replace function definitions and calls
        # Note: Using word boundaries
        js = re.sub(r'\b' + old + r'\b', new, js)
    
    # Put it back
    html = html.replace(match.group(1), js)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed JS conflicts successfully!")
else:
    print("Master JS block not found!")
