# Known Limitations & Disclaimers

This RAG Mutual fund Assistant is designed for **educational purposes only**. It operates under strict guardrails to prevent unauthorized investment advice.

## 1. Scope of Knowledge
- The assistant can only verify information from the provided corpus (SBI Mutual Fund, AMFI, SEBI).
- It does **not** have access to real-time market data or specific user portfolio details.

## 2. No Investment Advice
- In accordance with SEBI regulations, this bot **cannot** and **will not** provide:
    - Fund recommendations (e.g., "Buy SBI Bluechip").
    - Return predictions (e.g., "This fund will grow 15%").
    - Comparison-based advice (e.g., "Fund A is better than Fund B").

## 3. Potential for Latency
- The system generates embeddings locally on the CPU, which may result in a 2-5 second delay for fresh queries.

## 4. Hallucination Guardrails
- If the vector database search falls below a quality threshold, the assistant is programmed to refuse the query rather than hallucinate an answer.

## 5. Official Source Citation
- Every response includes at least one source link. Users are encouraged to verify information directly from the AMC website provided.
