🧾 Final Problem Statement (Groww UI Version)
Overview

Build a RAG-based Mutual Fund FAQ Assistant with a Groww-inspired user interface that answers facts-only queries about mutual fund schemes using official sources (AMC, AMFI, SEBI).

The assistant must:

Provide concise, factual answers
Include exactly one source link
Never give investment advice
Objective

Create a chatbot that:

Mimics a Groww-style experience
Helps users quickly find verified mutual fund information
Ensures high trust, compliance, and transparency
Product Context (Groww UI)

Design the UI similar to Groww:

Clean, minimal layout
Simple typography
Chat-first interaction
Mobile-friendly design
Core Features
1. Chat Interface (Main Screen)
Chat window (like Groww support/chat)
Input box for queries
Bot responses displayed in cards
2. Welcome Section
Title: “Mutual Fund FAQ Assistant”
Subtitle: Facts-only. No investment advice.
3 example questions:
“What is the expense ratio of [scheme]?”
“What is ELSS lock-in period?”
“How to download capital gains statement?”
3. Response Format (Strict)

Each response must:

Be ≤ 3 sentences
Include:
✅ Answer
🔗 One source link
📅 Footer: Last updated from sources: <date>
4. Refusal Handling UI

For advisory queries:

Show polite message:
“I can only provide factual information, not investment advice.”
Add one educational link (AMFI/SEBI)
5. Data Scope (Backend)
Select:
1 AMC
3–5 schemes
Use:
Factsheets
KIM / SID
AMC FAQs
AMFI / SEBI pages
Technical Architecture (Simple RAG Flow)
Data Collection
Scrape/download official documents
Preprocessing
Clean + chunk text
Embeddings
Convert chunks → vectors
Vector Store
Store in FAISS / Chroma
Query Flow
User asks → retrieve relevant chunks
LLM generates facts-only answer
UI Design Guidelines (Groww Style)
White background, lots of spacing
Rounded chat bubbles
Subtle colors (green/blue accents)
Minimal clutter
Focus on readability + trust
Constraints
❌ No investment advice
❌ No comparisons
❌ No return calculations
❌ No personal data collection
✅ Only official sources
✅ Always include citation
✅ Always factual
Deliverables
Working chatbot (preferably Streamlit / React UI)
Groww-style interface
README (with RAG explanation)
Source list (15–25 links)
Sample Q&A