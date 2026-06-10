# 🤖 Daily Task Bot

> A zero-cost Python automation bot that runs **3 tasks daily** and sends a beautiful HTML email report — fully automated via **GitHub Actions** (no server required).

**Author:** Goutham BS · CSE 2024–2028 · Muttathara Engineering College, Thiruvananthapuram  
**GitHub:** [@gout-ham24](https://github.com/gout-ham24)  
**Portfolio:** [gouthambs-portfolio.netlify.app](https://gouthambs-portfolio.netlify.app)

---

## ✨ Features

| Task | Level | Description |
|------|-------|-------------|
| Weather Fetcher | 🥉 Bronze | Live weather for Thiruvananthapuram via OpenWeatherMap API |
| News Headlines | 🥈 Silver | Top 10 India headlines + keyword trend extraction via NewsAPI |
| Portfolio Updater | 🥇 Gold | Fetches live GitHub stats and triggers Netlify portfolio rebuild daily |

- **Runs automatically** at 7:00 AM, 9:00 PM, 10:00 PM IST every day
- **Sends one clean HTML email** per run — Apple/Google minimal style
- **100% free** — GitHub Actions free tier + free API keys
- **Zero dependencies on external servers** — everything runs in the cloud

---

## 📁 Project Structure

```
daily-task-bot/
├── bot.py               # Entry point — orchestrates all 3 tasks
├── weather_task.py      # 🥉 Bronze: OpenWeatherMap API
├── news_task.py         # 🥈 Silver: NewsAPI headlines + trend extraction
├── portfolio_task.py    # 🥇 Gold: GitHub API stats + Netlify rebuild
├── email_sender.py      # HTML email builder & Gmail SMTP sender
├── requirements.txt     # Python dependencies (requests only)
├── .gitignore
└── .github/
    └── workflows/
        └── daily.yml    # GitHub Actions — runs 3x daily
```

---

## 🔐 GitHub Secrets Required

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Description |
|--------|-------------|
| `WEATHER_API_KEY` | OpenWeatherMap API key |
| `NEWS_API_KEY` | NewsAPI.org free API key |
| `FROM_EMAIL` | Gmail address the bot sends from |
| `APP_PASSWORD` | 16-digit Gmail App Password (not your main password) |
| `TO_EMAIL` | Email address to receive the daily report |

> **Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions — no need to set it manually.

---

## 🚀 Setup Guide

### 1. Clone & push to GitHub
```bash
git clone https://github.com/gout-ham24/daily-task-bot.git
cd daily-task-bot
# (or create new repo and push these files)
```

### 2. Get free API keys
- **OpenWeatherMap:** [openweathermap.org/api](https://openweathermap.org/api) → Free plan → API key
- **NewsAPI:** [newsapi.org/register](https://newsapi.org/register) → Free developer key

### 3. Generate Gmail App Password
1. Enable 2-Step Verification on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Select "Mail" → "Other (custom name)" → Generate
4. Copy the 16-digit password

### 4. Add all secrets to GitHub repo

(See table above)

### 5. Trigger a test run
Go to **Actions → Daily Task Bot → Run workflow** to test manually.

---

## 📧 Email Report Preview

The bot sends a single clean HTML email with:
- 🌤 Current weather card (temp, humidity, wind, sunrise/sunset)
- 📰 Top India headlines with trending keyword badges
- 📊 GitHub stats (repos, followers, top repos, language breakdown)
- 🔗 Link to live portfolio

---

## 🛠 Tech Stack

- **Python 3.11** — core language
- **requests** — HTTP calls to APIs
- **smtplib + email** — Gmail SMTP (standard library, no extra deps)
- **GitHub Actions** — free CI/CD for scheduled automation
- **Netlify** — portfolio hosting with build hooks

---

## 📄 License

MIT — free to use and modify.
