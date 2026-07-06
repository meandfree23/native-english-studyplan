import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the showView function
old_showView = '''  function showView(view) {
    const studyView = document.getElementById('study-plan-view');
    const mainContent = document.getElementById('main-content');
    const verbsView = document.getElementById('verbs-view');
    const prepsView = document.getElementById('preps-view');
    const phrasalView = document.getElementById('phrasal-view');
    const grammarView = document.getElementById('grammar-view');
    const trainingView = document.getElementById('training-view');
    const kiwiView = document.getElementById('kiwi-view');
    
    const navStudy = document.getElementById('nav-study');
    const navVerbs = document.getElementById('nav-verbs');
    const navPreps = document.getElementById('nav-preps');
    const navPhrasal = document.getElementById('nav-phrasal');
    const navGrammar = document.getElementById('nav-grammar');
    const navTraining = document.getElementById('nav-training');
    const navKiwi = document.getElementById('nav-kiwi');

    // Reset all
    [studyView, mainContent, verbsView, prepsView, phrasalView, grammarView, trainingView, kiwiView].forEach(v => { if(v) v.style.display = 'none'; });
    [navStudy, navVerbs, navPreps, navPhrasal, navGrammar, navTraining, navKiwi].forEach(n => { if(n) n.classList.remove('active'); });

    if (view === 'study') {
      studyView.style.display = 'block';
      mainContent.style.display = 'block';
      navStudy.classList.add('active');
    } else if (view === 'verbs') {
      verbsView.style.display = 'block';
      navVerbs.classList.add('active');
      renderVerbs();
    } else if (view === 'preps') {
      prepsView.style.display = 'block';
      navPreps.classList.add('active');
      renderPreps();
    } else if (view === 'phrasal') {
      phrasalView.style.display = 'block';
      navPhrasal.classList.add('active');
      renderPhrasal();
    } else if (view === 'grammar') {
      grammarView.style.display = 'block';
      navGrammar.classList.add('active');
      renderGrammar();
    } else if (view === 'kiwi') {
      kiwiView.style.display = 'block';
      if(navKiwi) navKiwi.classList.add('active');
      renderKiwi();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }'''

new_showView = '''  function showView(view) {
    const studyView = document.getElementById('study-plan-view');
    const mainContent = document.getElementById('main-content');
    const verbsView = document.getElementById('verbs-view');
    const prepsView = document.getElementById('preps-view');
    const phrasalView = document.getElementById('phrasal-view');
    const grammarView = document.getElementById('grammar-view');
    const trainingView = document.getElementById('training-view');
    const kiwiView = document.getElementById('kiwi-view');
    const masterView = document.getElementById('master-view');
    
    const navStudy = document.getElementById('nav-study');
    const navVerbs = document.getElementById('nav-verbs');
    const navPreps = document.getElementById('nav-preps');
    const navPhrasal = document.getElementById('nav-phrasal');
    const navGrammar = document.getElementById('nav-grammar');
    const navTraining = document.getElementById('nav-training');
    const navKiwi = document.getElementById('nav-kiwi');
    const navMaster = document.getElementById('nav-master');

    // Reset all
    [studyView, mainContent, verbsView, prepsView, phrasalView, grammarView, trainingView, kiwiView, masterView].forEach(v => { if(v) v.style.display = 'none'; });
    [navStudy, navVerbs, navPreps, navPhrasal, navGrammar, navTraining, navKiwi, navMaster].forEach(n => { if(n) n.classList.remove('active'); });

    // Handle hero visibility
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
      if (view === 'study') {
        heroSection.style.display = 'block';
      } else {
        heroSection.style.display = 'none';
      }
    }

    if (view === 'study') {
      studyView.style.display = 'block';
      mainContent.style.display = 'block';
      if(navStudy) navStudy.classList.add('active');
    } else if (view === 'verbs') {
      verbsView.style.display = 'block';
      if(navVerbs) navVerbs.classList.add('active');
      renderVerbs();
    } else if (view === 'preps') {
      prepsView.style.display = 'block';
      if(navPreps) navPreps.classList.add('active');
      renderPreps();
    } else if (view === 'phrasal') {
      phrasalView.style.display = 'block';
      if(navPhrasal) navPhrasal.classList.add('active');
      renderPhrasal();
    } else if (view === 'grammar') {
      grammarView.style.display = 'block';
      if(navGrammar) navGrammar.classList.add('active');
      if(typeof renderGrammar === 'function') renderGrammar();
    } else if (view === 'kiwi') {
      kiwiView.style.display = 'block';
      if(navKiwi) navKiwi.classList.add('active');
      if(typeof renderKiwi === 'function') renderKiwi();
    } else if (view === 'master') {
      masterView.style.display = 'flex'; // master uses flex
      if(navMaster) navMaster.classList.add('active');
      if(typeof masterInit === 'function') {
        if (!window.masterInitialized) {
            masterInit();
            window.masterInitialized = true;
        } else {
            if(typeof masterLoadDay === 'function') masterLoadDay(masterActiveDay);
        }
      }
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }'''

if old_showView in html:
    html = html.replace(old_showView, new_showView)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched showView successfully!")
else:
    print("old_showView not found!")
