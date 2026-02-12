def build_profile(features, logs):
    from debug_loop import detect_debug_loop
    from thinking_style import classify_thinking_style

    return {
        "thinking_style": classify_thinking_style(features),
        "debug_loop": detect_debug_loop(logs),
        "confidence_score": round(1 - features["error_repeat_rate"], 2)
    }
