#!/usr/bin/env python3
"""
Test suite for the pdf-tools skill: every command line tool (Poppler, QPDF, Ghostscript, 7-Zip), the 3 skill scripts,
and every PowerShell example of SKILL.md and GHOSTSCRIPT.md.

Location: [SKILL_FOLDER]/_test/test-pdf-tools.py (kept and versioned; the sandbox it creates is agent work and is deleted by /cleanup)

Usage:
  python test-pdf-tools.py [--filter TEXT ...] [--verbose] [--keep] [--work-dir DIR]

  --filter    run only tests whose name contains one of the texts
  --keep      keep the folder of every test case (default: delete after a passing test)
  --work-dir  sandbox folder (default: [WORKSPACE_FOLDER]/_agentwork/.tmp_pdftools_test)

Exit codes: 0 = no test failed (SKIPPED allowed), 1 = at least one test failed.
Fixtures are generated into the sandbox with Ghostscript, Poppler, and QPDF; no private files are used.
"""

import argparse, os, re, shutil, subprocess, sys, time, traceback
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
SKILL_DIR = TEST_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent.parent
TOOLS_DIR = (WORKSPACE_DIR.parent / ".tools").resolve()
POPPLER_DIR = TOOLS_DIR / "poppler" / "Library" / "bin"
QPDF_DIR = TOOLS_DIR / "qpdf" / "bin"
GS_EXE = TOOLS_DIR / "gs" / "bin" / "gswin64c.exe"
SEVEN_ZIP_EXE = TOOLS_DIR / "7z" / "7z.exe"
PYTHON_EXE = Path(sys.executable)
DEFAULT_WORK_DIR = WORKSPACE_DIR / "_agentwork" / ".tmp_pdftools_test"

TESTS = []
SANDBOX = {}


class TestSkipped(Exception):
  pass


def test(function):
  TESTS.append((function.__name__, function))
  return function


class ToolResult:
  def __init__(self, completed):
    self.exit_code = completed.returncode
    self.stdout_bytes = completed.stdout or b""
    self.stdout = self.stdout_bytes.decode("utf-8", errors="replace")
    self.stderr = (completed.stderr or b"").decode("utf-8", errors="replace")
    self.text = self.stdout + self.stderr


def run(arguments, cwd=None, input_bytes=None, timeout=600, environment=None):
  command = []
  for argument in arguments:
    command.append(str(argument))
  completed = subprocess.run(command, cwd=str(cwd) if cwd else None, input=input_bytes, capture_output=True, timeout=timeout, env=environment)
  return ToolResult(completed)


def poppler(tool_name, *arguments, cwd=None):
  return run([POPPLER_DIR / f"{tool_name}.exe", *arguments], cwd=cwd)


def qpdf(*arguments, cwd=None):
  return run([QPDF_DIR / "qpdf.exe", *arguments], cwd=cwd)


def ghostscript(*arguments, cwd=None):
  return run([GS_EXE, *arguments], cwd=cwd)


def seven_zip(*arguments, cwd=None):
  return run([SEVEN_ZIP_EXE, *arguments], cwd=cwd)


def run_powershell(script_text, cwd, name="snippet"):
  script_path = Path(cwd) / f".tmp_{name}.ps1"
  script_path.write_text(script_text, encoding="utf-8-sig")
  wrapper = "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); $global:LASTEXITCODE = 0; & '" + str(script_path) + "'; exit $LASTEXITCODE"
  return run(["pwsh", "-NoProfile", "-NonInteractive", "-Command", wrapper], cwd=cwd)


def check(condition, message):
  if not condition:
    raise AssertionError(message)


def expect_exit(result, allowed=(0,)):
  check(result.exit_code in allowed, f"exit code {result.exit_code}, allowed {allowed}\n{result.text[:600]}")


def expect_text(text, *fragments):
  for fragment in fragments:
    check(fragment in text, f"text not found: {fragment!r}\nin: {text[:600]!r}")


def expect_file(path, minimum_bytes=1):
  check(Path(path).is_file(), f"file missing: {path}")
  size = Path(path).stat().st_size
  check(size >= minimum_bytes, f"file too small ({size} bytes): {path}")
  return size


def page_count(path):
  result = poppler("pdfinfo", path)
  expect_exit(result)
  match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
  check(match is not None, f"no Pages line for {path}\n{result.text[:400]}")
  return int(match.group(1))


def skip(reason):
  raise TestSkipped(reason)


def new_case(name=None, copy_fixtures=True):
  if name is None:
    name = sys._getframe(1).f_code.co_name
  folder = SANDBOX["root"] / "cases" / name
  if folder.exists():
    shutil.rmtree(folder)
  folder.mkdir(parents=True)
  if copy_fixtures:
    for item in SANDBOX["fixtures"].iterdir():
      if item.is_file():
        shutil.copy2(item, folder / item.name)
  return folder


FIXTURE_POSTSCRIPT = r"""%!PS
[ /Title (PDF Tools Test Document) /Author (Test Author) /Subject (Fixture) /Keywords (alpha, beta) /DOCINFO pdfmark
/imageRow 2400 string def
/imageRowIndex 0 def
/imageRowProc {
  0 1 799 { /x exch def
    imageRow x 3 mul x imageRowIndex add rand 127 and add 255 and put
    imageRow x 3 mul 1 add x 2 mul imageRowIndex add rand 127 and add 255 and put
    imageRow x 3 mul 2 add rand 255 and put
  } for
  /imageRowIndex imageRowIndex 1 add def
  imageRow
} def
/drawImage {
  /imageRowIndex 0 def
  gsave 72 520 translate 144 144 scale
  800 800 8 [800 0 0 -800 0 800] imageRowProc false 3 colorimage
  grestore
} def
/Helvetica findfont 24 scalefont setfont
72 780 moveto (Page 1 Alpha Title) show
/Helvetica findfont 12 scalefont setfont
72 750 moveto (First page body text with the word needle.) show
drawImage
showpage
/Helvetica findfont 24 scalefont setfont
72 780 moveto (Page 2 Beta Section) show
[ /Rect [72 740 300 760] /Border [0 0 0] /Action << /Subtype /URI /URI (https://example.com/) >> /Subtype /Link /ANN pdfmark
[ /Dest /ChapterTwo /View [/XYZ null null null] /DEST pdfmark
drawImage
showpage
/Courier findfont 12 scalefont setfont
72 780 moveto (Name        Amount    Date) show
72 764 moveto (Alpha       100       2026-01-01) show
72 748 moveto (Beta        250       2026-02-01) show
0.8 0.2 0.2 setrgbcolor 72 600 200 100 rectfill
0 setgray /Helvetica findfont 24 scalefont setfont
72 560 moveto (Page 3 Gamma Table) show
showpage
"""


def create_fixtures(root):
  fixtures = root / "fixtures"
  fixtures.mkdir(parents=True)
  source_path = root / "source.ps"
  source_path.write_text(FIXTURE_POSTSCRIPT, encoding="utf-8")
  result = ghostscript("-sDEVICE=pdfwrite", "-dNOPAUSE", "-dBATCH", "-dQUIET", f"-sOutputFile={fixtures / 'input.pdf'}", str(source_path))
  expect_exit(result)
  expect_file(fixtures / "input.pdf", 10000)
  expect_exit(qpdf(fixtures / "input.pdf", "--pages", ".", "3,1", "--", fixtures / "input2.pdf"))
  (fixtures / "notes.txt").write_text("attachment text\n", encoding="utf-8")
  expect_exit(qpdf("--encrypt", "userpw", "ownerpw", "256", "--", fixtures / "input.pdf", fixtures / "encrypted.pdf"))
  data = (fixtures / "input.pdf").read_bytes()
  marker = data.rfind(b"startxref\n") + len(b"startxref\n")
  (fixtures / "damaged.pdf").write_bytes(data[:marker] + b"9" + data[marker:])
  return fixtures


@test
def test_environment_tool_files_exist():
  missing = []
  names = ["pdfattach", "pdfdetach", "pdffonts", "pdfimages", "pdfinfo", "pdfseparate", "pdftocairo", "pdftohtml", "pdftoppm", "pdftops", "pdftotext", "pdfunite"]
  for name in names:
    if not (POPPLER_DIR / f"{name}.exe").is_file():
      missing.append(name)
  for path in [QPDF_DIR / "qpdf.exe", QPDF_DIR / "fix-qdf.exe", QPDF_DIR / "zlib-flate.exe", GS_EXE, SEVEN_ZIP_EXE]:
    if not path.is_file():
      missing.append(str(path))
  check(not missing, f"missing tools: {missing}")


@test
def test_environment_tool_versions():
  expect_text(poppler("pdfinfo", "-v").text, "pdfinfo version")
  expect_text(qpdf("--version").text, "qpdf version")
  expect_text(ghostscript("--version").text, "10.")
  expect_text(seven_zip().text, "7-Zip")


@test
def test_environment_python_modules():
  result = run([PYTHON_EXE, "-c", "import pdf2image, PIL; print('modules ok')"])
  expect_exit(result)
  expect_text(result.stdout, "modules ok")


@test
def test_pdfinfo_basic_and_page_range():
  folder = new_case()
  result = poppler("pdfinfo", "input.pdf", cwd=folder)
  expect_exit(result)
  expect_text(result.text, "Title:", "PDF Tools Test Document", "Author:", "Test Author", "Pages:           3", "Page size:")
  ranged = poppler("pdfinfo", "-f", "2", "-l", "3", "input.pdf", cwd=folder)
  expect_exit(ranged)
  expect_text(ranged.text, "Page    2 size:", "Page    3 size:")
  check("Page    1 size:" not in ranged.text, "page 1 listed although -f 2")


@test
def test_pdfinfo_option_variants():
  folder = new_case()
  expect_text(poppler("pdfinfo", "-box", "input.pdf", cwd=folder).text, "MediaBox:", "CropBox:")
  expect_text(poppler("pdfinfo", "-meta", "input.pdf", cwd=folder).text, "<?xpacket", "PDF Tools Test Document")
  expect_text(poppler("pdfinfo", "-custom", "input.pdf", cwd=folder).text, "Title:")
  expect_text(poppler("pdfinfo", "-isodates", "input.pdf", cwd=folder).text, "CreationDate:")
  expect_text(poppler("pdfinfo", "-rawdates", "input.pdf", cwd=folder).text, "CreationDate:")
  expect_text(poppler("pdfinfo", "-dests", "input.pdf", cwd=folder).text, "ChapterTwo")
  expect_text(poppler("pdfinfo", "-url", "input.pdf", cwd=folder).text, "https://example.com/")
  expect_exit(poppler("pdfinfo", "-js", "input.pdf", cwd=folder))
  expect_exit(poppler("pdfinfo", "-struct", "input.pdf", cwd=folder))
  expect_text(poppler("pdfinfo", "-listenc").text, "UTF-8")
  expect_text(poppler("pdfinfo", "-enc", "UTF-8", "input.pdf", cwd=folder).text, "Pages:")


