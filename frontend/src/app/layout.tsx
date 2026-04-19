import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Mutual Fund Guide | Factual RAG Assistant",
  description: "Get grounded, factual information on mutual funds directly from official sources.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-background text-foreground antialiased`}>
        <nav className="h-20 border-b border-border flex items-center px-8 bg-background/50 backdrop-blur-md sticky top-0 z-50">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-growwGreen rounded-lg flex items-center justify-center font-bold text-black text-xl">^</div>
            <span className="font-bold text-xl tracking-tight">MutualFund<span className="text-growwGreen">Guide</span></span>
          </div>
          <div className="ml-auto flex gap-6 text-sm font-medium text-gray-400">
             <span className="px-3 py-1 bg-white/5 rounded-full border border-white/10 text-xs">Official Sources Only</span>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
