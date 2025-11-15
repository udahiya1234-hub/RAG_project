'use client';

import { useState } from 'react';
import { getMindMap } from '@/lib/services/apiClient';

export default function MindMapComponent() {
  const [mindmap, setMindmap] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateMindMap = async () => {
    setLoading(true);
    try {
      const response = await getMindMap();
      setMindmap(response.mindmap);
    } catch (error) {
      setMindmap(`❌ Error generating mind map: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">🧠 Mind Map</h2>

      <button
        onClick={handleGenerateMindMap}
        disabled={loading}
        className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white py-2 rounded transition mb-4"
      >
        {loading ? 'Generating...' : 'Generate Mind Map'}
      </button>

      {mindmap && (
        <div className="bg-gray-50 p-4 rounded text-sm whitespace-pre-wrap max-h-96 overflow-y-auto font-mono">
          {mindmap}
        </div>
      )}
    </div>
  );
}
