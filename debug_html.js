const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const htmlContent = fs.readFileSync('index.html', 'utf-8');
const dom = new JSDOM(htmlContent, { runScripts: "dangerously" });
const window = dom.window;
const document = window.document;

const dataContent = fs.readFileSync('master/data/month1.js', 'utf-8');
window.eval(dataContent.replace('window.dayData = Object.assign(window.dayData || {},', 'window.dayData = ').replace(/\)$/, ''));

const dictContent = fs.readFileSync('master/data/dictionary.js', 'utf-8');
window.eval(dictContent);

const coreInsights = fs.readFileSync('master/data/core_insights.js', 'utf-8');
window.eval(coreInsights);

try {
    // We need to simulate openChapterFromTOC or loadChapter
    // Since loadChapter is defined in a script tag in index.html, it's already parsed
    window.loadChapter(1, 1);
    
    // Check if the vocab notes have voice buttons
    setTimeout(() => {
        const renderArea = document.getElementById('chapter-render-area');
        const vocabNotes = renderArea.querySelector('.vocab-notes');
        console.log("Vocab Notes HTML:\n", vocabNotes ? vocabNotes.innerHTML : "Not found");
        
        const firstEx = renderArea.querySelector('.ex-en');
        console.log("\nFirst ex-en HTML:\n", firstEx ? firstEx.outerHTML : "Not found");
    }, 100);
} catch (e) {
    console.error(e);
}
