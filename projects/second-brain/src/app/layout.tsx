import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import SearchCommand from "@/components/SearchCommand";
import { getAllDocuments, getAllTags, getFolderStructure } from "@/lib/documents";

export const metadata: Metadata = {
  title: "Second Brain",
  description: "Never lose an idea again",
};

export const dynamic = 'force-dynamic';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const documents = getAllDocuments();
  const tags = getAllTags();
  const folders = getFolderStructure();

  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        <Sidebar folders={folders} tags={tags} />
        <SearchCommand documents={documents} />
        <main className="ml-64 min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
