import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

class LLMGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            print("Error: GROQ_API_KEY not found in .env")
            
        # Using Llama 3 70B via Groq for high performance / facts-only adherence
        self.llm = ChatGroq(
            temperature=0, 
            model_name="llama3-70b-8192",
            groq_api_key=self.api_key
        )

        # Strict System Prompt from Rag_Architecture.md
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a Mutual Fund FAQ Assistant.

Rules:
- Answer ONLY from the provided context.
- If the answer is not in the context, say: "Information not available in official sources."
- Do NOT give advice, opinions, or recommendations.
- Keep your answer concise: NO MORE than 3 sentences.
- Include exactly ONE source link from the context metadata.

Conversation History:
{history}

"""),
            ("human", "Context: {context}\n\nQuestion: {question}")
        ])

    def generate_answer(self, query, retrieved_chunks, history_text=""):
        """
        Phase F: Generates the final grounded answer.
        """
        if not retrieved_chunks:
            return "Information not available in official sources."

        # Format context from retrieved chunks
        context_text = ""
        for i, chunk in enumerate(retrieved_chunks):
            context_text += f"\n--- Document {i+1} ---\n"
            context_text += f"Content: {chunk.page_content}\n"
            context_text += f"Source URL: {chunk.metadata.get('source_url', 'N/A')}\n"

        # Construct final prompt
        chain = self.prompt_template | self.llm
        
        try:
            response = chain.invoke({
                "context": context_text, 
                "question": query,
                "history": history_text
            })
            return response.content
        except Exception as e:
            return f"Error during generation: {str(e)}"

if __name__ == "__main__":
    # Local Test (Mocking chunks)
    from langchain.schema import Document
    
    mock_chunks = [
        Document(
            page_content="The SBI Bluechip Fund has an expense ratio of 1.2% for the direct plan.",
            metadata={"source_url": "https://sbimf.com/bluechip-factsheet"}
        )
    ]
    
    gen = LLMGenerator()
    answer = gen.generate_answer("What is the expense ratio?", mock_chunks)
    print("\nTest Generation Output:")
    print(answer)
