import os
import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

VECTOR_SEARCH_INDEX = os.getenv("VECTOR_SEARCH_INDEX", "workspace_7474652187298449.default.resume_index")
LLM_ENDPOINT = os.getenv("SERVING_ENDPOINT", "databricks-meta-llama-3-3-70b-instruct")
TOP_K = 3

st.set_page_config(page_title="Resume RAG Chat", page_icon="💬", layout="wide")
st.title("Resume RAG Chat")
st.caption("Ask grounded questions about Sai Krishna's resume using Databricks Vector Search and Foundation Model APIs.")


def get_workspace_client():
    return WorkspaceClient()


@st.cache_data(show_spinner=False)
def retrieve_chunks(query_text: str, top_k: int = TOP_K):
    workspace_client = get_workspace_client()
    response = workspace_client.vector_search_indexes.query_index(
        index_name=VECTOR_SEARCH_INDEX,
        columns=["chunk_id", "chunk_text", "document_type", "page_numbers"],
        query_text=query_text,
        num_results=top_k,
    )

    manifest = response.manifest
    result = response.result
    columns = getattr(manifest, "columns", None)
    rows = getattr(result, "data_array", None)

    if not columns or not rows:
        return []

    column_names = [column.name for column in columns]
    return [dict(zip(column_names, row)) for row in rows]



def build_context(chunks: list[dict]) -> str:
    context_blocks = []
    for chunk in chunks:
        context_blocks.append(
            f"Chunk ID: {chunk.get('chunk_id')}\n"
            f"Page Numbers: {chunk.get('page_numbers')}\n"
            f"Content:\n{chunk.get('chunk_text', '')}"
        )
    return "\n\n".join(context_blocks)



def answer_question(query_text: str, chunks: list[dict]) -> str:
    workspace_client = get_workspace_client()
    retrieved_context = build_context(chunks)

    system_prompt = (
        "You are a helpful assistant answering questions about a candidate's resume. "
        "Use only the retrieved context provided to you. "
        "If the answer is not supported by the context, say that the context does not provide enough information. "
        "Answer in 4-6 concise bullet points."
    )
    user_prompt = f"Question:\n{query_text}\n\nRetrieved context:\n{retrieved_context}"

    response = workspace_client.serving_endpoints.query(
        name=LLM_ENDPOINT,
        messages=[
            ChatMessage(role=ChatMessageRole.SYSTEM, content=system_prompt),
            ChatMessage(role=ChatMessageRole.USER, content=user_prompt),
        ],
        max_tokens=500,
        temperature=0.1,
    )

    return response.choices[0].message.content


if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.subheader("Configuration")
    st.write(f"Index: `{VECTOR_SEARCH_INDEX}`")
    st.write(f"Model: `{LLM_ENDPOINT}`")
    show_sources = st.checkbox("Show retrieved sources", value=True)
    top_k = st.slider("Top K chunks", min_value=1, max_value=5, value=TOP_K)

prompt = st.chat_input("Ask a question about the resume")

if prompt:
    with st.spinner("Retrieving context and generating answer..."):
        chunks = retrieve_chunks(prompt, top_k=top_k)
        if not chunks:
            answer = "I could not retrieve any relevant resume chunks for that question."
        else:
            answer = answer_question(prompt, chunks)

    st.session_state.history.append(
        {
            "question": prompt,
            "answer": answer,
            "chunks": chunks,
        }
    )

for item in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(item["question"])
    with st.chat_message("assistant"):
        st.write(item["answer"])
        if show_sources and item["chunks"]:
            with st.expander("Retrieved sources"):
                for idx, chunk in enumerate(item["chunks"], start=1):
                    st.markdown(
                        f"**Chunk {idx}**  \\n"
                        f"chunk_id: `{chunk.get('chunk_id')}`  \\n"
                        f"page_numbers: `{chunk.get('page_numbers')}`"
                    )
                    if "score" in chunk:
                        st.write(f"score: {chunk.get('score')}")
                    st.code(chunk.get("chunk_text", "")[:1500])
