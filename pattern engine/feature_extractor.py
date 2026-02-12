import pandas as pd
from datetime import datetime

def extract_features(logs):
    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values("timestamp")

    total_events = len(df)

    error_events = df[df["event"] == "error"]
    edit_events = df[df["event"] == "edit"]
    run_events = df[df["event"] == "run"]

    # Error repeat rate
    error_repeat_rate = len(error_events) / max(1, total_events)

    # Avg time between edits (hesitation)
    edit_times = edit_events["timestamp"].diff().dt.total_seconds()
    avg_edit_interval = edit_times.mean() if not edit_times.empty else 0

    # Edit burstiness (rapid edits)
    edit_burstiness = (edit_times < 3).sum() if not edit_times.empty else 0

    # Run / Edit ratio
    run_edit_ratio = len(run_events) / max(1, len(edit_events))

    return {
        "error_repeat_rate": round(error_repeat_rate, 3),
        "avg_edit_interval": round(avg_edit_interval, 2),
        "edit_burstiness": int(edit_burstiness),
        "run_edit_ratio": round(run_edit_ratio, 2),
        "total_events": total_events
    }
