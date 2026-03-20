# Advanced Playwright MCP Workflows

## 1. Close Cookie Popups

**Strategy A: Click accept button (preferred)**
```
1. browser_snapshot()
2. // Look for: "Accept", "OK", "I agree", "Accept all"
3. browser_click(element: "Accept cookies button", ref: "e15")
4. browser_snapshot()  // Verify dismissed
```

**Strategy B: Remove via JavaScript**
```
1. browser_evaluate(expression: "(() => {
     const selectors = [
       '#cookie-banner', '#cookieModal', '.cookie-consent',
       '[class*=\"cookie\"]', '[id*=\"cookie\"]',
       '.gdpr-banner', '#onetrust-consent-sdk'
     ];
     selectors.forEach(sel => {
       document.querySelectorAll(sel).forEach(el => el.remove());
     });
     document.querySelectorAll('.modal-backdrop, [class*=\"overlay\"]')
       .forEach(el => el.remove());
     document.body.style.overflow = 'auto';
   })()")
```

Try clicking first (sets cookie to prevent reappearance), fall back to JS removal if button not found.

## 2. Scroll Page for Lazy-Loaded Content

**Scroll to bottom (simple):**
```
1. browser_evaluate(expression: "window.scrollTo(0, document.body.scrollHeight)")
2. browser_wait_for(time: 1)
3. browser_snapshot()
```

**Scroll incrementally (for lazy-load images):**
```
1. browser_evaluate(expression: "(async () => {
     const delay = ms => new Promise(r => setTimeout(r, ms));
     const maxScrolls = 50;
     let prevHeight = -1;
     for (let i = 0; i < maxScrolls; i++) {
       window.scrollBy(0, 400);
       await delay(200);
       if ((window.scrollY + window.innerHeight) >= document.body.scrollHeight) break;
     }
     window.scrollTo(0, 0);
   })()")
```

**Using keyboard:**
```
1. browser_press_key(key: "End")
2. browser_wait_for(time: 1)
3. browser_press_key(key: "Home")
```

**Using mouse wheel:** `browser_evaluate(expression: "window.scrollBy(0, 400)")` + `browser_wait_for(time: 0.3)`, repeat until bottom.

## 3. Expand Collapsed Items

**Find and click expand buttons:**
```
1. browser_snapshot()
2. // Look for: "+", "Show more", "Expand", chevron icons
3. browser_click(element: "Expand section", ref: "e20")
4. browser_snapshot()  // Repeat for remaining collapsed items
```

**Expand all via JavaScript:**
```
1. browser_evaluate(expression: "(() => {
     document.querySelectorAll('[aria-expanded=\"false\"]')
       .forEach(el => el.click());
     document.querySelectorAll('.collapsed, .accordion-button:not(.show), [data-toggle=\"collapse\"]')
       .forEach(el => el.click());
     document.querySelectorAll('details:not([open])')
       .forEach(el => el.setAttribute('open', ''));
   })()")
2. browser_wait_for(time: 0.5)
3. browser_snapshot()
```

**Patterns to look for:** `[aria-expanded="false"]`, `details` without `[open]`, buttons with "+"/"Show"/"Expand" text, elements with `collapsed` or `accordion` classes.

## 4. Full Page Screenshot (Complete Workflow)

```
1. browser_navigate(url: "https://example.com")
2. browser_wait_for(time: 2)
3. // Close cookie popup (Section 1)
4. // Scroll to load lazy content:
5. browser_evaluate(expression: "(async () => {
     const delay = ms => new Promise(r => setTimeout(r, ms));
     let prevHeight = -1;
     for (let i = 0; i < 30; i++) {
       window.scrollBy(0, 500);
       await delay(300);
       const newHeight = document.body.scrollHeight;
       if (newHeight === prevHeight) break;
       prevHeight = newHeight;
     }
     window.scrollTo(0, 0);
   })()")
6. browser_wait_for(time: 1)
7. browser_screenshot(fullPage: true, type: "jpeg")
```

**Remove fixed/sticky headers** (prevents repeating in screenshot):
```
1. browser_evaluate(expression: "document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]').forEach(el => el.style.position = 'relative')")
2. browser_screenshot(fullPage: true, type: "jpeg")
```

## 5. Find and Extract Links

**Find all PDFs:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a[href$=\".pdf\"], a[href*=\".pdf?\"]')).map(a => ({text: a.textContent.trim(), url: a.href}))")
```

**Find all videos:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a[href$=\".mp4\"], a[href$=\".webm\"], a[href$=\".mov\"], video source, iframe[src*=\"youtube\"], iframe[src*=\"vimeo\"]')).map(el => ({type: el.tagName, url: el.href || el.src}))")
```

**Find all downloadable files:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a[download], a[href$=\".pdf\"], a[href$=\".zip\"], a[href$=\".doc\"], a[href$=\".docx\"], a[href$=\".xls\"], a[href$=\".xlsx\"]')).map(a => ({text: a.textContent.trim(), url: a.href, filename: a.download || a.href.split('/').pop()}))")
```

**Find links by text pattern:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a')).filter(a => /download|attachment|pdf|document/i.test(a.textContent)).map(a => ({text: a.textContent.trim(), url: a.href}))")
```

**Complete download workflow:**
```
1. browser_navigate(url: "https://example.com/resources")
2. browser_wait_for(time: 2)
3. // Dismiss cookie popup (Section 1)
4. // Scroll to load lazy content (Section 2)
5. // Expand collapsed sections (Section 3)
6. browser_evaluate(expression: "Array.from(document.querySelectorAll('a[href$=\".pdf\"], a[download]')).map(a => ({text: a.textContent.trim(), url: a.href}))")
7. // Returns JSON array of {text, url} objects
```

**Download a specific file:**
```
1. browser_snapshot()
2. // Find download link by text or ref
3. browser_click(element: "Download PDF", ref: "e25")
4. // File downloads to browser's default download folder
```