def chunk_text(text, chunk_size=200):  # smaller chunk
    words = text.split()
    
    if len(words) == 0:
        return []

    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks