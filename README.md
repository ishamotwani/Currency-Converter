# FXChange — Live Currency Converter

A production-ready Python/Flask currency converter using **real-time exchange rates** from the free [open.er-api.com](https://open.er-api.com) API — **no API key or signup required**.

---

## Features

- 🌍 50+ currencies with live rates
- ⚡ Real-time conversion (rates update every 24h from the API)
- 🔁 Swap currencies with one click
- 📊 Live rates table for any base currency
- ⌨️ Quick-pair shortcuts (USD/EUR, USD/GBP, etc.)
- 📱 Fully responsive design
- 🐳 Docker-ready
- ☁️ Deploy to Render, Railway, or Heroku in minutes

---

## Project Structure

```
currency-converter/
├── app.py              # Flask backend + API routes
├── requirements.txt    # Python dependencies
├── Procfile            # For Heroku/Railway
├── Dockerfile          # Container deployment
├── render.yaml         # Render.com config
├── .gitignore
└── templates/
    └── index.html      # Frontend UI
```

---

## Running Locally — Step by Step

### Prerequisites
- Python 3.9 or higher installed
- `pip` available

---

### Step 1 — Clone / download the project

```bash
git clone <your-repo-url>
cd currency-converter
```

Or just place all files into a folder called `currency-converter`.

---

### Step 2 — Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt.

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Run the app

```bash
python app.py
```

You'll see:
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

Open your browser at **http://localhost:5000** — that's it! 🎉

---

### Optional: Run with Gunicorn (production-like locally)

```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

---

## Deploying to the Cloud

### Option A — Render.com (Recommended — Free tier available)

1. Push your project to a GitHub repo
2. Go to [render.com](https://render.com) and sign up (free)
3. Click **New → Web Service**
4. Connect your GitHub repo
5. Render auto-detects `render.yaml` — click **Deploy**
6. Your app will be live at `https://fxchange.onrender.com` (or similar)

> ✅ Free tier spins down after inactivity — first request may be slow.

---

### Option B — Railway.app (Free $5/month credit)

1. Push to GitHub
2. Go to [railway.app](https://railway.app) and sign in with GitHub
3. Click **New Project → Deploy from GitHub Repo**
4. Select your repo — Railway detects the `Procfile` automatically
5. Click **Deploy** — live in ~2 minutes

---

### Option C — Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login and create app:
```bash
heroku login
heroku create your-app-name
```
3. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```
4. Open:
```bash
heroku open
```

---

### Option D — Docker (any cloud or VPS)

```bash
# Build the image
docker build -t fxchange .

# Run locally
docker run -p 5000:5000 fxchange

# Run on a server (detached)
docker run -d -p 80:5000 --restart=always fxchange
```

Deploy the image to:
- **AWS ECS / App Runner**
- **Google Cloud Run** (`gcloud run deploy`)
- **DigitalOcean App Platform**
- **Any VPS** with Docker installed

---

### Option E — VPS (Ubuntu/Debian server)

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install Python & pip
sudo apt update && sudo apt install python3 python3-pip python3-venv -y

# 3. Upload project files (or git clone)
git clone <your-repo-url>
cd currency-converter

# 4. Setup venv + install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run with gunicorn (background)
nohup gunicorn app:app --bind 0.0.0.0:5000 --workers 2 &

# 6. (Optional) Set up Nginx as reverse proxy on port 80
sudo apt install nginx -y
# Configure /etc/nginx/sites-available/fxchange to proxy to localhost:5000
```

---

## API Reference

The app exposes two JSON endpoints you can call directly:

### `GET /api/convert`
| Param | Description | Example |
|-------|-------------|---------|
| `from` | Source currency code | `USD` |
| `to` | Target currency code | `EUR` |
| `amount` | Amount to convert | `100` |

```bash
curl "http://localhost:5000/api/convert?from=USD&to=EUR&amount=100"
```

### `GET /api/rates`
Returns all supported rates for a base currency.

| Param | Description | Default |
|-------|-------------|---------|
| `base` | Base currency | `USD` |

```bash
curl "http://localhost:5000/api/rates?base=GBP"
```

---

## About the Exchange Rate API

- **Provider**: [ExchangeRate-API Open Endpoint](https://open.er-api.com)
- **Cost**: Free — no API key required
- **Update frequency**: Every 24 hours
- **Endpoint**: `https://open.er-api.com/v6/latest/{BASE}`
- **Rate limit**: Generous free tier, suitable for personal/small projects

For higher update frequency or commercial use, consider [ExchangeRate-API Pro](https://www.exchangerate-api.com) (paid tiers available).

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Port to listen on |
| `FLASK_ENV` | `production` | Set to `development` for debug mode |

---

## License

MIT — free to use, modify, and deploy.
