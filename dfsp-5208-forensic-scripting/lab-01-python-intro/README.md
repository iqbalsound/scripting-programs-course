# Lab 1: Introduction to Python Scripting: Writing and Executing Basic Scripts

**Course:** DFSP-5208  |  **Lecture week:** 1  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Install and verify a modern Python 3 toolchain using only free, open-source components.
- Understand how scripting differs from compiled programming and why it matters for forensic automation.
- Write, save, and execute a first Python script from the command line and from VS Code.
- Use a virtual environment to keep project dependencies isolated and reproducible.

## Short theory

Scripting languages such as Python are interpreted, high-level languages optimized for quickly automating repetitive tasks rather than building large compiled systems. In a digital forensics lab that must process seized evidence logs, monitor chain-of-custody events, and automate repetitive investigative tasks, analysts rarely have time to write and compile a full application every time a repetitive task appears, instead they write a short script, run it immediately, and iterate. This lab establishes the tool-chain (Python 3, a code editor, and a virtual environment) that will be reused throughout the semester, and introduces the read-write-execute cycle that underlies every later lab.

## Prerequisites

- A laptop/desktop running Ubuntu or Kubuntu 24.04 LTS or newer, macOS, or Windows 11 with WSL2 (all free to use; Ubuntu is fully open source). Windows students complete every lab inside WSL2 with systemd enabled (see How to Use This Manual).
- Administrative rights to install software.
- Internet access for the initial download only (all tools work offline afterwards).
- No prior programming experience required.

## Step-by-step solution


### Step 1: Install Python 3.12 or newer (PSF open-source license)

Download the installer from the official Python website (python.org/downloads) or, on Ubuntu, install directly from the repositories. Ubuntu 24.04 provides Python 3.12, which is sufficient for every lab; Python 3.13 or 3.14 is equally fine if your lab PC already has it. Windows/macOS users must tick “Add Python to PATH” during installation.

```bash
# Ubuntu / Kubuntu / WSL2
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version   # confirm 3.12 or newer
```


### Step 2: Install Visual Studio Code (free) or VSCodium (fully open source)

VS Code is free to use; students who prefer a build with no telemetry and a fully open-source license should install VSCodium instead, both use the same editor engine and Python extension. Windows students install VS Code on Windows and add the WSL extension so the editor opens folders inside WSL2.

```bash
# Ubuntu (VS Code via snap) — or install the .deb from code.visualstudio.com
sudo snap install code --classic
# Fully open-source alternative:
# sudo snap install codium --classic
```


### Step 3: Create a project folder and virtual environment

A virtual environment keeps this course's Python packages separate from the rest of the system.

```bash
mkdir -p ~/forensic-scripting/lab01 && cd ~/forensic-scripting/lab01
python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell (outside WSL): .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```


### Step 4: Write the first script

In VS Code, create a file named hello_forensic.py with the following content. It prints the environment, a UTC timestamp and the SHA-256 hash of the script itself, which introduces the integrity idea used all semester.

```python
import hashlib, pathlib, platform, datetime

ROLL = "YOUR-ROLL-NUMBER"   # replace with your own roll number
print("Scripting environment ready.")
print("Student:", ROLL)
print(f"Python {platform.python_version()} running on {platform.system()}")
print("Course: DFSP-5208 - Scripting Programs")
print("UTC:", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
print("SHA256 of this script:", hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
```

> 📁 Saved as [`code/hello_forensic.py`](code/hello_forensic.py)


### Step 5: Execute the script from the terminal

Run the script and observe the interpreted, line-by-line execution.

```bash
python hello_forensic.py
```


### Step 6: Run the same script inside VS Code

Open the folder in VS Code (code .), install the Python extension when prompted, select the .venv interpreter (bottom-right status bar), then use Run ▸ Run Without Debugging.

### Step 7: Install Git and Docker once (used from Lab 3 and Lab 8 onward)

Install both tools now so later labs do not have to repeat the set-up. Docker is installed from the Ubuntu repositories, so no unreviewed script is piped into a root shell. Log out and back in (or run newgrp docker) after adding yourself to the docker group.

```bash
sudo apt install -y git docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER && newgrp docker
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git --version && docker --version
docker run --rm hello-world
```

Podman (sudo apt install podman) is a fully open-source, daemon-less alternative; Docker's own apt repository (docs.docker.com) can be used instead of docker.io if your instructor prefers the upstream package.

### Step 8: Exclude the virtual environment from Git

Create a .gitignore file so that the virtual environment, caches, secrets and evidence files are never committed, then make the first commit.

```text
.venv/
__pycache__/
.env
*.log
evidence/
```


```bash
git init
git add .gitignore hello_forensic.py
git commit -m "Lab 1: first script and .gitignore"
git status    # .venv must not be listed
```


## Required outcomes / tasks

- [ ] Screenshot of `python3 --version` showing 3.12 or newer, with the system clock visible.
- [ ] Submit hello_forensic.py (with your own roll number filled in) together with a terminal screenshot of its output, system clock visible.
- [ ] One-paragraph written reflection: how does an interpreted script differ from a compiled C/Java program?
- [ ] Screenshot of `git status` showing that the virtual environment (.venv) folder is excluded by .gitignore (used from Lab 3 onward).
- [ ] Screenshot of `docker run --rm hello-world` succeeding (or a note from your instructor that Docker is not available on your lab PC).

## Code files in this lab

- [`code/hello_forensic.py`](code/hello_forensic.py)
