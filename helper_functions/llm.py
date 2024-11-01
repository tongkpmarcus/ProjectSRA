import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import tiktoken
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pypdf import PdfReader

__import__('pysqlite3') 
import sys 
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3') 


if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), 
                base_url="https://litellm.govtext.gov.sg/", 
                default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"} 
                )

# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model="gpt-4o-prd-gcc2-lb", temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( #originally was openai.chat.completions
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content


# Note that this function directly take in "messages" as the parameter.
def get_completion_by_messages(messages, model="gpt-4o-prd-gcc2-lb", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content


# This function is for calculating the tokens given the "message"
# ⚠️ This is simplified implementation that is good enough for a rough estimation
def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-prd-gcc2-lb')
    return len(encoding.encode(text))

def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model('gpt-4o-prd-gcc2-lb')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))

# region <--------- RAG config --------->

# Load PDF and extract text from each page
def load_pdf(file_paths):
    documents = []
    for file_path in file_paths:
        reader = PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:  # Check if text extraction was successful
                documents.append({
                    'page_content': text,
                    'metadata': {'source': f"{file_path} - Page {i + 1}"}
                })
    
    return documents


def split_chunk_text(documents):
    # Initialize the CharacterTextSplitter
    r_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=5)

    # Split documents into chunks
    split_chunks = []
    for document in documents:
        chunks = r_splitter.split_text(document['page_content'])
        split_chunks.extend([{'metadata': document['metadata'], 'page_content': chunk} for chunk in chunks])

    # Further split each chunk's `page_content` using RecursiveCharacterTextSplitter
    text_splitter_ = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=50,
        chunk_overlap=10,
    )

    recursive_chunks = []
    for chunk in split_chunks:
        sub_chunks = text_splitter_.split_text(chunk['page_content'])
        recursive_chunks.extend([{'metadata': chunk['metadata'], 'page_content': sub_chunk} for sub_chunk in sub_chunks])

    return recursive_chunks




# Define a reusable embeddings model
embeddings_model = OpenAIEmbeddings(
    model='text-embedding-3-large-prd-gcc2-lb',
    openai_api_base="https://litellm.govtext.gov.sg/"
)

def get_embedding(input, embeddings_model = embeddings_model):
    response = client.embeddings.create(
        input=input,
        model=embeddings_model.model
    )
    return [x.embedding for x in response.data]


from langchain.schema import Document

def embed_vector_store(splitted_documents, embeddings_model=embeddings_model):
    # Convert dictionaries to Document objects
    document_objects = [
        Document(page_content=doc['page_content'], metadata=doc['metadata']) 
        for doc in splitted_documents]

    # Create and persist the vector store
    vector_store = Chroma.from_documents(
        collection_name="SRACollection",
        documents=document_objects,
        embedding=embeddings_model,
        persist_directory="./chroma_langchain_db"
    )

    return vector_store



# Load vector store from disk
def load_vector_store():
    embeddings_model = OpenAIEmbeddings(
        model='text-embedding-3-large-prd-gcc2-lb', 
        openai_api_base="https://litellm.govtext.gov.sg/"
    )
    vector_store = Chroma(
        collection_name="SRACollection",
        embedding_function=embeddings_model,
        persist_directory="./chroma_langchain_db"
    )
    return vector_store

def retrieve_QA(vectordb):
    # Initialize the language model
    llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),  
                  openai_api_base="https://litellm.govtext.gov.sg/", 
                  model='gpt-4o-prd-gcc2-lb',  
                  temperature=0.1,  
                  default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"})
    
    # Create the RetrievalQA chain
    rag_chain = RetrievalQA.from_llm(
        retriever=vectordb.as_retriever(),  # Ensure `vectordb` is initialized and loaded
        llm=llm
    )
    return rag_chain

# Define the llm_answer function to use the RAG chain and take prompt as a parameter
def llm_answer(prompt, qa_chain):
    response = qa_chain.run(prompt)
    return response





