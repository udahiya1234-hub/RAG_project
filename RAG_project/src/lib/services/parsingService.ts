import * as pdfjsLib from 'pdfjs-dist';
import { convertDocxToHtml } from 'mammoth';

// Set up PDF worker
if (typeof window === 'undefined') {
  pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;
}

export async function parsePDF(file: File): Promise<string> {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

    let text = '';
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map((item: any) => item.str).join(' ');
      text += pageText + '\n';
    }

    return text;
  } catch (error) {
    throw new Error(`Failed to parse PDF: ${error}`);
  }
}

export async function parseDocx(file: File): Promise<string> {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const result = await convertDocxToHtml({ arrayBuffer });
    // Extract text from HTML
    const div = document.createElement('div');
    div.innerHTML = result.value;
    return div.innerText || '';
  } catch (error) {
    throw new Error(`Failed to parse DOCX: ${error}`);
  }
}

export async function parseTxt(file: File): Promise<string> {
  try {
    return await file.text();
  } catch (error) {
    throw new Error(`Failed to parse TXT: ${error}`);
  }
}

export async function parseDocument(file: File): Promise<string> {
  const fileType = file.type;
  const fileName = file.name.toLowerCase();

  if (fileType === 'application/pdf' || fileName.endsWith('.pdf')) {
    return parsePDF(file);
  } else if (
    fileType ===
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
    fileName.endsWith('.docx')
  ) {
    return parseDocx(file);
  } else if (fileType === 'text/plain' || fileName.endsWith('.txt')) {
    return parseTxt(file);
  } else {
    throw new Error(`Unsupported file type: ${fileType}`);
  }
}
