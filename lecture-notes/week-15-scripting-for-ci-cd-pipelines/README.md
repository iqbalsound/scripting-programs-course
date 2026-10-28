# Week 15: Scripting for CI/CD Pipelines

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 2 (Create) | Erl, Cloud Computing: Concepts, Technology & Architecture, Ch. 8-9; GitHub Actions documentation; Trivy documentation | Test, build and scan pipeline |

> Revised for Fall 2026 aquasecurity/trivy-action@master is unpinned and the original step never fails the build. In a security course, pin third-party actions to a released tag or a full commit SHA and make the scan enforce a policy. Add permissions: contents: read (least privilege). Check the current major versions of actions/checkout and actions/setup-python and update the examples if newer ones exist. Cloud track: an optional integration job runs a Moto emulator as a service container. Git/CLO 3: protect main; merge only through a reviewed pull request.


### Learning objectives

- Distinguish continuous integration from continuous deployment.
- Write a GitHub Actions workflow using the free tier.
- Assemble test, build and vulnerability-scan stages and enforce a pass/fail policy.


### Hour 1: CI/CD concepts

- CI builds and tests every change automatically; CD ships changes that pass all checks.
- For security tooling, CI/CD gives repeatability and an auditable, timestamped record of what was tested and shipped.
- This week assembles everything: scripts (Weeks 1-11), hardening (12-13), image (14).


### Hour 2: GitHub Actions

- Workflows live in `.github/workflows/*.yml`: name, triggers (`on`), jobs, steps; each job runs on a fresh runner.
- YAML is indentation-sensitive; learn to read the Actions log.
- Free for public repositories and with a monthly quota for private ones (check current limits).
- Treat third-party actions as dependencies: pin and review.


### Hour 3: Test, build, scan

- Stage 1: install dependencies, `py_compile` smoke test and any unit tests.
- Stage 2: `docker build` with the commit SHA as tag.
- Stage 3: Trivy scans the image for known vulnerabilities and fails on HIGH/CRITICAL (ignore unfixed ones to keep the signal useful).
- Test must come before build: do not spend time building an image from code that does not even compile.

```yaml
name: CI
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python -m py_compile workflow.py
      - run: python -m unittest discover -s tests
  build-and-scan:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t forensic-tool:${{ github.sha }} .
      - uses: aquasecurity/trivy-action@<PINNED_TAG_OR_COMMIT_SHA>
        with:
          image-ref: forensic-tool:${{ github.sha }}
          format: table
          severity: CRITICAL,HIGH
          ignore-unfixed: true
          exit-code: "1"
```

> 📁 Saved as [`code/example_01.yml`](code/example_01.yml)

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Optional integration job: add services: moto: { image: motoserver/moto:latest, ports: ["5000:5000"] } and run your Week 10 script against http://localhost:5000. Pin the image tag in real projects.


### Step-by-step lab method (free and open-source tools only)

**Tools:** Free GitHub account, GitHub Actions, Docker (Week 14), Trivy via its official GitHub Action.

1. Create a GitHub repository and push the Week 14 project (script, Dockerfile, requirements, tests).
1. Add `.github/workflows/ci.yml` as above; pin the Trivy action to a released tag you looked up today.
1. Add a minimal unit test for `evaluate()` (normal, missing field, wrong type).
1. Push and watch the Actions tab; read each step's log.
1. If the pipeline is red, read the failing step and fix it.
1. Turn on branch protection for `main` (require a pull request and a passing check).
1. Make one change through a pull request and note the new commit SHA and image tag.
1. Write a README that documents each stage and which CLO it demonstrates.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Paste the exact YAML of your committed `ci.yml`.
1. Report the status (success/failure) of every step in your first run.
1. If any step failed, paste the exact log line that revealed the failure and the fix you made.
1. Report the exact image tag produced for your most recent successful run, with the SHA substituted.
1. Paste the Trivy summary output including the number of vulnerabilities found (even zero) and the severity filter you used.
1. Make a small change, push through a PR, and report the new commit SHA and the new image tag generated automatically.
1. Referring to your own step order, explain why the build comes after the test.
1. Quote the sentence from your README that says which CLO the Trivy stage demonstrates, and justify the mapping in one more sentence.
1. Show a pull request where the check failed, and the follow-up commit that made it pass.

## Code files in this week

- [`code/example_01.yml`](code/example_01.yml)
