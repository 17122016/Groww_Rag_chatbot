import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <main className="min-h-[calc(100vh-80px)]">
      {/* Background decoration */}
      <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-growwGreen/5 blur-[120px] rounded-full -z-10" />
      <div className="fixed bottom-0 left-0 w-[300px] h-[300px] bg-blue-500/5 blur-[100px] rounded-full -z-10" />
      
      <ChatInterface />
    </main>
  );
}
