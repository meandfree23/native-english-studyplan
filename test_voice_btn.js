const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    const filePath = `file:${path.join(__dirname, 'index.html')}`;
    await page.goto(filePath, { waitUntil: 'networkidle0' });
    
    // Click on the first chapter (Take)
    await page.evaluate(() => {
        window.openChapterFromTOC(1, 1);
    });
    
    // Wait for the timeout in loadChapter to fire
    await new Promise(r => setTimeout(r, 500));
    
    const voiceBtnCount = await page.evaluate(() => {
        const article = document.querySelector('.insight-article');
        if (!article) return 0;
        return article.querySelectorAll('.voice-btn').length;
    });
    
    const vocabVoiceBtnCount = await page.evaluate(() => {
        const vocabNotes = document.querySelector('.vocab-notes');
        if (!vocabNotes) return 0;
        return vocabNotes.querySelectorAll('.voice-btn').length;
    });
    
    console.log(`Insight Article voice buttons: ${voiceBtnCount}`);
    console.log(`Vocab Notes voice buttons: ${vocabVoiceBtnCount}`);
    
    await browser.close();
})();
