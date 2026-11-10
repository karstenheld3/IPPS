# STA Rules

Output standards for documents written `using STA` (case, principle, numbered application, quick check).

**Writing quality:** Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: APAPL-PR-07 (be specific), APAPL-PR-08 (examples for non-obvious rules), MECT-VO-02 (address reader as "you").

## Rule Index

Structure (ST)
- STA-ST-01: SHOW comes before TELL
- STA-ST-02: One principle per chapter or unit
- STA-ST-03: APPLY uses numbered steps, one action each
- STA-ST-04: Each unit ends with a quick check

Content (CT)
- STA-CT-01: SHOW has 3-5 sentences and no atmospheric filler
- STA-CT-02: TELL states the principle in 1-2 sentences
- STA-CT-03: Steps are transferable to the reader's context

Evidence (EV)
- STA-EV-01: SHOW case is real and attributed, or labeled as composite
- STA-EV-02: Quick check is observable and takes under 15 minutes
- STA-EV-03: Numbers in the case carry unit and context

## STA-ST-01: SHOW Before TELL

**BAD:**
```
Principle: always test your backups. Here is why. [case follows]
```

**GOOD:**
```
A design studio lost four days of client files when its nightly backup failed to restore.
[2-3 more sentences] An untested backup is a hope, not a backup.
```

## STA-ST-02: One Principle per Unit

**BAD:** One chapter teaches restore testing, password rotation, and disk encryption.

**GOOD:** Chapter teaches restore testing only; encryption moves to its own chapter.

## STA-ST-03: Numbered Single-Action Steps

**BAD:** "Set up a schedule, test a restore and document everything, then tell the team."

**GOOD:**
```
1. Pick one folder your team cannot work without.
2. Restore yesterday's backup of that folder to an empty test location.
3. Open three files and compare them with the originals.
```

## STA-ST-04: Quick Check per Unit

**BAD:** The chapter ends after the steps.

**GOOD:** "Quick check: you can name the date of your last successful test restore without looking it up."

## STA-CT-01: Lean SHOW

**BAD:** "It was a rainy Monday, and the coffee machine was broken, when..."

**GOOD:** "On a Monday in May, the studio's file server failed. The backup software reported 214 successful nightly runs."

## STA-CT-02: Short Principle

**BAD:** A 200-word paragraph that circles the idea without stating it.

**GOOD:** "An untested backup is a hope, not a backup."

## STA-CT-03: Transferable Steps

**BAD:** "Open VendorX Console 4.2 and click the green button."

**GOOD:** "Open your backup tool's restore function." (tool-specific notes follow as an optional sub-bullet)

## STA-EV-01: Real or Labeled Case

**BAD:** A named "real" company that does not exist.

**GOOD:** "A composite case from three small agencies:" or a named, sourced case.

## STA-EV-02: Observable Quick Check

**BAD:** "Make sure you feel confident about your backups."

**GOOD:** "Quick check: restore one file from last week; it should open within 15 minutes."

## STA-EV-03: Numbers with Context

**BAD:** "They lost a lot of data."

**GOOD:** "They lost four working days of files for 12 designers, about 380 hours of work."
