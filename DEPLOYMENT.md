# 🚀 Deployment & Production Guide

## Local Development Setup

### Windows

```bash
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create and configure .env
copy .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run app
streamlit run app.py
```

### macOS / Linux

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create and configure .env
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run app
streamlit run app.py
```

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account with repo containing the code
- GROQ API key

### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy RAG system"
git push origin main
```

2. **Create secrets.toml**
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_actual_key_here"
```

3. **Update app.py** to use secrets:
```python
import streamlit as st

api_key = st.secrets["GROQ_API_KEY"]
```

4. **Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Click "New app"
- Select your GitHub repo
- Set main file to `app.py`
- Add secrets in Advanced Settings
- Deploy!

### Production .streamlit/config.toml

```toml
[client]
showErrorDetails = false
toolbarMode = "minimal"

[server]
maxUploadSize = 200
timeoutSession = 3600

[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
COPY app.py .
COPY rag.py .
COPY utils.py .
COPY .env.example .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Set environment
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  rag-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      GROQ_API_KEY: ${GROQ_API_KEY}
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t rag-system .

# Run container
docker run -e GROQ_API_KEY=your_key -p 8501:8501 rag-system

# Or with docker-compose
docker-compose up
```

## AWS Deployment (Lightsail)

### Setup

```bash
# SSH into your instance
ssh -i your-key.pem ec2-user@your-instance

# Install Python and dependencies
sudo yum update -y
sudo yum install python3 python3-pip -y

# Clone repository
git clone your-repo-url
cd RAG_notebook

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env
cp .env.example .env
# Edit .env with your GROQ_API_KEY
nano .env

# Run with gunicorn
pip install gunicorn
streamlit run app.py &
```

### Using Systemd Service

Create `/etc/systemd/system/rag-app.service`:

```ini
[Unit]
Description=RAG System Application
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/RAG_notebook
Environment="GROQ_API_KEY=your_key"
ExecStart=/home/ec2-user/RAG_notebook/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rag-app
sudo systemctl start rag-app
sudo systemctl status rag-app
```

## Heroku Deployment

### Procfile

```
web: streamlit run app.py --logger.level=error --client.toolbarMode=minimal
```

### Setup

```bash
# Install Heroku CLI
# Create app
heroku create your-app-name

# Set environment variable
heroku config:set GROQ_API_KEY=your_key

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## Performance Optimization

### Caching Strategy

```python
import streamlit as st
from functools import lru_cache

@st.cache_resource
def get_rag_system():
    return RAGSystem()

@st.cache_data
def get_document_summary(doc_name):
    rag = get_rag_system()
    return rag.generate_summary()
```

### Reduce Model Inference Time

```python
# Use smaller model for speed
self.model = "llama-3.1-8b-instant"  # Fast

# Or use faster approach
temperature = 0.5  # Lower = faster
max_tokens = 300   # Shorter responses
```

### Optimize Chunking

```python
# Larger chunks = fewer retrievals = faster
RAGSystem(chunk_size=2000, overlap=300)

# Fewer chunks to retrieve
rag.query(question, top_k=2)  # Instead of 3
```

## Monitoring & Logging

### Add Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In RAGSystem
logger.info(f"Processing document: {doc_name}")
logger.info(f"Generated {len(quiz)} quiz questions")
logger.warning("Query took longer than expected")
logger.error(f"API error: {error_message}")
```

### Streamlit Monitoring

```python
import streamlit as st

# Track usage
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4()

# Log analytics
st.write(f"Session: {st.session_state.session_id}")
```

## Security Best Practices

### 1. API Key Management
- ✅ Store in .env (never commit)
- ✅ Use secrets in production
- ✅ Rotate keys regularly
- ❌ Don't hardcode keys
- ❌ Don't log keys

### 2. Input Validation
```python
# Validate file uploads
if uploaded_file.size > 50 * 1024 * 1024:  # 50 MB
    st.error("File too large")
    return
```

### 3. Rate Limiting
```python
import time
last_query_time = 0

def rate_limited_query():
    global last_query_time
    current_time = time.time()
    if current_time - last_query_time < 1:
        st.warning("Please wait before next query")
        return
    last_query_time = current_time
```

### 4. CORS Headers (if API)
```python
# For API deployment
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Scaling Considerations

### Load Balancing
```yaml
# Multiple instances with load balancer
rag-app-1: streamlit run app.py
rag-app-2: streamlit run app.py
rag-app-3: streamlit run app.py
# Nginx/HAProxy distributes traffic
```

### Database Integration (Future)
```python
# Replace in-memory storage with database
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost/rag_db')

# Store chunks in DB instead of memory
# Implement caching layer
# Use Redis for session state
```

### Vector Database (Future)
```python
# Add semantic search
from chromadb import Client

client = Client()
collection = client.get_or_create_collection("documents")

# Store embeddings
collection.add(
    ids=chunk_ids,
    embeddings=embeddings,
    documents=chunk_texts
)
```

## Backup & Recovery

### Backup Strategy
```bash
# Backup configuration
tar -czf backup-rag-$(date +%Y%m%d).tar.gz \
    .env \
    *.py \
    requirements.txt

# Upload to S3
aws s3 cp backup-rag-*.tar.gz s3://my-bucket/rag/
```

### Recovery
```bash
# Restore from backup
aws s3 cp s3://my-bucket/rag/backup-rag-latest.tar.gz .
tar -xzf backup-rag-latest.tar.gz
```

## Monitoring Checklist

- [ ] API key rotation schedule
- [ ] Disk space monitoring
- [ ] Memory usage tracking
- [ ] API rate limits
- [ ] Error logging
- [ ] Performance metrics
- [ ] User session tracking
- [ ] Cost monitoring (GROQ API)
- [ ] Uptime monitoring
- [ ] Backup verification

## Common Production Issues

### Issue: Out of Memory
**Solution**: 
- Reduce chunk cache size
- Implement database storage
- Use smaller model (8B instead of 70B)

### Issue: Slow Responses
**Solution**:
- Optimize retrieval (fewer chunks, faster algorithm)
- Use CDN for static files
- Implement response caching

### Issue: API Rate Limits
**Solution**:
- Upgrade GROQ plan
- Implement request queuing
- Cache results
- Batch operations

### Issue: High Latency
**Solution**:
- Deploy closer to users (regional deployment)
- Use smaller model for speed
- Implement streaming responses
- Add caching layer

## Maintenance Tasks

### Weekly
- [ ] Check API usage (GROQ dashboard)
- [ ] Review error logs
- [ ] Test backup process

### Monthly
- [ ] Update dependencies
- [ ] Review performance metrics
- [ ] Security audit
- [ ] Database cleanup

### Quarterly
- [ ] Update documentation
- [ ] Performance optimization review
- [ ] Capacity planning
- [ ] Cost analysis

## Support & Troubleshooting

**GROQ API Issues:**
- Status: https://status.groq.com
- Docs: https://console.groq.com/docs
- Support: console.groq.com

**Streamlit Issues:**
- Docs: https://docs.streamlit.io
- GitHub: https://github.com/streamlit/streamlit

**Docker Issues:**
- Docs: https://docs.docker.com
- Registry: https://hub.docker.com

---

**Last Updated**: November 2025
**Version**: 1.0.0

For production deployment, always:
1. ✅ Test thoroughly
2. ✅ Secure API keys
3. ✅ Monitor performance
4. ✅ Set up backups
5. ✅ Plan for scaling
