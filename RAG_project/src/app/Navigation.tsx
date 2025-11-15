'use client';

import Link from 'next/link';
import { useState } from 'react';
import {
  Menu,
  X,
  Home,
  MessageSquare,
  Upload,
  BookOpen,
  HelpCircle,
  Lightbulb,
  Brain,
  LayoutGrid,
} from 'lucide-react';

export default function Navigation({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigationItems = [
    { href: '/', label: 'Home', icon: Home },
    { href: '/upload', label: 'Upload', icon: Upload },
    { href: '/chat', label: 'Chat', icon: MessageSquare },
    { href: '/summary', label: 'Summary', icon: BookOpen },
    { href: '/study-guide', label: 'Study Guide', icon: Lightbulb },
    { href: '/quiz', label: 'Quiz', icon: HelpCircle },
    { href: '/flashcards', label: 'Flashcards', icon: LayoutGrid },
    { href: '/mindmap', label: 'Mind Map', icon: Brain },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-gray-900 text-white">
        <div className="p-6 border-b border-gray-700">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Brain size={28} />
            RAG App
          </h1>
        </div>

        <nav className="flex-1 overflow-y-auto p-4 space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-3 px-4 py-2 rounded hover:bg-gray-800 transition"
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-gray-700 text-xs text-gray-400">
          <p>🔐 API: Gemini 1.5 Flash</p>
          <p className="mt-2">📦 Memory-based storage</p>
        </div>
      </aside>

      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 bg-gray-900 text-white z-50 flex items-center justify-between p-4">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <Brain size={24} />
          RAG
        </h1>
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="p-2"
        >
          {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden fixed top-16 left-0 right-0 bg-gray-900 text-white z-40 p-4 space-y-2 max-h-96 overflow-y-auto">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-3 px-4 py-2 rounded hover:bg-gray-800 transition"
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto md:mt-0 mt-16">
        <div className="p-4 md:p-8">{children}</div>
      </main>
    </div>
  );
}
