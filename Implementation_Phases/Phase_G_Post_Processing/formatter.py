import re
from datetime import datetime

class ResponseFormatter:
    def __init__(self):
        # Mandatory educational link for any missing/refused info
        self.default_link = "https://www.amfiindia.com/investor-corner/knowledge-center/mutual-funds-basics"

    def format_last_updated(self, metadata_date=None):
        """Adds the mandatory footer date as per architecture"""
        if not metadata_date:
            metadata_date = datetime.now().strftime("%Y-%m-%d")
        return f"\n\n📅 Last updated from sources: {metadata_date}"

    def post_process(self, raw_llm_response, source_metadata_date=None):
        """
        Phase G: Ensures strict adherence to formatting constraints.
        1. Ensures exactly one link format.
        2. Limits sentences (redundant check).
        3. Adds footer.
        """
        # Split Answer and Source parts
        answer = "Information not available."
        source = self.default_link
        
        # Parse the 'Answer: <text>\nSource: <link>' format from Phase F
        if "Answer:" in raw_llm_response:
            parts = raw_llm_response.split("Source:")
            answer = parts[0].replace("Answer:", "").strip()
            if len(parts) > 1:
                source = parts[1].strip()
        else:
            # Fallback if LLM didn't use labels
            answer = raw_llm_response

        # 1. Enforce sentence limit (Hard truncate if LLM fails)
        sentences = re.split(r'(?<=[.!?]) +', answer)
        if len(sentences) > 3:
            answer = " ".join(sentences[:3])

        # 2. Format final string for Groww UI
        formatted_response = {
            "answer": answer,
            "source_link": source,
            "footer": self.format_last_updated(source_metadata_date)
        }
        
        return formatted_response

if __name__ == "__main__":
    # Local Test
    formatter = ResponseFormatter()
    raw = "Answer: Mutual funds are investment vehicles that pool money. They are managed by professionals. They offer diversification. This is a fourth sentence that should be removed.\nSource: https://sbimf.com"
    
    print(formatter.post_process(raw))
