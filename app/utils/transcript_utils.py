def deduplicate_segments(segments, min_gap_sec=0.2):
    """
    Remove overlapping / duplicate segments based on timestamps.
    """
    cleaned = []
    last_end = -1.0

    for seg in segments:
        if seg["start"] >= last_end - min_gap_sec:
            cleaned.append(seg)
            last_end = seg["end"]

    return cleaned
