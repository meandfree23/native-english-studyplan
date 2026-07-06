import re

with open('master/index.html', 'r', encoding='utf-8') as f:
    master_html = f.read()

body_match = re.search(r'<body>(.*?)<!-- Data files -->', master_html, re.DOTALL)
body_html = body_match.group(1) if body_match else ''
body_html = body_html.replace('class="content"', 'class="master-content"')
body_html = body_html.replace('class="tag"', 'class="master-tag"')
body_html = body_html.replace('<header>', '<div class="master-header">')
body_html = body_html.replace('</header>', '</div>')

new_view = f'''
<div id="master-view" style="display:none;" class="theme-dark master-wrapper">
{body_html}
</div>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    main_html = f.read()

# Insert right before <div class="progress-float">
insertion_point = '<div class="progress-float">'

if insertion_point in main_html and 'id="master-view"' not in main_html:
    main_html = main_html.replace(insertion_point, new_view + '\n' + insertion_point)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(main_html)
    print("Inserted master-view successfully!")
elif 'id="master-view"' in main_html:
    print("master-view already exists.")
else:
    print("insertion_point not found!")
