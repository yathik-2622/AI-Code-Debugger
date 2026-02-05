import os
import time
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class CodeAnalysisEngine:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key: raise ValueError("GROQ_API_KEY missing")

        # Using your specified high-performance model
        self.llm = ChatGroq(
            temperature=0.3, 
            model_name="llama-3.3-70b-versatile", # Strong Logic Model
            groq_api_key=api_key,
            streaming=True
        )
        
        # Local CPU Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = self._build_knowledge_base()

    def _build_knowledge_base(self):
        practices = [
            "Use context managers (with open...) for file handling.",
            "Always validate user inputs before processing.",
            "Use try-except blocks for error handling.",
            "Follow PEP-8 naming conventions (snake_case for variables).",
            "Avoid global variables where possible."
        ]
        return FAISS.from_texts(practices, self.embeddings)

    def get_context(self, query):
        docs = self.vector_store.similarity_search(query, k=1)
        return docs[0].page_content if docs else "General best practices."

    def stream_analysis(self, code, language, context):
        """
        Streams the response with an artificial delay for better readability.
        """
        system = f"""
        You are an expert Code Reviewer. Analyze this {language} code.
        Context: {context}
        
        Provide:
        1. 🚨 **Diagnosis**: What is wrong?
        2. 🛠️ **Fix**: The corrected code.
        3. 💡 **Explanation**: Why this fix is better.
        """
        
        chain = ChatPromptTemplate.from_messages([("system", system), ("user", "{code}")]) | self.llm | StrOutputParser()
        
        # SLOW STREAMING LOGIC
        for chunk in chain.stream({"code": code}):
            yield chunk
            time.sleep(0.02) # <-- This slows it down (Adjust 0.02 to 0.05 for even slower)