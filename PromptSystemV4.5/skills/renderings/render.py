"""Render Markdown files to HTML and PDF.

Step 1: inject the Markdown into an HTML template that renders it in the browser (styles + markdown-it inlined).
Step 2: print the HTML with headless Chromium (Playwright) to PDF.

Usage:
  python render.py <inputs...> [--format html|pdf|both] [--template NAME|PATH] [--options TEXT] [--output-dir DIR] [--paper A4|Letter] [--landscape]
                   [--lang xx] [--title TEXT] [--render-timeout S] [--keep-html] [--overwrite] [--recursive] [--quiet] [--list-templates]

Exit codes: 0 all ok or skipped, 1 at least one input failed, 2 setup or argument error.
"""
import argparse
import glob
import html
import json
import re
import shutil
import sys
import time
import urllib.parse
from pathlib import Path

SCRIPT_FOLDER = Path(__file__).resolve().parent
TEMPLATES_FOLDER = SCRIPT_FOLDER / "templates"
INCLUDE_PATTERN = re.compile(r"\{\{FILE:([^}]+)\}\}")
PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z_]+(?::[^}]*)?\}\}")
RENDER_OPTIONS_PATTERN = re.compile(r'(<meta\s+name="render-options"\s+content=")([^"]*)(")')
PROMPTSYSTEM_LINE_PATTERN = re.compile(r"^[ \t]*<PromptSystem\b[^>]*>[ \t]*\r?\n?", re.MULTILINE)
# Image sources: ![alt](<path with spaces>), ![alt](path "title"), raw <img src="path">
IMAGE_SOURCE_PATTERNS = [re.compile(r"!\[[^\]]*\]\(\s*<([^>]+)>"), re.compile(r"!\[[^\]]*\]\(\s*([^)\s<][^)\s]*)"), re.compile(r"<img\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)]
CODE_SPAN_PATTERN = re.compile(r"(`+)(.+?)\1")
FENCE_PATTERN = re.compile(r"^[ \t]*(`{3,}|~{3,})")
INSTALL_HINT = 'Run: "{python}" -m playwright install chromium-headless-shell'


class SetupError(Exception):
  """Argument or environment problem detected before or during setup. Exit code 2."""


def parse_arguments():
  parser = argparse.ArgumentParser(description="Render Markdown to HTML and PDF via an HTML template and headless Chromium.")
  parser.add_argument("inputs", nargs="*", help="Markdown files, folders, or glob patterns")
  parser.add_argument("--format", choices=["html", "pdf", "both"], default="both")
  parser.add_argument("--template", default="document", help="template name in templates/ or path to an HTML file")
  parser.add_argument("--options", help='override the template <meta name="render-options"> content, e.g. "columns=DE:DE,EN:EN,PT:PT; markers=^###\\s*DE,^###\\s*EN,^###\\s*PT"')
  parser.add_argument("--output-dir", help="output folder (default: next to each input)")
  parser.add_argument("--paper", choices=["A4", "Letter"], help="override template page size")
  parser.add_argument("--landscape", action="store_true", help="override template orientation")
  parser.add_argument("--lang", default=None, help="html lang attribute (default: front matter lang:, else en)")
  parser.add_argument("--title", help="override document title (single input)")
  parser.add_argument("--render-timeout", type=float, default=30.0, help="seconds to wait for the template to finish rendering")
  parser.add_argument("--keep-html", action="store_true", help="keep HTML when --format pdf")
  parser.add_argument("--overwrite", action="store_true")
  parser.add_argument("--recursive", action="store_true", help="include subfolders for folder inputs")
  parser.add_argument("--quiet", action="store_true", help="print failures and summary only")
  parser.add_argument("--list-templates", action="store_true")
  return parser.parse_args()


def resolve_inputs(patterns, recursive):
  retVal = []
  for pattern in patterns:
    path = Path(pattern)
    if path.is_file():
      retVal.append(path.resolve())
    elif path.is_dir():
      iterator = path.rglob("*.md") if recursive else path.glob("*.md")
      for candidate in iterator:
        retVal.append(candidate.resolve())
    else:
      for match in glob.glob(pattern, recursive=recursive):
        candidate = Path(match)
        if candidate.is_file() and candidate.suffix.lower() == ".md":
          retVal.append(candidate.resolve())
  unique = []
  seen = set()
  for candidate in sorted(retVal):
    if candidate in seen or candidate.name.startswith("."):
      continue
    seen.add(candidate)
    unique.append(candidate)
  return unique


def list_templates():
  retVal = []
  for candidate in sorted(TEMPLATES_FOLDER.glob("*.html")):
    retVal.append(candidate.stem)
  return retVal


def load_template(name_or_path):
  candidate = TEMPLATES_FOLDER / f"{name_or_path}.html"
  if not candidate.is_file():
    candidate = Path(name_or_path)
  if not candidate.is_file():
    raise SetupError(f"Template '{name_or_path}' not found. Available: {', '.join(list_templates())}")
  text = candidate.read_text(encoding="utf-8")
  text = resolve_includes(text)
  if "{{MARKDOWN}}" not in text:
    raise SetupError(f"Template '{candidate.name}' lacks the {{{{MARKDOWN}}}} placeholder")
  return text


def resolve_includes(text):
  def replace(match):
    relative = match.group(1).strip()
    target = (TEMPLATES_FOLDER / relative).resolve()
    if TEMPLATES_FOLDER.resolve() not in target.parents:
      raise SetupError(f"Include outside templates folder: {relative}")
    if not target.is_file():
      raise SetupError(f"Include not found: {target}")
    return target.read_text(encoding="utf-8")
  return INCLUDE_PATTERN.sub(replace, text)


def read_document(path, lang_override, title_override):
  raw = path.read_bytes()
  text = raw.decode("utf-8-sig")
  text = text.replace("\r\n", "\n").replace("\r", "\n")
  text = PROMPTSYSTEM_LINE_PATTERN.sub("", text)
  front = read_front_matter(text)
  lang = lang_override or front.get("lang") or "en"
  title = title_override or front.get("title") or first_heading(text) or path.stem
  return {"path": path, "title": title, "lang": lang, "text": text, "images": find_image_sources(text)}


def first_heading(text):
  in_fence = False
  for line in text.split("\n"):
    stripped = line.strip()
    if stripped.startswith("```") or stripped.startswith("~~~"):
      in_fence = not in_fence
      continue
    if not in_fence and stripped.startswith("# "):
      return stripped[2:].strip()
  return ""


def read_front_matter(text):
  retVal = {}
  # Same block boundaries as splitFrontMatter() in render-common.js, so only a block the template hides supplies lang/title
  if not text.startswith("---\n"):
    return retVal
  end = text.find("\n---\n", 4)
  if end < 0:
    return retVal
  for line in text[4:end].split("\n"):
    if ":" not in line:
      continue
    key, value = line.split(":", 1)
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
      value = value[1:-1].strip()
    if key.strip() and value:
      retVal[key.strip().lower()] = value
  return retVal


def blank_code(text):
  # Image syntax inside code fences and code spans is an example, not an image
  lines = []
  fence = ""
  for line in text.split("\n"):
    match = FENCE_PATTERN.match(line)
    if fence:
      if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence) and line.strip() == match.group(1):
        fence = ""
      lines.append("")
      continue
    if match:
      fence = match.group(1)
      lines.append("")
      continue
    lines.append(CODE_SPAN_PATTERN.sub("", line))
  retVal = "\n".join(lines)
  return retVal


def find_image_sources(text):
  retVal = []
  scanned = blank_code(text)
  found = []
  for pattern in IMAGE_SOURCE_PATTERNS:
    for match in pattern.finditer(scanned):
      found.append((match.start(), match.group(1)))
  found.sort()
  for item in found:
    source = item[1].strip()
    lowered = source.lower()
    if lowered.startswith(("http://", "https://", "//", "data:")):
      continue
    for separator in ("?", "#"):
      if separator in source:
        source = source.split(separator, 1)[0]
    source = urllib.parse.unquote(source)
    if source and source not in retVal:
      retVal.append(source)
  return retVal


def copy_images(document, output_dir, overwrite):
  retVal = []
  input_folder = document["path"].parent.resolve()
  output_folder = Path(output_dir).resolve() if output_dir else input_folder
  elsewhere = output_folder != input_folder
  not_found = []
  outside = []
  for source in document["images"]:
    local = source[len("file:///"):] if source.lower().startswith("file:///") else source
    absolute = local.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", local) is not None
    image_path = (Path(local) if absolute else input_folder / local).resolve()
    if not image_path.is_file():
      not_found.append(source)
      continue
    if absolute or input_folder not in image_path.parents:
      if elsewhere:
        outside.append(source)
      continue
    if not elsewhere:
      continue
    target = output_folder / image_path.relative_to(input_folder)
    if target.exists():
      source_stat = image_path.stat()
      target_stat = target.stat()
      if source_stat.st_size == target_stat.st_size and int(source_stat.st_mtime) == int(target_stat.st_mtime):
        continue
      if not overwrite:
        continue
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image_path, target)
  if not_found:
    retVal.append(f"WARNING: {len(not_found)} image{'s' if len(not_found) != 1 else ''} not found (first: {not_found[0]})")
  if outside:
    retVal.append(f"WARNING: {len(outside)} image path{'s' if len(outside) != 1 else ''} outside the input folder (first: {outside[0]})")
  return retVal


