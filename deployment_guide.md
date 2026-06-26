# QueueStorm Investigator - Deployment Guide

## Quick Deploy to Render (Recommended)

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Final submission ready"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `queuestorm-investigator`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables:
     - `OPENAI_API_KEY`: (your API key)
     - `OPENAI_API_BASE`: (your base URL)
     - `MODEL_NAME`: `deepseek-v4-flash-free`
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment

3. **Test Your Deployment**:
   ```bash
   curl https://your-app.onrender.com/health
   ```

## Alternative: Railway

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy**:
   ```bash
   railway init
   railway up
   railway variables set OPENAI_API_KEY="your-key"
   railway variables set OPENAI_API_BASE="your-base-url"
   railway variables set MODEL_NAME="deepseek-v4-flash-free"
   ```

3. **Get URL**:
   ```bash
   railway domain
   ```

## Alternative: Fly.io

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Create fly.toml**:
   ```toml
   app = "queuestorm-investigator"
   
   [build]
     builder = "paketobuildpacks/builder:base"
   
   [env]
     PORT = "8080"
   
   [[services]]
     http_checks = []
     internal_port = 8080
     protocol = "tcp"
   
     [[services.ports]]
       port = 80
       handlers = ["http"]
   
     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]
   ```

3. **Deploy**:
   ```bash
   fly launch
   fly secrets set OPENAI_API_KEY="your-key"
   fly secrets set OPENAI_API_BASE="your-base-url"
   fly secrets set MODEL_NAME="deepseek-v4-flash-free"
   fly deploy
   ```

## Docker Deployment

1. **Build Image**:
   ```bash
   docker build -t queuestorm-investigator .
   ```

2. **Run Locally**:
   ```bash
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY="your-key" \
     -e OPENAI_API_BASE="your-base-url" \
     -e MODEL_NAME="deepseek-v4-flash-free" \
     queuestorm-investigator
   ```

3. **Push to Docker Hub** (optional):
   ```bash
   docker tag queuestorm-investigator your-username/queuestorm-investigator
   docker push your-username/queuestorm-investigator
   ```

## Submission Checklist

- [ ] Service deployed and accessible via HTTPS
- [ ] `/health` endpoint returns `{"status":"ok"}`
- [ ] `/analyze-ticket` processes requests successfully
- [ ] GitHub repository is public or accessible to `bipulhf`
- [ ] README.md is complete with setup instructions
- [ ] .env.example is in repo (no real secrets)
- [ ] queuestorm_sample_outputs.json is committed
- [ ] Submit live URL + GitHub link through official form

## Testing Your Live Deployment

```bash
# Test health
curl https://your-deployed-url.com/health

# Test analyze-ticket
curl -X POST https://your-deployed-url.com/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TEST-001",
    "complaint": "I sent 5000 taka to wrong number",
    "transaction_history": []
  }'
```

## Troubleshooting

- **Service won't start**: Check environment variables are set correctly
- **Slow responses**: Verify LLM API is accessible from deployment platform
- **Timeout errors**: Check timeout is set to 15s in llm.py (already fixed)
- **Memory issues**: Most platforms need 512MB minimum RAM

Good luck with your submission! 🚀
