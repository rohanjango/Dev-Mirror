def classify_thinking_style(features):
    if features["edit_burstiness"] > 3:
        return "trial_and_error"

    if features["avg_edit_interval"] > 25:
        return "analytical"

    if features["run_edit_ratio"] < 0.4:
        return "planner"

    if features["error_repeat_rate"] > 0.3:
        return "brute_force"

    return "balanced"