@test
def test_pdfinfo_encrypted_and_errors():
  folder = new_case()
  denied = poppler("pdfinfo", "encrypted.pdf", cwd=folder)
  check(denied.exit_code != 0, "encrypted PDF without password must fail")
  expect_text(poppler("pdfinfo", "-upw", "userpw", "encrypted.pdf", cwd=folder).text, "Encrypted:", "Pages:           3")
  check(poppler("pdfinfo", "missing.pdf", cwd=folder).exit_code != 0, "missing file must fail")


@test
def test_pdftotext_file_and_stdout():
  folder = new_case()
  expect_exit(poppler("pdftotext", "input.pdf", "out.txt", cwd=folder))
  text = (folder / "out.txt").read_text(encoding="utf-8")
  expect_text(text, "Page 1 Alpha Title", "needle", "Page 2 Beta Section", "Page 3 Gamma Table")
  check("\f" in text, "page break (form feed) missing")
  stdout = poppler("pdftotext", "input.pdf", "-", cwd=folder)
  expect_exit(stdout)
  expect_text(stdout.stdout, "Page 1 Alpha Title")
  default_name = poppler("pdftotext", "input.pdf", cwd=folder)
  expect_exit(default_name)
  expect_file(folder / "input.txt")


@test
def test_pdftotext_page_range_and_layout_options():
  folder = new_case()
  second = poppler("pdftotext", "-f", "2", "-l", "2", "input.pdf", "-", cwd=folder)
  expect_text(second.stdout, "Page 2 Beta Section")
  check("Page 1 Alpha" not in second.stdout, "page 1 text present with -f 2 -l 2")
  layout_text = poppler("pdftotext", "-layout", "-f", "3", "-l", "3", "input.pdf", "-", cwd=folder).stdout
  check(re.search(r"Alpha\s+100\s+2026-01-01", layout_text) is not None, f"-layout did not keep the table row on one line: {layout_text[:200]!r}")
  expect_text(poppler("pdftotext", "-raw", "-f", "3", "-l", "3", "input.pdf", "-", cwd=folder).stdout, "Beta")
  no_break = poppler("pdftotext", "-nopgbrk", "input.pdf", "-", cwd=folder)
  check("\f" not in no_break.stdout, "-nopgbrk still wrote form feed")
  expect_text(poppler("pdftotext", "-fixed", "6", "-f", "3", "-l", "3", "input.pdf", "-", cwd=folder).stdout, "Alpha")
  expect_exit(poppler("pdftotext", "-nodiag", "-colspacing", "0.5", "-r", "100", "input.pdf", "-", cwd=folder))


@test
def test_pdftotext_formats_and_crop():
  folder = new_case()
  expect_text(poppler("pdftotext", "-htmlmeta", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder).stdout, "<html", "<meta")
  expect_text(poppler("pdftotext", "-bbox", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder).stdout, "<word xMin=", "needle")
  expect_text(poppler("pdftotext", "-bbox-layout", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder).stdout, "<block", "<line")
  expect_text(poppler("pdftotext", "-tsv", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder).stdout, "level\tpage_num")
  dos = poppler("pdftotext", "-eol", "dos", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder)
  expect_text(dos.stdout, "\r\n")
  expect_text(poppler("pdftotext", "-enc", "UTF-8", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder).stdout, "Alpha")
  expect_text(poppler("pdftotext", "-listenc").text, "UTF-8")
  cropped = poppler("pdftotext", "-r", "72", "-x", "0", "-y", "0", "-W", "600", "-H", "100", "-f", "1", "-l", "1", "input.pdf", "-", cwd=folder)
  expect_exit(cropped)
  expect_text(cropped.stdout, "Page 1 Alpha Title")
  encrypted = poppler("pdftotext", "-upw", "userpw", "-f", "1", "-l", "1", "encrypted.pdf", "-", cwd=folder)
  expect_text(encrypted.stdout, "Page 1 Alpha Title")


def image_size(path):
  from PIL import Image
  with Image.open(path) as image:
    return image.size


def names_in(folder, pattern):
  retVal = []
  for item in sorted(Path(folder).glob(pattern)):
    retVal.append(item.name)
  return retVal


@test
def test_pdftoppm_formats_and_names():
  folder = new_case()
  expect_exit(poppler("pdftoppm", "-png", "-r", "72", "input.pdf", "out", cwd=folder))
  check(names_in(folder, "out-*.png") == ["out-1.png", "out-2.png", "out-3.png"], f"names: {names_in(folder, 'out-*')}")
  check(image_size(folder / "out-1.png") == (612, 792), f"Letter at 72 DPI: {image_size(folder / 'out-1.png')}")
  expect_exit(poppler("pdftoppm", "-jpeg", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "pic", cwd=folder))
  check(names_in(folder, "pic-*.jpg") == ["pic-1.jpg"], f"jpeg names: {names_in(folder, 'pic*')}")
  expect_exit(poppler("pdftoppm", "-tiff", "-tiffcompression", "lzw", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "scan", cwd=folder))
  check(names_in(folder, "scan-*.tif") == ["scan-1.tif"], f"tiff names: {names_in(folder, 'scan*')}")
  expect_exit(poppler("pdftoppm", "-gray", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "gray", cwd=folder))
  expect_file(folder / "gray-1.pgm")
  expect_exit(poppler("pdftoppm", "-mono", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "mono", cwd=folder))
  expect_file(folder / "mono-1.pbm")
  expect_exit(poppler("pdftoppm", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "color", cwd=folder))
  expect_file(folder / "color-1.ppm")


@test
def test_pdftoppm_page_selection_and_numbering():
  folder = new_case()
  expect_exit(poppler("pdftoppm", "-png", "-r", "36", "-f", "2", "-l", "3", "input.pdf", "range", cwd=folder))
  check(names_in(folder, "range-*.png") == ["range-2.png", "range-3.png"], f"range names: {names_in(folder, 'range*')}")
  expect_exit(poppler("pdftoppm", "-png", "-r", "36", "-singlefile", "input.pdf", "single", cwd=folder))
  check(names_in(folder, "single*.png") == ["single.png"], f"singlefile names: {names_in(folder, 'single*')}")
  expect_exit(poppler("pdftoppm", "-png", "-r", "36", "-o", "input.pdf", "odd", cwd=folder))
  check(names_in(folder, "odd-*.png") == ["odd-1.png", "odd-3.png"], f"odd names: {names_in(folder, 'odd*')}")
  expect_exit(poppler("pdftoppm", "-png", "-r", "36", "-e", "input.pdf", "even", cwd=folder))
  check(names_in(folder, "even-*.png") == ["even-2.png"], f"even names: {names_in(folder, 'even*')}")
  expect_exit(poppler("pdftoppm", "-png", "-r", "36", "-f", "1", "-l", "1", "-sep", "_", "input.pdf", "sep", cwd=folder))
  expect_file(folder / "sep_1.png")
  expect_exit(poppler("pdftoppm", "-png", "-r", "36", "-f", "1", "-l", "1", "-forcenum", "input.pdf", "force", cwd=folder))
  expect_file(folder / "force-1.png")


@test
def test_pdftoppm_size_and_crop_options():
  folder = new_case()
  expect_exit(poppler("pdftoppm", "-png", "-scale-to", "200", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "scaled", cwd=folder))
  width, height = image_size(folder / "scaled.png")
  check(max(width, height) == 200, f"-scale-to 200 gave {width}x{height}")
  expect_exit(poppler("pdftoppm", "-png", "-scale-to-x", "100", "-scale-to-y", "150", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "xy", cwd=folder))
  check(image_size(folder / "xy.png") == (100, 150), f"-scale-to-x/-y gave {image_size(folder / 'xy.png')}")
  expect_exit(poppler("pdftoppm", "-png", "-r", "72", "-x", "10", "-y", "20", "-W", "120", "-H", "80", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "crop", cwd=folder))
  check(image_size(folder / "crop.png") == (120, 80), f"crop gave {image_size(folder / 'crop.png')}")
  expect_exit(poppler("pdftoppm", "-png", "-r", "72", "-sz", "64", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "square", cwd=folder))
  check(image_size(folder / "square.png") == (64, 64), f"-sz gave {image_size(folder / 'square.png')}")
  expect_exit(poppler("pdftoppm", "-png", "-rx", "36", "-ry", "72", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "rxry", cwd=folder))
  check(image_size(folder / "rxry.png") == (306, 792), f"-rx/-ry gave {image_size(folder / 'rxry.png')}")


@test
def test_pdftoppm_quality_and_rendering_flags():
  folder = new_case()
  expect_exit(poppler("pdftoppm", "-jpeg", "-jpegopt", "quality=50,progressive=y", "-r", "72", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "q50", cwd=folder))
  expect_exit(poppler("pdftoppm", "-jpeg", "-jpegopt", "quality=95", "-r", "72", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "q95", cwd=folder))
  check((folder / "q95.jpg").stat().st_size > (folder / "q50.jpg").stat().st_size, "quality=95 not larger than quality=50")
  expect_exit(poppler("pdftoppm", "-jpegcmyk", "-r", "36", "-f", "1", "-l", "1", "-singlefile", "input.pdf", "cmyk", cwd=folder))
  for flags in (["-aa", "no"], ["-aaVector", "no"], ["-freetype", "no"], ["-thinlinemode", "solid"], ["-overprint"], ["-hide-annotations"], ["-cropbox"], ["-q"]):
    result = poppler("pdftoppm", "-png", "-r", "36", *flags, "-f", "2", "-l", "2", "-singlefile", "input.pdf", "flag", cwd=folder)
    expect_exit(result)
    expect_file(folder / "flag.png")
  progress = poppler("pdftoppm", "-png", "-r", "36", "-progress", "input.pdf", "prog", cwd=folder)
  expect_exit(progress)
  expect_text(progress.text, "1 3 prog-1.png", "3 3 prog-3.png")
  encrypted = poppler("pdftoppm", "-png", "-r", "36", "-upw", "userpw", "-f", "1", "-l", "1", "-singlefile", "encrypted.pdf", "enc", cwd=folder)
  expect_exit(encrypted)
  expect_file(folder / "enc.png")
  check(poppler("pdftoppm", "-png", "encrypted.pdf", "denied", cwd=folder).exit_code != 0, "encrypted without password must fail")