def add_warning(entry, warning):
  if warning:
    entry["warning"] = f"{entry['warning']} | {warning}" if entry["warning"] else warning


def encode_markdown(text):
  return json.dumps(text, ensure_ascii=False).replace("<", "\\u003c")


def apply_options(template_text, options):
  if not options:
    return template_text
  if not RENDER_OPTIONS_PATTERN.search(template_text):
    raise SetupError("--options given but the template has no <meta name=\"render-options\"> tag")
  escaped = html.escape(options, quote=True)
  return RENDER_OPTIONS_PATTERN.sub(lambda match: match.group(1) + escaped + match.group(3), template_text, count=1)


def inject(template_text, document, paper, landscape):
  retVal = template_text.replace("{{MARKDOWN}}", encode_markdown(document["text"]))
  retVal = retVal.replace("{{TITLE}}", html.escape(document["title"], quote=True))
  retVal = retVal.replace("{{LANG}}", html.escape(document["lang"], quote=True))
  if paper or landscape:
    size = paper or "A4"
    orientation = "landscape" if landscape else "portrait"
    retVal = retVal.replace("</head>", f"<style>@page {{ size: {size} {orientation}; }}</style>\n</head>", 1)
  leftover = PLACEHOLDER_PATTERN.search(retVal)
  if leftover:
    raise SetupError(f"Unresolved placeholder in template: {leftover.group(0)}")
  return retVal


