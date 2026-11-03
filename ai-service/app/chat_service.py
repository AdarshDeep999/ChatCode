from .retriever import search_code
from .context_builder import build_context
from .prompt_builder import build_prompt
from .llm import generate_answer


def chat_with_repository(repository_id: str, question: str):

    # 1. Retrieve relevant code chunks
    results = search_code(
        repository_id=repository_id,
        query=question
    )

    # 2. Build context
    context = build_context(results)

    if not context:
        return {
            "repositoryId": repository_id,
            "answer": "I couldn't find relevant code in this repository to answer your question."
        }

    # 3. Build prompt
    prompt = build_prompt(question, context)

    # 4. Generate answer
    answer = generate_answer(prompt)

    return {
        "repositoryId": repository_id,
        "answer": answer
    }