@test
def test_pdftocairo_image_formats():
  folder = new_case()
  expect_exit(poppler("pdftocairo", "-png", "-r", "36", "input.pdf", "cairo", cwd=folder))
  check(names_in(folder, "cairo-*.png") == ["cairo-1.png", "cairo-2.png", "cairo-3.png"], f"names: {names_in(folder, 'cairo*')}")
  expect_exit(poppler("pdftocairo", "-png", "-singlefile", "-r", "36", "-f", "2", "-l", "2", "input.pdf", "one", cwd=folder))
  expect_file(folder / "one.png")
  expect_exit(poppler("pdftocairo", "-jpeg", "-singlefile", "-jpegopt", "quality=60", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "pic", cwd=folder))
  expect_file(folder / "pic.jpg")
  expect_exit(poppler("pdftocairo", "-tiff", "-tiffcompression", "deflate", "-singlefile", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "scan", cwd=folder))
  expect_file(folder / "scan.tif")
  expect_exit(poppler("pdftocairo", "-png", "-transp", "-gray", "-singlefile", "-r", "36", "-f", "1", "-l", "1", "input.pdf", "gray", cwd=folder))
  expect_file(folder / "gray.png")
  expect_exit(poppler("pdftocairo", "-png", "-scale-to", "150", "-singlefile", "-f", "1", "-l", "1", "input.pdf", "scaled", cwd=folder))
  check(max(image_size(folder / "scaled.png")) == 150, f"-scale-to gave {image_size(folder / 'scaled.png')}")
  expect_exit(poppler("pdftocairo", "-png", "-x", "0", "-y", "0", "-W", "50", "-H", "40", "-r", "72", "-singlefile", "-f", "1", "-l", "1", "input.pdf", "crop", cwd=folder))
  check(image_size(folder / "crop.png") == (50, 40), f"crop gave {image_size(folder / 'crop.png')}")
  expect_exit(poppler("pdftocairo", "-png", "-r", "36", "-o", "input.pdf", "odd", cwd=folder))
  check(names_in(folder, "odd-*.png") == ["odd-1.png", "odd-3.png"], f"odd names: {names_in(folder, 'odd*')}")


@test
def test_pdftocairo_vector_formats():
  folder = new_case()
  expect_exit(poppler("pdftocairo", "-pdf", "input.pdf", "copy.pdf", cwd=folder))
  check(page_count(folder / "copy.pdf") == 3, "pdftocairo -pdf lost pages")
  expect_exit(poppler("pdftocairo", "-ps", "-paper", "A4", "input.pdf", "copy.ps", cwd=folder))
  expect_text((folder / "copy.ps").read_text(encoding="latin-1"), "%!PS-Adobe")
  expect_exit(poppler("pdftocairo", "-eps", "-f", "1", "-l", "1", "input.pdf", "copy.eps", cwd=folder))
  expect_text((folder / "copy.eps").read_text(encoding="latin-1"), "%!PS-Adobe", "EPSF")
  expect_exit(poppler("pdftocairo", "-svg", "-f", "1", "-l", "1", "input.pdf", "copy.svg", cwd=folder))
  expect_text((folder / "copy.svg").read_text(encoding="utf-8"), "<svg")
  expect_exit(poppler("pdftocairo", "-pdf", "-origpagesizes", "-f", "1", "-l", "2", "input.pdf", "orig.pdf", cwd=folder))
  check(page_count(folder / "orig.pdf") == 2, "pdftocairo -f 1 -l 2 should give 2 pages")


@test
def test_pdfimages_list_and_extract():
  folder = new_case()
  listing = poppler("pdfimages", "-list", "input.pdf", cwd=folder)
  expect_exit(listing)
  expect_text(listing.stdout, "page   num  type", "image")
  rows = []
  for line in listing.stdout.splitlines()[2:]:
    if line.strip():
      rows.append(line.split())
  check(len(rows) == 2, f"expected 2 images, got {len(rows)}: {listing.stdout}")
  check(rows[0][3] == "800" and rows[0][4] == "800", f"image size columns: {rows[0]}")
  expect_exit(poppler("pdfimages", "-png", "input.pdf", "img", cwd=folder))
  check(names_in(folder, "img-*.png") == ["img-000.png", "img-001.png"], f"names: {names_in(folder, 'img*')}")
  check(image_size(folder / "img-000.png") == (800, 800), "extracted image size")
  expect_exit(poppler("pdfimages", "-all", "-p", "input.pdf", "all", cwd=folder))
  check(len(names_in(folder, "all-*")) == 2, f"-all -p names: {names_in(folder, 'all-*')}")
  check(names_in(folder, "all-*")[0].startswith("all-001-000"), f"-p page numbers: {names_in(folder, 'all-*')}")
  expect_exit(poppler("pdfimages", "-j", "-f", "2", "-l", "2", "input.pdf", "jpg", cwd=folder))
  check(len(names_in(folder, "jpg-*")) == 1, f"-f 2 -l 2 names: {names_in(folder, 'jpg-*')}")
  printed = poppler("pdfimages", "-png", "-print-filenames", "-q", "input.pdf", "printed", cwd=folder)
  expect_exit(printed)
  expect_text(printed.stdout, "printed-000.png")
  expect_exit(poppler("pdfimages", "-tiff", "-f", "1", "-l", "1", "input.pdf", "tiffimg", cwd=folder))
  expect_exit(poppler("pdfimages", "-list", "-upw", "userpw", "encrypted.pdf", cwd=folder))


@test
def test_pdffonts_listing():
  folder = new_case()
  result = poppler("pdffonts", "input.pdf", cwd=folder)
  expect_exit(result)
  expect_text(result.stdout, "name", "Helvetica", "Courier")
  last = poppler("pdffonts", "-f", "3", "-l", "3", "input.pdf", cwd=folder)
  expect_text(last.stdout, "Courier")
  first = poppler("pdffonts", "-f", "1", "-l", "1", "input.pdf", cwd=folder)
  check("Courier" not in first.stdout, "Courier listed for page 1")
  expect_exit(poppler("pdffonts", "-subst", "input.pdf", cwd=folder))
  expect_exit(poppler("pdffonts", "-upw", "userpw", "encrypted.pdf", cwd=folder))


@test
def test_pdfseparate_and_pdfunite():
  folder = new_case()
  expect_exit(poppler("pdfseparate", "input.pdf", "page-%d.pdf", cwd=folder))
  check(names_in(folder, "page-*.pdf") == ["page-1.pdf", "page-2.pdf", "page-3.pdf"], f"names: {names_in(folder, 'page-*')}")
  expect_exit(poppler("pdfseparate", "-f", "2", "-l", "3", "input.pdf", "part-%03d.pdf", cwd=folder))
  check(names_in(folder, "part-*.pdf") == ["part-002.pdf", "part-003.pdf"], f"names: {names_in(folder, 'part-*')}")
  check(page_count(folder / "page-1.pdf") == 1, "separated page must have 1 page")
  expect_exit(poppler("pdfunite", "page-1.pdf", "page-3.pdf", "input2.pdf", "merged.pdf", cwd=folder))
  check(page_count(folder / "merged.pdf") == 4, "merge of 1 + 1 + 2 pages must have 4 pages")
  text = poppler("pdftotext", "merged.pdf", "-", cwd=folder).stdout
  check(text.index("Page 1 Alpha") < text.index("Page 3 Gamma"), "page order after pdfunite")
  no_pattern = poppler("pdfseparate", "input.pdf", "single.pdf", cwd=folder)
  check(no_pattern.exit_code != 0, "multi-page pdfseparate without %d in the pattern must fail")


@test
def test_pdftohtml_modes():
  folder = new_case()
  expect_exit(poppler("pdftohtml", "-q", "input.pdf", "frames", cwd=folder))
  expect_file(folder / "frames.html")
  expect_exit(poppler("pdftohtml", "-q", "-s", "-noframes", "input.pdf", "single", cwd=folder))
  expect_text((folder / "single.html").read_text(encoding="utf-8", errors="replace"), "Page 1 Alpha Title", "Page 3 Gamma Table")
  stdout = poppler("pdftohtml", "-q", "-stdout", "-noframes", "-f", "1", "-l", "1", "-i", "input.pdf", cwd=folder)
  expect_exit(stdout)
  expect_text(stdout.stdout, "<html", "needle")
  expect_exit(poppler("pdftohtml", "-q", "-xml", "-f", "1", "-l", "1", "input.pdf", "layout", cwd=folder))
  expect_text((folder / "layout.xml").read_text(encoding="utf-8", errors="replace"), "<pdf2xml", "<page")
  expect_exit(poppler("pdftohtml", "-q", "-c", "-zoom", "1.0", "-fmt", "png", "-f", "1", "-l", "1", "input.pdf", "complex", cwd=folder))
  check(len(names_in(folder, "complex*.png")) >= 1, f"complex mode wrote no PNG: {names_in(folder, 'complex*')}")
  expect_exit(poppler("pdftohtml", "-q", "-p", "-hidden", "-nomerge", "-wbt", "5", "-f", "1", "-l", "1", "input.pdf", "flags", cwd=folder))
  expect_exit(poppler("pdftohtml", "-q", "-upw", "userpw", "-f", "1", "-l", "1", "encrypted.pdf", "enc", cwd=folder))


@test
def test_pdftops_levels_and_paper():
  folder = new_case()
  expect_exit(poppler("pdftops", "input.pdf", "out.ps", cwd=folder))
  expect_text((folder / "out.ps").read_text(encoding="latin-1"), "%!PS-Adobe", "%%Pages: 3")
  for level in ("-level1", "-level2", "-level3", "-level2sep", "-level3sep"):
    expect_exit(poppler("pdftops", level, "-f", "1", "-l", "1", "input.pdf", f"{level[1:]}.ps", cwd=folder))
    expect_file(folder / f"{level[1:]}.ps")
  expect_exit(poppler("pdftops", "-eps", "-f", "1", "-l", "1", "input.pdf", "one.eps", cwd=folder))
  expect_text((folder / "one.eps").read_text(encoding="latin-1"), "EPSF")
  expect_exit(poppler("pdftops", "-paper", "A4", "-expand", "-nocenter", "-noshrink", "-f", "1", "-l", "1", "input.pdf", "a4.ps", cwd=folder))
  expect_exit(poppler("pdftops", "-origpagesizes", "-opi", "-noembt1", "-noembtt", "-passfonts", "-f", "1", "-l", "1", "input.pdf", "flags.ps", cwd=folder))
  expect_exit(poppler("pdftops", "-rasterize", "always", "-r", "72", "-f", "1", "-l", "1", "input.pdf", "raster.ps", cwd=folder))
  expect_exit(poppler("pdftops", "-upw", "userpw", "-f", "1", "-l", "1", "encrypted.pdf", "enc.ps", cwd=folder))


