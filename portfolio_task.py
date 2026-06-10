"""
GOLD Task — Portfolio Auto-Updater
Fetches live GitHub stats for gout-ham24 and triggers a Netlify rebuild
so the portfolio always shows up-to-date data.
"""

import os
import datetime
import requests


GITHUB_USER = "gout-ham24"
NETLIFY_BUILD_HOOK = "https://api.netlify.com/build_hooks/6a2991a2e261f09dc35df619"


def fetch_github_stats(token: str | None = None) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # ── Repos ────────────────────────────────────────────────────
    repos_resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}/repos",
        headers=headers,
        params={"per_page": 100, "sort": "updated"},
        timeout=10,
    )
    repos_resp.raise_for_status()
    repos = repos_resp.json()

    public_repos = [r for r in repos if not r.get("fork", False)]

    # Language breakdown
    lang_counts: dict[str, int] = {}
    for repo in public_repos:
        lang = repo.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

    # Top repos by stars
    top_repos = sorted(public_repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:5]
    top_repos_clean = [
        {
            "name": r["name"],
            "description": r.get("description") or "No description",
            "stars": r.get("stargazers_count", 0),
            "language": r.get("language") or "N/A",
            "url": r.get("html_url", "#"),
            "updated": r.get("updated_at", "")[:10],
        }
        for r in top_repos
    ]

    # ── User profile ─────────────────────────────────────────────
    user_resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}",
        headers=headers,
        timeout=10,
    )
    user_resp.raise_for_status()
    user = user_resp.json()

    return {
        "username": GITHUB_USER,
        "name": user.get("name") or GITHUB_USER,
        "public_repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "languages": lang_counts,
        "top_repos": top_repos_clean,
        "profile_url": f"https://github.com/{GITHUB_USER}",
        "avatar_url": user.get("avatar_url", ""),
    }


def trigger_netlify_rebuild() -> bool:
    resp = requests.post(NETLIFY_BUILD_HOOK, timeout=10)
    return resp.status_code in (200, 201, 202)


def update_portfolio() -> dict:
    github_token = os.getenv("GITHUB_TOKEN")   # optional — raises rate limit to 5000/hr
    stats = fetch_github_stats(token=github_token)

    rebuilt = trigger_netlify_rebuild()

    return {
        "github": stats,
        "netlify_rebuild_triggered": rebuilt,
        "portfolio_url": "https://gouthambs-portfolio.netlify.app",
        "updated_at": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p IST"),
    }
