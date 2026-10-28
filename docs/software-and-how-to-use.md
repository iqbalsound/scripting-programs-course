# Software & tools reference and how to use the manual

Front matter of the lab manual (PDF pages 8–11).


## Software & Tools Reference (Free / Open-Source Stack)

The table below lists every tool, platform, and library used across both courses in this manual,
together with its License type and the labs that depend on it. Wherever the original course outline
referenced a paid or closed-source service (for example AWS Lambda, Azure Functions or Docker
Hub private repositories), an equivalent free and open-source substitute is used so that every
exercise can be completed at zero cost, on a student's own machine.

| Category | Tool / Platform | License / Cost | Used In |
| --- | --- | --- | --- |
| Language runtime | Python 3.12 or newer (3.13 and 3.14 also work) | PSF License - free, open source | Labs 1–3, 6, 9–16 |
| Language runtime | Node.js current LTS (22 or 24) | MIT - free, open source (OpenJS Foundation) | Labs 7–16 |
| Editor | Visual Studio Code (or VSCodium, fully OSS) | Free to use / MIT (VSCodium) | All labs |
| Shell | GNU Bash 5.x (native Linux/macOS; WSL2 with systemd on Windows) | GPL - free, open source | Labs 4–5, 13–16 |
| Scheduler | cron | Bundled with Linux — free, open source | Labs 5, 10 |
| Web scraping | requests + BeautifulSoup4 | Apache-2.0 / MIT - free, open source | Lab 6 |
| Version control | Git + GitHub (free tier) or Gitea (fully OSS, self-hosted) | GPL (Git) - free | Labs 1, 3, 7, 11, 15–16 |
| Containers | Docker Engine CE (or Podman, fully OSS), installed once in Lab 1 | Apache-2.0 - free, open source | Labs 8 (optional), 10, 13–16 |
| Serverless / FaaS | Local test harness (required); OpenFaaS + faasd CE (optional) | Harness: course material. faasd CE: non- commercial, personal use under the faasd CE EULA (confirm for classroom use) | Lab 8 |
| Database | SQLite and the sqlite3 command- line client | Public domain - free | Labs 9–10 |
| Mail testing | Mailpit (or Python aiosmtpd) | MIT / Apache-2.0 - free, open source | Labs 10, 16 |
| Debugger | VS Code built-in debugger and Python pdb | Free (bundled) | Lab 11 |
| Logging | Python logging, Winston (Node.js), lnav | Stdlib / MIT / BSD - free, open source | Lab 12 |
| Container registry | Docker Registry (registry:2) | Apache-2.0 - free, open source | Labs 8 (optional), 14–16 |
| Object storage emulator | Moto (S3 emulator) with boto3 and the AWS CLI | Apache-2.0 - free, open source | Labs 5, 9, 14, 16 (CCSP-5213) |
| CI/CD | GitHub Actions (free tier) and Jenkins (lts-jdk21) | GitHub free tier / MIT (Jenkins) | Labs 15–16 |
| Security scanning | Trivy | Apache-2.0 - free, open source | Lab 15 |
| Diagramming | Excalidraw or draw.io (free tier) | MIT (Excalidraw) - free | Lab 16 (capstone) |

Version numbers are minimums, not claims about the newest release. Students should run the
official installer or package-manager command for their OS, which resolves to a current supported
version. Tool and License statements for faasd, Jenkins and MinIO were re-checked for the Fall 2026
revision and should be re-checked just before term because they can change again.

## How to Use This Manual

This manual is organized into two parts, one per course, each containing 16 sequential labs mapped
to the corresponding weekly theory schedule:
- 
Part I: DFSP-5208 (Scripting Programs): Labs 1–16, forensic/cyber-security automation focus.
- 
Part II: CCSP-5213 (Scripting Program and Cloud Architecture): Labs 1–16, cloud
application/DevOps automation focus.
Every lab follows the same six-section structure so students always know where to look:
- 
Title - the lab name and lecture week.
- 
Objectives - what the student will be able to do after completing the lab.
- 
Preamble / Short Theory - the concept(s) underpinning the lab, in plain language.
- 
Prerequisites - exactly what must already be installed or completed before starting.
- 
Step-by-Step Guide - numbered, copy-paste-able commands and code with explanations.
- 
Required Outcomes / Tasks - the specific deliverables the student must submit.
Each lab begins on a new page for easy printing and photocopying. All headings are bookmarked so
they can be navigated directly from Word's Navigation Pane (View ▸ Navigation Pane) or linked to from
other documents/LMS pages.

## Windows students: use WSL2 with systemd

The commands in this manual are Linux commands (source, ~, $(pwd), sudo apt, cron). Windows 11
students must therefore work inside WSL2 with systemd enabled, which cron and faasd need. Open
PowerShell as administrator and run the first command below, then inside Ubuntu add the two lines
to /etc/wsl.conf and restart WSL from PowerShell.

```powershell
wsl --install -d Ubuntu
# inside Ubuntu: sudo nano /etc/wsl.conf and add
#   [boot]
#   systemd=true
# then, in PowerShell:
wsl --shutdown
```

The few commands that differ outside WSL are noted in the labs: activating the virtual environment
(.venv\Scripts\Activate.ps1 in PowerShell) and Docker bind mounts (-v "${PWD}/out:/app/out" in
PowerShell, without --user).

## Evidence rules that apply to every lab

- 
Every screenshot must show the system clock, and every lab asks for one personal value (for
example your roll number), so submissions can be told apart.
- 
Timestamps are written in UTC, and sample data is generated with a fixed random seed (42) so
that results can be checked.
- 
Required work is graded on the local tools; steps marked optional (for example faasd in Lab 8) are
extensions.

## Lab-to-lecture-week mapping

Week 9 is the midterm and has no lab, so Labs 9–16 are taught one lecture week later than their
numbers suggest. Lab 14 shares Week 14 (second half) or Week 15 with the CI/CD lab.

| Manual lab | Lecture week | Topic |
| --- | --- | --- |
| Lab 1–8 | Weeks 1–8 | Python, Bash, cron, scraping, Node.js, serverless |
| (none) | Week 9 | Midterm, no lab |
| Lab 9 | Week 10 | REST/JSON and evidence handling |
| Lab 10 | Week 11 | Workflow automation and alerts |
| Lab 11 | Week 12 | Errors and debugging |
| Lab 12 | Week 13 | Logging and monitoring |
| Lab 13 | Week 14 | Docker |
| Lab 14 | Week 14 (second half) or 15 | Registry and object storage |
| Lab 15 | Week 15 | CI/CD and security scanning |
| Lab 16 | Week 16 | Capstone |
