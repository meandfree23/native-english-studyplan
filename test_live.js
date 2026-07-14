const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    
    // Using a random query string to bypass CDN cache
    await page.goto('https://meandfree23.github.io/native-english-studyplan/?bypass=' + Date.now(), { waitUntil: 'networkidle0' });
    
    // Wait for the master button to be available and click it
    await page.waitForSelector('.master-btn');
    await page.click('.master-btn');
    
    // Click on chapter 1
    await page.evaluate(() => {
        if(typeof window.openChapterFromTOC === 'function') {
            window.openChapterFromTOC(1, 1);
        }
    });
    
    await new Promise(r => setTimeout(r, 1000));
    
    const voiceBtnCount = await page.evaluate(() => {
        const article = document.querySelector('.insight-article');
        if (!article) return 0;
        return article.querySelectorAll('.voice-btn').length;
    });
    
    console.log(`Live Insight Article voice buttons: ${voiceBtnCount}`);
    
    await page.screenshot({ path: 'live_screenshot.png' });
    await browser.close();
})();