def output_path_for(document, output_dir, suffix):
  folder = Path(output_dir).resolve() if output_dir else document["path"].parent
  return folder / (document["path"].stem + suffix)


def write_html(html_text, target, overwrite):
  if target.exists() and not overwrite:
    return "skipped-exists"
  target.parent.mkdir(parents=True, exist_ok=True)
  target.write_text(html_text, encoding="utf-8")
  return "ok"


def launch_chromium(playwright, log):
  try:
    retVal = playwright.chromium.launch()
    log(f"  Chromium {retVal.version}")
    return retVal
  except Exception:
    pass
  candidates = sorted(Path.home().glob("AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe"))
  if candidates:
    retVal = playwright.chromium.launch(executable_path=str(candidates[-1]))
    log(f"  Chromium {retVal.version} (fallback: installed build {candidates[-1].parent.parent.name})")
    return retVal
  try:
    retVal = playwright.chromium.launch(channel="chrome")
    log(f"  Chromium {retVal.version} (fallback: system Chrome)")
    return retVal
  except Exception as error:
    raise SetupError("No Chromium available. " + INSTALL_HINT.format(python=sys.executable) + f" ({str(error).splitlines()[0]})")


def print_pdf(page, html_path, pdf_path, render_timeout):
  # Template scripts measure and align at load time; print media + a viewport close to the printed content width keeps those measurements valid for print
  page.emulate_media(media="print")
  page.goto(html_path.resolve().as_uri(), wait_until="load")
  page.wait_for_selector('body[data-rendered="true"]', timeout=int(render_timeout * 1000), state="attached")
  page.evaluate("() => document.fonts.ready")
  pdf_path.parent.mkdir(parents=True, exist_ok=True)
  page.pdf(path=str(pdf_path), print_background=True, prefer_css_page_size=True, outline=True, tagged=True)
  facts = page.evaluate("() => [parseInt(document.body.dataset.tableOverflow || '0', 10), parseInt(document.body.dataset.imageBroken || '0', 10), document.body.dataset.imageBrokenFirst || '']")
  retVal = {"table_overflow": facts[0] or 0, "image_broken": facts[1] or 0, "image_broken_first": facts[2]}
  return retVal


