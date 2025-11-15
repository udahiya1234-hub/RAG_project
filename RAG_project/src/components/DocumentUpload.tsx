'use client';

import { useState, useRef } from 'react';
import { uploadDocument } from '@/lib/services/apiClient';

export default function DocumentUploadComponent() {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];
    const validTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

    if (!validTypes.includes(file.type)) {
      setMessage('❌ Invalid file type. Please upload PDF, TXT, or DOCX.');
      return;
    }

    setUploading(true);
    setMessage(null);

    try {
      const response = await uploadDocument(file);
      setMessage(
        `✅ ${response.message} (${response.chunksCreated} chunks created)`
      );
    } catch (error) {
      setMessage(`❌ Upload failed: ${error}`);
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-md">
      <h2 className="text-2xl font-bold mb-4">📄 Upload Documents</h2>

      <div className="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center cursor-pointer hover:bg-blue-50 transition"
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          hidden
          onChange={handleFileSelect}
          disabled={uploading}
          accept=".pdf,.txt,.docx"
        />
        <div className="text-4xl mb-2">📁</div>
        <p className="text-sm text-gray-600">
          {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
        </p>
        <p className="text-xs text-gray-400">PDF, TXT, DOCX</p>
      </div>

      {message && (
        <div className="mt-4 p-3 bg-gray-100 rounded text-sm">
          {message}
        </div>
      )}
    </div>
  );
}
