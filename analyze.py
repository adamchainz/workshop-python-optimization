"""
Analyze a web server access log in the Combined Log Format.

Usage: python analyze.py access.log
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime

LINE_PATTERN = (
    r"(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "
    r'"(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) (?P<size>\d+|-) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

BROWSERS = [
    ("Googlebot", "Googlebot"),
    ("curl", "curl/"),
    ("Firefox", "Firefox/"),
    ("Chrome", "Chrome/"),
    ("Safari", "Safari/"),
]


@dataclass
class Request:
    ip: str
    timestamp: datetime
    method: str
    path: str
    status: int
    size: int
    referrer: str
    user_agent: str


def main(argv: list[str]) -> None:
    filename = argv[0] if argv else "access.log"
    bot_ips = load_bot_ips("bots.txt")

    requests = []
    with open(filename) as f:
        for line in f:
            request = parse_line(line)
            if request is not None:
                requests.append(request)

    report(requests, bot_ips)


def load_bot_ips(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f]


def parse_line(line: str) -> Request | None:
    match = re.match(LINE_PATTERN, line)
    if match is None:
        return None
    return Request(
        ip=match["ip"],
        timestamp=parse_timestamp(match["timestamp"]),
        method=match["method"],
        path=match["path"],
        status=int(match["status"]),
        size=0 if match["size"] == "-" else int(match["size"]),
        referrer=match["referrer"],
        user_agent=match["user_agent"],
    )


def parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%d/%b/%Y:%H:%M:%S %z")


def is_bot(request: Request, bot_ips: list[str]) -> bool:
    return request.ip in bot_ips


def browser_name(user_agent: str) -> str:
    for name, marker in BROWSERS:
        if marker in user_agent:
            return name
    return "Other"


def report(requests: list[Request], bot_ips: list[str]) -> None:
    print(f"Requests: {len(requests):,}")

    human_requests = [r for r in requests if not is_bot(r, bot_ips)]
    print(f"Human requests: {len(human_requests):,}")

    total_bytes = sum(r.size for r in human_requests)
    print(f"Human bytes served: {total_bytes / 1_000_000:,.1f} MB")

    print("\nStatus codes:")
    for status, count in sorted(Counter(r.status for r in human_requests).items()):
        print(f"  {status}: {count:,}")

    print("\nTop paths:")
    for path, count in Counter(r.path for r in human_requests).most_common(5):
        print(f"  {count:6,} {path}")

    print("\nBrowsers:")
    browsers = Counter(browser_name(r.user_agent) for r in human_requests)
    for name, count in browsers.most_common():
        print(f"  {count:6,} {name}")

    print("\nBusiest hours:")
    hours = Counter(r.timestamp.strftime("%Y-%m-%d %H:00") for r in human_requests)
    for hour, count in hours.most_common(3):
        print(f"  {count:6,} {hour}")


if __name__ == "__main__":
    main(sys.argv[1:])
