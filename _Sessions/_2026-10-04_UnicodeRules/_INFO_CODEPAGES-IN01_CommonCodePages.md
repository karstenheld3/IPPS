# INFO: Common Code Pages and the Problems They Cause

**Doc ID**: CODEPAGES-IN01
**Goal**: Identify the legacy code pages a Windows-centric codebase meets in practice, what each cannot represent, how its mojibake looks, and which traps it adds beyond mojibake
**Timeline**: Created 2026-10-04, 1 update

**Depends on:**
- `@skills:coding-conventions` `UNICODE_RULES.md` for the rules this document provides evidence for

## Summary

- UTF-8 is used by 99.1% of websites with known encoding (October 2026); every legacy code page together is below 1% [VERIFIED]
- Every Windows locale has two legacy code pages at once: ANSI (GUI, files, `GetACP`) and OEM (console, `cmd.exe`, batch files). They differ for all European locales: 1252/850 (Western Europe), 1250/852 (Central Europe), 1251/866 (Cyrillic) [TESTED]
- East Asian locales (932, 936, 949, 950) are multi-byte (DBCS) and use the same code page for ANSI and OEM [TESTED]
- Single-byte code pages cover one script each; Windows-1252 cannot store `ő` (Hungarian) or `€` in ISO-8859-1. Encoding outside the repertoire produces `?` or best-fit letters - silent, irreversible data loss [TESTED]
- On the web and in every WHATWG-conformant decoder, the labels `iso-8859-1`, `latin1`, and `ascii` mean Windows-1252 [VERIFIED]
- Shift_JIS (932) and Big5 (950) use byte `0x5C` (backslash) as the second byte of some characters (`ソ` = `83 5C`, `表` = `95 5C`, `許` = `B3 5C`) - byte-based path, escape, and regex processing breaks [TESTED]
- On Japanese and Korean systems byte `0x5C` / U+005C displays as `¥` / `₩`; the character is still the path separator [VERIFIED]
- Cyrillic has three competing legacy encodings (1251, 866, KOI8-R) that turn the same word into three different garbage strings [TESTED]
- GB 18030-2022 is a mandatory national standard in China since 2023-08-01 for products processing Chinese text [VERIFIED]
- Recommendation: UTF-8 everywhere, legacy code pages only at explicitly declared input boundaries, never as output (UNICODE-GN-01, UNICODE-GN-02, UNICODE-GN-05)

## Table of Contents

