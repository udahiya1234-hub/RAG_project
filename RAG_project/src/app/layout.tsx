import type { Metadata } from 'next';
import './globals.css';
import Navigation from './Navigation';

export const metadata: Metadata = {
  title: 'RAG Application',
  description: 'Retrieval-Augmented Generation with Gemini API',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        <Navigation>{children}</Navigation>
      </body>
    </html>
  );
}
