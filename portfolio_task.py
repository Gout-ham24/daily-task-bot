"""
GOLD Task — Portfolio Auto-Updater
Fetches GitHub repos via API → generates projects.json
→ auto-updates portfolio via Netlify build hook on every run.
"""

import os
import json
import datetime
import requests

GITHUB_USER       = "gout-ham24"
NETLIFY_BUILD_HOOK = "https://api.netlify.com/build_hooks/6a2991a2e261f09dc35df619"
PORTFOLIO_URL     = "https://gouthambs-portfolio.netlify.app"


def fetch_github_stats(token: str = None) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # User profile
    user_resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}",
        headers=headers, timeout=10
    )
    user_resp.raise_for_status()
    user = user_resp.json()

    # All repos
    repos_resp = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}/repos",
        headers=headers,
        params={"per_page": 100, "sort": "updated"},
        timeout=10,
    )
    repos_resp.raise_for_status()
    repos = [r for r in repos_resp.json() if not r.get("fork", False)]

    # Language breakdown
    lang_counts = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

    # Top repos by stars then by updated
    top_repos = sorted(repos, key=lambda r: (r.get("stargazers_count", 0), r.get("updated_at", "")), reverse=True)[:6]
    top_repos_clean = [
        {
            "name":        r["name"],
            "description": r.get("description") or "No description",
            "stars":       r.get("stargazers_count", 0),
            "forks":       r.get("forks_count", 0),
            "language":    r.get("language") or "N/A",
            "url":         r.get("html_url", "#"),
            "updated":     r.get("updated_at", "")[:10],
        }
        for r in top_repos
    ]

    return {
        "username":     GITHUB_USER,
        "name":         user.get("name") or GITHUB_USER,
        "bio":          user.get("bio") or "",
        "public_repos": user.get("public_repos", 0),
        "followers":    user.get("followers", 0),
        "following":    user.get("following", 0),
        "languages":    lang_counts,
        "top_repos":    top_repos_clean,
        "profile_url":  f"https://github.com/{GITHUB_USER}",
        "avatar_url":   user.get("avatar_url", ""),
    }


def generate_projects_json(stats: dict) -> str:
    """
    Generates a projects.json file in the repo root.
    Your portfolio JS can fetch this file to show live data.
    """
    payload = {
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "github": {
            "username":     stats["username"],
            "public_repos": stats["public_repos"],
            "followers":    stats["followers"],
            "following":    stats["following"],
            "languages":    stats["languages"],
            "profile_url":  stats["profile_url"],
            "avatar_url":   stats["avatar_url"],
        },
        "projects": stats["top_repos"],
    }
    path = "projects.json"
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"      ✅ projects.json written ({len(stats['top_repos'])} repos)")
    return path


def trigger_netlify_rebuild() -> bool:
    try:
        resp = requests.post(NETLIFY_BUILD_HOOK, timeout=10)
        success = resp.status_code in (200, 201, 202)
        if success:
            print("      ✅ Netlify rebuild triggered")
        else:
            print(f"      ⚠  Netlify rebuild returned {resp.status_code}")
        return success
    except Exception as e:
        print(f"      ⚠  Netlify rebuild failed: {e}")
        return False


def update_portfolio() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    stats = fetch_github_stats(token=token)

    generate_projects_json(stats)
    rebuilt = trigger_netlify_rebuild()

    return {
        "github":                   stats,
        "netlify_rebuild_triggered": rebuilt,
        "portfolio_url":            PORTFOLIO_URL,
        "updated_at":               datetime.datetime.now().strftime("%d %b %Y, %I:%M %p IST"),
    }
