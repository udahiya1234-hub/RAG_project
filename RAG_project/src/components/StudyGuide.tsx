'use client';

import { useState } from 'react';
import { getStudyGuide } from '@/lib/services/apiClient';

export default function StudyGuideComponent() {
  const [guide, setGuide] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateGuide = async () => {
    setLoading(true);
    try {
      const response = await getStudyGuide();
      setGuide(response.guide);
    } catch (error) {
      setGuide(`❌ Error generating study guide: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">📚 Study Guide</h2>

      <button
        onClick={handleGenerateGuide}
        disabled={loading}
        className="w-full bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white py-2 rounded transition mb-4"
      >
        {loading ? 'Generating...' : 'Generate Study Guide'}
      </button>

      {guide && (
        <div className="bg-gray-50 p-4 rounded text-sm whitespace-pre-wrap max-h-96 overflow-y-auto">
          {guide}
        </div>
      )}
    </div>
  );
}