@test
def test_pdfattach_and_pdfdetach():
  folder = new_case()
  expect_exit(poppler("pdfattach", "input.pdf", "notes.txt", "with-attachment.pdf", cwd=folder))
  listing = poppler("pdfdetach", "-list", "with-attachment.pdf", cwd=folder)
  expect_exit(listing)
  expect_text(listing.stdout, "1 embedded files", "notes.txt")
  expect_exit(poppler("pdfdetach", "-save", "1", "-o", "saved-by-number.txt", "with-attachment.pdf", cwd=folder))
  check((folder / "saved-by-number.txt").read_text(encoding="utf-8") == "attachment text\n", "saved attachment content differs")
  expect_exit(poppler("pdfdetach", "-save", "1", "with-attachment.pdf", cwd=folder))
  expect_file(folder / "notes.txt")
  extract_folder = folder / "extracted"
  extract_folder.mkdir()
  expect_exit(poppler("pdfdetach", "-saveall", "../with-attachment.pdf", cwd=extract_folder))
  expect_file(extract_folder / "notes.txt")
  (folder / "notes.txt").write_text("replaced text\n", encoding="utf-8")
  expect_exit(poppler("pdfattach", "-replace", "with-attachment.pdf", "notes.txt", "replaced.pdf", cwd=folder))
  expect_exit(poppler("pdfdetach", "-save", "1", "-o", "after-replace.txt", "replaced.pdf", cwd=folder))
  check((folder / "after-replace.txt").read_text(encoding="utf-8") == "replaced text\n", "-replace did not replace the attachment")
  none = poppler("pdfdetach", "-list", "input.pdf", cwd=folder)
  expect_text(none.stdout, "0 embedded files")


@test
def test_pdfdetach_savefile_known_defect():
  folder = new_case()
  expect_exit(poppler("pdfattach", "input.pdf", "notes.txt", "with-attachment.pdf", cwd=folder))
  result = poppler("pdfdetach", "-savefile", "notes.txt", "with-attachment.pdf", cwd=folder)
  check(result.exit_code == 99 and "Invalid file name" in result.text,
    f"pdfdetach -savefile now works (exit {result.exit_code}): remove the known-defect warning from SKILL.md and this test")


@test
def test_qpdf_inspection_options():
  folder = new_case()
  check_result = qpdf("--check", "input.pdf", cwd=folder)
  expect_exit(check_result)
  expect_text(check_result.text, "No syntax or stream encoding errors found")
  check(qpdf("--show-npages", "input.pdf", cwd=folder).stdout.strip() == "3", "--show-npages")
  expect_text(qpdf("--show-pages", "input.pdf", cwd=folder).text, "page 1:", "page 3:")
  expect_text(qpdf("--show-object=1", "input.pdf", cwd=folder).text, "<<")
  expect_text(qpdf("--json", "--json-key=pages", "input.pdf", cwd=folder).stdout, '"pages"')
  encryption = qpdf("--show-encryption", "--password=userpw", "encrypted.pdf", cwd=folder)
  expect_exit(encryption)
  expect_text(encryption.text, "R = 6", "extract for accessibility: allowed")
  check(qpdf("--is-encrypted", "encrypted.pdf", cwd=folder).exit_code == 0, "--is-encrypted on encrypted.pdf")
  check(qpdf("--is-encrypted", "input.pdf", cwd=folder).exit_code == 2, "--is-encrypted on plain pdf must exit 2")
  check(qpdf("--requires-password", "encrypted.pdf", cwd=folder).exit_code == 0, "--requires-password")
  check(qpdf("--check", "encrypted.pdf", cwd=folder).exit_code == 2, "--check without password must exit 2")
  expect_exit(qpdf("--check", "--password=userpw", "encrypted.pdf", cwd=folder))


@test
def test_qpdf_page_selection_merge_split():
  folder = new_case()
  expect_exit(qpdf("--empty", "--pages", "input.pdf", "input2.pdf", "--", "merged.pdf", cwd=folder))
  check(page_count(folder / "merged.pdf") == 5, "merge 3 + 2 pages")
  expect_exit(qpdf("input.pdf", "--pages", ".", "1-2", "--", "range.pdf", cwd=folder))
  check(page_count(folder / "range.pdf") == 2, "range 1-2")
  expect_exit(qpdf("input.pdf", "--pages", ".", "3,1", "--", "reorder.pdf", cwd=folder))
  first_text = poppler("pdftotext", "-f", "1", "-l", "1", "reorder.pdf", "-", cwd=folder).stdout
  expect_text(first_text, "Page 3 Gamma Table")
  expect_exit(qpdf("input.pdf", "--pages", ".", "z", "--", "last.pdf", cwd=folder))
  expect_text(poppler("pdftotext", "last.pdf", "-", cwd=folder).stdout, "Page 3 Gamma Table")
  expect_exit(qpdf("input.pdf", "--pages", ".", "r1", "--", "last-too.pdf", cwd=folder))
  expect_exit(qpdf("input.pdf", "--pages", ".", "1-z:odd", "--", "odd.pdf", cwd=folder))
  check(page_count(folder / "odd.pdf") == 2, "odd pages 1 and 3")
  expect_exit(qpdf("--collate", "--empty", "--pages", "input.pdf", "input2.pdf", "--", "collated.pdf", cwd=folder))
  expect_exit(qpdf("--split-pages=1", "input.pdf", "split.pdf", cwd=folder))
  check(len(names_in(folder, "split-*.pdf")) == 3, f"split names: {names_in(folder, 'split*')}")
  expect_exit(qpdf("--empty", "--pages", "encrypted.pdf", "--password=userpw", "1-2", "--", "from-encrypted.pdf", cwd=folder))
  check(page_count(folder / "from-encrypted.pdf") == 2, "pages from encrypted input")


@test
def test_qpdf_transform_options():
  folder = new_case()
  expect_exit(qpdf("input.pdf", "--rotate=+90:1", "rotated.pdf", cwd=folder))
  rotation_text = poppler("pdfinfo", "-f", "1", "-l", "1", "rotated.pdf", cwd=folder).text
  check(re.search(r"Page\s+1 rot:\s+90", rotation_text) is not None, f"rotation not 90: {rotation_text[-200:]!r}")
  expect_exit(qpdf("input.pdf", "--flatten-rotation", "--flatten-annotations=screen", "flat.pdf", cwd=folder))
  expect_exit(qpdf("input.pdf", "--overlay", "input2.pdf", "--from=1", "--to=1-2", "--", "overlay.pdf", cwd=folder))
  check(page_count(folder / "overlay.pdf") == 3, "overlay keeps 3 pages")
  expect_exit(qpdf("input.pdf", "--underlay", "input2.pdf", "--from=1", "--to=3", "--", "underlay.pdf", cwd=folder))
  expect_exit(qpdf("input.pdf", "--coalesce-contents", "--normalize-content=y", "--generate-appearances", "--remove-restrictions", "norm.pdf", cwd=folder))
  (folder / "args.txt").write_text("input.pdf\n--pages\n.\n2\n--\nfrom-argfile.pdf\n", encoding="utf-8")
  expect_exit(qpdf("@args.txt", cwd=folder))
  check(page_count(folder / "from-argfile.pdf") == 1, "argument file @args.txt")


@test
def test_qpdf_encrypt_and_decrypt():
  folder = new_case()
  expect_exit(qpdf("--encrypt", "userpw", "ownerpw", "256", "--", "input.pdf", "enc256.pdf", cwd=folder))
  expect_exit(qpdf("--check", "--password=userpw", "enc256.pdf", cwd=folder))
  expect_exit(qpdf("--encrypt", "userpw", "ownerpw", "128", "--use-aes=y", "--", "input.pdf", "enc128aes.pdf", cwd=folder))
  weak = qpdf("--encrypt", "userpw", "ownerpw", "128", "--", "input.pdf", "enc128rc4.pdf", cwd=folder)
  check(weak.exit_code == 2 and "weak crypto" in weak.text, f"RC4 without --allow-weak-crypto must be refused: {weak.text[:200]!r}")
  expect_exit(qpdf("--allow-weak-crypto", "--encrypt", "userpw", "ownerpw", "128", "--", "input.pdf", "enc128rc4.pdf", cwd=folder))
  expect_exit(qpdf("--encrypt", "", "ownerpw", "256", "--print=none", "--modify=none", "--", "input.pdf", "restricted.pdf", cwd=folder))
  expect_text(qpdf("--show-encryption", "restricted.pdf", cwd=folder).text, "print low resolution: not allowed")
  expect_exit(qpdf("--decrypt", "--password=userpw", "encrypted.pdf", "decrypted.pdf", cwd=folder))
  expect_text(poppler("pdfinfo", "decrypted.pdf", cwd=folder).text, "Encrypted:       no")
  expect_exit(qpdf("--decrypt", "--password=ownerpw", "encrypted.pdf", "decrypted-owner.pdf", cwd=folder))
  wrong = qpdf("--decrypt", "--password=wrong", "encrypted.pdf", "never.pdf", cwd=folder)
  check(wrong.exit_code == 2 and not (folder / "never.pdf").exists(), "wrong password must fail with exit 2 and write nothing")


@test
def test_qpdf_optimize_and_linearize():
  folder = new_case()
  expect_exit(qpdf("--linearize", "input.pdf", "linear.pdf", cwd=folder))
  expect_exit(qpdf("--check-linearization", "linear.pdf", cwd=folder))
  expect_text(poppler("pdfinfo", "linear.pdf", cwd=folder).text, "Optimized:       yes")
  expect_exit(qpdf("--linearize", "--object-streams=generate", "--compress-streams=y", "--recompress-flate", "--compression-level=9",
    "--optimize-images", "--flatten-annotations=screen", "input.pdf", "optimized.pdf", cwd=folder))
  check(page_count(folder / "optimized.pdf") == 3, "optimized pdf keeps 3 pages")
  expect_exit(qpdf("--stream-data=uncompress", "--object-streams=disable", "input.pdf", "uncompressed.pdf", cwd=folder))
  check((folder / "uncompressed.pdf").stat().st_size > (folder / "input.pdf").stat().st_size * 0.5, "uncompressed size sanity")
  expect_exit(qpdf("--stream-data=compress", "--decode-level=generalized", "input.pdf", "compressed.pdf", cwd=folder))
  expect_exit(qpdf("--newline-before-endstream", "--preserve-unreferenced", "--object-streams=preserve", "input.pdf", "misc.pdf", cwd=folder))


