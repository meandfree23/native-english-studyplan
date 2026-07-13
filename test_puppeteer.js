const puppeteer = require('puppeteer');

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception thrown:', err);
});

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      if (!msg.text().includes('net::ERR_FAILED') && !msg.text().includes('net::ERR_ABORTED')) {
        errors.push(msg.text());
      }
    }
  });
  page.on('pageerror', error => {
    errors.push(error.stack || error.message);
  });

  // Enable request interception to block slow external CDN connections
  await page.setRequestInterception(true);
  page.on('request', request => {
    const url = request.url();
    if (url.startsWith('file://') || url.includes('month')) {
      request.continue();
    } else {
      // Abort external network requests (fonts, CDNs, youtube) to avoid hanging offline
      request.abort();
    }
  });

  console.log('Browser page created with request interception. Navigating to index.html...');
  await page.setDefaultNavigationTimeout(30000);
  await page.setDefaultTimeout(30000);

  // Load the local index.html with domcontentloaded
  await page.goto('file://' + __dirname + '/index.html', { waitUntil: 'domcontentloaded' });
  console.log('Navigation completed.');

  // Check if button is visible
  const hasButton = await page.evaluate(() => {
    const btn = document.getElementById('nav-master');
    return btn !== null && btn.innerText.includes('365 스터디 코스');
  });

  // Check if master-view exists
  const hasMasterView = await page.evaluate(() => {
    return document.getElementById('toc-view') !== null;
  });

  // Click the button to see if it works without error
  if (hasButton) {
    await page.click('#nav-master');
    // wait a bit for any errors
    await new Promise(r => setTimeout(r, 1000));
  }

  const isMasterVisible = await page.evaluate(() => {
    const tv = document.getElementById('toc-view');
    console.log("toc-view element:", tv);
    if(tv) console.log("toc-view display style:", window.getComputedStyle(tv).display);
    return tv && window.getComputedStyle(tv).display !== 'none';
  });

  console.log('--- TEST RESULTS ---');
  console.log('JS Errors:', errors.length > 0 ? errors : 'None');
  console.log('Has Master Button:', hasButton);
  console.log('Has Master View:', hasMasterView);
  console.log('Is Master Visible after click:', isMasterVisible);
  
  try {
    await browser.close();
  } catch (e) {
    console.log('Error closing browser:', e.message);
  }
  process.exit(0);
})();
