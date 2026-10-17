# Architecture

Every box below is a real module in the private repo (`applier/...`); the names are the file names. Two
deployments share the engine: the Mac app (SQLite, Keychain, Chrome on the person's machine) and the cloud worker
(Postgres on Neon, one container per run, Chrome inside the container). The Next.js site is the front door for
the cloud version: sign-up, profile, runs and the "ready for you" list.

```mermaid
flowchart TB
    subgraph discover["1. Find roles"]
        jobs["jobs.py<br/>Greenhouse / Lever / Ashby board feeds<br/>+ postings from URLs"]
        boards["boards.py<br/>auto / hand / never per hiring system<br/>(from docs/platform-policy.md)"]
        tracker["tracker.py<br/>SQLite (Mac) or Postgres (cloud)<br/>never apply twice"]
    end
    subgraph tailor["2. Tailor"]
        tailorpy["tailor.py<br/>one LaTeX resume per posting<br/>guardrails: no new facts, no new numbers"]
        latex["latex.py<br/>tectonic compile + text check"]
    end
    subgraph fill["3. Fill, verify, submit"]
        extract["js/extract.js<br/>reads the whole form as text"]
        answers["answers.py<br/>1 your answers -> 2 profile rules -><br/>3 reusable model answers -> 4 one model call"]
        filler["filler.py<br/>Playwright drives Chrome<br/>fill, read back, verify, submit"]
        terms["boards.terms_forbid_automation()<br/>employer terms scanned before Submit"]
        handover["Application._hand_over()<br/>everything filled, the person presses Submit"]
        mail["applemail.py / gmail.py<br/>emailed security codes"]
    end
    subgraph llm["Model"]
        llmpy["llm.py<br/>one gateway, per-call cost log,<br/>monthly budget stop"]
    end
    subgraph ui["4. Track and ask"]
        app["app.py (FastAPI) + web/index.html<br/>Tracker, Needs you, Approve answers, Results"]
        needs["needs.py<br/>asks that block a run:<br/>a code, a password, a Submit click"]
    end
    subgraph cloud["Cloud only (APPLIER_CLOUD)"]
        worker["cloud/worker.py<br/>one run per machine"]
        memory["cloud/memory.py<br/>shared form memory;<br/>board questions promoted into every profile"]
        policy["cloud/policy.py<br/>engine status -> what the person sees"]
        site["job-applier-site (Next.js, Postgres)<br/>sign-up, profile, runs, ready-for-you"]
    end

    jobs --> boards --> tracker --> tailorpy --> latex --> filler
    filler --> extract --> answers --> llmpy
    answers --> filler
    filler --> terms --> handover
    filler --> mail
    filler --> tracker --> app
    needs <--> filler
    needs --> app
    tailorpy --> llmpy
    worker --> filler
    worker --> memory --> answers
    tracker --> policy --> site
```

## The decision path for one application

1. `boards.forbidden(url)`: a LinkedIn, Indeed, Glassdoor, ZipRecruiter or Dice URL is never opened.
2. `boards.mode(ats)`: Lever, Ashby and iCIMS are `hand`; Greenhouse, Workday, SmartRecruiters and Workable are `auto`.
3. `filler.py` fills every page, reads it back and verifies it. No screenshots are interpreted; the form is read as
   text by `extract.js`.
4. Before Submit, the consent and certification wording seen on the form (saved as `terms.txt` next to the
   application) is run through `boards.terms_forbid_automation()`. One sentence that forbids automated or
   third-party submission turns that job into a hand submit, whatever the vendor allows.
5. `auto`: Submit is pressed once; the page or a confirmation email settles the status (`submitted`). No
   confirmation means `submit_unconfirmed`, and it is never pressed again. A bot check that holds the submission
   back means `blocked_by_site`, and it is never retried with tricks.
6. `hand`: `_hand_over()` leaves the filled form open and posts a Needs-you card; the person presses Submit. In the
   cloud, only Workday keeps a draft under the person's account (`ready_for_you`); everywhere else the job is set
   aside for their own machine.

## Where the model is called

Only through `llm.py`. Answering a form is cheapest-source-first (`answers.py`): the person's own saved answers,
then rules that read the profile (name, links, school, work authorisation, EEO), then model answers marked
reusable, then one call for whatever is left on the page. Tailoring is one call per posting, with the result
checked for invented numbers (`tailor.py`). Every call is appended to `usage.jsonl` with its list-price cost, and
a monthly budget stops sessions.
