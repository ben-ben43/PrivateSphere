import operator
from typing import TypedDict, Annotated, List
import chromadb
from chromadb.utils import embedding_functions
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(
    name="enterprise_docs", 
    embedding_function=embedding_model
)

llm = ChatOllama(model="llama3.1:8b", temperature=0.1)

class ResearchState(TypedDict):
    question: str
    filename: str
    context: Annotated[List[str], operator.add] 
    answer: str

def retrieve_node(state: ResearchState):
    question = state["question"]
    current_file = state["filename"]
    
    results = collection.query(
        query_texts=[question],
        n_results=3,
        where={"source": current_file}
    )
    
    retrieved_chunks = results["documents"][0]
    return {"context": retrieved_chunks}

def generate_node(state: ResearchState):
    question = state["question"]
    context_text = "\n\n---\n\n".join(state["context"])
    
    prompt = f"""You are a highly capable enterprise AI assistant.
Answer the user's question using ONLY the context provided below. 
If the context does not contain the answer, reply EXACTLY with: "I do not have enough information in the provided documents to answer that."

Context:
{context_text}

Question: {question}
Answer:"""

    response = llm.invoke(prompt)
    return {"answer": response.content}

builder = StateGraph(ResearchState)
builder.add_node("retriever", retrieve_node)
builder.add_node("generator", generate_node)

builder.set_entry_point("retriever")
builder.add_edge("retriever", "generator")
builder.add_edge("generator", END)

agent_app = builder.compile()