@test
def test_qpdf_repair_and_exit_codes():
  folder = new_case()
  missing = qpdf("missing.pdf", "out.pdf", cwd=folder)
  check(missing.exit_code == 2, f"missing input must exit 2, got {missing.exit_code}")
  check_damaged = qpdf("--check", "damaged.pdf", cwd=folder)
  check(check_damaged.exit_code in (2, 3), f"--check damaged.pdf exit {check_damaged.exit_code}")
  repaired = qpdf("damaged.pdf", "repaired.pdf", cwd=folder)
  check(repaired.exit_code == 3, f"repair with warnings must exit 3, got {repaired.exit_code}\n{repaired.text[:300]}")
  expect_file(folder / "repaired.pdf", 1000)
  check(page_count(folder / "repaired.pdf") == 3, "repaired pdf pages")
  expect_exit(qpdf("--check", "repaired.pdf", cwd=folder), allowed=(0, 3))
  expect_text(poppler("pdftotext", "repaired.pdf", "-", cwd=folder).stdout, "Page 1 Alpha Title", "Page 3 Gamma Table")
  in_place = qpdf("--replace-input", "damaged.pdf", cwd=folder)
  check(in_place.exit_code in (0, 3), f"--replace-input exit {in_place.exit_code}\n{in_place.text[:300]}")
  expect_exit(qpdf("--check", "damaged.pdf", cwd=folder), allowed=(0, 3))
  check(page_count(folder / "damaged.pdf") == 3, "pages of the in-place repaired file")
  expect_exit(qpdf("--replace-input", "--linearize", "input.pdf", cwd=folder))
  expect_exit(qpdf("--check-linearization", "input.pdf", cwd=folder))


@test
def test_qpdf_qdf_roundtrip_with_fix_qdf():
  folder = new_case()
  expect_exit(qpdf("--qdf", "--object-streams=disable", "input.pdf", "edit.qdf", cwd=folder))
  data = (folder / "edit.qdf").read_bytes()
  marker = b"(PDF Tools Test Document)"
  if marker not in data:
    skip("title not stored as literal string in the QDF file")
  (folder / "edit.qdf").write_bytes(data.replace(marker, b"(PDF Tools Test Document EDITED BY HAND)"))
  unfixed = qpdf("--check", "edit.qdf", cwd=folder)
  check(unfixed.exit_code in (0, 3), "unfixed QDF still readable")
  with open(folder / "edit.qdf", "rb") as source, open(folder / "fixed.pdf", "wb") as target:
    fixed = subprocess.run([str(QPDF_DIR / "fix-qdf.exe")], stdin=source, stdout=target, stderr=subprocess.PIPE)
  check(fixed.returncode == 0, f"fix-qdf exit {fixed.returncode}")
  expect_exit(qpdf("--check", "fixed.pdf", cwd=folder))
  expect_text(poppler("pdfinfo", "fixed.pdf", cwd=folder).text, "EDITED BY HAND")
  expect_exit(run([QPDF_DIR / "fix-qdf.exe", "edit.qdf", "fixed-by-names.pdf"], cwd=folder))
  expect_file(folder / "fixed-by-names.pdf")


@test
def test_qpdf_attachments_and_json():
  folder = new_case()
  expect_exit(qpdf("input.pdf", "--add-attachment", "notes.txt", "--", "attached.pdf", cwd=folder))
  expect_text(qpdf("--list-attachments", "attached.pdf", cwd=folder).stdout, "notes.txt")
  shown = qpdf("--show-attachment=notes.txt", "attached.pdf", cwd=folder)
  expect_text(shown.stdout, "attachment text")
  expect_exit(qpdf("attached.pdf", "--remove-attachment=notes.txt", "removed.pdf", cwd=folder))
  check(qpdf("--list-attachments", "removed.pdf", cwd=folder).stdout.strip() == "", "attachment not removed")
  expect_exit(qpdf("input2.pdf", "--copy-attachments-from", "attached.pdf", "--", "copied.pdf", cwd=folder))
  expect_text(qpdf("--list-attachments", "copied.pdf", cwd=folder).stdout, "notes.txt")
  json_text = qpdf("--json=latest", "input.pdf", cwd=folder).stdout
  expect_text(json_text, '"qpdf"', '"pages"')
  expect_exit(qpdf("--json=latest", "--json-output", "input.pdf", "out.json", cwd=folder))
  expect_file(folder / "out.json")


@test
def test_zlib_flate_roundtrip():
  import zlib
  original = (b"zlib-flate roundtrip " * 200) + bytes(range(256))
  exe = QPDF_DIR / "zlib-flate.exe"
  compressed = run([exe, "-compress"], input_bytes=original)
  expect_exit(compressed)
  check(zlib.decompress(compressed.stdout_bytes) == original, "zlib-flate -compress output is not valid zlib data")
  fast = run([exe, "-compress=1"], input_bytes=original)
  best = run([exe, "-compress=9"], input_bytes=original)
  check(len(best.stdout_bytes) <= len(fast.stdout_bytes), "level 9 larger than level 1")
  restored = run([exe, "-uncompress"], input_bytes=zlib.compress(original))
  expect_exit(restored)
  check(restored.stdout_bytes == original, "zlib-flate -uncompress differs from original")
  check(run([exe, "-uncompress"], input_bytes=b"not zlib data").exit_code != 0, "invalid input must fail")


@test
def test_sevenzip_archive_commands():
  folder = new_case()
  formats = seven_zip("i", cwd=folder).stdout
  expect_text(formats, "7z", "zip", "Nsis")
  for archive_name, method in (("a.zip", "-tzip"), ("a.7z", "-t7z")):
    expect_exit(seven_zip("a", method, "-mx9", "-bd", "-y", archive_name, "input.pdf", "notes.txt", cwd=folder))
    expect_file(folder / archive_name)
    listing = seven_zip("l", archive_name, cwd=folder)
    expect_exit(listing)
    expect_text(listing.stdout, "input.pdf", "notes.txt", "2 files")
    expect_exit(seven_zip("t", archive_name, cwd=folder))
  extract_folder = folder / "extracted"
  expect_exit(seven_zip("x", "-y", "-bd", f"-o{extract_folder}", "a.zip", cwd=folder))
  check((extract_folder / "input.pdf").read_bytes() == (folder / "input.pdf").read_bytes(), "extracted content differs")
  expect_exit(seven_zip("e", "-y", "-bd", f"-o{folder / 'flat'}", "a.7z", "notes.txt", cwd=folder))
  expect_file(folder / "flat" / "notes.txt")
  hashes = seven_zip("h", "-scrcSHA256", "notes.txt", cwd=folder)
  expect_exit(hashes)
  expect_text(hashes.stdout, "SHA256")
  expect_exit(seven_zip("d", "-bd", "a.zip", "notes.txt", cwd=folder))
  check("notes.txt" not in seven_zip("l", "a.zip", cwd=folder).stdout, "d did not delete the entry")
  expect_exit(seven_zip("u", "-bd", "a.zip", "notes.txt", cwd=folder))
  expect_text(seven_zip("l", "a.zip", cwd=folder).stdout, "notes.txt")


@test
def test_sevenzip_password_and_errors():
  folder = new_case()
  expect_exit(seven_zip("a", "-tzip", "-pSecret123", "-mem=AES256", "-bd", "-y", "secure.zip", "input.pdf", cwd=folder))
  denied = seven_zip("t", "-pwrong", "secure.zip", cwd=folder)
  check(denied.exit_code != 0, "wrong password must fail")
  expect_exit(seven_zip("t", "-pSecret123", "secure.zip", cwd=folder))
  expect_exit(seven_zip("x", "-pSecret123", "-y", "-bd", f"-o{folder / 'out'}", "secure.zip", cwd=folder))
  expect_file(folder / "out" / "input.pdf")
  check(seven_zip("l", "missing.zip", cwd=folder).exit_code != 0, "missing archive must fail")


@test
def test_sevenzip_extracts_nsis_installer_like_setup_md():
  installer = TOOLS_DIR / "_installer" / "gs10060w64.exe"
  if not installer.is_file():
    skip(f"installer not present: {installer}")
  folder = new_case()
  listing = seven_zip("l", installer, cwd=folder)
  expect_exit(listing)
  expect_text(listing.stdout, "gswin64c.exe")


def gs_run(*arguments, cwd=None):
  return ghostscript("-dNOPAUSE", "-dBATCH", "-dQUIET", *arguments, cwd=cwd)


@test
def test_ghostscript_help_and_devices():
  help_text = ghostscript("-h").text
  expect_text(help_text, "Available devices:", "pdfwrite", "png16m", "jpeg", "tiffg4", "txtwrite", "Search path:")
  expect_text(ghostscript("--version").text, "10.")
  expect_exit(ghostscript("-dNOPAUSE", "-dBATCH", "-dQUIET", "-sDEVICE=nullpage", "input.pdf", cwd=new_case()))


@test
def test_ghostscript_output_file_forms():
  folder = new_case()
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOutputFile=a.pdf", "input.pdf", cwd=folder))
  check(page_count(folder / "a.pdf") == 3, "-sOutputFile")
  expect_exit(ghostscript("-sDEVICE=pdfwrite", "-o", "b.pdf", "input.pdf", cwd=folder))
  check(page_count(folder / "b.pdf") == 3, "-o implies -dBATCH -dNOPAUSE")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOutputFile=c%d.pdf", "input.pdf", cwd=folder))
  check(len(names_in(folder, "c*.pdf")) >= 3, f"%d pattern: {names_in(folder, 'c*')}")
  missing = gs_run("-sDEVICE=pdfwrite", "input.pdf", cwd=folder)
  check(missing.exit_code != 0 and "requires an output file" in missing.text, f"no -sOutputFile: {missing.text[:300]!r}")
  stray = gs_run("-sDEVICE=pdfwrite", "-dCompatibilityLevel=1", ".4", "-sOutputFile=d.pdf", "input.pdf", cwd=folder)
  check(stray.exit_code != 0 and "requires an output file" in stray.text, "stray input argument before -sOutputFile must reproduce the error")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOutputFile=out%%file.pdf", "input.pdf", cwd=folder))
  expect_file(folder / "out%file.pdf")
  to_stdout = gs_run("-sDEVICE=txtwrite", "-sOutputFile=-", "-dFirstPage=1", "-dLastPage=1", "input.pdf", cwd=folder)
  expect_exit(to_stdout)
  expect_text(to_stdout.stdout, "Page 1 Alpha Title")


@test
def test_ghostscript_pdfsettings_presets():
  folder = new_case()
  original = (folder / "input.pdf").stat().st_size
  sizes = {}
  for preset in ("screen", "ebook", "printer", "prepress", "default"):
    expect_exit(gs_run("-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", f"-dPDFSETTINGS=/{preset}", f"-sOutputFile={preset}.pdf", "input.pdf", cwd=folder))
    sizes[preset] = expect_file(folder / f"{preset}.pdf", 1000)
    check(page_count(folder / f"{preset}.pdf") == 3, f"{preset}: page count")
    expect_text(poppler("pdftotext", f"{preset}.pdf", "-", cwd=folder).stdout, "Page 1 Alpha Title", "Page 3 Gamma Table")
  check(sizes["screen"] < sizes["ebook"] < original, f"expected screen < ebook < original: {sizes}, original {original}")
  check(sizes["ebook"] <= sizes["printer"], f"ebook must not exceed printer: {sizes}")


