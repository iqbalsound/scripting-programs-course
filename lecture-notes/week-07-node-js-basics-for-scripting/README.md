# Week 7: Node.js Basics for Scripting

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Casciaro, Node.js Design Patterns, Ch. 1-2 | File-renaming automation |

> Revised for Fall 2026 Use the current Node.js LTS. Teach fs/promises with async/await first; callbacks are covered as legacy (they come back in Week 12 as error-first callbacks). Git thread: students create a feature branch for the lab and merge it with a pull request.


### Learning objectives

- Run Node scripts, use modules and `npm`.
- Use `fs/promises` and `path` to rename and organise files.
- Understand callbacks, promises and `async/await`.


### Hour 1: JavaScript and Node fundamentals

- `const`/`let`, arrow functions, template strings, destructuring, `require` vs `import`.
- `process.argv` for arguments; `npm init -y`; `package.json`.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Case study: rename evidence files to CASE-0001_YYYYMMDD_hash8.ext so they sort and cannot collide.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Case study: normalise object names before upload to storage.


### Hour 2: Asynchronous programming

- Why Node is non-blocking; the event loop in one diagram.
- Callbacks, promises (`.then`), `async/await` with `try/catch`.
- Pitfall: `forEach` with `await` does not wait; use `for...of` or `Promise.all`.

```javascript
const fs = require("fs/promises");
const path = require("path");
async function main(dir) {
  const names = await fs.readdir(dir);
  for (const [i, name] of names.entries()) {
    const ext = path.extname(name);
    const next = `file_${String(i + 1).padStart(4, "0")}${ext}`;
    console.log(`DRY RUN ${name} -> ${next}`);
  }
}
main(process.argv[2]).catch(e => { console.error(e.message); process.exit(1); });
```

> 📁 Saved as [`code/example_01.js`](code/example_01.js)


### Hour 3: Lab

- Add a `--apply` flag: dry run by default, rename only with the flag.
- Never overwrite: check that the target does not exist.
- Work on a branch, open a pull request, have a classmate review.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalized, see the Appendix on personalisation.

1. Paste the dry-run output on your own test folder, then the folder listing after `--apply`.
1. Show how your script prevents overwriting a file and the message it prints when it refuses.
1. Show the pull-request URL for your lab and one review comment from a classmate.
1. Explain, using one line of your script, why `await` is needed there. What printed if you removed it?
1. Compare your Node.js renamer with how you would write it in Python. State one difference you actually observed.

## Code files in this week

- [`code/example_01.js`](code/example_01.js)
