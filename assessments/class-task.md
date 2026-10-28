# One-Hour Class Task (Mid-Semester Practical), 10 marks

[⬅ Assessments index](README.md)

| Item | Detail |
| --- | --- |
| Coverage | Weeks 1-8 |
| Marks and CLOs | CLO 1 = 3, CLO 2 = 4, CLO 3 = 3 (as in both marks tables) |
| Format | Timed, individual, in the lab, no internet except documentation, no chat assistants |

Each student receives a broken script (Forensic: log parser or hash checker; Cloud: CSV/resource processor) with no error handling, `print` statements only and **one logical bug** . Create a different bug per student group, for example off-by-one in a date range, wrong comparison operator, or a counter reset inside a loop.

1. Identify and fix the logical bug; write one sentence explaining the root cause.
1. Add at least one `try/except` around a genuinely fragile operation (file or network I/O).
1. Replace `print()` calls with at least one `logging` call at a suitable level.
1. Commit to Git with a meaningful message.
1. Submit the corrected script and a screenshot of a successful run showing the system clock.

| Rubric (as approved) | Marks | CLO |
| --- | --- | --- |
| Correct identification and repair of the logical bug | 4 | 2 |
| Appropriate, specific exception handling added | 3 | 3 |
| Correct use of scripting fundamentals throughout | 3 | 1 |

> Instructor note on CLO mapping Finding a logical bug is an "Analyze" skill (CLO 3), and the approved table gives CLO 2 the largest share (4 marks). I kept the approved split so totals stay valid. To make the CLO 2 marks defensible, require the repair to include redesign for reuse: moving the fix into a function with parameters and no hard-coded paths or credentials. Please align the wording at the next outline revision. Primers for exceptions, logging, Bash exit codes and Git are now taught before the test (Weeks 2, 3, 5, 7).
