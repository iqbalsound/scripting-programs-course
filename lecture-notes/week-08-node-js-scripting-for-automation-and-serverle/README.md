# Week 8: Node.js Scripting for Automation and Serverless Deployment

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 2 (Create) | Casciaro, Node.js Design Patterns, Ch. 3-4 | Serverless function (local-first) |

> Revised for Fall 2026 The original lab requires a real AWS Lambda or Azure Functions account. That means card details and a billing risk for students. Use the tiers below and let each student pick the highest tier they can run safely. Free-tier terms of public clouds change often. Verify the current AWS Free Tier / Azure free account terms yourself before offering Tier 4.


### Learning objectives

- Explain serverless (functions as a service), events, cold starts and statelessness.
- Package a Node.js function and invoke it with an event.
- Deploy to a local or emulated serverless runtime.


### Hour 1: Serverless concepts

- Event-driven functions, pay-per-invocation, stateless execution, time and memory limits.
- Trade-offs vs containers and VMs: scaling and cost vs cold start, vendor lock-in and debugging difficulty.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Case study: an on-upload function that hashes a new evidence file and writes the hash to a log.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Case study: an on-upload function that thumbnails an image or validates a JSON object.


### Hour 2: Packaging and deployment

- Handler signature `exports.handler = async (event) => {...}`; returning a response object.
- Dependencies: `npm ci --omit=dev`, zip the folder, keep the package small.
- Secrets: environment variables, never in the zip.

```javascript
exports.handler = async (event) => {
  const text = event.text ?? "";
  const words = text.split(/\s+/).filter(Boolean).length;
  return { statusCode: 200, body: JSON.stringify({ words }) };
};
```

> 📁 Saved as [`code/example_01.js`](code/example_01.js)


### Hour 3: Lab (choose a tier)

- **Tier 1, required for all:** run the handler locally with a tiny harness: `node -e "require('./index').handler({text:'a b c'}).then(console.log)"`.
- **Tier 2:** deploy and invoke the zip on a local AWS emulator (Moto server with Docker available for Lambda execution, or another emulator).
- **Tier 3:** Azure Functions Core Tools (`func start`) running a Node.js HTTP function locally.
- **Tier 4, optional:** deploy to a real AWS or Azure free account if the student already has one and understands the billing alerts. Never required for marks.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Paste the exact output of your Tier 1 harness for three different inputs, including an empty one.
1. State the tier you completed, and paste the invoke command and the JSON response.
1. Add input validation that returns status 400 for non-string input. Paste the code and the response for a bad event.
1. Report the time (ms) of the first and second invocation, and explain any difference in terms of cold starts or process start-up.
1. Name one workload in your own track that is a good fit for serverless and one that is not. Justify both in one sentence each.

> Suggested date for the one-hour class task (mid-semester) The approved plan says "mid-semester, Weeks 1-8" without a date. Run it at the end of the Week 8 lab slot (after the local-first serverless lab, which is shorter than the original cloud-account version). That keeps it before the Week 9 midterm. Every skill it tests (exceptions, logging, Bash exit codes, Git) now has a primer by Week 5.

## Code files in this week

- [`code/example_01.js`](code/example_01.js)
