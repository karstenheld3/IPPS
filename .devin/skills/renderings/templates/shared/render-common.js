/* Shared rendering helpers for all templates. Templates inline this file with the FILE include placeholder. */

function readSource() {
  var node = document.getElementById("source");
  var raw = node ? node.textContent : '""';
  try { return JSON.parse(raw); } catch (error) { return raw; }
}

function splitFrontMatter(text) {
  var retVal = { frontMatter: {}, body: text };
  if (text.indexOf("---\n") !== 0) return retVal;
  var end = text.indexOf("\n---\n", 4);
  if (end < 0) return retVal;
  var block = text.substring(4, end);
  var lines = block.split("\n");
  for (var i = 0; i < lines.length; i++) {
    var match = lines[i].match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (match) retVal.frontMatter[match[1]] = match[2].replace(/^["']|["']$/g, "");
  }
  retVal.body = text.substring(end + 5);
  return retVal;
}

function createMarkdown() {
  return window.markdownit({ html: true, linkify: true, typographer: false, breaks: true });
}

/* Reads <meta name="render-options" content="key=value; key=value"> into a plain object. Templates interpret the keys they know. */
function readRenderOptions() {
  var retVal = {};
  var meta = document.querySelector('meta[name="render-options"]');
  if (!meta) return retVal;
  var parts = meta.getAttribute("content").split(";");
  for (var i = 0; i < parts.length; i++) {
    var pair = parts[i].split("=");
    if (pair.length < 2) continue;
    retVal[pair[0].trim()] = pair.slice(1).join("=").trim();
  }
  return retVal;
}

/* Sets --code-line-height to the font-box ratio of the resolved monospace font, so box-drawing glyphs (which fill the font box) touch between rows. */
function measureCodeLineHeight() {
  var fallback = 1.2;
  var probe = document.createElement("pre");
  probe.textContent = "\u2502";
  probe.style.cssText = "position:absolute;visibility:hidden;margin:0;padding:0;border:0;";
  document.body.appendChild(probe);
  var fontFamily = getComputedStyle(probe).fontFamily;
  probe.remove();
  var context = document.createElement("canvas").getContext("2d");
  if (!context) return fallback;
  context.font = "100px " + fontFamily;
  var metrics = context.measureText("\u2502");
  if (typeof metrics.fontBoundingBoxAscent !== "number") return fallback;
  var ratio = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent) / 100;
  ratio = Math.round(Math.min(1.3, Math.max(1.1, ratio)) * 1000) / 1000;
  document.documentElement.style.setProperty("--code-line-height", String(ratio));
  return ratio;
}

function githubSlug(text, usedSlugs) {
  var slug = text.trim().toLowerCase();
  slug = slug.replace(/[^\p{L}\p{N}\s-]/gu, "");
  slug = slug.replace(/\s+/g, "-");
  var retVal = slug;
  var counter = 1;
  while (usedSlugs[retVal]) { retVal = slug + "-" + counter; counter++; }
  usedSlugs[retVal] = true;
  return retVal;
}

function addHeadingAnchors(root) {
  var usedSlugs = {};
  var headings = root.querySelectorAll("h1, h2, h3, h4, h5, h6");
  for (var i = 0; i < headings.length; i++) {
    if (!headings[i].id) headings[i].id = githubSlug(headings[i].textContent, usedSlugs);
  }
}

function convertTaskLists(root) {
  var items = root.querySelectorAll("li");
  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var first = item.firstChild;
    if (first && first.nodeType === 1 && first.tagName === "P") first = first.firstChild;
    if (!first || first.nodeType !== 3) continue;
    var match = first.nodeValue.match(/^\[([ xX])\]\s+/);
    if (!match) continue;
    first.nodeValue = first.nodeValue.substring(match[0].length);
    var box = document.createElement("input");
    box.type = "checkbox"; box.disabled = true; box.checked = match[1] !== " ";
    first.parentNode.insertBefore(box, first);
    item.classList.add("task-list-item");
    if (item.parentNode) item.parentNode.classList.add("contains-task-list");
  }
}

function longestLineLength(text) {
  var lines = text.split("\n");
  var retVal = 0;
  for (var i = 0; i < lines.length; i++) { if (lines[i].length > retVal) retVal = lines[i].length; }
  return retVal;
}

function classifyCodeBlocks(root) {
  var threshold = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--code-wrap-threshold"), 10) || 110;
  var blocks = root.querySelectorAll("pre");
  for (var i = 0; i < blocks.length; i++) {
    var pre = blocks[i];
    var code = pre.querySelector("code");
    var text = code ? code.textContent : pre.textContent;
    if (longestLineLength(text) > threshold) pre.classList.add("wrap");
    if (code && code.className) {
      var lang = code.className.match(/language-([\w+#.-]+)/);
      if (lang && lang[1] !== "text") pre.setAttribute("data-lang", lang[1]);
    }
    if (pre.offsetHeight > 600) pre.classList.add("tall");
  }
}

function contentWidth(element) {
  var style = getComputedStyle(element);
  return element.getBoundingClientRect().width - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
}

function tableOverflows(table) {
  var parent = table.parentElement;
  return !!parent && table.getBoundingClientRect().width > contentWidth(parent) + 1;
}

/* Fits tables into their container: 6+ columns start at dense-2, then dense steps up to 3 while the table is wider than its container.
   Tables inside .card (columns template) are skipped - they use fixed layout. Options: tableFont=condensed, landscapeTables=N (columns that trigger class landscape). */
function fitTables(root, options) {
  var landscapeColumns = options && options.landscapeTables ? parseInt(options.landscapeTables, 10) || 0 : 0;
  var condensed = !!options && options.tableFont === "condensed";
  var tables = root.querySelectorAll("table");
  var retVal = 0;
  for (var i = 0; i < tables.length; i++) {
    var table = tables[i];
    if (table.closest(".card")) continue;
    var firstRow = table.querySelector("tr");
    var columnCount = firstRow ? firstRow.children.length : 0;
    if (condensed) table.classList.add("condensed");
    var step = 0;
    if (columnCount >= 6) { table.classList.add("wide"); step = 2; table.classList.add("dense-2"); }
    while (step < 3 && tableOverflows(table)) {
      table.classList.remove("dense-" + step);
      step++;
      table.classList.add("dense-" + step);
    }
    if (tableOverflows(table)) { table.classList.add("overflow"); retVal++; }
    if (landscapeColumns > 0 && columnCount >= landscapeColumns) table.classList.add("landscape");
  }
  document.body.dataset.tableOverflow = String(retVal);
  return retVal;
}

function postProcess(root, options) {
  addHeadingAnchors(root);
  convertTaskLists(root);
  classifyCodeBlocks(root);
  fitTables(root, options);
}

function firstHeadingText(root) {
  var heading = root.querySelector("h1");
  return heading ? heading.textContent.trim() : "";
}

function addPageHeader(title, options) {
  var style = document.createElement("style");
  var text = JSON.stringify(title);
  var rules = "@page { @top-center { content: " + text + "; font-family: \"Segoe UI\", \"Noto Sans\", Arial, sans-serif; font-size: 8pt; color: #536078; } }";
  if (options && options.skipFirstPage) rules += "\n@page :first { @top-center { content: none; } }";
  style.textContent = rules;
  document.head.appendChild(style);
}

function finishRendering() {
  var done = function () { document.body.dataset.rendered = "true"; };
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(done, done); } else { done(); }
}
