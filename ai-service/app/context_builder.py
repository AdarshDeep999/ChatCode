def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        return ""

    context_parts = []

    for code, metadata in zip(documents, metadatas):
        source = metadata["source"]
        language = metadata["language"]
        start_line = metadata["start_line"]
        end_line = metadata["end_line"]

        context = f"""
File: {source}
Language: {language}
Lines: {start_line}-{end_line}

{code}
"""
        context_parts.append(context)

    return "\n".join(context_parts)