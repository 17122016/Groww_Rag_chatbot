"use client";

import { useState, useRef, useEffect } from "react";
import { Message, ChatResponse } from "@/types/chat";

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello! I am your Mutual Fund Factual Assistant. I can provide grounded information from SBI, AMFI, and SEBI official documents. Please note: I cannot predict returns or suggest which funds you should buy.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initialize or retrieve thread ID
    let tid = localStorage.getItem("chat_thread_id");
    if (!tid) {
      tid = "thread_" + Math.random().toString(36).substring(7);
      localStorage.setItem("chat_thread_id", tid);
    }
    setThreadId(tid);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, thread_id: threadId }),
      });

      if (!response.ok) throw new Error("Backend offline");

      const data: ChatResponse = await response.json();
      
      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer,
        source_link: data.source_link,
        footer: data.footer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I had trouble connecting to the backend. Please ensure the API is running." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (msgIndex: number, rating: number) => {
    const msg = messages[msgIndex];
    const prevMsg = messages[msgIndex - 1]; // The user query
    
    try {
      await fetch("http://localhost:8000/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          thread_id: threadId,
          query: prevMsg?.content || "N/A",
          response: msg.content,
          rating: rating
        }),
      });
      // Simple UI feedback: replace buttons with thank you
      const updated = [...messages];
      updated[msgIndex].footer = "Thanks for your feedback! " + (updated[msgIndex].footer || "");
      setMessages(updated);
    } catch (e) {
      console.error("Feedback failed", e);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] max-w-4xl mx-auto p-4">
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto space-y-6 pr-2 scrollbar-thin scrollbar-thumb-gray-700">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start animate-fade-in"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 shadow-lg ${
                m.role === "user"
                  ? "bg-growwGreen text-black rounded-tr-none font-medium"
                  : "bg-cardBg text-white border border-border rounded-tl-none"
              }`}
            >
              <p className="text-[15px] leading-relaxed">{m.content}</p>
              
              {m.source_link && (
                <div className="mt-3 pt-3 border-t border-gray-700">
                  <span className="text-xs text-gray-400 block mb-1 uppercase tracking-wider font-semibold">Verified Source:</span>
                  <a
                    href={m.source_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-growwGreen hover:underline text-sm break-all inline-flex items-center gap-1"
                  >
                    {m.source_link}
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
              )}
              
              {m.footer && (
                <p className="text-[10px] text-gray-500 mt-2 font-mono">{m.footer}</p>
              )}

              {/* Feedback Section for Assistant */}
              {m.role === "assistant" && i > 0 && !m.footer?.includes("Thanks") && (
                <div className="flex gap-4 mt-3 pt-2 border-t border-white/5 items-center">
                   <button 
                    onClick={() => handleFeedback(i, 1)}
                    className="text-gray-500 hover:text-growwGreen transition-colors flex items-center gap-1 text-xs"
                   >
                     <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" /></svg>
                     Helpful
                   </button>
                   <button 
                    onClick={() => handleFeedback(i, -1)}
                    className="text-gray-500 hover:text-red-400 transition-colors flex items-center gap-1 text-xs"
                   >
                     <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.737 3h4.017c.163 0 .326.02.485.06L17 4m-7 10v5a2 2 0 002 2h.095c.5 0 .905-.405.905-.905 0-.714.211-1.412.608-2.006L17 13V4m-7 10h2m7-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" /></svg>
                     Unhelpful
                   </button>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-cardBg p-4 rounded-2xl rounded-tl-none border border-border">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-growwGreen rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-growwGreen rounded-full animate-bounce [animation-delay:-0.15s]" />
                <div className="w-2 h-2 bg-growwGreen rounded-full animate-bounce [animation-delay:-0.3s]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <form onSubmit={handleSubmit} className="mt-4 relative group">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about returns, exit loads, or schemes..."
          className="w-full bg-cardBg border border-border rounded-2xl py-4 pl-6 pr-16 text-white focus:outline-none focus:border-growwGreen transition-all placeholder:text-gray-500 shadow-xl"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 bg-growwGreen rounded-xl text-black hover:bg-growwGreen-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </form>

      {/* Sticky Disclaimer (Phase 6) */}
      <div className="mt-4 text-[10px] text-gray-500 text-center px-4 leading-relaxed">
        ⚠️ Disclaimer: This bot provides educational information based on official sources (SBI/AMFI/SEBI). 
        It does <span className="text-gray-400 font-semibold underline">NOT</span> provide SEBI-registered investment advice or return predictions.
      </div>
    </div>
  );
}
