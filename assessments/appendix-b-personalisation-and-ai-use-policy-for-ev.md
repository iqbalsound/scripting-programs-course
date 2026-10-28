# Appendix B: Personalisation and AI-Use Policy for Evidence-Based Questions

[⬅ Assessments index](README.md)

The original scenario questions could be answered by pasting them into a chatbot. The Fall 2026 questions need artefacts from the student's own machine. Suggested rules to announce in Week 1:

- **Evidence rule:** every answer includes own terminal output, a screenshot with the system clock, a file hash, a log or a repository link.
- **Personal seed:** students derive a parameter from their roll number (threshold = last two digits, `--top` = last digit, rename prefix = roll number). A copied answer will not match the seed.
- **Spot viva:** the instructor asks 2-3 students per lab to explain one line live (2 minutes). Failing the viva voids the evidence.
- **Allowed AI use (suggested):** explaining an error message or a concept is allowed if the student can reproduce and explain the result; submitting generated code or output that the student cannot explain is academic misconduct under the university by-laws. The instructor should decide and state the exact rule.
- **Commit history:** a repository whose full solution arrives in one commit is flagged for a viva.
