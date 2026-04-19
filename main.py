from Implementation_Phases.Phase_E_Query_Processing.query_processor import QueryProcessor
from Implementation_Phases.Phase_F_Generation.generator import LLMGenerator
from Implementation_Phases.Phase_G_Post_Processing.formatter import ResponseFormatter
from Implementation_Phases.Phase_H_Chat_History.history_manager import ChatHistoryManager

class RAGChatbotExecutor:
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.generator = LLMGenerator()
        self.formatter = ResponseFormatter()
        self.history_manager = ChatHistoryManager()

    def ask(self, user_query, thread_id="default"):
        """
        Orchestrates Phases E, F, G, and H in a single execution flow.
        """
        # 0. Get History
        history_text = self.history_manager.format_history_for_llm(thread_id)

        # 1. Phase E: Process & Retrieve (w/ Guardrails)
        processed = self.query_processor.process_query(user_query)
        
        if processed["status"] == "refused":
            # Direct return for advisory queries (No LLM needed)
            res = {
                "answer": processed["message"],
                "source_link": processed["educational_link"],
                "footer": self.formatter.format_last_updated()
            }
            # Record refusal in history if needed, or skip
            return res
            
        if processed["status"] == "not_found":
            return {
                "answer": processed["message"],
                "source_link": self.formatter.default_link,
                "footer": self.formatter.format_last_updated()
            }

        # 2. Phase F: Generate via Groq (with History)
        raw_answer = self.generator.generate_answer(user_query, processed["chunks"], history_text)
        
        # 3. Save to History
        self.history_manager.add_message(thread_id, "user", user_query)
        self.history_manager.add_message(thread_id, "assistant", raw_answer)
        
        # Get metadata from the first chunk for the footer date
        source_date = None
        if processed["chunks"]:
            source_date = processed["chunks"][0].metadata.get("last_updated")

        # 4. Phase G: Final Post-processing
        final_response = self.formatter.post_process(raw_answer, source_date)
        
        return final_response

if __name__ == "__main__":
    # Integration Test
    bot = RAGChatbotExecutor()
    print("\n--- Running Integrated RAG Pipeline (E+F+G) ---\n")
    
    query = "What is a mutual fund?"
    print(f"User: {query}")
    response = bot.ask(query)
    print(f"Bot: {response['answer']}")
    print(f"Link: {response['source_link']}")
    print(f"Footer: {response['footer']}")
