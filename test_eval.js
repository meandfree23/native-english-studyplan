const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    
    await page.setContent('<html><body><div id="test">I\'ll</div></body></html>');
    
    const htmlOutput = await page.evaluate(() => {
        const div = document.getElementById('test');
        let text = div.innerText.trim();
        // Emulate my code:
        div.innerHTML += ` <button onclick="console.log('${text.replace(/'/g, "\\'")}')">🔊</button>`;
        return div.innerHTML;
    });
    
    console.log(htmlOutput);
    
    // Test if clicking it throws an error
    try {
        await page.click('button');
        console.log("Click successful, no syntax error.");
    } catch (e) {
        console.error("Click failed:", e);
    }
    
    await browser.close();
})();
