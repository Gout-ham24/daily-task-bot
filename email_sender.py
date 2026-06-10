"""
Email Sender — Minimal Apple/Google-style HTML report
Sends the daily bot results as a single beautiful HTML email.
"""

import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ── HTML Template ────────────────────────────────────────────────────────────

def build_html(results: dict) -> str:
    now = datetime.datetime.now().strftime("%A, %d %B %Y — %I:%M %p IST")

    # ── Weather section ──────────────────────────────────────────
    w = results.get("weather", {})
    if "error" in w:
        weather_html = f'<p class="error">⚠️ Weather fetch failed: {w["error"]}</p>'
    else:
        weather_html = f"""
        <div class="card">
          <div class="card-header bronze">🥉 Weather — {w.get('city', '')}, {w.get('country', '')}</div>
          <div class="stats-grid">
            <div class="stat">
              <span class="stat-value">{w.get('temp', '—')}°C</span>
              <span class="stat-label">Temperature</span>
            </div>
            <div class="stat">
              <span class="stat-value">{w.get('feels_like', '—')}°C</span>
              <span class="stat-label">Feels Like</span>
            </div>
            <div class="stat">
              <span class="stat-value">{w.get('humidity', '—')}%</span>
              <span class="stat-label">Humidity</span>
            </div>
            <div class="stat">
              <span class="stat-value">{w.get('wind_speed', '—')} km/h</span>
              <span class="stat-label">Wind Speed</span>
            </div>
          </div>
          <p class="sub">{w.get('description', '')} &nbsp;·&nbsp; Visibility: {w.get('visibility', '—')} km
            &nbsp;·&nbsp; 🌅 {w.get('sunrise', '—')} &nbsp; 🌇 {w.get('sunset', '—')}</p>
        </div>
        """

    # ── News section ─────────────────────────────────────────────
    n = results.get("news", {})
    if "error" in n:
        news_html = f'<p class="error">⚠️ News fetch failed: {n["error"]}</p>'
    else:
        headlines = n.get("headlines", [])
        trend_badges = "".join(
            f'<span class="badge">{t}</span>' for t in n.get("trends", [])
        )
        headline_rows = "".join(
            f'<li><a href="{h["url"]}" style="color:#1a73e8;text-decoration:none;">{h["title"]}</a>'
            f' <span class="src">— {h["source"]}</span></li>'
            for h in headlines[:8]
        )
        news_html = f"""
        <div class="card">
          <div class="card-header silver">🥈 Top India Headlines</div>
          <div class="trends">Trending: {trend_badges}</div>
          <ul class="headlines">{headline_rows}</ul>
          <p class="sub">Fetched {n.get('total', 0)} headlines · {n.get('fetched_at', '')}</p>
        </div>
        """

    # ── Portfolio section ────────────────────────────────────────
    p = results.get("portfolio", {})
    if "error" in p:
        portfolio_html = f'<p class="error">⚠️ Portfolio update failed: {p["error"]}</p>'
    else:
        gh = p.get("github", {})
        rebuild_status = "✅ Rebuild triggered" if p.get("netlify_rebuild_triggered") else "⚠️ Rebuild skipped"

        lang_pills = "".join(
            f'<span class="badge lang">{lang} <b>{count}</b></span>'
            for lang, count in sorted(gh.get("languages", {}).items(), key=lambda x: -x[1])
        )

        repo_rows = "".join(
            f'<tr><td><a href="{r["url"]}" style="color:#1a73e8;text-decoration:none;">{r["name"]}</a></td>'
            f'<td>{r["language"]}</td><td>⭐ {r["stars"]}</td><td>{r["updated"]}</td></tr>'
            for r in gh.get("top_repos", [])
        )

        portfolio_html = f"""
        <div class="card">
          <div class="card-header gold">🥇 Portfolio — GitHub Stats</div>
          <div class="stats-grid">
            <div class="stat">
              <span class="stat-value">{gh.get('public_repos', 0)}</span>
              <span class="stat-label">Repositories</span>
            </div>
            <div class="stat">
              <span class="stat-value">{gh.get('followers', 0)}</span>
              <span class="stat-label">Followers</span>
            </div>
            <div class="stat">
              <span class="stat-value">{gh.get('following', 0)}</span>
              <span class="stat-label">Following</span>
            </div>
          </div>
          <div class="trends">Languages: {lang_pills}</div>
          <table class="repo-table">
            <thead><tr><th>Repo</th><th>Language</th><th>Stars</th><th>Updated</th></tr></thead>
            <tbody>{repo_rows}</tbody>
          </table>
          <p class="sub">{rebuild_status} &nbsp;·&nbsp;
            <a href="{p.get('portfolio_url','#')}" style="color:#1a73e8;">View Portfolio →</a>
            &nbsp;·&nbsp; {p.get('updated_at','')}</p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Daily Task Bot Report</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
        background:#f5f5f7;color:#1d1d1f;font-size:15px;line-height:1.6}}
  .wrapper{{max-width:640px;margin:32px auto;padding:0 16px}}
  .header{{background:#fff;border-radius:18px 18px 0 0;padding:32px 32px 24px;
           border-bottom:1px solid #e5e5ea;text-align:center}}
  .header h1{{font-size:22px;font-weight:700;letter-spacing:-0.3px}}
  .header .date{{color:#6e6e73;font-size:13px;margin-top:4px}}
  .card{{background:#fff;padding:24px 28px;margin-top:2px}}
  .card:last-of-type{{border-radius:0 0 18px 18px}}
  .card-header{{font-size:13px;font-weight:600;text-transform:uppercase;
                letter-spacing:.6px;padding:4px 10px;border-radius:6px;
                display:inline-block;margin-bottom:14px}}
  .bronze{{background:#fff3e0;color:#e65100}}
  .silver{{background:#f3f3f3;color:#424242}}
  .gold{{background:#fffde7;color:#f57f17}}
  .stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));
               gap:12px;margin-bottom:14px}}
  .stat{{background:#f5f5f7;border-radius:12px;padding:14px;text-align:center}}
  .stat-value{{display:block;font-size:22px;font-weight:700}}
  .stat-label{{display:block;font-size:11px;color:#6e6e73;margin-top:2px;text-transform:uppercase;letter-spacing:.4px}}
  .sub{{color:#6e6e73;font-size:12px;margin-top:12px}}
  .trends{{margin-bottom:12px}}
  .badge{{display:inline-block;background:#e8f0fe;color:#1a73e8;
          border-radius:20px;padding:3px 10px;font-size:12px;font-weight:500;margin:2px 3px 2px 0}}
  .badge.lang{{background:#e8f5e9;color:#2e7d32}}
  .headlines{{padding-left:18px;margin:8px 0}}
  .headlines li{{margin-bottom:7px;font-size:13.5px}}
  .src{{color:#8e8e93;font-size:11.5px}}
  .repo-table{{width:100%;border-collapse:collapse;font-size:13px;margin-top:10px}}
  .repo-table th{{text-align:left;color:#6e6e73;font-weight:500;
                  padding:6px 8px;border-bottom:1px solid #e5e5ea;font-size:11px;text-transform:uppercase;letter-spacing:.4px}}
  .repo-table td{{padding:8px 8px;border-bottom:1px solid #f2f2f7}}
  .footer{{text-align:center;padding:20px;color:#8e8e93;font-size:12px}}
  .error{{color:#c0392b;background:#fdf2f2;padding:10px 14px;border-radius:8px;font-size:13px}}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h1>Daily Task Bot Report</h1>
    <div class="date">{now}</div>
    <div class="date" style="margin-top:2px">Goutham BS · gout-ham24 · Muttathara Engineering College</div>
  </div>
  {weather_html}
  {news_html}
  {portfolio_html}
  <div class="footer">
    Generated automatically by Daily Task Bot · GitHub Actions<br/>
    <a href="https://github.com/gout-ham24/daily-task-bot" style="color:#1a73e8;text-decoration:none;">
      github.com/gout-ham24/daily-task-bot
    </a>
  </div>
</div>
</body>
</html>"""


# ── Send via Gmail SMTP ──────────────────────────────────────────────────────

def send_report(results: dict) -> None:
    from_email = os.environ["FROM_EMAIL"]
    app_password = os.environ["APP_PASSWORD"]
    to_email = os.environ["TO_EMAIL"]

    subject = (
        f"🤖 Daily Task Bot — "
        f"{datetime.datetime.now().strftime('%d %b %Y, %I:%M %p IST')}"
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Daily Task Bot <{from_email}>"
    msg["To"] = to_email

    html_content = build_html(results)
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())
