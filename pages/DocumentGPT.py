import io
import streamlit as st
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

st.title("Document GPT")
st.set_page_config(page_title="Document GPT", page_icon="📄")


def embed_fiile(file):
    file_io = io.BytesIO(file.read())
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embeddings, cache_dir, key_encoder="sha256"
    )
    loader = UnstructuredFileIOLoader(file_io)
    docs = loader.load_and_split(text_splitter=splitter)
    vectorstore = Chroma.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()

    return retriever


chat = ChatOpenAI(
    temperature=0.1,
    # streaming=True,
    # callbacks=[StreamingStdOutCallbackHandler()]
)
splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=600, chunk_overlap=100, separator="\n"
)
embeddings = OpenAIEmbeddings()

st.markdown("""
Use this chatbot to ask question to AI about your documents.
""")

file = st.file_uploader(".txt, .pdx, .docx", type=["txt", "pdf", "docx"])

if file:
    retriever = embed_fiile(file)
    st.write(retriever.invoke("ministry of truth"))
