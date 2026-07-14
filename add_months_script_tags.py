with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_scripts = """  <script src="master/data/month8.js?v=1783994588"></script>
  <script src="master/data/month9.js?v=1783994588"></script>
  <script src="master/data/month10.js?v=1783994588"></script>
  <script src="master/data/month11.js?v=1783994588"></script>
  <script src="master/data/month12.js?v=1783994588"></script>"""

if 'month9.js' not in html:
    html = html.replace('<script src="master/data/month8.js?v=1783994588"></script>', new_scripts)
    
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Added script tags for months 9-12.")
