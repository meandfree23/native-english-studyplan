import re

with open('master/index.html', 'r', encoding='utf-8') as f:
    master_html = f.read()

# 1. Extract CSS
style_match = re.search(r'<style>(.*?)</style>', master_html, re.DOTALL)
css = style_match.group(1) if style_match else ''

# Replace :root with #master-view
css = css.replace(':root', '#master-view')
css = css.replace('body {', '#master-view {')
# To prevent global CSS from breaking, we can scope all selectors.
# Since it's a bit complex, we'll just rename conflicting generic classes:
# .content -> .master-content
css = css.replace('.content ', '.master-content ')
css = css.replace('.content {', '.master-content {')
css = css.replace('.tag ', '.master-tag ')
css = css.replace('.tag {', '.master-tag {')
css = css.replace('header {', '.master-header {')

# 2. Extract HTML (the body content except scripts)
body_match = re.search(r'<body>(.*?)<!-- Data files -->', master_html, re.DOTALL)
body_html = body_match.group(1) if body_match else ''
body_html = body_html.replace('class="content"', 'class="master-content"')
body_html = body_html.replace('class="tag"', 'class="master-tag"')
body_html = body_html.replace('<header>', '<div class="master-header">')
body_html = body_html.replace('</header>', '</div>')
body_html = body_html.replace('../index.html', '#')
body_html = body_html.replace('← Back to 365 Course', '← Back to Main')
# Add onclick to the back button
body_html = body_html.replace('<a href="#"', '<a href="#" onclick="showView(\'study\')"')

# 3. Extract JS
script_match = re.search(r'<script>(.*?)</script>', master_html, re.DOTALL)
js = script_match.group(1) if script_match else ''

# Prefix functions to prevent collision
js = js.replace('function init()', 'function masterInit()')
js = js.replace('init();', '') # We'll call it manually when view is shown
js = js.replace('activeMonth', 'masterActiveMonth')
js = js.replace('activeDay', 'masterActiveDay')
js = js.replace('userProgress', 'masterUserProgress')

# Now, read target index.html
with open('index.html', 'r', encoding='utf-8') as f:
    main_html = f.read()

# Insert CSS before </style>
if '</style>' in main_html:
    main_html = main_html.replace('</style>', css + '\n</style>', 1)
else:
    print("Could not find </style> in index.html")

# Insert HTML inside <body>, for example at the end of views
# Find <div id="kiwi-view">...</div> and insert after it
# Wait, let's just insert before <script src="test.js"></script>
insertion_point = '<script src="test.js"></script>'
new_view = f'''
<div id="master-view" style="display:none; height: 100vh; overflow: hidden;" class="theme-dark">
{body_html}
</div>
'''
main_html = main_html.replace(insertion_point, new_view + '\n' + insertion_point)

# Insert JS before </body>
js_wrapped = f'''
<script>
// --- MASTER DASHBOARD JS ---
{js}
// ---------------------------
</script>
'''
main_html = main_html.replace('</body>', js_wrapped + '\n</body>')

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(main_html)

print("Merge complete!")
