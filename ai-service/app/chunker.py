from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    # Keep the original file content so we can calculate line numbers
    source_to_text = {
        document.metadata["source"]: document.page_content
        for document in documents
    }

    for chunk in chunks:
        source = chunk.metadata["source"]
        original_text = source_to_text[source]

        start_index = chunk.metadata["start_index"]
        end_index = start_index + len(chunk.page_content)

        # Convert character position → line number
        start_line = original_text.count(
            "\n", 0, start_index
        ) + 1

        if end_index > start_index:
            end_line = original_text.count(
                "\n", 0, end_index - 1
            ) + 1
        else:
            end_line = start_line

        chunk.metadata["start_line"] = start_line
        chunk.metadata["end_line"] = end_line

        # We don't need this in Chroma
        chunk.metadata.pop("start_index", None)

    return chunks