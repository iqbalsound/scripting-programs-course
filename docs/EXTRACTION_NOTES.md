# Extraction notes

How this repository was produced from the source files, and what to double-check.

## Sources

| Source file | Used for |
| --- | --- |
| `Scripting_Programs_Combined_Lab_Manual_Fall_2026.pdf` (136 pages) | 32 labs (16 per course): theory, steps, code, required tasks; tools table; manual change log |
| `Lecture_Notes_Weeks_1-16_Fall_2026.docx` | Week folders, code examples, evidence-based questions, quizzes with model answers, assignments, class task, appendices |
| `Lab_Manual_Verification_Report_Fall_2026.docx` | `CHANGELOG.md` and `docs/verification-report.md` |

## Code from the PDF

The PDF wraps long code lines at 70 characters, so line breaks had to be rebuilt. All 226 code blocks were reconstructed from character positions (indentation and blank lines preserved) and re-joined where a line had only been wrapped by the page. The result was syntax-checked: every Python block parses, every JavaScript block passes `node --check`, every Bash block passes `bash -n` (except blocks containing placeholders such as `<newest-node-template>` or a `(Pdb)` session, which are not shell code).

Known manual repair: in Lab 2 (both courses) the PDF shows the `log.write(...)` line after `with open(...) as log:` without indentation and with a blank line; it was indented so the script runs.

Please still read each script once before running it. Ambiguous wrap points were resolved with syntax checks, not by the original source files.

## File names

Code files are named from the file names mentioned in the lab text. Where the text gives none, the file is named after the step (for example `step08_keys-and-rate-limits.py`) and is a snippet to add to an existing script, not a standalone program. Commands (Bash one-liners) stay in the lab README only.

## Lecture notes

Code in the lecture notes is saved under each week's `code/` folder. `example_NN.*` files are named by order because the text does not name them.
