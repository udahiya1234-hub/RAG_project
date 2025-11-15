'use client';

import { useState } from 'react';
import { chatQuery } from '@/lib/services/apiClient';
import { ChatMessage, SourceReference } from '@/lib/types/index';
import { Send } from 'lucide-react';

export default function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatQuery({ query: input, conversationHistory: messages });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.raw,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ Error: ${error}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-8">
            💬 Start a conversation by uploading documents and asking questions
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-2 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-none'
                  : 'bg-gray-200 text-black rounded-bl-none'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>

              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 text-xs opacity-75 border-t pt-2">
                  <p className="font-semibold">📚 Sources:</p>
                  {msg.sources.map((src, i) => (
                    <p key={i}>
                      {src.filename} (chunk {src.chunkIndex})
                    </p>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-black px-4 py-2 rounded-lg rounded-bl-none">
              <p className="text-sm">⏳ Thinking...</p>
            </div>
          </div>
        )}
      </div>

      <div className="border-t p-4">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your documents..."
            disabled={loading}
            rows={2}
            className="flex-1 border rounded p-2 text-sm resize-none disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={loading || !input.trim()}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded transition h-full"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
