'use client';

import ChatPanel from '@/components/ChatPanel';

export default function ChatPage() {
  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-120px)] flex flex-col">
      <h1 className="text-4xl font-bold mb-4">💬 Chat with Documents</h1>
      <div className="flex-1 min-h-0">
        <ChatPanel />
      </div>
    </div>
  );
}
