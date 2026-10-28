def always_fails():
    raise OSError("simulated outage")

try:
    with_retry(always_fails, attempts=3, delay=0.1)
except RetryExhausted as exc:
    print("giving up:", exc)