@test
def test_ghostscript_downsampling_and_optimization_flags():
  folder = new_case()
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dPDFSETTINGS=/ebook", "-sOutputFile=ebook.pdf", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dDownsampleColorImages=true", "-dColorImageResolution=50",
    "-dDownsampleGrayImages=true", "-dGrayImageResolution=50", "-dDownsampleMonoImages=true", "-dMonoImageResolution=50", "-sOutputFile=r50.pdf", "input.pdf", cwd=folder))
  check(expect_file(folder / "r50.pdf") < expect_file(folder / "ebook.pdf"), "50 DPI must be smaller than the ebook preset")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dPDFSETTINGS=/screen", "-dDetectDuplicateImages=true", "-dCompressFonts=true", "-dSubsetFonts=true",
    "-dConvertCMYKImagesToRGB=true", "-dColorImageDownsampleType=/Bicubic", "-dGrayImageDownsampleType=/Bicubic", "-sOutputFile=strategy1.pdf", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dPDFSETTINGS=/ebook", "-dAutoRotatePages=/None", "-sOutputFile=base14.pdf", "input.pdf", cwd=folder))
  check(" no " in poppler("pdffonts", "base14.pdf", cwd=folder).stdout, "base-14 fonts must stay unembedded by default")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dEmbedAllFonts=true", "-dSubsetFonts=true", "-sOutputFile=embed.pdf", "-c", "<< /NeverEmbed [ ] >> setdistillerparams", "-f", "input.pdf", cwd=folder))
  fonts = poppler("pdffonts", "embed.pdf", cwd=folder).stdout
  check(re.search(r"\s+yes\s+yes\s+yes\s+\d+", fonts) is not None, f"fonts not embedded with /NeverEmbed [ ]: {fonts}")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sColorConversionStrategy=Gray", "-dProcessColorModel=/DeviceGray", "-sOutputFile=gray.pdf", "input.pdf", cwd=folder))
  expect_text(poppler("pdfimages", "-list", "gray.pdf", cwd=folder).stdout, "gray")


@test
def test_ghostscript_page_selection_and_merge():
  folder = new_case()
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dFirstPage=2", "-dLastPage=3", "-sOutputFile=pages23.pdf", "input.pdf", cwd=folder))
  check(page_count(folder / "pages23.pdf") == 2, "-dFirstPage/-dLastPage")
  expect_text(poppler("pdftotext", "pages23.pdf", "-", cwd=folder).stdout, "Page 2 Beta Section")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sPageList=1,3", "-sOutputFile=pagelist.pdf", "input.pdf", cwd=folder))
  pagelist_text = poppler("pdftotext", "pagelist.pdf", "-", cwd=folder).stdout
  expect_text(pagelist_text, "Page 1 Alpha Title", "Page 3 Gamma Table")
  check("Page 2 Beta" not in pagelist_text, "-sPageList=1,3 contains page 2")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOutputFile=merged.pdf", "input.pdf", "input2.pdf", cwd=folder))
  check(page_count(folder / "merged.pdf") == 5, "merge of two inputs in one call")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sPAPERSIZE=a4", "-dFIXEDMEDIA", "-dPDFFitPage", "-sOutputFile=a4.pdf", "input.pdf", cwd=folder))
  expect_text(poppler("pdfinfo", "a4.pdf", cwd=folder).text, "595 x 842")