def pdf_page_count(pdf_path):
  try:
    import fitz
    with fitz.open(str(pdf_path)) as pdf:
      return pdf.page_count
  except Exception:
    return 0


def format_size(path):
  return f"{max(1, path.stat().st_size // 1024)} KB"


def main():
  args = parse_arguments()
  log = (lambda message: None) if args.quiet else (lambda message: print(message, flush=True))
  if args.list_templates:
    for name in list_templates():
      print(name)
    return 0
  if not args.inputs:
    print("ERROR: no inputs given. Use --help for usage.", file=sys.stderr)
    return 2
  try:
    template_text = apply_options(load_template(args.template), args.options)
  except SetupError as error:
    print(f"ERROR: {error}", file=sys.stderr)
    return 2
  documents_paths = resolve_inputs(args.inputs, args.recursive)
  if not documents_paths:
    print(f"ERROR: no Markdown files found for: {', '.join(args.inputs)}", file=sys.stderr)
    return 1
  want_html = args.format in ("html", "both")
  want_pdf = args.format in ("pdf", "both")
  formats_label = {"html": "HTML", "pdf": "PDF", "both": "HTML and PDF"}[args.format]
  log(f"Rendering {len(documents_paths)} file{'s' if len(documents_paths) != 1 else ''} with template '{args.template}' to {formats_label}...")
  artifacts = []
  for index, path in enumerate(documents_paths, start=1):
    entry = {"index": index, "total": len(documents_paths), "path": path, "html": None, "pdf": None, "html_status": None, "pdf_status": None, "error": "", "warning": "", "seconds": 0.0}
    started = time.perf_counter()
    artifacts.append(entry)
    try:
      document = read_document(path, args.lang, args.title if len(documents_paths) == 1 else None)
      for warning in copy_images(document, args.output_dir, args.overwrite):
        add_warning(entry, warning)
      entry["html"] = output_path_for(document, args.output_dir, ".html")
      entry["pdf"] = output_path_for(document, args.output_dir, ".pdf")
      html_text = inject(template_text, document, args.paper, args.landscape)
      html_exists_before = entry["html"].exists()
      if want_html:
        entry["html_status"] = write_html(html_text, entry["html"], args.overwrite)
      else:
        if want_pdf and (args.overwrite or not entry["pdf"].exists()):
          entry["html"].parent.mkdir(parents=True, exist_ok=True)
          entry["html"].write_text(html_text, encoding="utf-8")
          entry["html_status"] = "temporary" if not (html_exists_before and args.keep_html) else "ok"
    except SetupError as error:
      print(f"ERROR: {error}", file=sys.stderr)
      return 2
    except Exception as error:
      entry["error"] = f"{type(error).__name__}: {error}"
    entry["seconds"] += time.perf_counter() - started
  if want_pdf:
    pending = []
    for entry in artifacts:
      if entry["error"]:
        continue
      if entry["pdf"].exists() and not args.overwrite:
        entry["pdf_status"] = "skipped-exists"
        continue
      pending.append(entry)
    if pending:
      try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
          browser = launch_chromium(playwright, log)
          page = browser.new_page(viewport={"width": 1040 if args.landscape else 720, "height": 1000})
          for entry in pending:
            started = time.perf_counter()
            try:
              facts = print_pdf(page, entry["html"], entry["pdf"], args.render_timeout)
              entry["pdf_status"] = "ok"
              overflowing_tables = facts["table_overflow"]
              if overflowing_tables:
                add_warning(entry, f"WARNING: {overflowing_tables} table{'s' if overflowing_tables != 1 else ''} wider than the page after font step-down (clipped in PDF)")
              if facts["image_broken"]:
                broken = facts["image_broken"]
                add_warning(entry, f"WARNING: {broken} image{'s' if broken != 1 else ''} failed to load (first: {facts['image_broken_first']})")
            except Exception as error:
              message = str(error).splitlines()[0]
              if "wait_for_selector" in message or "Timeout" in message:
                message = f"template '{args.template}' did not set data-rendered within {args.render_timeout:g} s (HTML kept for inspection)"
                entry["html_status"] = "ok"
              entry["error"] = f"pdf FAILED: {message}"
              if "Target closed" in message or "crashed" in message.lower():
                browser = launch_chromium(playwright, log)
                page = browser.new_page(viewport={"width": 1040 if args.landscape else 720, "height": 1000})
            entry["seconds"] += time.perf_counter() - started
          browser.close()
      except SetupError as error:
        for entry in artifacts:
          report_line(entry, log)
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    for entry in artifacts:
      if entry["html_status"] == "temporary" and entry["pdf_status"] == "ok" and not args.keep_html:
        entry["html"].unlink(missing_ok=True)
        entry["html_status"] = None
  failed = 0
  skipped = 0
  ok = 0
  for entry in artifacts:
    report_line(entry, lambda message: print(message, flush=True) if (not args.quiet or entry["error"]) else None)
    if entry["error"]:
      failed += 1
    elif entry["html_status"] == "skipped-exists" or entry["pdf_status"] == "skipped-exists":
      skipped += 1
      if entry["html_status"] == "ok" or entry["pdf_status"] == "ok":
        ok += 1
    else:
      ok += 1
  output_folder = Path(args.output_dir).resolve() if args.output_dir else artifacts[0]["path"].parent
  print(f"DONE: {ok} ok, {failed} failed, {skipped} skipped. Output: {output_folder}", flush=True)
  return 1 if failed else 0


def report_line(entry, log):
  parts = []
  if entry["html_status"] == "ok" and entry["html"] and entry["html"].exists():
    parts.append(f"html {format_size(entry['html'])}")
  elif entry["html_status"] == "skipped-exists":
    parts.append("html skipped (exists)")
  if entry["pdf_status"] == "ok" and entry["pdf"] and entry["pdf"].exists():
    pages = pdf_page_count(entry["pdf"])
    parts.append(f"pdf {pages} pages {format_size(entry['pdf'])}" if pages else f"pdf {format_size(entry['pdf'])}")
  elif entry["pdf_status"] == "skipped-exists":
    parts.append("pdf skipped (exists)")
  if entry["error"]:
    parts.append(entry["error"] if entry["error"].startswith("pdf FAILED") else f"FAILED: {entry['error']}")
  if entry["warning"]:
    parts.append(entry["warning"])
  log(f"  [ {entry['index']} / {entry['total']} ] {entry['path'].name} ... {' | '.join(parts)} | {entry['seconds']:.1f} s")


if __name__ == "__main__":
  sys.stdout.reconfigure(encoding="utf-8")
  sys.stderr.reconfigure(encoding="utf-8")
  sys.exit(main())
