# STA Example 01: EbookChapterAndGuide

Practitioner ebook chapter written `using STA as BOOK-AUTHOR`. The studio, people, and figures are a labeled composite case.

## Context

A paid ebook for owners of small creative agencies (5-30 people) teaches basic IT resilience without assuming technical training. Chapter 5 must teach one principle, restore testing, so that a reader can apply it the same week.

## Document

```markdown
# Chapter 5: Test the Restore Before You Need It

## The backup that reported 214 successes

Composite case from three small agencies: on a Monday in May, a 12-person design studio's file server stopped booting. The backup software had reported 214 successful nightly runs in a row. When the owner tried to restore, the newest usable copy was four days old, because a full disk had silently cut every backup short since Thursday. Four days of work for 12 designers, about 380 hours, had to be redone before two client deadlines.

## An untested backup is a promise nobody has checked

A backup report tells you that copying started and ended. It does not tell you that you can open the files afterwards. Untested backups are not a recovery plan: a backup only counts after you have restored from it and opened what came back.

The reason is simple. Backups fail in ways the backup software cannot see: full disks, changed folder paths, expired passwords for the storage account. Only a restore exposes these failures, and a restore you run on a quiet Tuesday costs minutes instead of days.

## How to test a restore in your studio

1. Pick the one folder your studio cannot work without, usually the active client projects.
2. Create an empty test folder on a different drive or computer.
3. Restore yesterday's backup of the chosen folder into the test folder.
4. Open three files of different types (a layout, an image, a spreadsheet) and compare them with the originals - they should open without errors and show yesterday's changes.
5. Write the date and the result in a shared note titled "Restore tests".
6. Put a repeating 20-minute appointment in your calendar for the first Tuesday of every month.

Quick check: you can name the date of your last successful test restore without looking it up.

## What would have changed in May

If the studio owner had run this test on the first Tuesday of May, the full disk would have appeared as a failed restore and been fixed in an afternoon. The server would still have failed on that Monday; the studio would have lost one night of work instead of four days.
```

## Key Decisions

- SHOW in 4 sentences with numbers (214 runs, 12 designers, 380 hours), labeled as composite (STA-CT-01, STA-EV-01, STA-EV-03)
- One principle for the whole chapter, stated directly after the case (STA-ST-01, STA-ST-02)
- Six numbered single-action steps written for any backup tool, with the expected result in step 4, where readers most often get stuck (STA-ST-03, STA-CT-03)
- Quick check is observable and immediate (STA-EV-02)
- Persona `BOOK-AUTHOR` (Warmth 6, Technicality 3): plain words for a non-technical owner; one trait, The Colon Law, in the principle paragraph ("Untested backups are not a recovery plan: ..."); the chapter close returns to the opening case
