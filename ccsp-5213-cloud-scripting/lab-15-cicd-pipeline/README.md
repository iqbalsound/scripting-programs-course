# Lab 15: CI/CD Pipeline Automation

**Course:** CCSP-5213  |  **Lecture week:** 15  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Build a CI/CD pipeline that builds, tests, scans for vulnerabilities and pushes the tool image automatically on every commit.
- Route A: run Jenkins (free, open source, self-hosted) with a Jenkinsfile that polls the repository.
- Route B: write the equivalent GitHub Actions workflow, which is the route used in the lecture notes and in Assignment 3.

## Short theory

CI/CD automates build-test-deploy so every change is validated consistently, and a vulnerability scan (Trivy) fails the build when serious problems are found. Jenkins is free, open source (MIT) and self-hostable with no per-seat costs, a common alternative to SaaS-only CI/CD in cost-sensitive or air-gapped cloud environments; GitHub Actions has a free tier and is what the course notes and Assignment 3 use. Complete Route A (Jenkins) and then Route B, which takes about 15 minutes. Both wire the pipeline to the Git repository and local registry built in Labs 13–14.

## Prerequisites

- Labs 13–14 completed (registry running on localhost:5000).
- Git installed; the lab13 folder will become the repository.
- Docker running (Jenkins runs as a container). Route B needs a free GitHub account.

## Step-by-step solution


### Step 1: Route A: initialise the Git repository

The Jenkinsfile belongs in the lab13 repository, next to the Dockerfile.

```bash
cd ~/cloud-scripting/lab13
git init
git add Dockerfile .dockerignore log_filter_cli.py sample_data.csv
git commit -m 'Initial tool'
```


### Step 2: Write the Jenkinsfile (build, test, scan, push)

The pipeline polls the repository every two minutes, builds the image, runs it as a test, scans it with Trivy and only then pushes. Test comes first so a broken image is never pushed; `--exit-code 1` makes the scan stage fail the build when HIGH or CRITICAL vulnerabilities with a fix are found. Replace <PINNED_VERSION> with the Trivy release your instructor announces (pinning a version avoids surprise changes).

```groovy
pipeline {
  agent any
  triggers { pollSCM('H/2 * * * *') }
  environment {
    IMAGE = "localhost:5000/cloud-log-filter"
    TAG = "${env.BUILD_NUMBER}"
  }
  stages {
    stage('Build') { steps { sh 'docker build -t $IMAGE:$TAG .' } }
    stage('Test') {
      steps { sh 'docker run --rm $IMAGE:$TAG --input sample_data.csv --output /tmp/out.csv --level WARN' }
    }
    stage('Scan') {
      steps {
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:<PINNED_VERSION> image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed $IMAGE:$TAG'
      }
    }
    stage('Push') { steps { sh 'docker push $IMAGE:$TAG' } }
  }
  post {
    success { echo 'Pipeline completed: image built, tested, scanned and pushed.' }
    failure { echo 'Pipeline failed: check the console output.' }
  }
}
```

> 📁 Saved as [`code/Jenkinsfile`](code/Jenkinsfile)


```bash
cd ~/cloud-scripting/lab13
git add Jenkinsfile && git commit -m 'Add Jenkinsfile'
```


### Step 3: Build a Jenkins image that contains the Docker CLI

The official Jenkins image has no Docker CLI, so docker build would fail with “docker: not found”. Build a small image on the lts-jdk21 tag (Jenkins now requires Java 21).

```dockerfile
# Dockerfile.jenkins
FROM jenkins/jenkins:lts-jdk21
USER root
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
USER jenkins
```

> 📁 Saved as [`code/Dockerfile.jenkins`](code/Dockerfile.jenkins)


```bash
docker build -f Dockerfile.jenkins -t jenkins-docker:lts .
```


### Step 4: Run Jenkins

The container needs three things: the Docker socket (with its group), the repository as a read-only folder it can see, and a volume for its own data.

```bash
docker build -f Dockerfile.jenkins -t jenkins-docker:lts .
docker volume create jenkins_home
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --group-add "$(stat -c %g /var/run/docker.sock)" \
  -v "$HOME/cloud-scripting/lab13:/repo:ro" \
  jenkins-docker:lts
docker exec jenkins git config --global --add safe.directory /repo
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```


### Step 5: Complete setup in the browser

Open http://localhost:8080, paste the initial admin password, choose “Install suggested plugins” (all free/OSS), and create an admin user.

### Step 6: Create the pipeline job and run it

New Item ▸ Pipeline ▸ name it cloud-log-filter-pipeline ▸ under Pipeline choose “Pipeline script from SCM” ▸ SCM: Git ▸ Repository URL /repo (or a GitHub/Gitea URL) ▸ Script Path Jenkinsfile. Choose Build Now, then make a small change, commit it, and wait for the poll to start a build by itself.

```bash
# trigger from the Jenkins UI: 'Build Now', then prove the commit trigger:
cd ~/cloud-scripting/lab13
echo '# change' >> log_filter_cli.py && git commit -am 'Trigger build'
curl http://localhost:5000/v2/cloud-log-filter/tags/list     # the new build number appears
```


### Step 7: Route B: the same pipeline in GitHub Actions

Create .github/workflows/ci.yml in your repository, push to GitHub, and open the Actions tab. Permissions are limited to reading the repository, and the Trivy action should be pinned to a released tag or commit that you have checked; replace <PINNED_TAG_OR_SHA> and check the current major versions of actions/checkout and actions/setup-python.

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
      - run: python -m py_compile log_filter_cli.py
      - run: python log_filter_cli.py --input sample_data.csv --output /tmp/out.csv --level WARN
  build-and-scan:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t cloud-log-filter:${{ github.sha }} .
      - uses: aquasecurity/trivy-action@<PINNED_TAG_OR_SHA>
        with:
          image-ref: cloud-log-filter:${{ github.sha }}
          severity: CRITICAL,HIGH
          ignore-unfixed: true
          exit-code: "1"
```

> 📁 Saved as [`code/ci.yml`](code/ci.yml)


### Step 8: Protect the main branch

In the repository settings add a branch protection rule for main: require a pull request and require the CI checks to pass before merging. Then open a pull request that breaks the build on purpose and show that it cannot be merged.

## Required outcomes / tasks

- [ ] Jenkinsfile submitted alongside a screenshot of a green pipeline run showing the Build, Test, Scan and Push stages, with the system clock visible.
- [ ] Console output log from the Test stage showing the containerised script executed correctly.
- [ ] Confirm via `curl http://localhost:5000/v2/cloud-log-filter/tags/list` that the new build tag was pushed.
- [ ] Route B: ci.yml submitted with a screenshot of a green GitHub Actions run, and a screenshot of the branch-protection rule.
- [ ] Short answer: why does Test come before Build/Push, and what does `exit-code: 1` do in the scan stage?

## Code files in this lab

- [`code/Dockerfile.jenkins`](code/Dockerfile.jenkins)
- [`code/Jenkinsfile`](code/Jenkinsfile)
- [`code/ci.yml`](code/ci.yml)
