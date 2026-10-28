# Week 16: Best Practices and Final Project Presentations

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 2 and CLO 3 | Consolidated readings; GitHub README guides | Capstone demonstration |

> Revised for Fall 2026 The original notes stopped at Week 15, but both outlines schedule Week 16 (final project presentation, capstone lab). This week is new.


### Hour 1: Best practices checklist

- **Secrets:** no credentials in code, logs, images or commits. `.env` ignored; use `--env-file` at runtime.
- **Reliability:** timeouts on every network call, specific exceptions, no silent `except: pass`, idempotent scheduled jobs.
- **Observability:** structured logs at the right level, rotation, retention policy.
- **Reproducibility:** pinned versions, `requirements.txt`, Dockerfile, CI on every push.
- **Collaboration:** small commits, meaningful messages, pull requests with review, README with run instructions.
- **Ethics and law:** respect terms of service and `robots.txt`, lab data only, no scanning of systems you do not own or have permission to test.


### Hours 2-3: Final project presentations

Each student or team (maximum three) presents a **10-minute demo and 5-minute viva** of the capstone from Assignment 3: a script from earlier weeks, now with logging, error handling, a Dockerfile and a CI workflow.

| Component | What to show | Evidence |
| --- | --- | --- |
| Application | What it does, for which track (forensic or cloud) | Live run, console output |
| Reliability | One handled failure demonstrated live | Log line and traceback |
| Container | Build and run, with a volume mount | docker build and run output |
| Pipeline | A green run and one deliberately failing run | Actions tab, Trivy summary |
| Collaboration | Commit history, a pull request and review | GitHub links |
| Viva (5 min) | Instructor asks about a line of code, a design choice and a failure mode | Spoken answers |

> Marks The approved outlines give the final presentation no separate marks; its assessment value comes through Assignment 3 (4 marks) and the final exam. Use the presentation as the viva check that the submitted Assignment 3 is the student's own work. If you want presentation marks, they must come out of an approved component, so decide that before you announce it.


### Final exam revision plan (Weeks 1-16)

| Block | Revisit | Weeks |
| --- | --- | --- |
| A: Scripting fundamentals (CLO 1) | Python, Bash and Node.js syntax; file parsing; CLI tools | 1-8 |
| B: Design and deployment (CLO 2) | API workflow design, serverless, Dockerfile ordering, CI/CD pipeline | 8, 10, 11, 14, 15 |
| C: Analysis and reliability (CLO 3) | Tracebacks, debugging, custom exceptions, logging levels and rotation, Git workflow | 12, 13, 15 |
