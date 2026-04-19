import os
import datetime
from Implementation_Phases.Phase_D_Retriever.retriever import VectorRetriever

class QueryProcessor:
    def __init__(self):
        self.retriever = VectorRetriever()
        
        # Guardrail keywords for advisory detection
        self.advisory_keywords = [
            "should i invest", "which fund is better", "recommend", 
            "advice", "suggest", "best mutual fund", "is it good to buy",
            "buy or sell", "where should i put my money"
        ]
        
        # Educational link for refusal (as per architecture)
        self.educational_link = "https://www.amfiindia.com/investor-corner/knowledge-center/mutual-funds-basics"

    def is_advisory_query(self, query):
        """
        Phase 4: Explicit Refusal for Advisory detection.
        """
        query_lower = query.lower()
        # Expanded keywords for better advisory detection
        self.advisory_keywords = [
            "should i invest", "recommend", "best fund", "advice", 
            "is it good to buy", "suggest a fund", "where to put money",
            "prediction", "will it go up", "investing advice"
        ]
        for kw in self.advisory_keywords:
            if kw in query_lower:
                return True
        return False

    def process_query(self, user_query):
        """
        Step I & J: Orchestrates Refusal Handling System.
        """
        # Step I: Advisory Guardrail
        if self.is_advisory_query(user_query):
            return {
                "status": "refused",
                "message": "I am a factual assistant. I cannot provide investment advice. Please consult a SEBI registered advisor.",
                "educational_link": "https://www.amfiindia.com/investor-corner/knowledge-center/mutual-funds-basics",
                "chunks": []
            }

        # Step J: Hallucination Guardrail (Retrieval)
        relevant_chunks = self.retriever.retrieve_relevant_chunks(user_query, k=3)
        
        # Check if chunks are found (Hallucination Guardrail)
        if not relevant_chunks:
            return {
                "status": "not_found",
                "message": "I don't have enough verified information in official sources to answer this accurately.",
                "educational_link": "https://www.amfiindia.com/en-us/faq",
                "chunks": []
            }

        return {
            "status": "success",
            "chunks": relevant_chunks
        }

if __name__ == "__main__":
    processor = QueryProcessor()
    
    # Test case 1: Factual
    print(processor.process_query("What are the different types of mutual funds?"))
    
    # Test case 2: Advisory
    print(processor.process_query("Should i invest in SBI Bluechip fund?"))
