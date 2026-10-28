class EvidenceIntegrityError(Exception):
    """Raised when a computed hash does not match the recorded hash."""

def verify(path, expected):
    actual = sha256_of(path)
    if actual != expected:
        raise EvidenceIntegrityError(f"{path}: expected {expected[:12]}..., got {actual[:12]}...")
