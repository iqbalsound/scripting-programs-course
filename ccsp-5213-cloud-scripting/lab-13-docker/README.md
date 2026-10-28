# Lab 13: Introduction to Docker: Containerizing Applications

**Course:** CCSP-5213  |  **Lecture week:** 14  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Install Docker Engine Community Edition (Apache-2.0, free and open source).
- Write a Dockerfile that packages a cloud automation Python script and its dependencies.
- Build and run the container, confirming identical output to the host run.

## Short theory

Containerization is foundational to cloud-native deployment: the same image runs identically on a laptop, in CI, and in production. Docker Engine CE is free and fully open source (Apache-2.0). This course standardizes on Docker Engine CE on Linux/WSL2 rather than Docker Desktop, avoiding Desktop's commercial-use licensing restrictions; Podman is offered as a fully open-source, daemon-less alternative for students who prefer it.
One rule prevents the most common failure in this lab: a bind mount (-v) replaces whatever the image has at that path with the host folder. Keep the code in /app and mount only a separate output folder (/app/out). The container also runs as a non-root user, which limits the damage if the program is ever compromised.

## Prerequisites

- Lab 1, Step 7 completed (Docker installed and `docker run --rm hello-world` works).
- A working corrected script from Lab 3 (and sample_data.csv from Lab 2).

## Step-by-step solution


### Step 1: Confirm Docker Engine CE


```bash
docker --version
docker run --rm hello-world
# Fully open-source daemon-less alternative: sudo apt install podman
```


### Step 2: Prepare the application


```bash
mkdir -p ~/cloud-scripting/lab13 && cd ~/cloud-scripting/lab13
cp ../lab03/log_filter_cli.py .
cp ../lab02/sample_data.csv .
```


### Step 3: Write the Dockerfile and .dockerignore

The image is small, creates a non-root user, and keeps the output folder separate from the code. No requirements.txt is needed because the script uses only the standard library. Use python:3.13-slim if that is what your lab PC provides; the version is not important for the exercise.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY log_filter_cli.py sample_data.csv ./
RUN useradd --create-home appuser && mkdir -p /app/out && chown appuser /app/out
USER appuser
ENTRYPOINT ["python", "log_filter_cli.py"]
CMD ["--input", "sample_data.csv", "--output", "/app/out/output.csv", "--level", "WARN"]
```

> 📁 Saved as [`code/Dockerfile`](code/Dockerfile)

Add a .dockerignore file so that the virtual environment, Git data, secrets, logs and earlier output never enter the image:

```text
.venv/
.git/
__pycache__/
.env
*.log
out/
```

> 📁 Saved as [`code/requirements.txt`](code/requirements.txt)


### Step 4: Build the image


```bash
docker build -t cloud-log-filter:1.0 .
```


### Step 5: Run the container and retrieve the output

Mount only the out sub-folder. Mounting a host folder over /app would hide log_filter_cli.py and the run would fail with “can't open file”.

```bash
docker build -t cloud-log-filter:1.0 .
mkdir -p out
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/out:/app/out" cloud-log-filter:1.0
cat out/output.csv | head
# PowerShell: -v "${PWD}/out:/app/out" (and omit --user)
docker images cloud-log-filter
docker history cloud-log-filter:1.0
```

Expected: the console prints N rows with level=WARN written to /app/out/output.csv (0 skipped), and out/output.csv appears on the host. Compare it with a host run; the two hashes must match:

```bash
python log_filter_cli.py --input sample_data.csv --output host_output.csv --level WARN
sha256sum out/output.csv host_output.csv
```


### Step 6: Inspect the image


```bash
docker images cloud-log-filter
docker history cloud-log-filter:1.0
```


### Step 7: Prove the build cache, .dockerignore and --env-file

Build twice without changing anything: every layer is reused (shown as CACHED). Then change only log_filter_cli.py and rebuild: layers before the COPY line stay cached, which is why files that change often are copied late. Finally pass a setting with --env-file.

```bash
docker build -t cloud-log-filter:1.0 .        # run it a second time: layers show CACHED
printf 'LEVEL=WARN\n' > .env
docker run --rm --env-file .env --entrypoint sh cloud-log-filter:1.0 -c 'echo "LEVEL is $LEVEL"'
```

To prove that .dockerignore works, create a file named secret.env, rebuild, and confirm that `docker` `run --rm --entrypoint ls cloud-log-filter:1.0 /app` does not list it (add secret.env to .dockerignore first).

## Required outcomes / tasks

- [ ] Dockerfile and .dockerignore submitted along with `docker images` output showing the built image (system clock visible).
- [ ] out/output.csv produced by the containerized run, with `sha256sum` showing that it matches the host-run output from Lab 3.
- [ ] Screenshot of the second build showing CACHED layers, and of the --env-file demonstration.
- [ ] One paragraph: what would need to change in the Dockerfile to add a healthcheck for this container, and does a run-once batch job need one?

## Code files in this lab

- [`code/Dockerfile`](code/Dockerfile)
- [`code/requirements.txt`](code/requirements.txt)
