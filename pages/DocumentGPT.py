import io
import streamlit as st
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.vectorstores import Chroma
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

st.title("Document GPT")
st.set_page_config(page_title="Document GPT", page_icon="📄")
st.session_state["messages"] = st.session_state.get("messages", [])


class ChatCallbackHandler(BaseCallbackHandler):
    message = ""
    message_box = None

    def on_llm_start(self, *args, **kwargs):
        self.message = ""
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        with st.sidebar:
            st.write("LLM ended")

        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


chat = ChatOpenAI(temperature=0.1, streaming=True, callbacks=[ChatCallbackHandler()])
splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=600, chunk_overlap=100, separator="\n"
)
embeddings = OpenAIEmbeddings()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the question in Korean using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.\nContext: {context}",
        ),
        ("human", "{question}"),
    ]
)


@st.cache_resource(show_spinner="Embedding document...")
def embed_fiile(file):
    file_io = io.BytesIO(file.read())
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embeddings, cache_dir, key_encoder="sha256"
    )

    loader = UnstructuredFileIOLoader(file_io, content_type=file.type)
    docs = loader.load_and_split(text_splitter=splitter)
    vectorstore = Chroma.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()

    return retriever


def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})


def send_message(message, role, is_save=True):
    with st.chat_message(role):
        st.markdown(message)

    if is_save:
        save_message(message, role)


def draw_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], is_save=False)


st.markdown("""
Use this chatbot to ask question to AI about your documents.
""")

with st.sidebar:
    file = st.file_uploader(".txt, .pdx, .docx", type=["txt", "pdf", "docx"])

if file:
    retriever = embed_fiile(file)
    send_message(f"{file.name} ready!", "ai", is_save=False)
    draw_history()
    message = st.chat_input("Ask about your document")

    if message:
        send_message(message, "human")
        chain = (
            {
                "context": retriever
                | RunnableLambda(lambda docs: "\n\n".join(doc.page_content for doc in docs)),
                "question": RunnablePassthrough(),
            }
            | prompt
            | chat
        )

        with st.chat_message("ai"):
            response = chain.invoke(message)
else:
    st.session_state["messages"] = []
