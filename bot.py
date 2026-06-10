"""
Daily Task Bot - Entry Point
Author: Goutham BS | CSE 2024-2028 | Muttathara Engineering College
GitHub: gout-ham24
"""

import os
import sys
import datetime
from weather_task import get_weather_data
from news_task import get_news_data
from portfolio_task import update_portfolio
from email_sender import send_report


def main():
    print("=" * 60)
    print(f"  Daily Task Bot — {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print("  Author: Goutham BS | gout-ham24")
    print("=" * 60)

    results = {}

    # ── BRONZE: Weather ──────────────────────────────────────────
    print("\n[1/3] 🥉 BRONZE — Fetching weather...")
    try:
        results["weather"] = get_weather_data()
        print("      ✅ Weather task complete.")
    except Exception as e:
        results["weather"] = {"error": str(e)}
        print(f"      ❌ Weather task failed: {e}")

    # ── SILVER: News ─────────────────────────────────────────────
    print("\n[2/3] 🥈 SILVER — Fetching news headlines...")
    try:
        results["news"] = get_news_data()
        print("      ✅ News task complete.")
    except Exception as e:
        results["news"] = {"error": str(e)}
        print(f"      ❌ News task failed: {e}")

    # ── GOLD: Portfolio Updater ───────────────────────────────────
    print("\n[3/3] 🥇 GOLD — Updating portfolio via GitHub + Netlify...")
    try:
        results["portfolio"] = update_portfolio()
        print("      ✅ Portfolio task complete.")
    except Exception as e:
        results["portfolio"] = {"error": str(e)}
        print(f"      ❌ Portfolio task failed: {e}")

    # ── Send Email Report ─────────────────────────────────────────
    print("\n[📧] Sending HTML email report...")
    try:
        send_report(results)
        print("      ✅ Email sent successfully.")
    except Exception as e:
        print(f"      ❌ Email send failed: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  All tasks complete. Bot run finished.")
    print("=" * 60)


if __name__ == "__main__":
    main()