@test
def test_ghostscript_raster_and_text_devices():
  folder = new_case()
  expect_exit(gs_run("-sDEVICE=png16m", "-r72", "-sOutputFile=page-%03d.png", "input.pdf", cwd=folder))
  check(names_in(folder, "page-*.png") == ["page-001.png", "page-002.png", "page-003.png"], f"names: {names_in(folder, 'page-*')}")
  check(image_size(folder / "page-001.png") == (612, 792), "png16m 72 DPI size")
  expect_exit(gs_run("-sDEVICE=pnggray", "-r36", "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-dFirstPage=1", "-dLastPage=1", "-sOutputFile=gray.png", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=jpeg", "-dJPEGQ=50", "-r36", "-dFirstPage=1", "-dLastPage=1", "-sOutputFile=pic.jpg", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=tiffg4", "-r72", "-dFirstPage=1", "-dLastPage=1", "-sOutputFile=fax.tif", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=pngalpha", "-r36", "-dFirstPage=1", "-dLastPage=1", "-sOutputFile=alpha.png", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=bmp16m", "-r36", "-dFirstPage=1", "-dLastPage=1", "-sOutputFile=pic.bmp", "input.pdf", cwd=folder))
  for name in ("gray.png", "pic.jpg", "fax.tif", "alpha.png", "pic.bmp"):
    expect_file(folder / name)
  expect_exit(gs_run("-sDEVICE=txtwrite", "-sOutputFile=out.txt", "input.pdf", cwd=folder))
  expect_text((folder / "out.txt").read_text(encoding="utf-8", errors="replace"), "Page 2 Beta Section")
  expect_exit(gs_run("-sDEVICE=ps2write", "-sOutputFile=out.ps", "-dFirstPage=1", "-dLastPage=1", "input.pdf", cwd=folder))
  expect_text((folder / "out.ps").read_text(encoding="latin-1"), "%!PS-Adobe")
  expect_exit(gs_run("-sDEVICE=eps2write", "-sOutputFile=out.eps", "-dFirstPage=1", "-dLastPage=1", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOutputFile=-", "-dFirstPage=1", "-dLastPage=1", "input.pdf", cwd=folder))


@test
def test_ghostscript_filters_metadata_and_encryption():
  folder = new_case()
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dFILTERIMAGE", "-sOutputFile=noimages.pdf", "input.pdf", cwd=folder))
  check(poppler("pdfimages", "-list", "noimages.pdf", cwd=folder).stdout.count("image") == 0, "-dFILTERIMAGE kept images")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dFILTERTEXT", "-sOutputFile=notext.pdf", "input.pdf", cwd=folder))
  check("Alpha" not in poppler("pdftotext", "notext.pdf", "-", cwd=folder).stdout, "-dFILTERTEXT kept text")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-dFILTERVECTOR", "-sOutputFile=novector.pdf", "input.pdf", cwd=folder))
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOutputFile=titled.pdf", "input.pdf", "-c", "[ /Title (Changed Title) /Author (Changed Author) /DOCINFO pdfmark", cwd=folder))
  expect_text(poppler("pdfinfo", "titled.pdf", cwd=folder).text, "Changed Title", "Changed Author")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sPDFPassword=userpw", "-sOutputFile=from-encrypted.pdf", "encrypted.pdf", cwd=folder))
  check(page_count(folder / "from-encrypted.pdf") == 3, "read encrypted input with -sPDFPassword")
  expect_exit(gs_run("-sDEVICE=pdfwrite", "-sOwnerPassword=owner1", "-sUserPassword=user1", "-dEncryptionR=3", "-dKeyLength=128",
    "-sOutputFile=encrypted-by-gs.pdf", "input.pdf", cwd=folder))
  expect_text(poppler("pdfinfo", "-upw", "user1", "encrypted-by-gs.pdf", cwd=folder).text, "Encrypted:       yes")
  denied = gs_run("-sDEVICE=pdfwrite", "-sOutputFile=denied.pdf", "encrypted.pdf", cwd=folder)
  check(denied.exit_code == 0, "KNOWN QUIRK: Ghostscript exits 0 although the password is missing; if this changed, update GHOSTSCRIPT.md")
  expect_text(denied.text, "requires a password", "**** Error")
  check((folder / "denied.pdf").stat().st_size < 5000, "output of a failed password must be an empty shell, not the document")
  wrong = gs_run("-sDEVICE=pdfwrite", "-sPDFPassword=wrong", "-sOutputFile=wrong.pdf", "encrypted.pdf", cwd=folder)
  expect_text(wrong.text, "Password did not work")


POWERSHELL_GS_PREFIX = "$gs = '" + str(GS_EXE) + "'\n"
POWERSHELL_GS_VARIANTS = {
  "unquoted_dot": ("& $gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET -sOutputFile=out.pdf input.pdf", False),
  "unquoted_relative_output": ("& $gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dQUIET -sOutputFile=out.pdf input.pdf", False),
  "unquoted_variable": ("$out = 'out.pdf'\n& $gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dQUIET -sOutputFile=$out input.pdf", False),
  "quoted_tokens": ('& $gs -sDEVICE=pdfwrite "-dCompatibilityLevel=1.4" -dNOPAUSE -dBATCH -dQUIET "-sOutputFile=out.pdf" input.pdf', True),
  "quoted_variable": ("$out = 'out.pdf'\n" + '& $gs -sDEVICE=pdfwrite "-dCompatibilityLevel=1.4" -dNOPAUSE -dBATCH -dQUIET "-sOutputFile=$out" input.pdf', True),
  "single_quoted_tokens": ("& $gs -sDEVICE=pdfwrite '-dCompatibilityLevel=1.4' -dNOPAUSE -dBATCH -dQUIET '-sOutputFile=out.pdf' input.pdf", True),
  "argument_array": ("$gsArgs = @('-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dNOPAUSE', '-dBATCH', '-dQUIET', '-sOutputFile=out.pdf', 'input.pdf')\n& $gs @gsArgs", True),
  "backtick_escape": ("& $gs -sDEVICE=pdfwrite `-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET `-sOutputFile=out.pdf input.pdf", True),
  "stop_parsing": ("& $gs --% -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dQUIET -sOutputFile=out.pdf input.pdf", True),
  "argument_file": (
    "Set-Content -LiteralPath args.txt -Value @('-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dNOPAUSE', '-dBATCH', '-dQUIET', '-sOutputFile=out.pdf', 'input.pdf')\n"
    "& $gs '@args.txt'", True),
}


@test
def test_ghostscript_powershell_argument_quoting():
  failures = []
  for name, (body, should_work) in POWERSHELL_GS_VARIANTS.items():
    folder = new_case(f"test_ghostscript_powershell_argument_quoting_{name}")
    result = run_powershell(POWERSHELL_GS_PREFIX + body + "\n", folder, name)
    produced = (folder / "out.pdf").is_file() and (folder / "out.pdf").stat().st_size > 1000
    if should_work and not produced:
      failures.append(f"{name}: expected out.pdf, exit {result.exit_code}: {result.text[:200]!r}")
    if not should_work and produced:
      failures.append(f"{name}: expected a failure but out.pdf exists")
    if name == "unquoted_dot" and "requires an output file" not in result.text:
      failures.append(f"{name}: expected the 'requires an output file' error: {result.text[:200]!r}")
    if name == "unquoted_variable" and not (folder / "$out").exists():
      failures.append(f"{name}: expected a file literally named '$out' in the current folder")
    shutil.rmtree(folder, ignore_errors=True)
  check(not failures, "PowerShell quoting behavior differs from GHOSTSCRIPT.md:\n" + "\n".join(failures))


@test
def test_ghostscript_special_characters_in_paths():
  failures = []
  names = ["space name.pdf", "Ermächtigung ünï.pdf", "bang!name.pdf", "paren (1).pdf", "semi;colon.pdf", "amp&name.pdf", "comma,name.pdf", "quote'name.pdf", "hash#name.pdf"]
  folder = new_case()
  for name in names:
    source = folder / name
    shutil.copy2(folder / "input.pdf", source)
    output = folder / f"out_{name}"
    result = gs_run("-sDEVICE=pdfwrite", f"-sOutputFile={output}", str(source), cwd=folder)
    if not output.is_file() or output.stat().st_size < 1000 or result.exit_code != 0:
      failures.append(f"{name}: exit {result.exit_code}, exists {output.is_file()}: {result.text[:160]!r}")
  sub = folder / "dir with space !x ü"
  sub.mkdir()
  shutil.copy2(folder / "input.pdf", sub / "in.pdf")
  result = gs_run("-sDEVICE=pdfwrite", f"-sOutputFile={sub / 'out.pdf'}", str(sub / "in.pdf"), cwd=folder)
  if not (sub / "out.pdf").is_file():
    failures.append(f"folder with space/bang/umlaut: {result.text[:160]!r}")
  check(not failures, "Ghostscript failed for these path styles (document workaround in GHOSTSCRIPT.md):\n" + "\n".join(failures))


@test
def test_ghostscript_stdin_and_argument_file():
  folder = new_case()
  data = (folder / "input.pdf").read_bytes()
  result = run([GS_EXE, "-dNOPAUSE", "-dBATCH", "-dQUIET", "-sDEVICE=txtwrite", "-sOutputFile=-", "-"], cwd=folder, input_bytes=data)
  expect_exit(result)
  expect_text(result.stdout, "Page 1 Alpha Title")
  (folder / "gs-args.txt").write_text("-sDEVICE=pdfwrite\n-dNOPAUSE\n-dBATCH\n-dQUIET\n-sOutputFile=from-args.pdf\ninput.pdf\n", encoding="utf-8")
  expect_exit(ghostscript("@gs-args.txt", cwd=folder))
  check(page_count(folder / "from-args.pdf") == 3, "@argument-file")


def run_skill_script(script_name, *arguments, cwd=None):
  environment = dict(os.environ)
  environment["PYTHONIOENCODING"] = "utf-8"
  return run([PYTHON_EXE, "-u", SKILL_DIR / script_name, *arguments], cwd=cwd, environment=environment)


@test
def test_script_compress_pdf_levels_and_errors():
  folder = new_case()
  original = (folder / "input.pdf").stat().st_size
  sizes = {}
  for level in ("high", "medium", "low"):
    result = run_skill_script("compress-pdf.py", "input.pdf", "--compression", level, "--output", f"out-{level}.pdf", cwd=folder)
    expect_exit(result)
    expect_text(result.stdout, "Analyzing PDF", "Done:")
    sizes[level] = expect_file(folder / f"out-{level}.pdf", 1000)
    check(page_count(folder / f"out-{level}.pdf") == 3, f"{level}: page count")
  check(sizes["high"] < original, f"high compression must shrink the fixture: {sizes}, original {original}")
  check(sizes["high"] <= sizes["medium"] <= sizes["low"] * 1.05, f"high <= medium <= low expected: {sizes}")
  nested = run_skill_script("compress-pdf.py", "input.pdf", "--output", "new folder/deep/out.pdf", cwd=folder)
  expect_exit(nested)
  expect_file(folder / "new folder" / "deep" / "out.pdf")
  missing = run_skill_script("compress-pdf.py", "missing.pdf", "--output", "never.pdf", cwd=folder)
  check(missing.exit_code == 1 and "File not found" in missing.text, f"missing input: exit {missing.exit_code} {missing.text[:200]!r}")
  expect_text(run_skill_script("compress-pdf.py", "--help", cwd=folder).stdout, "--compression", "high,medium,low")
  check(run_skill_script("compress-pdf.py", "input.pdf", "--compression", "extreme", cwd=folder).exit_code == 2, "invalid level must exit 2")


@test
def test_script_compress_pdf_special_names():
  folder = new_case()
  shutil.copy2(folder / "input.pdf", folder / "Ermächtigung ünï (1).pdf")
  result = run_skill_script("compress-pdf.py", "Ermächtigung ünï (1).pdf", "--output", "Ergebnis größer.pdf", cwd=folder)
  expect_exit(result)
  expect_file(folder / "Ergebnis größer.pdf", 1000)


@test
def test_script_convert_pdf_to_jpg():
  folder = new_case()
  out_dir = folder / "jpgs"
  result = run_skill_script("convert-pdf-to-jpg.py", "input.pdf", "--output", out_dir, "--dpi", "50", cwd=folder)
  expect_exit(result)
  check(names_in(out_dir / "input", "*.jpg") == ["input_page001.jpg", "input_page002.jpg", "input_page003.jpg"], f"names: {names_in(out_dir / 'input', '*')}")
  check(image_size(out_dir / "input" / "input_page001.jpg") == (425, 550), f"50 DPI Letter size: {image_size(out_dir / 'input' / 'input_page001.jpg')}")
  expect_exit(run_skill_script("convert-pdf-to-jpg.py", "input.pdf", "--output", folder / "range", "--pages", "2-3", "--dpi", "40", cwd=folder))
  check(names_in(folder / "range" / "input", "*.jpg") == ["input_page002.jpg", "input_page003.jpg"], "page range 2-3")
  expect_exit(run_skill_script("convert-pdf-to-jpg.py", "input.pdf", "--output", folder / "one", "--pages", "1", cwd=folder))
  check(names_in(folder / "one" / "input", "*.jpg") == ["input_page001.jpg"], "single page")
  expect_exit(run_skill_script("convert-pdf-to-jpg.py", "input.pdf", "--output", folder / "all", "--pages", "all", "--dpi", "30", cwd=folder))
  check(len(names_in(folder / "all" / "input", "*.jpg")) == 3, "pages all")
  shutil.copy2(folder / "input.pdf", folder / "Ermächtigung ünï.pdf")
  expect_exit(run_skill_script("convert-pdf-to-jpg.py", "Ermächtigung ünï.pdf", "--output", folder / "unicode", "--pages", "1", "--dpi", "30", cwd=folder))
  expect_file(folder / "unicode" / "Ermächtigung ünï" / "Ermächtigung ünï_page001.jpg")
  missing = run_skill_script("convert-pdf-to-jpg.py", "missing.pdf", "--output", folder / "x", cwd=folder)
  check(missing.exit_code == 1 and "File not found" in missing.text, f"missing input: exit {missing.exit_code}")
  broken = run_skill_script("convert-pdf-to-jpg.py", "notes.txt", "--output", folder / "y", cwd=folder)
  check(broken.exit_code == 1 and "ERROR" in broken.text, f"non-PDF input: exit {broken.exit_code} {broken.text[:200]!r}")


@test
def test_script_downsize_pdf_images():
  folder = new_case()
  out_dir = folder / "small"
  sizes = {}
  for preset, dpi in (("screen", 72), ("ebook", 150), ("printer", 300)):
    result = run_skill_script("downsize-pdf-images.py", "input.pdf", "--output", out_dir, "--preset", preset, cwd=folder)
    expect_exit(result)
    expect_text(result.stdout, "Reduction:", "Done.")
    sizes[preset] = expect_file(out_dir / f"input_{dpi}dpi.pdf", 1000)
    check(page_count(out_dir / f"input_{dpi}dpi.pdf") == 3, f"{preset}: page count")
  check(sizes["screen"] < sizes["ebook"], f"screen must be smaller than ebook: {sizes}")
  expect_exit(run_skill_script("downsize-pdf-images.py", "input.pdf", "--output", out_dir, "--dpi", "100", cwd=folder))
  expect_file(out_dir / "input_100dpi.pdf", 1000)
  expect_exit(run_skill_script("downsize-pdf-images.py", "input.pdf", "--output", out_dir, "--preset", "prepress", cwd=folder))
  shutil.copy2(folder / "input.pdf", folder / "Ermächtigung ünï.pdf")
  expect_exit(run_skill_script("downsize-pdf-images.py", "Ermächtigung ünï.pdf", "--output", folder / "unicode", "--preset", "screen", cwd=folder))
  expect_file(folder / "unicode" / "Ermächtigung ünï_72dpi.pdf", 1000)
  missing = run_skill_script("downsize-pdf-images.py", "missing.pdf", "--output", folder / "x", cwd=folder)
  check(missing.exit_code == 1 and "File not found" in missing.text, f"missing input: exit {missing.exit_code}")
  check(run_skill_script("downsize-pdf-images.py", "input.pdf", "--preset", "huge", cwd=folder).exit_code == 2, "invalid preset must exit 2")


def extract_powershell_blocks(markdown_path):
  text = Path(markdown_path).read_text(encoding="utf-8")
  retVal = []
  for match in re.finditer(r"^```powershell[ \t]*\n(.*?)\n```[ \t]*$", text, re.MULTILINE | re.DOTALL):
    line_number = text.count("\n", 0, match.start()) + 2
    retVal.append((line_number, match.group(1)))
  return retVal


def run_doc_examples(markdown_name, test_name):
  blocks = extract_powershell_blocks(SKILL_DIR / markdown_name)
  check(len(blocks) > 0, f"no powershell blocks found in {markdown_name}")
  tools_text = str(TOOLS_DIR).replace("\\", "/")
  skill_text = str(SKILL_DIR).replace("\\", "/")
  prelude = ""
  for line_number, block in blocks:
    if block.lstrip().startswith("# setup"):
      prelude += block.replace("../.tools", tools_text).replace(".devin/skills/pdf-tools", skill_text) + "\n"
  prelude = prelude.replace("../.tools", tools_text)
  failures = []
  checked = 0
  for line_number, block in blocks:
    if block.lstrip().startswith("# setup"):
      continue
    body = block.replace("../.tools", tools_text).replace(".devin/skills/pdf-tools", skill_text)
    script = "$ErrorActionPreference = 'Stop'\n$PSNativeCommandUseErrorActionPreference = $true\n" + prelude + body + "\n"
    folder = new_case(f"{test_name}_line{line_number}")
    result = run_powershell(script, folder, f"example{line_number}")
    checked += 1
    if result.exit_code != 0 or "Exception" in result.stderr or "Cannot " in result.stderr:
      failures.append(f"{markdown_name} line {line_number}: exit {result.exit_code}\n  block: {block.strip().splitlines()[0][:120]}\n  output: {result.text.strip()[-500:]}")
    else:
      shutil.rmtree(folder, ignore_errors=True)
  print(f"     ({checked} example blocks of {markdown_name} executed)")
  check(checked > 0, f"no example blocks besides setup in {markdown_name}")
  check(not failures, f"{len(failures)} of {checked} example blocks failed:\n" + "\n".join(failures))


@test
def test_doc_examples_ghostscript_md():
  run_doc_examples("GHOSTSCRIPT.md", "test_doc_examples_ghostscript_md")


@test
def test_doc_harness_detects_failures_and_invoke_gs_guards():
  folder = new_case()
  check(run_powershell("throw 'boom'", folder, "boom").exit_code != 0, "harness must report a throwing script as failed")
  check(run_powershell("& '" + str(GS_EXE) + "' --no-such-switch", folder, "badswitch").exit_code != 0, "harness must report a failing native command as failed")
  prelude = ""
  for line_number, block in extract_powershell_blocks(SKILL_DIR / "GHOSTSCRIPT.md"):
    if block.lstrip().startswith("# setup"):
      prelude += block.replace("../.tools", str(TOOLS_DIR).replace("\\", "/")) + "\n"
  check(prelude != "", "GHOSTSCRIPT.md has no '# setup' block")
  guarded = run_powershell(prelude + '$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sOutputFile=denied.pdf", "encrypted.pdf"\n', folder, "guard_password")
  check(guarded.exit_code != 0 and "Ghostscript failed" in guarded.text, f"Invoke-Gs must throw on a missing password: {guarded.text[-300:]!r}")
  fine = run_powershell(prelude + '$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sOutputFile=fine.pdf", "input.pdf"\n', folder, "guard_ok")
  check(fine.exit_code == 0 and (folder / "fine.pdf").is_file(), f"Invoke-Gs must pass a normal run: {fine.text[-300:]!r}")


@test
def test_doc_examples_skill_md():
  run_doc_examples("SKILL.md", "test_doc_examples_skill_md")


@test
def test_pdftoppm_page_number_padding():
  folder = new_case()
  expect_exit(qpdf("input.pdf", "--pages", ".", "1,1,1,1,1,1,1,1,1,1,1,1", "--", "twelve.pdf", cwd=folder))
  check(page_count(folder / "twelve.pdf") == 12, "12-page fixture")
  expect_exit(poppler("pdftoppm", "-png", "-r", "10", "twelve.pdf", "pad", cwd=folder))
  names = names_in(folder, "pad-*.png")
  check(names[0] == "pad-01.png" and names[-1] == "pad-12.png", f"padding: {names}")
  expect_exit(poppler("pdfseparate", "twelve.pdf", "sep-%d.pdf", cwd=folder))
  check(names_in(folder, "sep-*.pdf")[0] == "sep-1.pdf", "pdfseparate %d is not padded")


@test
def test_poppler_exit_codes():
  folder = new_case()
  check(poppler("pdfinfo", "missing.pdf", cwd=folder).exit_code == 1, "missing input: exit 1")
  check(poppler("pdftotext", "input.pdf", "no-such-folder/out.txt", cwd=folder).exit_code == 2, "unwritable output: exit 2")
  expect_exit(qpdf("--encrypt", "", "ownerpw", "256", "--extract=n", "--accessibility=n", "--print=none", "--modify=none", "--", "input.pdf", "restricted.pdf", cwd=folder))
  for tool_name, arguments in ("pdftotext", ["restricted.pdf", "-"]), ("pdftops", ["restricted.pdf", "out.ps"]), ("pdftoppm", ["-png", "restricted.pdf", "r"]):
    check(poppler(tool_name, *arguments, cwd=folder).exit_code == 0, f"{tool_name} must open a PDF with owner-only restrictions (empty user password)")
  check(poppler("pdfinfo", "encrypted.pdf", cwd=folder).exit_code == 1, "missing user password: exit 1")
  check(poppler("pdfinfo", "-upw", "wrong", "encrypted.pdf", cwd=folder).exit_code == 1, "wrong user password: exit 1")
  usage_error = poppler("pdftotext", cwd=folder)
  check(usage_error.exit_code == 99, f"missing arguments: exit 99, got {usage_error.exit_code}")
  unknown = poppler("pdftotext", "--no-such-option", "input.pdf", cwd=folder)
  check(unknown.exit_code != 0, f"unknown option must fail: {unknown.exit_code}")


QUOTED_TEXT_PATTERN = re.compile(r'"(?:[^"`]|`.)*"|\'[^\']*\'')
UNQUOTED_DASH_ARGUMENT_PATTERN = re.compile(r"(?:^|\s)-{1,2}[A-Za-z][A-Za-z0-9-]*=\S*[.$]")
UNQUOTED_ARGUMENT_FILE_PATTERN = re.compile(r"(?:^|\s)@[A-Za-z0-9_-]+\.[A-Za-z]+")


@test
def test_doc_examples_have_no_unquoted_dash_arguments():
  problems = []
  for markdown_name in ("SKILL.md", "GHOSTSCRIPT.md"):
    for line_number, block in extract_powershell_blocks(SKILL_DIR / markdown_name):
      for offset, line in enumerate(block.splitlines()):
        position = f"{markdown_name} line {line_number + offset}"
        if "2>&1" in line:
          problems.append(f"{position}: uses 2>&1: {line.strip()[:100]}")
        unquoted = QUOTED_TEXT_PATTERN.sub('""', line)
        if UNQUOTED_DASH_ARGUMENT_PATTERN.search(unquoted):
          problems.append(f"{position}: unquoted -option=value with '.' or '$': {line.strip()[:100]}")
        if UNQUOTED_ARGUMENT_FILE_PATTERN.search(unquoted):
          problems.append(f"{position}: unquoted @file argument (PowerShell splatting): {line.strip()[:100]}")
  check(not problems, "documented examples break the PowerShell argument rules:\n" + "\n".join(problems))
  sample = '& $gs -sDEVICE=pdfwrite "-dCompatibilityLevel=1.4" -sOutputFile=out.pdf input.pdf'
  check(UNQUOTED_DASH_ARGUMENT_PATTERN.search(QUOTED_TEXT_PATTERN.sub('""', sample)) is not None, "lint pattern must catch an unquoted -sOutputFile=out.pdf")
  good = '& $gs -sDEVICE=pdfwrite "-dCompatibilityLevel=1.4" "-sOutputFile=out.pdf" input.pdf'
  check(UNQUOTED_DASH_ARGUMENT_PATTERN.search(QUOTED_TEXT_PATTERN.sub('""', good)) is None, "lint pattern must accept quoted arguments")


@test
def test_suite_options_and_sandbox_guard():
  folder = new_case()
  suite = Path(__file__).resolve()
  sandbox = folder / ".tmp_nested_sandbox"
  case_name = "test_pdfinfo_basic_and_page_range"
  result = run([PYTHON_EXE, suite, "--filter", case_name, "--work-dir", sandbox], cwd=folder)
  expect_exit(result)
  expect_text(result.stdout, f"PASS {case_name}", "SUMMARY: 1 PASS, 0 FAIL, 0 SKIP")
  check(not (sandbox / "cases" / case_name).exists(), "case folder of a passing test must be deleted")
  kept = run([PYTHON_EXE, suite, "--filter", case_name, "--keep", "--work-dir", sandbox], cwd=folder)
  expect_exit(kept)
  check((sandbox / "cases" / case_name / "input.pdf").is_file(), "--keep must keep the case folder")
  nothing = run([PYTHON_EXE, suite, "--filter", "no_such_test_name", "--work-dir", sandbox], cwd=folder)
  expect_exit(nothing)
  expect_text(nothing.stdout, "SUMMARY: 0 PASS, 0 FAIL, 0 SKIP")
  protected = folder / "protected-folder"
  protected.mkdir()
  (protected / "marker.txt").write_text("keep me", encoding="utf-8")
  refused = run([PYTHON_EXE, suite, "--filter", case_name, "--work-dir", protected], cwd=folder)
  check(refused.exit_code == 1 and "Refusing to delete" in refused.text, f"sandbox guard: exit {refused.exit_code} {refused.text[:200]!r}")
  check((protected / "marker.txt").is_file(), "the guard must not delete a folder whose name does not start with .tmp_")


# ===== END OF TESTS =====


def main():
  parser = argparse.ArgumentParser(description="Test suite for the pdf-tools skill")
  parser.add_argument("--filter", nargs="*", default=[], help="run only tests whose name contains one of these texts")
  parser.add_argument("--verbose", action="store_true", help="print the output of failed tests in full")
  parser.add_argument("--keep", action="store_true", help="keep the folder of every test case")
  parser.add_argument("--work-dir", default=str(DEFAULT_WORK_DIR), help="sandbox folder")
  arguments = parser.parse_args()

  root = Path(arguments.work_dir).resolve()
  if root.exists():
    if not root.name.startswith(".tmp_"):
      print(f"Refusing to delete '{root}': sandbox folder name must start with '.tmp_'")
      sys.exit(1)
    shutil.rmtree(root)
  root.mkdir(parents=True)
  SANDBOX["root"] = root
  print(f"Sandbox: {root}")
  try:
    SANDBOX["fixtures"] = create_fixtures(root)
  except Exception:
    print("FIXTURES FAILED")
    traceback.print_exc()
    sys.exit(1)

  counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
  failed_names = []
  started = time.time()
  for name, function in TESTS:
    if arguments.filter:
      selected = False
      for text in arguments.filter:
        if text in name:
          selected = True
      if not selected:
        continue
    test_started = time.time()
    status = "PASS"
    detail = ""
    try:
      function()
    except TestSkipped as skipped:
      status = "SKIP"
      detail = str(skipped)
    except Exception as error:
      status = "FAIL"
      detail = str(error) if isinstance(error, AssertionError) else traceback.format_exc()
    counts[status] += 1
    print(f"{status:4} {name} ({time.time() - test_started:.1f}s)")
    if status != "PASS" and detail:
      print("     " + (detail if arguments.verbose else detail[:700]).replace("\n", "\n     "))
    if status == "FAIL":
      failed_names.append(name)
    elif not arguments.keep:
      case_folder = root / "cases" / name
      if case_folder.exists():
        shutil.rmtree(case_folder, ignore_errors=True)

  print(f"\nSUMMARY: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['SKIP']} SKIP in {time.time() - started:.0f}s")
  if failed_names:
    print("FAILED: " + ", ".join(failed_names))
  sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
  main()