1. [Which Code Pages Matter](#1-which-code-pages-matter)
2. [Code Page Families](#2-code-page-families)
3. [Problems per Code Page](#3-problems-per-code-page)
4. [Cross-Cutting Problems](#4-cross-cutting-problems)
5. [Implications for Code](#5-implications-for-code)
6. [Exclusions](#6-exclusions)
7. [Sources](#7-sources)
8. [Document History](#8-document-history)

## 1. Which Code Pages Matter

### 1.1 ANSI and OEM Code Page per Windows Locale

Read from .NET `CultureInfo.TextInfo` (Windows NLS data) on Windows 11 [TESTED]:

- en-US: ANSI 1252, OEM 437
- de-DE, fr-FR, pt-BR: ANSI 1252, OEM 850
- pl-PL, cs-CZ, hu-HU: ANSI 1250, OEM 852
- ru-RU, uk-UA: ANSI 1251, OEM 866
- el-GR: ANSI 1253, OEM 737
- tr-TR: ANSI 1254, OEM 857
- he-IL: ANSI 1255, OEM 862
- ar-SA: ANSI 1256, OEM 720
- lt-LT: ANSI 1257, OEM 775
- vi-VN: ANSI 1258, OEM 1258
- th-TH: ANSI 874, OEM 874
- ja-JP: 932 (Shift_JIS) for both
- zh-CN: 936 (GBK) for both
- ko-KR: 949 (Unified Hangul Code) for both
- zh-TW: 950 (Big5) for both

The active pair follows the system locale ("Language for non-Unicode programs"), not the display language [VERIFIED: Microsoft Learn, Code Pages]. Test machine: GetACP 1252, console 437 [TESTED].

```
Windows process
├─> GUI, files, "A" APIs ........ ANSI code page (GetACP)      e.g. 1252
├─> Console, cmd.exe, .bat ...... OEM code page (chcp)         e.g. 850 / 437
├─> Wide "W" APIs, .NET strings . UTF-16LE (no code page)
└─> UTF-8 ....................... code page 65001, only when explicitly used
                                  or when the system-wide UTF-8 beta option is on
```

### 1.2 Web Usage

W3Techs, October 2026, share of websites with known encoding [VERIFIED]:
- UTF-8: 99.1%
- Above 0.1%: ISO-8859-1, Windows-1252, Windows-1251, EUC-JP
- Below 0.1%: Shift_JIS, EUC-KR, Windows-1250, GB2312, ISO-8859-2, Big5, ISO-8859-15, all others

Web usage understates legacy code pages in local files: CSV exports, batch files, console output, and archives are not counted.

## 2. Code Page Families

- Windows-125x (1250-1258): 9 single-byte ANSI code pages by Microsoft, ASCII in 0x00-0x7F, script-specific characters in 0x80-0xFF. Each is close to, but not identical with, an ISO-8859 part [VERIFIED]
- DOS / OEM (437, 737, 775, 850, 852, 857, 862, 866, ...): single-byte console code pages with box-drawing characters; same letters as the ANSI code page at different byte positions [VERIFIED]
- East Asian DBCS (932, 936, 949, 950): 1 or 2 bytes per character; the lead byte is >= 0x81, the trail byte can be an ASCII value [VERIFIED]
- ISO-8859-x: international single-byte standards; 0x80-0x9F are C1 control characters, not printable [VERIFIED]
- Mac (10000 Mac Roman, 10007 Mac Cyrillic, ...): classic Mac OS encodings, found in pre-2001 files [ASSUMED]; Mac Roman read as 1252: `Müller Café` → `MŸller CafŽ` [TESTED]
- GB 18030: Chinese national standard, 1, 2, or 4 bytes per character [VERIFIED: GB 18030-2022 text], maps characters outside the BMP (`😀` = `94 39 FC 36`) [TESTED]

## 3. Problems per Code Page

Mojibake strings below are computed with Python codecs (write with one code page, read with another) [TESTED].

### 3.1 Windows-1252 (Western Europe, Americas)

- Repertoire: Western European Latin letters plus 27 symbols in 0x80-0x9F, among them `€`, curly quotes U+2018-U+201D, `–`, `—`, `…`, `™`, `Š š Ž ž Œ œ Ÿ`
- Cannot represent: Central European letters (`ő ű ł ć ř`), Greek, Cyrillic, all Asian scripts. `Erdős` → `UnicodeEncodeError` in Python, `Erdos` or `Erd?s` in .NET best-fit [TESTED]
- UTF-8 read as 1252: `Café` → `CafÃ©`, `Erdős` → `ErdÅ‘s`, `’` → `â€™` [TESTED]; the pattern behind most mojibake in Western European data [ASSUMED]; reversible with `repair_mojibake_win-1252.py` [TESTED]
- 5 undefined bytes (0x81, 0x8D, 0x8F, 0x90, 0x9D): .NET maps them to U+0081 etc., Python `cp1252` raises an error - repair tools must handle both [TESTED]
- Confusion with ISO-8859-1: identical in 0xA0-0xFF, different in 0x80-0x9F. `€` (0x80 in 1252) has no ISO-8859-1 code; 1252 text read as Latin-1 turns `€` into invisible U+0080 [TESTED]
- Read as OEM 850: `Müller Café` → `M³ller CafÚ`; 850 read as 1252: `M�ller Caf‚` [TESTED]

### 3.2 OEM 437 and 850 (Console, Western)

- 437: US console default; box-drawing characters in 0xB0-0xDF, only 8 Latin capitals beyond ASCII (`Ç Ä Å É Æ Ö Ü Ñ`) [TESTED]
- 850: Western European console default, full ISO-8859-1 repertoire at different positions [VERIFIED]
- Problem: same machine, different code page than files (1252). Text written by a console program and read by a GUI program, or the reverse, is garbled even without UTF-8 involved [TESTED]
- UTF-8 read as 437: `Café` → `Caf├⌐`, UTF-8 BOM → `∩╗┐` (visible in `cmd.exe` error messages) [TESTED]
- ZIP names without UTF-8 flag are defined as 437; tools on 850 systems write 850 → `Sørensen` read as 437 shows `S¢rensen` [TESTED]

### 3.3 Windows-1250 and OEM 852 (Central Europe)

- Covers Polish, Czech, Slovak, Hungarian, Slovenian, Croatian, Albanian, and Romanian with cedilla letters `Ş ş Ţ ţ` only - the correct comma-below letters `Ș ș` are not representable [TESTED]
- 1250 read as 1252: `Łódź Žluťoučký` → `£ódŸ Žlu�ouèký` - partially readable, so the corruption is often missed [TESTED]
- UTF-8 read as 1250: `Łódź` → `Ĺ�ĂłdĹş` [TESTED]
- 852 read as 1250: `Łódź` → `ť˘d«` [TESTED]

### 3.4 Windows-1251, OEM 866, KOI8-R (Cyrillic)

- Three legacy encodings in parallel use: 1251 (Windows files), 866 (console), KOI8-R / KOI8-U (Unix, old e-mail) [VERIFIED]
- `Привет` misread [TESTED]:
  - UTF-8 as 1251: `РџСЂРёРІРµС‚` (typical: alternating `Р` / `С`)
  - 1251 as 866: `╧ЁштхЄ`
  - 866 as 1251: `ЏаЁўҐв`
  - KOI8-R as 1251: `рТЙЧЕФ` (case inverted)
  - 1251 as 1252: `Ïðèâåò`
- Problem: mojibake of Cyrillic as Cyrillic still looks like Cyrillic letters, so non-Russian-speaking developers do not notice it

### 3.5 Windows-1253 (Greek), 1254 (Turkish), 1255 (Hebrew), 1256 (Arabic), 1257 (Baltic), 1258 (Vietnamese), 874 (Thai)

- 1253 read as 1252: `Καλημέρα` → `ÊáëçìÝñá` [TESTED]
- 1254 read as 1252: `İstanbul ığdır şeker` → `Ýstanbul ýðdýr þeker`; UTF-8 read as 1254: `Ä°stanbul Ä±ÄŸdÄ±r ÅŸeker` [TESTED]
- Turkish casing is a locale problem on top of the code page: dotted `İ` lowercases to `i` + U+0307 (2 code points), dotless `ı` uppercases to `I`. Culture-sensitive `ToUpper()` / `ToLower()` on identifiers breaks comparisons; use invariant culture for keys [TESTED: Python `'İ'.lower()` length 2]
- 1255 read as 1252: `שלום` → `ùìåí`; 1256: `مرحبا` → `ãÑÍÈÇ` [TESTED]. Right-to-left scripts add display-order problems independent of encoding
- 1258 Vietnamese uses combining diacritics for some tones; the same visible text exists in precomposed and decomposed form → NFC normalization needed (UNICODE-GN-08) [ASSUMED]
- 874 Thai: extends TIS-620 / ISO-8859-11 with characters from 1252 [VERIFIED]

### 3.6 East Asian Multi-Byte Code Pages (932, 936, 949, 950) and GB 18030

- 932 Shift_JIS (Japan), 936 GBK (Simplified Chinese), 949 Unified Hangul Code (Korea), 950 Big5 (Traditional Chinese): ANSI and OEM at once, 1-2 bytes per character [TESTED: locale table]
- Trail byte 0x5C: Shift_JIS `ソ` = `83 5C`, `表` = `95 5C`, `能` = `94 5C`, `十` = `8F 5C`, `予` = `97 5C`, `構` = `8D 5C`, `申` = `90 5C`; Big5 `許` = `B3 5C` [TESTED]. Code that scans bytes for `\` (path splitting, escape handling, regex, C string literals) cuts these characters in half [VERIFIED: Microsoft Learn, Double-Byte Character Sets]
- Byte-level APIs on a 932 system fail for file names containing these characters; Unicode ("W") APIs are unaffected [VERIFIED: Stack Overflow 8857221]
- Mojibake [TESTED]:
  - Shift_JIS read as 1252: `ソフト 東京` → `ƒ\ƒtƒg “Œ‹ž` (note the backslash)
  - UTF-8 read as 932: `ソフト 東京` → `繧ｽ繝輔ヨ 譚ｱ莠ｬ` (looks like real Japanese text)
  - Shift_JIS read as UTF-8: `�\�t�g ����` (lossy)
  - GBK read as 1252: `中文 编码` → `ÖÐÎÄ ±àÂë`; UTF-8 read as GBK: `涓�鏂� 缂栫爜`; GBK read as Big5: `笢恅 晤鎢`
  - 949 read as 1252: `한국어` → `ÇÑ±¹¾î`
- Mojibake between two CJK code pages produces valid-looking CJK characters; only native readers detect it
- GB 18030: mandatory national standard GB 18030-2022, in force since 2023-08-01, three implementation levels; level 2 applies to operating systems, databases, middleware [VERIFIED: SAC announcement, GB 18030-2022 text]. Superset of GBK; maps characters outside the Basic Multilingual Plane (BMP) with 4-byte sequences [TESTED]

### 3.7 ISO-8859-1, ISO-8859-15, and the "latin1" Label

- WHATWG Encoding Standard: labels `iso-8859-1`, `latin1`, `l1`, `us-ascii`, `ascii`, `windows-1252` all resolve to windows-1252; browsers decode 0x80 as `€` even for a document declared "ASCII" [VERIFIED]
- Python `latin-1` and .NET `GetEncoding(28591)` are true ISO-8859-1 (0x80 = U+0080). Data that a browser wrote as "iso-8859-1" can contain 1252 bytes in 0x80-0x9F that these decoders turn into invisible controls [TESTED]
- ISO-8859-15 (Latin-9) adds `€ Š š Ž ž Œ œ Ÿ` at 0xA4-0xBE, different positions than 1252. 1252 read as ISO-8859-15: `€ Œ` → U+0080 U+008C (invisible) [TESTED]
- Windows PowerShell 5.1 `Export-Csv` (ASCII default) stores `€` as `?` [TESTED]; HTTP clients and databases configured as "Latin-1" lose `€` the same way [ASSUMED]

## 4. Cross-Cutting Problems

- Two code pages per machine: a value passed from a GUI program (ANSI) to a console program (OEM) or batch file is re-interpreted. Example: 1252 `Müller Café` displayed as 850 → `M³ller CafÚ` [TESTED]
- Untagged data: CSV, TXT, batch files, console pipes, and ZIP names carry no encoding declaration. The reader guesses from its own locale; the same file gives different text on machines with different system locales [VERIFIED: Wikipedia, Windows code page]
- Lossy encoding: encoding Unicode text into a code page that lacks a character yields `?` (strict-less encoders), best-fit substitutes (`ő` → `o`), or an exception (Python strict) [TESTED]. Best-fit can also produce dangerous characters: U+00A5 `¥` best-fits to 0x5C (backslash) on 932 under Windows "A" APIs [VERIFIED: Michael Kaplan, When is a backslash not a backslash]; Python `cp932` has no best-fit and emits `?` [TESTED]
- Display of U+005C: Japanese and Korean fonts on Japanese/Korean system locales draw backslash as `¥` / `₩`. Paths shown as `C:¥Users¥...` are correct [VERIFIED: Michael Kaplan]
- Mojibake detection by eye fails within one script family (Cyrillic ↔ Cyrillic, CJK ↔ CJK, 1250 → 1252 partially readable); detection needs strict decoding, not visual review [TESTED]
- Case mapping: Turkish/Azeri `i`/`İ`/`ı`/`I` and German `ß` → `SS` change string length or identity under case conversion (`'ß'.upper()` = `'SS'`) [TESTED]

## 5. Implications for Code

- Write UTF-8 only; never produce legacy code page output except for a consumer that requires it (UNICODE-GN-02, UNICODE-BM-08)
- Read legacy input only with an explicitly configured code page per input source, never with the process default (UNICODE-GN-01, UNICODE-GN-05)
- For DBCS input (932, 936, 949, 950): decode to Unicode before any byte-level search for `\`, `/`, quotes, or delimiters
- For console boundaries: set the console / pipe encoding explicitly (UNICODE-PR-01); do not assume ANSI = OEM
- For archives: set `metadata_encoding` to the creator's OEM code page (UNICODE-PR-04)
- For case-insensitive keys: use invariant culture or Unicode case folding (`str.casefold()`), plus NFC (UNICODE-GN-08)

## 6. Exclusions

- EBCDIC (IBM mainframe code pages 037, 500, 1047): not met in Windows/web data paths of this workspace
- ISO-2022-JP, EUC-JP, EUC-KR: stateful or Unix encodings, mainly e-mail and legacy web; EUC-JP still above 0.1% web share, decoding only via explicit label
- UTF-7: deprecated, PowerShell 7.1+ warns on use
- Font and rendering problems (missing glyphs, tofu boxes): not encoding errors
- Database collations and server-side character sets: separate topic

## 7. Sources

Research for this document:
- `CODEPAGES-IN01-SC-WIKI-WINCP`: https://en.wikipedia.org/wiki/Windows_code_page - Windows-125x series, DOS code pages, problems section [VERIFIED]
- `CODEPAGES-IN01-SC-W3T-ENC`: https://w3techs.com/technologies/overview/character_encoding - UTF-8 99.1% of websites, October 2026 [VERIFIED]
- `CODEPAGES-IN01-SC-WHATWG-ENC`: https://encoding.spec.whatwg.org/ - section 4.2, `latin1`/`ascii` labels resolve to windows-1252 [VERIFIED]
- `CODEPAGES-IN01-SC-MSL-CPID`: https://learn.microsoft.com/en-us/windows/win32/Intl/code-page-identifiers - code page numbers and names (932, 936, 949, 950) [VERIFIED]
- `CODEPAGES-IN01-SC-MSL-DBCS`: https://learn.microsoft.com/en-us/windows/win32/intl/double-byte-character-sets - trail byte can look like backslash, byte scanning unsafe [VERIFIED]
- `CODEPAGES-IN01-SC-MK-BKSL`: https://archives.miloush.net/michkap/archive/2005/09/17/469941.html - 0x5C displayed as yen/won, best-fit mapping of U+00A5 / U+20A9 to 0x5C [VERIFIED]
- `CODEPAGES-IN01-SC-SO-SJIS5C`: https://stackoverflow.com/questions/8857221 - byte-based file APIs fail for Shift_JIS names with 0x5C trail byte [VERIFIED]
- `CODEPAGES-IN01-SC-JAWIKI-SJIS`: https://ja.wikipedia.org/wiki/Shift_JIS - list of characters with trail byte 0x5C, mojibake examples [VERIFIED]
- `CODEPAGES-IN01-SC-SAC-GB18030`: https://std.sacinfo.org.cn/gnoc/queryInfo?id=8274D316D07E79F65E062DC53CC5B1D2 - GB 18030-2022 mandatory, in force 2023-08-01 [VERIFIED]
- `CODEPAGES-IN01-SC-UTC-GB18030`: https://www.unicode.org/L2/L2022/22274r-disruptive-changes.pdf - GB 18030-2022 implementation levels, disruptive mapping changes [VERIFIED]
- Local tests 2026-10-04: .NET `CultureInfo.TextInfo` code page pairs (Windows PowerShell 5.1), Python 3.12 codecs for all mojibake strings

Evidence for `@skills:coding-conventions` `UNICODE_RULES.md` (moved from the rules file):
- `CODEPAGES-IN01-SC-MSPS-CHRENC`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1 - PowerShell 5.1 and 7 encoding defaults per cmdlet, BOM advice for scripts [VERIFIED]
- `CODEPAGES-IN01-SC-RFC-8259`: https://www.rfc-editor.org/rfc/rfc8259#section-8.1 - JSON MUST be UTF-8, MUST NOT add BOM [VERIFIED]
- `CODEPAGES-IN01-SC-PEP-686`: https://peps.python.org/pep-0686/ - UTF-8 mode default from Python 3.15 [VERIFIED]
- `CODEPAGES-IN01-SC-PEP-597`: https://peps.python.org/pep-0597/ - `EncodingWarning`, `-X warn_default_encoding` [VERIFIED]
- `CODEPAGES-IN01-SC-PEP-790`: https://peps.python.org/pep-0790/ - 3.15.0 final expected 2026-10-09 [VERIFIED]
- `CODEPAGES-IN01-SC-PY-WN315`: https://docs.python.org/3.15/whatsnew/3.15.html - Python 3.15 uses UTF-8 as default encoding (docs at 3.15.0rc3 on 2026-10-04) [VERIFIED]
- `CODEPAGES-IN01-SC-W3C-XML`: https://www.w3.org/TR/REC-xml/ - section 4.3.3, UTF-16 entities must begin with BOM [VERIFIED]
- `CODEPAGES-IN01-SC-WHATWG-HTML`: https://html.spec.whatwg.org/dev/semantics.html - `meta charset` within first 1024 bytes, must be `utf-8` [VERIFIED]
- `CODEPAGES-IN01-SC-YAML-122`: https://yaml.org/spec/1.2.2/ - section 5.2, BOM allowed at document start, UTF-8 recommended output [VERIFIED]
- `CODEPAGES-IN01-SC-MSO-CSV`: https://support.microsoft.com/en-us/office/opening-csv-utf-8-files-correctly-in-excel-8a935af5-3416-4edd-ba7e-3dfd2bc4a032 - Excel opens UTF-8 CSV normally only with BOM [VERIFIED]
- `CODEPAGES-IN01-SC-MSL-XLSEP`: https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/formula-errors - Excel uses the Windows list separator as CSV delimiter [VERIFIED]
- `CODEPAGES-IN01-SC-MSPS-IWR74`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.4 - 7.4 request encoding defaults to UTF-8 (requests only) [VERIFIED]
- `CODEPAGES-IN01-SC-GH-PS20488`: https://github.com/PowerShell/PowerShell/issues/20488 - 5.1 decodes as ISO-8859-1; 7.0 UTF-8 for JSON responses, 7.4 for all (community comment) [VERIFIED]
- `CODEPAGES-IN01-SC-REQ-UTILS`: https://github.com/psf/requests/blob/main/src/requests/utils.py - `get_encoding_from_headers`: `text/*` → ISO-8859-1, `application/json` → utf-8 [VERIFIED]
- `CODEPAGES-IN01-SC-PYI-ENV`: https://pyinstaller.org/en/latest/advanced-topics.html - frozen apps do not process Python interpreter environment variables [VERIFIED]
- `CODEPAGES-IN01-SC-YTDLP-README`: https://github.com/yt-dlp/yt-dlp/blob/master/README.md - `--encoding ENCODING` (experimental) [VERIFIED]
- `CODEPAGES-IN01-SC-PKW-APPNOTE`: https://pkwaredownloads.blob.core.windows.net/pkware-general/Documentation/APPNOTE-6.3.0.TXT - bit 11 = UTF-8 names, Appendix D [VERIFIED]
- `CODEPAGES-IN01-SC-CPY-ZIP`: https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py - `_encodeFilenameFlags` sets UTF-8 flag for non-ASCII names [VERIFIED]
- `CODEPAGES-IN01-SC-CPY-ET`: https://github.com/python/cpython/blob/3.12/Lib/xml/etree/ElementTree.py - `_get_writer`: `encoding='unicode'` with file name writes UTF-8 [VERIFIED]
- `CODEPAGES-IN01-SC-MSPS-CTJ`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-json?view=powershell-7.5 - depth warning since 7.1 [VERIFIED]
- `CODEPAGES-IN01-SC-MSPS-CLIXML`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/export-clixml?view=powershell-7.5 - default `utf8NoBOM` in 7 [VERIFIED]
- `CODEPAGES-IN01-SC-SO-UTF8BETA`: https://stackoverflow.com/questions/56419639 - UTF-8 beta option sets ACP/OEMCP/MACCP to 65001 [VERIFIED]
- `CODEPAGES-IN01-SC-MSL-UTF8CP`: https://learn.microsoft.com/en-us/windows/apps/design/globalizing/use-utf8-code-page - UTF-8 code page, system-wide beta option [VERIFIED]
- `CODEPAGES-IN01-SC-ONT-BATU16`: https://devblogs.microsoft.com/oldnewthing/20210726-00/?p=105483 - UTF-16LE batch file: null byte ends the file after the first character [VERIFIED]
- `CODEPAGES-IN01-SC-SU-BATBOM`: https://superuser.com/questions/601282 - `cmd.exe` treats UTF-8 BOM as part of first command [VERIFIED]
- `CODEPAGES-IN01-SC-SU-CHCP`: https://superuser.com/questions/1118106 - `chcp 65001` in batch files [VERIFIED]
- `CODEPAGES-IN01-SC-SO-SHEBANG`: https://stackoverflow.com/questions/19065522 - BOM breaks shebang [VERIFIED]
- `CODEPAGES-IN01-SC-SO-EXCELCSV`: https://stackoverflow.com/questions/155097 - Excel CSV BOM behavior across versions [VERIFIED]
- Local tests 2026-10-04: Windows 11, Windows PowerShell 5.1.26100, PowerShell 7.5.0, Python 3.12.6, system code page 1252, console code page 437

## 8. Document History

**[2026-10-04 21:45]**
- Initial research: locale code page pairs, per-code-page problems and mojibake signatures, cross-cutting problems
- Moved: source list from `UNICODE_RULES.md` (sources do not belong in rule files)
