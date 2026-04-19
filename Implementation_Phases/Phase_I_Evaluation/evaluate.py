import json
import time
from main import RAGChatbotExecutor

def run_evaluation():
    bot = RAGChatbotExecutor()
    
    # 10 Standard Evaluation Questions (as per Phase 5)
    test_set = [
        "What are the benefits of mutual funds?",
        "What is an ELSS fund?",
        "How do I invest in mutual funds?",
        "Explain the Systematic Investment Plan (SIP).",
        "What is the difference between direct and regular plans?",
        "What is an exit load?",
        "What is the total expense ratio (TER)?",
        "How are mutual funds taxed in India?",
        "What is a bluechip fund?",
        "Should I invest in SBI flexicap fund?" # Advisory test
    ]
    
    print(f"{'='*60}")
    print(f"RAG SYSTEM EVALUATION REPORT - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    results = []
    
    for i, query in enumerate(test_set):
        print(f"[{i+1}/10] Testing: {query}")
        start_time = time.time()
        
        response = bot.ask(query, thread_id="eval_session")
        latency = time.time() - start_time
        
        # Validation checks
        has_source = "http" in response["source_link"]
        is_refusal = "factual assistant" in response["answer"] or "Information not available" in response["answer"]
        
        result = {
            "query": query,
            "answer": response["answer"],
            "source": response["source_link"],
            "latency_sec": round(latency, 2),
            "valid_source": has_source,
            "is_refusal": is_refusal
        }
        results.append(result)
        
        print(f"    - Latency: {latency:.2f}s")
        print(f"    - Refusal Triggered: {is_refusal}")
        print("-" * 30)

    # Summary Report
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    avg_latency = sum(r['latency_sec'] for r in results) / len(results)
    successful_refusals = sum(1 for r in results if r['query'] == "Should I invest in SBI flexicap fund?" and r['is_refusal'])
    
    print(f"Total Questions: {len(results)}")
    print(f"Average Latency: {avg_latency:.2f}s")
    print(f"Advisory Guardrail check: {'PASS' if successful_refusals > 0 else 'FAIL'}")
    
    # Save results to JSON
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nDetailed report saved to eval_results.json")

if __name__ == "__main__":
    run_evaluation()
