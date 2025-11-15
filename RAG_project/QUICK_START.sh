#!/bin/bash
# RAG Application Quick Start Script

echo "🚀 RAG Application Setup"
echo "========================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

echo "✅ Node.js $(node --version) found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🔑 Environment Setup"
echo "===================="
echo ""
echo "Create .env.local file:"
echo ""
echo "1. Go to https://aistudio.google.com/app/apikey"
echo "2. Click 'Create API key'"
echo "3. Copy your API key"
echo "4. Create file: .env.local"
echo "5. Add: GEMINI_API_KEY=your_key_here"
echo ""

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "⚠️  .env.local not found"
    echo "Please create .env.local with your GEMINI_API_KEY before running dev server"
    echo ""
fi

echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. Create .env.local with GEMINI_API_KEY"
echo "2. Run: npm run dev"
echo "3. Open: http://localhost:3000"
echo "4. Upload a document"
echo "5. Start asking questions!"
echo ""
echo "📚 Documentation:"
echo "=================="
echo "- README.md - Full setup & deployment guide"
echo "- PROJECT_GUIDE.md - Detailed feature overview"
echo ".env.example - Environment template"
echo ""
echo "🌐 Deployment:"
echo "==============="
echo "1. Push to GitHub"
echo "2. Connect to Vercel"
echo "3. Add GEMINI_API_KEY environment variable"
echo "4. Deploy!"
echo ""
echo "✨ Happy building! 🚀"
