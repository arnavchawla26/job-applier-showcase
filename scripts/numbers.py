"""The exact query behind the numbers in README.md.

Usage:  python3 -I scripts/numbers.py /path/to/applier_tracker.csv [--from 2026-10-06 --to 2026-10-12]

The tracker CSV is the spreadsheet copy the app rewrites on every change (columns: updated_at, status,
company, title, location, url, detail, resume_pdf). It is not in this repo: it holds the real companies the
owner applied to. Only this query and its output are published.
"""
from __future__ import annotations

import argparse
import collections
import csv
import urllib.parse

ATS_HOSTS = [("greenhouse", "Greenhouse"), ("ashbyhq", "Ashby"), ("lever.co", "Lever"), ("myworkday", "Workday"),
             ("smartrecruiters", "SmartRecruiters"), ("workable", "Workable"), ("icims", "iCIMS"),
             ("taleo", "Taleo"), ("oracle", "Oracle"), ("successfactors", "SuccessFactors")]


def ats(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    return next((name for marker, name in ATS_HOSTS if marker in host), "company careers site")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--from", dest="start", default="2026-10-06")
    ap.add_argument("--to", dest="end", default="2026-10-12")
    a = ap.parse_args()
    with open(a.csv, encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if a.start <= r["updated_at"][:10] <= a.end]

    status = collections.Counter(r["status"] for r in rows)
    sub = [r for r in rows if r["status"] == "submitted"]
    confirmed = [r for r in sub if r["detail"].startswith(("confirmation page seen", "confirmation email received"))]
    pressed = status["submitted"] + status["submit_unconfirmed"] + status["blocked_by_site"]
    attempted = len(rows) - status["tailored"] - status["ready_to_submit"] - status["skipped"]

    print(f"window {a.start} .. {a.end}")
    print(f"rows                         {len(rows)}")
    print(f"distinct companies           {len({r['company'] for r in rows})}")
    print(f"rows with a tailored resume  {sum(1 for r in rows if r['resume_pdf'])}")
    print("status counts:")
    for s, n in status.most_common():
        print(f"  {s:20s} {n}")
    print(f"submitted, confirmation seen on the page or by email: {len(confirmed)}")
    print(f"submitted, other detail:     {len(sub) - len(confirmed)}  "
          f"({collections.Counter(r['detail'].split(':')[0] for r in sub if r not in confirmed).most_common()})")
    print(f"distinct companies submitted {len({r['company'] for r in sub})}")
    print(f"submit button pressed        {pressed}  (submitted + submit_unconfirmed + blocked_by_site)")
    print(f"confirmed / pressed          {len(sub)}/{pressed} = {100 * len(sub) / pressed:.0f}%")
    print(f"attempted (not dry, not skipped, not merely tailored): {attempted}; submitted / attempted = {100 * len(sub) / attempted:.0f}%")
    print("submitted by day:", sorted(collections.Counter(r["updated_at"][:10] for r in sub).items()))
    print("submitted by hiring system:", collections.Counter(ats(r["url"]) for r in sub).most_common())
    print("all rows by hiring system:  ", collections.Counter(ats(r["url"]) for r in rows).most_common())
    print("why rows were skipped:", collections.Counter(r["detail"][:40] for r in rows if r["status"] == "skipped").most_common(3))


if __name__ == "__main__":
    main()
