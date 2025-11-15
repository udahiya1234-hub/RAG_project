'use client';

import { useState } from 'react';
import { getSummary } from '@/lib/services/apiClient';

export default function SummaryComponent() {
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [length, setLength] = useState<'short' | 'medium' | 'long'>('medium');

  const handleGenerateSummary = async () => {
    setLoading(true);
    try {
      const response = await getSummary(length);
      setSummary(response.summary);
    } catch (error) {
      setSummary(`❌ Error generating summary: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">📝 Summary</h2>

      <div className="flex gap-2 mb-4">
        {(['short', 'medium', 'long'] as const).map((option) => (
          <button
            key={option}
            onClick={() => setLength(option)}
            className={`px-4 py-2 rounded capitalize transition ${
              length === option
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            {option}
          </button>
        ))}
      </div>

      <button
        onClick={handleGenerateSummary}
        disabled={loading}
        className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white py-2 rounded transition mb-4"
      >
        {loading ? 'Generating...' : 'Generate Summary'}
      </button>

      {summary && (
        <div className="bg-gray-50 p-4 rounded text-sm whitespace-pre-wrap max-h-96 overflow-y-auto">
          {summary}
        </div>
      )}
    </div>
  );
}
