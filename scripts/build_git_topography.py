#!/usr/bin/env python3
"""Build a custom isometric Git contribution terrain for the DT-09 profile."""
import json
import os
import urllib.request
from datetime import datetime, timezone

USER = "DT-09"
TOKEN = os.environ["GITHUB_TOKEN"]
QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def fetch_calendar():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "User-Agent": "DT-09-git-topography",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode())
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(calendar):
    weeks = calendar["weeks"][-53:]
    days = [day for week in weeks for day in week["contributionDays"]]
    maximum = max((d["contributionCount"] for d in days), default=1) or 1
    total = calendar["totalContributions"]
    # Isometric cell geometry: week axis moves right/down; weekday axis left/down.
    ox, oy = 225, 125
    sx, sy = 15.2, 8.0
    cw, ch = 11.5, 6.5
    parts = []
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week["contributionDays"]):
            count = day["contributionCount"]
            x = ox + wi * sx - di * sy
            y = oy + wi * 4.0 + di * 7.5
            height = 2.5 + (count / maximum) * 30 if count else 1.5
            # A warm, restrained scale: stone -> bronze -> champagne.
            if count == 0:
                top, left, right = "#302422", "#171312", "#241B1A"
            elif count / maximum < .25:
                top, left, right = "#71615C", "#3B302E", "#574440"
            elif count / maximum < .55:
                top, left, right = "#A18F82", "#65554F", "#817167"
            elif count / maximum < .8:
                top, left, right = "#C6B69E", "#84766B", "#A79783"
            else:
                top, left, right = "#EEE6D8", "#A89A8A", "#C9BCA9"
            a = (x, y - height)
            b = (x + cw, y - height + ch * .5)
            c = (x, y - height + ch)
            d = (x - cw, y - height + ch * .5)
            # Extruded front and right faces.
            front = f"{d[0]},{d[1]} {c[0]},{c[1]} {c[0]},{c[1]+height} {d[0]},{d[1]+height}"
            side = f"{c[0]},{c[1]} {b[0]},{b[1]} {b[0]},{b[1]+height} {c[0]},{c[1]+height}"
            top_poly = f"{a[0]},{a[1]} {b[0]},{b[1]} {c[0]},{c[1]} {d[0]},{d[1]}"
            title = f'{day["date"]}: {count} contributions'
            parts.append(
                f'<g><title>{esc(title)}</title>'
                f'<polygon points="{front}" fill="{left}" opacity=".96"/>'
                f'<polygon points="{side}" fill="{right}" opacity=".98"/>'
                f'<polygon points="{top_poly}" fill="{top}" stroke="#E2D2BB" stroke-opacity=".28" stroke-width=".45"/>'
                f'</g>'
            )
    # Isometric base grid and month labels.
    grid = []
    for i in range(0, 54, 4):
        x = ox + i * sx
        y = oy + i * 4
        grid.append(f'<path d="M{x-65:.1f} {y+62:.1f} l-50 42" stroke="#887D75" stroke-opacity=".16"/>')
    month_labels = []
    last_month = None
    for wi, week in enumerate(weeks):
        if not week["contributionDays"]:
            continue
        date = week["contributionDays"][0]["date"]
        month = date[5:7]
        if month != last_month:
            x = ox + wi * sx - 35
            y = oy + wi * 4 - 26
            label = datetime.strptime(month, "%m").strftime("%b").upper()
            month_labels.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="#B9AA99" font-size="10" font-family="monospace" letter-spacing="1.4">{label}</text>')
            last_month = month
    refreshed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 590" role="img" aria-labelledby="title desc">
<title id="title">DT-09 Git contribution topography</title>
<desc id="desc">A custom isometric terrain built from the public GitHub contribution calendar. Taller blocks indicate more contributions on that day. Total in the displayed calendar: {total}.</desc>
<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#211B1A"/><stop offset=".55" stop-color="#0D0B0A"/><stop offset="1" stop-color="#2C2220"/></linearGradient>
 <radialGradient id="glow"><stop stop-color="#8F6B63" stop-opacity=".18"/><stop offset="1" stop-color="#8F6B63" stop-opacity="0"/></radialGradient>
 <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dy="7"/><feComponentTransfer><feFuncA type="linear" slope=".42"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <style>.scan{{stroke-dasharray:3 12;animation:sweep 24s linear infinite}}@keyframes sweep{{to{{stroke-dashoffset:-300}}}}@media(prefers-reduced-motion:reduce){{.scan{{animation:none}}}}</style>
</defs>
<rect width="1200" height="590" rx="16" fill="url(#bg)"/>
<ellipse cx="630" cy="310" rx="560" ry="290" fill="url(#glow)"/>
<path d="M25 24H1175M25 566H1175" stroke="#CDBDA8" stroke-opacity=".35"/>
<text x="42" y="58" fill="#D9C8AD" font-family="monospace" font-size="12" letter-spacing="3">GIT TOPOGRAPHY / CONTRIBUTION TERRAIN</text>
<text x="42" y="88" fill="#F3EEE5" font-family="Arial,sans-serif" font-size="22" font-weight="700">A year of building, mapped in elevation.</text>
<text x="1155" y="59" fill="#E3D2B5" font-family="monospace" font-size="18" text-anchor="end">{total:,}</text>
<text x="1155" y="78" fill="#AFA398" font-family="monospace" font-size="9" letter-spacing="1.5" text-anchor="end">CONTRIBUTIONS</text>
<g>{''.join(grid)}</g>
<g filter="url(#shadow)">{"".join(parts)}</g>
<g>{''.join(month_labels)}</g>
<path class="scan" d="M150 520L1080 520" stroke="#CDBDA8" stroke-opacity=".5"/>
<text x="42" y="548" fill="#AFA398" font-family="monospace" font-size="10" letter-spacing="1.2">HEIGHT = DAILY CONTRIBUTION VOLUME · SOURCE: GITHUB CONTRIBUTION CALENDAR</text>
<text x="1155" y="548" fill="#9B8E82" font-family="monospace" font-size="9" text-anchor="end">{refreshed}</text>
</svg>'''


if __name__ == "__main__":
    calendar = fetch_calendar()
    os.makedirs("assets", exist_ok=True)
    with open("assets/git-topography.svg", "w", encoding="utf-8") as output:
        output.write(build_svg(calendar))
