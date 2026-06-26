# VPS Deployment Checklist

## ✅ Repository Status
- [x] Committed all changes
- [x] Pushed to GitHub: https://github.com/TahsinArafat/SUST_Hackathon_2026_Preli
- [x] Commit hash: 04ebc8b

---

## 🚀 Quick VPS Deployment Commands

### Step 1: Clone Repository
```bash
# SSH into your VPS
ssh user@your-vps-ip

# Clone the repo
git clone https://github.com/TahsinArafat/SUST_Hackathon_2026_Preli.git
cd SUST_Hackathon_2026_Preli
```

### Step 2: Setup Environment
```bash
# Install Python 3.9+ if needed
python3 --version

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure .env
```bash
# Copy example
cp .env.example .env

# Edit with your API keys
nano .env

# Add this line with YOUR keys:
LLM_PROVIDERS='[{"name":"provider-1","api_key":"gsk_YOUR_KEY_HERE","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15}]'
```

### Step 4: Test Everything
```bash
# Run unit tests (should pass all 37)
pytest tests/ -v

# Start server for testing
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Test API
curl -X POST http://localhost:8000/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TEST-001",
    "complaint": "I sent 5000 taka to wrong number",
    "transaction_history": []
  }'
```

### Step 5: Production Deployment

#### Option A: Using systemd (Recommended)
```bash
# Create service file
sudo nano /etc/systemd/system/queuestorm.service

# Paste this content (adjust paths):
[Unit]
Description=QueueStorm Investigator API
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/SUST_Hackathon_2026_Preli
Environment="PATH=/home/YOUR_USERNAME/SUST_Hackathon_2026_Preli/.venv/bin"
ExecStart=/home/YOUR_USERNAME/SUST_Hackathon_2026_Preli/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable queuestorm
sudo systemctl start queuestorm
sudo systemctl status queuestorm

# View logs
sudo journalctl -u queuestorm -f
```

#### Option B: Using Screen (Quick & Simple)
```bash
# Start screen session
screen -S queuestorm

# Run server
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Detach: Press Ctrl+A, then D
# Reattach later: screen -r queuestorm
```

#### Option C: Using PM2 (Node.js ecosystem)
```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << 'INNER_EOF'
module.exports = {
  apps: [{
    name: 'queuestorm',
    script: '.venv/bin/uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    cwd: '/home/YOUR_USERNAME/SUST_Hackathon_2026_Preli',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
  }]
};
INNER_EOF

# Start
pm2 start ecosystem.config.js
pm2 save
pm2 startup  # Follow instructions to enable startup
```

### Step 6: Setup Nginx Reverse Proxy (Optional but Recommended)
```bash
# Install nginx
sudo apt update
sudo apt install nginx

# Create config
sudo nano /etc/nginx/sites-available/queuestorm

# Paste:
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 30s;
        proxy_read_timeout 30s;
    }
}

# Enable
sudo ln -s /etc/nginx/sites-available/queuestorm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 7: Setup Firewall
```bash
# Allow HTTP, HTTPS, SSH
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

---

## 🧪 Verification Tests

### 1. Health Check
```bash
curl http://YOUR_VPS_IP/health
# Expected: {"status":"ok"}
```

### 2. Simple API Test
```bash
curl -X POST http://YOUR_VPS_IP/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "VPS-TEST-001",
    "complaint": "I sent 5000 taka to wrong number +8801712345678",
    "transaction_history": [{
      "transaction_id": "TXN-001",
      "timestamp": "2026-04-14T14:10:00Z",
      "type": "transfer",
      "amount": 5000,
      "counterparty": "+8801712345678",
      "status": "completed"
    }]
  }'

# Should return JSON with:
# - case_type: "wrong_transfer"
# - evidence_verdict: "consistent"
# - department: "dispute_resolution"
# - customer_reply: English text with safety warnings
```

### 3. Bangla Test
```bash
curl -X POST http://YOUR_VPS_IP/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "VPS-TEST-002",
    "complaint": "আমি ভুল নম্বরে টাকা পাঠিয়েছি",
    "language": "bn",
    "transaction_history": []
  }'

# Should return Bangla response
```

### 4. Load Test (Optional)
```bash
# Install apache bench
sudo apt install apache2-utils

# Test 100 requests, 10 concurrent
ab -n 100 -c 10 -p test_payload.json -T application/json http://YOUR_VPS_IP/analyze-ticket

# Expected: ~10-20 req/sec
```

---

## 📊 Monitoring Commands

### Check Service Status
```bash
# Systemd
sudo systemctl status queuestorm

# PM2
pm2 status
pm2 logs queuestorm

# Screen
screen -ls
screen -r queuestorm
```

### View Logs
```bash
# Systemd
sudo journalctl -u queuestorm -f

# PM2
pm2 logs queuestorm --lines 100

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Check Resource Usage
```bash
# CPU and memory
htop

# Disk space
df -h

# Network
netstat -tulpn | grep 8000
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 already in use
```bash
# Find and kill process
sudo lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8080
```

### Issue: Import errors
```bash
# Ensure venv is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "No LLM provider configuration found"
```bash
# Check .env exists
ls -la .env

# Check LLM_PROVIDERS is set
cat .env | grep LLM_PROVIDERS

# Test loading
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('LLM_PROVIDERS'))"
```

### Issue: Slow responses
```bash
# Check LLM API latency
curl -w "@curl-format.txt" -X POST http://localhost:8000/analyze-ticket ...

# Check system resources
top
free -h
```

### Issue: 502 Bad Gateway (Nginx)
```bash
# Check if app is running
curl http://localhost:8000/health

# Check nginx config
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## 📦 Files to Check After Deployment

```bash
# Verify all files are present
ls -la
# Should see: app/, tests/, .env, requirements.txt, etc.

# Check Python version
python3 --version
# Need: 3.9+

# Check dependencies installed
pip list | grep -E "fastapi|uvicorn|openai|httpx"

# Run validation
python3 final_validation.py
```

---

## 🎯 Success Criteria

- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] API test returns valid JSON response
- [ ] Response time < 5 seconds
- [ ] Bangla test returns Bangla reply
- [ ] Unit tests pass (37/37)
- [ ] Service auto-restarts on failure
- [ ] Logs are accessible
- [ ] Firewall configured
- [ ] (Optional) Nginx reverse proxy working
- [ ] (Optional) SSL certificate installed

---

## 📞 Support Resources

1. **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
2. **RELEASE_NOTES.md** - Full feature list and known issues
3. **TEST_CASES_ANALYSIS_REPORT.md** - Test results and analysis
4. **README.md** - Project overview and API documentation

---

## 🚀 Ready to Deploy!

Your code is on GitHub:
https://github.com/TahsinArafat/SUST_Hackathon_2026_Preli

**Quick Start:**
```bash
git clone https://github.com/TahsinArafat/SUST_Hackathon_2026_Preli.git
cd SUST_Hackathon_2026_Preli
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Good luck! 🎉
