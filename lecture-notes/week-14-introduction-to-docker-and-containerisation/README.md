# Week 14: Introduction to Docker and Containerisation

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 2 (Create) | Poulton, Docker Deep Dive, Ch. 2-5; Docker "Dockerfile best practices" | Build and run a container for the workflow |

> Revised for Fall 2026 .dockerignore excludes .env, but the script needs its key at run time. Pass secrets at run time with --env-file or -e, never bake them into the image. The image now runs as a non-root user and uses a pinned base tag. Windows path syntax added for volume mounts. Lab network tip: pre-pull python:3.12-slim and share it with docker save / docker load so 30 students do not hit Docker Hub limits at once.


### Learning objectives

- Explain images, containers, registries and how containers differ from virtual machines.
- Write a minimal, cache-friendly, least-privilege Dockerfile for a Python script.
- Build, run, mount volumes and (optionally) push an image.


### Hour 1: Why containerise

- "Works on my machine" arises from different Python versions, libraries and OS settings. An image packages the application with its exact dependencies.
- A VM virtualises hardware and runs its own kernel; a container shares the host kernel and isolates processes and file systems, so it starts in about a second.
- Core terms: **image** (read-only template), **container** (running instance), **registry** (Docker Hub, ECR).

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Reproducibility: the same tool produces the same output on every investigator's machine.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Portability: the same image runs in development, staging and production.


### Hour 2: Writing the Dockerfile

- Choose a slim official base (`python:3.12-slim`).
- Copy `requirements.txt` first and install, then copy the code. Docker caches layers, so code changes do not reinstall dependencies.
- `.dockerignore` keeps `venv/`, `.env`, `.git`, evidence and logs out of the image.
- Run as a non-root user. `ENTRYPOINT` makes the script behave like a tool.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home appuser && mkdir -p /app/evidence && chown -R appuser /app
USER appuser
ENTRYPOINT ["python3", "workflow.py"]

# .dockerignore
venv/
.env
.git/
__pycache__/
*.log
evidence/
output/
```

> 📁 Saved as [`code/Dockerfile`](code/Dockerfile)


### Hour 3: Build, run, share

- `docker build -t forensic-workflow .` then `docker run --rm --env-file .env -v "$(pwd)/evidence:/app/evidence" forensic-workflow` (Windows PowerShell: `${PWD}`).
- Without `-v`, the container file system is discarded when it stops, so evidence written inside is lost.
- If the mounted folder is not writable on Linux, add `--user "$(id -u):$(id -g)"`.
- Compare the container output to the Week 11 host run; they should match.
- `docker login`, `docker tag`, `docker push` to a free Docker Hub repository (optional). Never push an image that contains secrets.


### Step-by-step lab method (free and open-source tools only)

**Tools:** Docker Engine (Linux) or Docker Desktop (education/personal use, check current terms); optional free Docker Hub account.

1. Install Docker and verify with `docker run --rm hello-world`.
1. Create `requirements.txt` listing exactly the third-party packages used.
1. Write the Dockerfile and `.dockerignore`.
1. Build: `docker build -t forensic-workflow .` (Cloud: `cloud-workflow`).
1. Run with `--env-file` and the evidence/output volume.
1. Compare the container output with the host output from Week 11.
1. Check size with `docker images`.
1. Run `docker run --rm --entrypoint sh <image> -c "ls -a /app"` and confirm that `.env` is **not** inside.
1. (Optional) log in, tag and push to Docker Hub.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Paste the exact `docker build` output, including the final image ID.
1. Run `docker images` and report the exact size. Build once with `python:3.12` (non-slim) and compare the sizes.
1. Run with the volume mount and paste the output confirming the evidence/output file appeared on the host.
1. Run once **without** `-v`, report what happened to the output file and explain in terms of the container file-system lifecycle.
1. Compare the container run with your Week 11 host run on the same input and report whether they matched exactly.
1. Show your `.dockerignore` and explain, with a real file, what would have gone wrong without it. Paste the output proving `.env` is not in the image.
1. If you did the push: paste the exact `docker push` output with the repository name.
1. Introduce an ordering mistake (copy all files before installing dependencies), change only application code, and report the rebuild time difference versus the correct order.

## Code files in this week

- [`code/Dockerfile`](code/Dockerfile)
