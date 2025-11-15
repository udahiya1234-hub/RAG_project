'use client';

import QuizComponent from '@/components/Quiz';

export default function QuizPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-8">❓ Quiz</h1>
      <QuizComponent />
    </div>
  );
}
