def stop_stream(prompt, stream, eos, limit):
    result = list(prompt)
    if result[-1] == eos:
        return result
    for token in stream[:limit]:
        result.append(token)
        if ...:
            break
    return result
