// Usage: NODE_PATH=$(npm root -g) node site_check.js <site-root-dir> <https://domain.com>
// Loads every sitemap URL from the local checkout in headless Chromium (iPhone 13) and prints problems only.
const { chromium, devices } = require('playwright');
const fs = require('fs'), path = require('path');
const R = path.resolve(process.argv[2] || '.');
const D = (process.argv[3] || '').replace(/\/$/, '');
const sm = fs.readFileSync(R + '/sitemap.xml', 'utf8');
const pages = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].replace(D, '').replace(/^\//, '')).map(p => (p === '' || p.endsWith('/')) ? p + 'index.html' : p);
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext(devices['iPhone 13']); let bad = 0;
  for (const pg of pages) {
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    if (!fs.existsSync(R + '/' + pg)) { console.log('MISSING FILE', pg); bad++; continue; }
    await p.goto('file://' + R + '/' + pg); await p.waitForTimeout(500);
    const r = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, w: innerWidth, tl: document.title.length,
      d: ((document.querySelector('meta[name=description]') || {}).content || '').length, h1: document.querySelectorAll('h1').length,
      can: !!document.querySelector('link[rel=canonical]'),
      ld: [...document.querySelectorAll('script[type="application/ld+json"]')].filter(s => { try { JSON.parse(s.textContent); return false; } catch (e) { return true; } }).length,
      links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => !/^(https?:|mailto:|tel:|#|data:|javascript:|\/)/.test(h)) }));
    const base = path.dirname(R + '/' + pg);
    const broken = [...new Set(r.links)].filter(h => { const t = path.resolve(base, h.split('#')[0].split('?')[0]); return !(fs.existsSync(t) && (fs.statSync(t).isFile() || fs.existsSync(t + '/index.html'))); });
    const issues = [];
    if (r.sw > r.w) issues.push(`horizontal scroll ${r.sw}/${r.w}`);
    if (r.tl > 60) issues.push(`title ${r.tl} chars`);
    if (r.d < 120 || r.d > 160) issues.push(`description ${r.d} chars`);
    if (r.h1 !== 1) issues.push(`${r.h1} H1s`);
    if (!r.can) issues.push('no canonical');
    if (r.ld) issues.push(`${r.ld} invalid JSON-LD`);
    if (broken.length) issues.push('broken links: ' + broken.join(', '));
    if (errs.length) issues.push('JS errors: ' + errs.join(' | '));
    if (issues.length) { bad++; console.log(pg + ': ' + issues.join('; ')); }
    await p.close();
  }
  console.log(`checked ${pages.length} pages, ${bad} with issues`); await b.close();
})();
