# Change log printed at the end of the lab manual (PDF pages 133–136)

The 35-row table is merged with the verification findings in [`../CHANGELOG.md`](../CHANGELOG.md).

This edition was regenerated from the Fall 2026 verification report (35 findings: 11 blockers, 12 major,
12 minor) using the corrected code of the solution pack. The table lists every finding and what was
changed in this manual.

### Changes made for each finding


[table of changes: see CHANGELOG.md]


### New material added

- Lab 1 Step 7 (Git and Docker once) and Step 8 (.gitignore and first commit).
- Lab 2: exception primer; CCSP resources.csv generator.
- Lab 6: local test page for offline testing; Lab 9: local mock API.
- Lab 12: tamper-evidence step; Lab 13: build-cache, .dockerignore and --env-file demonstrations.
- Lab 15: Trivy scan and GitHub Actions route; Lab 16: complete connected pipelines for both
courses.
- Evidence rules, Windows/WSL2 guidance and the lab-to-week mapping in How to Use This
Manual.

### Formatting standard applied


| Element | Setting |
| --- | --- |
| Regular text | Aptos 12, justified |
| Headings | Aptos bold in deep dark purple: 18 (parts, lab titles, major sections), 16 (section headings), 14 (step titles); justified |
| Code and configuration | Aptos Mono 12, left aligned, in a grey box with a purple left bar and a language label |
| Tables | Aptos 12, justified, deep dark purple header row with white text |
| Page | A4 portrait, margins, header and footer unchanged; each lab starts on a new page |


### Verification status and open items

- Code in Labs 1–7 and 9–12 comes from the tested solution pack, and the new snippets (mock API,
resources generator, Lab 8 harness and handlers, CCSP alert, parsers, both capstone pipelines
against a local SMTP sink) were run when this edition was built. Not run: faasd (Lab 8 Tier 2),
Docker (Labs 13, 14, 16 container steps), Jenkins and GitHub Actions (Lab 15), Moto/aws CLI
steps and the public websites; please run Labs 13 and 15 once on a lab PC before term.
- Decision needed: whether the faasd CE EULA covers classroom use. Until then Tier 1 of Lab 8 is
the graded route.
- Placeholders to fill before term: the Trivy version in the Jenkinsfile and the pinned Trivy action tag
in ci.yml; check the current major versions of the GitHub actions used.
- Open: CCSP Lab 10 does not yet read costs from the Moto emulator; CCSP Labs 3, 6 and 7 still
share code with Part I.
- Re-check the Moto cloud-state path (/moto-api/data.json) on the version you install.
