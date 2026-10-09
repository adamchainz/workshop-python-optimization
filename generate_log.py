"""
Generate a fake web server access log, in the Combined Log Format, for
analyze.py to read.

Usage: python generate_log.py [number_of_lines]
"""

from __future__ import annotations

import random
import sys
from datetime import UTC, datetime, timedelta

PATHS = [
    "/",
    "/about/",
    "/blog/",
    "/contact/",
    "/favicon.ico",
    "/robots.txt",
    "/static/app.css",
    "/static/app.js",
    "/static/logo.png",
    *(
        f"/blog/{year}/post-{number}/"
        for year in range(2015, 2026)
        for number in range(40)
    ),
]
STATUSES = [200] * 90 + [301] * 3 + [304] * 4 + [404] * 2 + [500]
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "curl/8.7.1",
]
REFERRERS = [
    "-",
    "https://www.google.com/",
    "https://duckduckgo.com/",
    "https://example.com/",
]


def main(argv: list[str]) -> None:
    count = int(argv[0]) if argv else 100_000
    rng = random.Random(42)

    ips = [
        f"{rng.randint(1, 223)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}"
        for _ in range(5_000)
    ]
    bot_ips = rng.sample(ips, 500)
    with open("bots.txt", "w") as f:
        for ip in bot_ips:
            f.write(ip + "\n")

    timestamp = datetime(2025, 10, 1, tzinfo=UTC)
    with open("access.log", "w") as f:
        for _ in range(count):
            timestamp += timedelta(seconds=rng.choice([0, 0, 0, 0, 0, 0, 0, 1]))
            ip = rng.choice(ips)
            path = rng.choice(PATHS)
            status = rng.choice(STATUSES)
            size = "-" if status == 304 else str(rng.randint(200, 50_000))
            f.write(
                f"{ip} - - [{timestamp:%d/%b/%Y:%H:%M:%S %z}] "
                f'"GET {path} HTTP/1.1" {status} {size} '
                f'"{rng.choice(REFERRERS)}" "{rng.choice(USER_AGENTS)}"\n'
            )
    print(f"Wrote {count:,} lines to access.log, and {len(bot_ips)} IPs to bots.txt.")


if __name__ == "__main__":
    main(sys.argv[1:])
