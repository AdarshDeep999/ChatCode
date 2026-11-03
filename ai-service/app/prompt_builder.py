def build_prompt(question, context):
    prompt = f"""
You are a codebase assistant.

Answer the user's question using only the provided code context.

When referring to code, mention the file path and line range.

If the provided context does not contain enough information to answer,
say that you don't have enough information.

Question:
{question}

Code Context:
{context}
"""

    return prompt