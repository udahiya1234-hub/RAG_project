'use client';

import { useState } from 'react';
import { getQuiz } from '@/lib/services/apiClient';
import { QuizQuestion } from '@/lib/types/index';

export default function QuizComponent() {
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [showResults, setShowResults] = useState(false);

  const handleGenerateQuiz = async () => {
    setLoading(true);
    setShowResults(false);
    setSelectedAnswers({});
    try {
      const response = await getQuiz();
      setQuestions(response.questions || []);
    } catch (error) {
      console.error('Error generating quiz:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (questionId: string, option: string) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: option,
    }));
  };

  const handleSubmitQuiz = () => {
    setShowResults(true);
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q) => {
      if (selectedAnswers[q.id] === q.correctAnswer) correct++;
    });
    return ((correct / questions.length) * 100).toFixed(0);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">❓ Quiz</h2>

      {questions.length === 0 ? (
        <button
          onClick={handleGenerateQuiz}
          disabled={loading}
          className="w-full bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white py-2 rounded transition"
        >
          {loading ? 'Generating...' : 'Generate Quiz'}
        </button>
      ) : (
        <div>
          <div className="space-y-4 max-h-96 overflow-y-auto mb-4">
            {questions.map((question) => (
              <div key={question.id} className="border rounded p-3">
                <p className="font-semibold text-sm mb-2">{question.question}</p>
                <div className="space-y-2">
                  {question.options.map((option) => (
                    <label key={option} className="flex items-center gap-2 cursor-pointer text-sm">
                      <input
                        type="radio"
                        name={question.id}
                        value={option}
                        checked={selectedAnswers[question.id] === option}
                        onChange={() => handleSelectAnswer(question.id, option)}
                        disabled={showResults}
                        className="cursor-pointer"
                      />
                      <span
                        className={`${
                          showResults
                            ? option === question.correctAnswer
                              ? 'bg-green-100 text-green-800'
                              : option === selectedAnswers[question.id]
                              ? 'bg-red-100 text-red-800'
                              : ''
                            : ''
                        } px-2 py-1 rounded`}
                      >
                        {option}
                      </span>
                    </label>
                  ))}
                </div>

                {showResults && (
                  <div className="mt-2 text-xs text-gray-600 border-t pt-2">
                    <p>✅ Correct: {question.correctAnswer}</p>
                    <p>{question.explanation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {!showResults && (
            <button
              onClick={handleSubmitQuiz}
              className="w-full bg-purple-500 hover:bg-purple-600 text-white py-2 rounded transition mb-4"
            >
              Submit Quiz
            </button>
          )}

          {showResults && (
            <div className="bg-blue-50 p-4 rounded text-center">
              <p className="text-lg font-bold">Score: {calculateScore()}%</p>
              <button
                onClick={handleGenerateQuiz}
                className="mt-2 bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded transition text-sm"
              >
                New Quiz
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
