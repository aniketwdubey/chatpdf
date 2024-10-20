from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
import os

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def initialize_embeddings():
    return HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def initialize_llm():
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    return HuggingFaceEndpoint(
        repo_id=repo_id,
        max_length=128,
        temperature=0.7,
        token=HUGGINGFACEHUB_API_TOKEN
    )

def process_pdf(file_path):
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_documents(documents)
        return final_documents
    except Exception as e:
        raise RuntimeError(f"Failed to process PDF: {str(e)}")

def create_vectorstore(documents, embeddings):
    try:
        return FAISS.from_documents(documents, embeddings)
    except Exception as e:
        raise RuntimeError(f"Failed to create vectorstore: {str(e)}")

def setup_retriever(vectorstore):
    try:
        return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    except Exception as e:
        raise RuntimeError(f"Failed to set up retriever: {str(e)}")

def setup_qa_chain(llm, retriever):
    prompt_template = """
    Use the following piece of context to answer the question asked.
    Please try to provide the answer only based on the context.

    {context}
    Question: {question}

    Helpful Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

def get_answer(qa_chain, question):
    result = qa_chain.invoke({"query": question})
    return result['result']