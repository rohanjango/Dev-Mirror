def detect_debug_loop(logs, window=5):
    """
    Detects repeating pattern:
    error → edit → run → error → edit → run
    """
    recent = logs[-window:]

    events = [e["event"] for e in recent]

    pattern = ["error", "edit", "run", "error", "edit"]

    return events[:len(pattern)] == pattern
