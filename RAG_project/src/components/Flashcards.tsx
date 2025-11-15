'use client';

import { useState } from 'react';
import { getFlashcards } from '@/lib/services/apiClient';
import { Flashcard } from '@/lib/types/index';

export default function FlashcardsComponent() {
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [loading, setLoading] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  const handleGenerateFlashcards = async () => {
    setLoading(true);
    setCurrentIndex(0);
    setIsFlipped(false);
    try {
      const response = await getFlashcards();
      setCards(response.cards || []);
    } catch (error) {
      console.error('Error generating flashcards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setIsFlipped(false);
    }
  };

  const currentCard = cards[currentIndex];

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">🎴 Flashcards</h2>

      {cards.length === 0 ? (
        <button
          onClick={handleGenerateFlashcards}
          disabled={loading}
          className="w-full bg-indigo-500 hover:bg-indigo-600 disabled:bg-gray-400 text-white py-2 rounded transition"
        >
          {loading ? 'Generating...' : 'Generate Flashcards'}
        </button>
      ) : (
        <div>
          <div
            onClick={() => setIsFlipped(!isFlipped)}
            className="h-64 bg-gradient-to-br from-indigo-400 to-indigo-600 rounded-lg cursor-pointer flex items-center justify-center text-white text-center p-4 transition transform hover:scale-105"
          >
            <div>
              <p className="text-sm opacity-75 mb-2">
                {isFlipped ? 'Answer' : 'Question'}
              </p>
              <p className="text-xl font-semibold">
                {isFlipped ? currentCard.back : currentCard.front}
              </p>
            </div>
          </div>

          <div className="flex justify-between items-center mt-4">
            <button
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="px-4 py-2 bg-gray-300 disabled:bg-gray-200 rounded transition"
            >
              ← Prev
            </button>

            <span className="text-sm text-gray-600">
              {currentIndex + 1} / {cards.length}
            </span>

            <button
              onClick={handleNext}
              disabled={currentIndex === cards.length - 1}
              className="px-4 py-2 bg-gray-300 disabled:bg-gray-200 rounded transition"
            >
              Next →
            </button>
          </div>

          <button
            onClick={handleGenerateFlashcards}
            className="w-full mt-4 bg-indigo-500 hover:bg-indigo-600 text-white py-2 rounded transition text-sm"
          >
            New Set
          </button>
        </div>
      )}
    </div>
  );
}
