# Lab 7: Node.js Scripting for File System Automation

**Course:** CCSP-5213  |  **Lecture week:** 7  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Install a current Node.js LTS release (22 or 24; free, open source, OpenJS Foundation) and verify npm.
- Use Node's built-in `fs` and `path` modules to automate file renaming safely (dry run first, never overwrite).
- Compare JavaScript/Node.js scripting patterns with the Python equivalents from Lab 2.

## Short theory

Node.js lets JavaScript run outside the browser, and is entirely free and open source. Many cloud-native and forensic tooling ecosystems (including serverless platforms used later in the course) run on Node.js, so this lab introduces its asynchronous file-handling model using the built-in `fs/promises` API, no paid packages required.

## Prerequisites

- Administrative rights to install Node.js (current LTS: 22 or 24).
- Comfort with basic JavaScript syntax (variables, functions) is helpful but not required.
- Git installed and configured (Lab 1, Step 7).

## Step-by-step solution


### Step 1: Install the current Node.js LTS (22 or 24)

Do not pipe a downloaded script straight into a root shell. Use the snap package, or download the NodeSource set-up script, read it, and only then run it.

```bash
# Option A (simplest on Ubuntu/Kubuntu)
sudo snap install node --classic --channel=24

# Option B: download, inspect, then run
curl -fsSLo nodesource_setup.sh https://deb.nodesource.com/setup_24.x
less nodesource_setup.sh          # read it before running it
sudo -E bash nodesource_setup.sh
sudo apt install -y nodejs

node --version   # v22.x or v24.x
npm --version
```


### Step 2: Create the project


```bash
mkdir -p ~/cloud-scripting/lab07 && cd ~/cloud-scripting/lab07
npm init -y
```


### Step 3: Write a batch file-renamer

Create rename_cloud_files.js that adds a standardised timestamp prefix to every file in a folder. It is a dry run unless --apply is given, skips files that already carry a timestamp prefix, never overwrites, and exits with code 1 on an error.

```javascript
// Usage: node rename_cloud_files.js <dir> [--apply]   (dry run by default; never overwrites)
const fs = require('fs/promises');
const path = require('path');

const STAMPED = /^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z_/;

async function renameFiles(dir, apply) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  let count = 0, skipped = 0;
  for (const file of await fs.readdir(dir)) {
    const oldPath = path.join(dir, file);
    if (!(await fs.stat(oldPath)).isFile()) continue;
    if (STAMPED.test(file)) { skipped++; continue; }              // already has a timestamp prefix
    const newPath = path.join(dir, `${stamp}_${file}`);
    try { await fs.access(newPath); console.error(`refusing to overwrite ${newPath}`); continue; } catch {}
    console.log(`${apply ? 'RENAME' : 'DRY RUN'} ${file} -> ${path.basename(newPath)}`);
    if (apply) await fs.rename(oldPath, newPath);
    count++;
  }
  console.log(`${apply ? 'Renamed' : 'Would rename'} ${count} files, skipped ${skipped}, in ${dir}`);
}

const args = process.argv.slice(2);
renameFiles(args.find(a => !a.startsWith('--')) || '.', args.includes('--apply'))
  .catch(err => { console.error('Error:', err.message); process.exit(1); });
```

> 📁 Saved as [`code/rename_cloud_files.js`](code/rename_cloud_files.js)


### Step 4: Test the script


```bash
mkdir sample_files && touch sample_files/a.txt sample_files/b.csv
node rename_cloud_files.js sample_files            # dry run: shows what would change
node rename_cloud_files.js sample_files --apply    # renames the files
node rename_cloud_files.js sample_files --apply    # second run: renames 0, skips 2
ls sample_files
node rename_cloud_files.js nodir; echo "exit code: $?"   # error message and exit code 1
```


### Step 5: Practise the Git branch and pull-request workflow

Commit the working script on the main branch, then make your change on a feature branch. Push the branch to GitHub (free tier) or Gitea and open a pull request; ask a classmate to review and approve it.

```bash
git init
git add rename_cloud_files.js package.json
git commit -m "Lab 7: dry-run renamer"
git switch -c feature/prefix-option
# make your change (see Required Outcomes), then:
git add -A && git commit -m "Add --prefix option"
```


## Required outcomes / tasks

- [ ] rename_cloud_files.js submitted with before/after directory listing screenshots (system clock visible), including the dry run.
- [ ] Extend the script with a `--prefix NAME` option that replaces the timestamp text in the new file name, on a feature branch, and submit the pull-request link or a screenshot of the reviewed pull request.
- [ ] Short comparison table (3 rows) contrasting Python's pathlib/os calls with Node's `fs/promises` equivalents.

## Code files in this lab

- [`code/rename_cloud_files.js`](code/rename_cloud_files.js)
