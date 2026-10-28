# Week 12: Error Handling, Debugging and Collaboration

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 3 (Analyze) | Lutz, Learning Python, Ch. 10 (or the Python tutorial chapter on Errors and Exceptions); Pro Git, Ch. 1-3 (free online) | pdb, custom exceptions, Git pull-request workflow |

> Revised for Fall 2026 Gap closed: CLO 3 explicitly requires version control and collaborative project management, but the original notes had no Git content. Hour 3 now includes a pull-request workflow for the debugging lab. Node.js section keeps async/await as the primary model; error-first callbacks are taught as legacy.


### Learning objectives

- Distinguish syntax, runtime and logical errors and choose a strategy for each.
- Use `try/except/else/finally` and custom exceptions.
- Debug with `pdb` and VS Code breakpoints and read tracebacks bottom to top.
- Collaborate with branches, pull requests and code review.


### Hour 1: A taxonomy of errors

- **Syntax errors** are caught before the program runs. **Runtime errors** (exceptions) occur during execution: missing file, timeout, missing key. **Logical errors** are the most dangerous: the script finishes but the result is wrong.
- `try` contains the risky code; catch the most specific exception first; `else` runs if nothing failed; `finally` always runs (close files, release locks).
- Custom exceptions make failure modes self-documenting.

```python
class EvidenceIntegrityError(Exception):
    """Raised when a computed hash does not match the recorded hash."""

def verify(path, expected):
    actual = sha256_of(path)
    if actual != expected:
        raise EvidenceIntegrityError(f"{path}: expected {expected[:12]}..., got {actual[:12]}...")
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Domain exception: EvidenceIntegrityError when a hash does not match.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Domain exception: ResourceProvisioningError when the cloud API confirms a resource was not created.


### Hour 2: Debugging beyond print()

- `python3 -m pdb script.py`; `n` next, `s` step into, `c` continue, `b 42` breakpoint, `p var` print, `l` list, `q` quit.
- Reading a traceback: the exception type and message are at the **bottom** ; the innermost frame is just above it.
- Never write `except: pass`. Every I/O, hash and ingestion point needs an explicit, logged failure path.
- Log the full stack with `logging.error(traceback.format_exc())` or `logging.exception(...)`.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) A silent failure in an evidence script can produce an incomplete report that nobody notices.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) A silent failure in a provisioning script can leave infrastructure in an inconsistent or costly state.


### Hour 3: Node.js error handling and team workflow

- Node: `try/catch/finally` with `async/await`; `.catch()` on promises; error-first callbacks in older APIs (`cb(err, data)`).
- **Git collaboration lab:** create a branch `fix/evaluate-bug`, commit the fix, push, open a **pull request** , request a review from a classmate, address one comment, and merge. Write a clear commit message and PR description.
- Agree a team convention: all scripts, regardless of language, log errors in the same structured format (this prepares Week 13).

```javascript
async function run(url) {
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(10000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("Fetch failed:", err.message);
    throw err;
  } finally {
    console.log("fetch attempt finished");
  }
}
```

> 📁 Saved as [`code/example_02.js`](code/example_02.js)


### Step-by-step lab method (free and open-source tools only)

**Tools:** Python `pdb` and `traceback`, VS Code debugger, Node.js, Git and GitHub (all free).

1. Introduce a deliberate bug into your Week 11 `evaluate()` (for example misspell a variable).
1. Launch `python3 -m pdb workflow.py`; use `n`, `c`, `p` to locate the line.
1. Fix the bug on a Git branch.
1. Wrap the relevant I/O in a specific handler: `FileNotFoundError` (Forensic) or `requests.exceptions.RequestException` with `raise_for_status()` (Cloud).
1. Define and raise one custom exception.
1. Reproduce the logic error in a small Node.js script and catch it with `try/catch`.
1. Add `logging.error(traceback.format_exc())`.
1. Re-run end to end and confirm graceful degradation.
1. Set a breakpoint in VS Code and see the same root cause.
1. Open a pull request for the fix and get one peer review.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Reproduce a runtime error in `pdb` and paste the exact session transcript (commands and output).
1. Paste the full traceback produced before your fix and explain which line was actually at fault, reading from bottom to top.
1. Show your custom exception class and one real line where it is raised, with the triggering condition.
1. **Forensic:** rename or delete the evidence file and paste the exact log line from your `FileNotFoundError` handler. **Cloud:** stop the emulator and paste the exact log line from your `RequestException` handler.
1. In Node.js, cause the awaited call to fail (invalid URL) and paste the exact `console.error` output.
1. Paste the `traceback.format_exc()` output captured in your log file for one real exception.
1. Set a breakpoint at the faulty line in VS Code and describe the exact variable values you saw.
1. Find one place where a broad `except: pass` could hide a real failure and show the specific handler you would use instead.
1. Give the URL of your pull request, the review comment you received and the commit that resolved it.

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
- [`code/example_02.js`](code/example_02.js)
