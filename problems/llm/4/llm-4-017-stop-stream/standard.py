def stop_stream(prompt, stream, eos, limit):
    result = list(prompt)
    if result[-1] == eos:
        return result
    for index in range(min(limit, len(stream))):
        token = stream[index]
        result.append(token)
        if token == eos:
            break
    return result
