const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    console.log("Starting comprehensive audit...");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    
    // Capture page errors
    const errors = [];
    page.on('pageerror', err => {
        errors.push(err.toString());
    });
    page.on('console', msg => {
        if (msg.type() === 'error') {
            errors.push(msg.text());
        }
    });

    const filePath = `file:${__dirname}/index.html`;
    await page.goto(filePath, { waitUntil: 'networkidle0' });
    
    console.log("Page loaded. Checking global variables...");
    
    // Check if data is loaded correctly
    const dataCheck = await page.evaluate(() => {
        return {
            hasDayData: !!window.dayData && Object.keys(window.dayData).length > 0,
            hasDictionary: !!window.globalDictionary && Object.keys(window.globalDictionary).length > 0,
            hasCoreInsights: !!window.coreInsights && Object.keys(window.coreInsights).length > 0
        };
    });
    console.log("Data loaded:", dataCheck);

    console.log("Clicking Master course...");
    await page.waitForSelector('.master-btn');
    await page.click('.master-btn');
    await new Promise(r => setTimeout(r, 500));

    console.log("Checking Chapter 1 (Take)...");
    await page.evaluate(() => window.openChapterFromTOC(1, 1));
    await new Promise(r => setTimeout(r, 1000));
    
    const chapter1Stats = await page.evaluate(() => {
        const insightButtons = document.querySelectorAll('.insight-article .voice-btn').length;
        const vocabButtons = document.querySelectorAll('.vocab-notes .voice-btn').length;
        const sentenceCards = document.querySelectorAll('.sentence-card').length;
        return { insightButtons, vocabButtons, sentenceCards };
    });
    console.log("Chapter 1 Stats:", chapter1Stats);
    
    console.log("Checking floating TOC button...");
    const tocBtn = await page.evaluate(() => {
        const btn = document.querySelector('.floating-toc-btn');
        return btn ? btn.style.display : 'not found';
    });
    console.log("Floating TOC button display:", tocBtn);

    if (errors.length > 0) {
        console.error("Errors found during audit:", errors);
    } else {
        console.log("No console/JS errors found.");
    }
    
    await browser.close();
})();
