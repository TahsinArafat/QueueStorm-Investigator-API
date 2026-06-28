# VPS Deployment Checklist

## Quick Deployment

### 1. Clone and Setup

```bash
ssh user@your-vps-ip
git clone https://github.com/TahsinArafat/QueueStorm-Investigator-API.git
cd SUST_Hackathon_2026_Preli
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
nano .env
```

Add your API keys:
```bash
LLM_PROVIDERS='[{"name":"provider-1","api_key":"gsk_YOUR_KEY_HERE","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15}]'
```

### 3. Test

```bash
pytest tests/ -v
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In another terminal:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### 4. Production Deployment

Option A: Systemd (recommended)
```bash
sudo nano /etc/systemd/system/queuestorm.service
```

```ini
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

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable queuestorm
sudo systemctl start queuestorm
```

Option B: Screen (quick)
```bash
screen -S queuestorm
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Detach: Ctrl+A, then D
# Reattach: screen -r queuestorm
```

### 5. Nginx (optional)

```bash
sudo apt update && sudo apt install nginx
sudo nano /etc/nginx/sites-available/queuestorm
```

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/queuestorm /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 6. Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Verification

```bash
# Health check
curl http://YOUR_VPS_IP/health

# API test
curl -X POST http://YOUR_VPS_IP/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "VPS-TEST-001",
    "complaint": "I sent 5000 taka to wrong number",
    "transaction_history": [{
      "transaction_id": "TXN-001",
      "timestamp": "2026-04-14T14:10:00Z",
      "type": "transfer",
      "amount": 5000,
      "counterparty": "+8801712345678",
      "status": "completed"
    }]
  }'
```

## Troubleshooting

Port in use:
```bash
sudo lsof -ti:8000 | xargs kill -9
```

Import errors:
```bash
source .venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

No LLM provider:
```bash
cat .env | grep LLM_PROVIDERS
```

Logs:
```bash
# Systemd
sudo journalctl -u queuestorm -f

# PM2
pm2 logs queuestorm

# Nginx
sudo tail -f /var/log/nginx/error.log
```

## Success Criteria

- Health endpoint returns `{"status":"ok"}`
- API returns valid JSON response
- Response time < 5 seconds
- Unit tests pass (37/37)
- Service auto-restarts on failure
