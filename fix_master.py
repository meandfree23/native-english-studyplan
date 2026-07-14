import re

def fix_html():
    file_path = "index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Change window.onload default view to study
    html = html.replace("showView('master');", "showView('study');")

    # Remove master view logic in showView
    html = re.sub(r"\} else if \(view === 'master'\) \{.*?\}\s*window\.scrollTo", "} window.scrollTo", html, flags=re.DOTALL)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

def fix_test():
    file_path = "test_puppeteer.js"
    with open(file_path, "r", encoding="utf-8") as f:
        js = f.read()

    js = js.replace("'master-view'", "'curriculum-view'")
    js = js.replace("Master Dashboard", "365 스터디 코스")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == "__main__":
    fix_html()
    fix_test()
    print("Fixed!")
