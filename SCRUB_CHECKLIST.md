# Scrub checklist

This repository was assembled by hand from the private `job-applier` repository on 2026-10-17. Nothing was
copied wholesale except the `terms_forbid_automation` excerpt from `applier/boards.py` (no URLs, keys or personal strings in it).

## Excluded on purpose

| Item in the private repo | Why it is not here |
|---|---|
| `config.yaml`, `config.yaml.bak` | the owner's search settings, budget, consent choices, mail settings |
| `profile.yaml` | the owner's identity, address, work authorisation, EEO answers, compensation guidance |
| `tailoring_guide.md` | the owner's tailoring rules, quoting lines of the owner's resume |
| `data/` | `applications.db` and the tracker (real companies), `answer_bank.yaml` (213 KB of the owner's answers), `usage.jsonl`, `queue.json`, `browser-profiles/` (logged-in Chrome profiles), logs |
| `files/` | the owner's resume (`.tex`, PDFs) and uploaded documents |
| `.env` | API keys and app passwords (never read by any script here) |
| the tracker CSV (`Applications/applier_tracker.csv`) | 638 rows naming the companies applied to; only the query over it (`scripts/numbers.py`) and its aggregate output are published |
| `docs/LEGAL-job-boards.md` | rewritten as `docs/platform-policy.md`. The private file is written in operator voice for a product with users who pay ("our servers", an early-access list, third-party data processors, credentials held for people, a survey of competing applier companies). This project is presented as a personal agentic app, so the public copy keeps the research (how the exposure works, the per-platform verdict table, the rules the app follows, every source link) in project voice and drops the company obligations and the competitor survey entirely. No quote is longer than 15 words. |
| `presets/`, `*.example.yaml` | harmless, but not needed for the showcase |
| all application source (`applier/*.py`, `applier/cloud/*.py`, `applier/js/extract.js`, `applier/web/index.html`, `tests/`) | the product stays private; the showcase describes it instead |
| `job-applier-site/` (Next.js) | contains `.env.local`, the DMG and zip artifacts and the early-access list |
| `CLAUDE.md`, `docs/HANDOFF-*.md`, `docs/PLAN-*.md`, `docs/SETUP_OAUTH.md`, `docs/PROVIDER-meta.md`, build scripts, `Dockerfile.worker`, `fly.toml` | internal notes, OAuth setup and deployment details |

The screenshot is rendered from `assets/demo_tracker.html`, a static page with made-up company names. The stat
tiles and the by-board table on it are real aggregate counts from the tracker; no row, URL, email, phone or
file name from the tracker appears.

## The grep

Run from the repository root after everything was written. Patterns: any email address, any US-style phone
number, the owner's email local part and phone prefix (the real strings were used; they are written as
placeholders here so this file does not itself carry them), API-key shapes (Anthropic, OpenAI/OpenRouter, AWS,
GitHub, Google), and absolute paths under a home directory.

```
grep -rInE --exclude-dir=.git --exclude=SCRUB_CHECKLIST.md \
  -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' \
  -e '\(?[0-9]{3}\)?[-. ][0-9]{3}[-. ][0-9]{4}' \
  -e '<owner email local part>' -e '<owner other email local part>' -e '<owner phone prefix>' -e '<owner phone digits>' \
  -e 'sk-ant-' -e 'sk-or-' -e 'sk-[A-Za-z0-9]{20,}' -e 'AKIA[0-9A-Z]{16}' -e 'ghp_' -e 'github_pat_' -e 'AIza' \
  -e '/Users/[a-z]+' \
  .
```

Output on 2026-10-17, after the policy doc rewrite and the demo-row change (grep exit status 1, no line matched):

```
exit=1
```

A second grep for product, money and finance words, run exactly as written (no exclusions):

```
grep -rnEi "customer|paying|fly\.io|fly machines|beta|sub-processor|gmail\.readonly|quant|trading|capital" --exclude-dir=.git .
```

```
docs/platform-policy.md:72:  on career-site terms, https://doc.workday.com/admin-guide/en-us/human-capital-management/recruiting/career-sites/mwk1531772332109.html
exit=0
```

The one match is the path segment `human-capital-management` inside a Workday documentation URL in the Sources
list of `docs/platform-policy.md`, kept because every source link is kept. (Before this file was written, that
grep had no other match; it would match the words in this file's own text once they are pasted, which is why the
output above was captured first.)

`SCRUB_CHECKLIST.md` is excluded from the first grep because its own pattern line matches the key-shape patterns;
it holds no value, only the patterns above. The binary `assets/tracker.png` is a render of `assets/demo_tracker.html`,
which both greps cover.
