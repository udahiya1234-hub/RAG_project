'use client';

import DocumentUploadComponent from '@/components/DocumentUpload';

export default function UploadPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold mb-8">📄 Upload Documents</h1>
      <DocumentUploadComponent />

      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-3">ℹ️ Supported Formats</h2>
        <ul className="space-y-2 text-sm">
          <li>✅ PDF (.pdf)</li>
          <li>✅ Text (.txt)</li>
          <li>✅ Word (.docx)</li>
        </ul>
        <p className="text-xs text-gray-600 mt-4">
          Documents are chunked into 800-character segments with 120-character overlap
          and stored in memory for RAG queries.
        </p>
      </div>
    </div>
  );
}
