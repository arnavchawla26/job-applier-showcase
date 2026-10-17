# Job boards and hiring systems: what each platform allows an applicant-side tool to do (research, 2026-10-14)

Written from the applicant's side: the app acts for one person, in their name, with their data and their
consent, on their own machine. Not legal advice; every quote is from the platform's own published document,
checked on 2026-10-14. Quotes are at most 15 words. This research is what `applier/boards.py` encodes.

## How the exposure works

Three layers decide what the app may do on a site:

1. **The vendor's terms.** Workday, Greenhouse, Lever, Ashby, SmartRecruiters, Workable, iCIMS, Oracle and SAP
   host the employer's form. None of them publishes terms that a candidate accepts on the hosted apply page; each
   says the employer is the controller and the employer's text governs. A few vendor website terms would bind a
   tool directly if they reached the career sites (Workday: no "applications that interact with our Sites";
   SAP: no "agent-frameworks", no bypassing controls; Oracle: no "automated means"), but each is scoped to the
   vendor's own www site, not the hosted career pages. Job boards (LinkedIn, Indeed, ZipRecruiter, Dice,
   Glassdoor, Handshake) are different: the person accepts the board's own terms, and those terms name automation.
2. **The employer's terms.** On Workday the employer configures a terms checkbox on the application; on Lever,
   Greenhouse, SmartRecruiters and Workable the consent line links the employer's policy. If an employer's text
   forbids automated submission, an automated submit is the breach, even though the vendor is silent. That is why
   the app scans the wording on the form before every Submit.
3. **Law behind the terms.** In the US a terms violation is a contract matter for the person whose account it
   is, not by itself a computer-crime matter (Van Buren v. United States, 2021). Two things change that:
   circumventing a technical block (CAPTCHA, bot wall, IP ban, user-agent spoofing) and lying to the site. hiQ v.
   LinkedIn ended in 2022 with a $500,000 judgment and a permanent injunction under the User Agreement's
   anti-scraping and fake-account clauses, after the court found those clauses enforceable in contract. Deceiving
   an employer (a false "no tool was used", invented facts) is the person's misrepresentation, and the tool that
   produced it shares the blame. The app's rules forbid all of these; they are what keeps the exposure contractual
   and small.

## Verdict per platform

| Platform | Who governs the apply page | What their text says about automation | Bot check seen | What the app does |
|---|---|---|---|---|
| Greenhouse | Employer (vendor has no board terms; Privacy Policy says the employer is controller) | Nothing for board applicants. The separate My Greenhouse account agreement bans "automated means" (§3(z)); the app never uses those accounts | Invisible reCAPTCHA Enterprise; fallback to an emailed code or a visible captcha, per the employer's spam setting | **Auto-submit.** Honour a visible captcha by setting the job aside; the emailed-code path is fine (the app reads the code from the person's inbox when they allow it) |
| Workday | Employer's configured terms checkbox (Workday Website Terms cover www.workday.com only) | Vendor: not addressed for career sites. Website Terms §2 forbid "robots" and "applications that interact with our Sites without our prior written consent", scoped to their own site | None observed through account creation; email verification instead | **Auto-submit is allowed by the vendor.** The real control is per employer: read the terms text on the apply page and hand-submit where it forbids automation |
| SmartRecruiters | Employer privacy notice; vendor Candidate Terms (2019) only for the optional portal account | "Use automatic means to access content or data from other users" is the only clause, aimed at other users' data | DataDome through Cloudflare on registration and apply flows (vendor case study, Feb 2026) | **Auto-submit.** A DataDome block is a "no": set aside, never retry with tricks |
| Workable | Employer; vendor terms bind employers only | Not addressed. Vendor help centre distinguishes "AI-assisted applications" from "bot-driven spam" and tags the former rather than blocking | Cloudflare Turnstile on apply.workable.com | **Auto-submit.** The vendor's own stance is the most permissive of all |
| Lever | Employer; vendor terms are employer agreements | Not addressed | hCaptcha on every submit (jobs.lever.co) | **No automated submit** (a captcha on every submit is the site saying no). Fill everything and let the person press Submit in their own browser |
| Ashby | Employer; vendor terms bind employers | Not addressed; vendor Spam Protection levels documented | reCAPTCHA Enterprise behind the employer's spam-protection level | Same as Lever: **hand-submit**, the person presses Submit |
| iCIMS | Employer; vendor ToU covers icims.com only | Employer AUP §2(viii): no "robot, spider, automatic device, or technology to act as a headless user", and employers "shall not authorize its Candidates to violate" it | None documented | **Do not auto-submit.** The vendor has told every employer that candidate-side headless automation breaches the employer's contract. Hand-submit only, if ever supported |
| Oracle Recruiting / Taleo | Employer-authored legal disclaimer | Employer sites: not addressed. Oracle's own careers site: Oracle Web Terms §7, no "robot, spider, scraper or other automated means" | hCaptcha on Apply if the employer enables it (ORC) | **Auto-submit on employer sites; never on oracle.com careers.** Not supported by the engine today |
| SAP SuccessFactors | Employer's Data Privacy Consent Statement | Employer sites: SAP ToU §2 excludes cloud solutions. jobs.sap.com: ToU §4 forbids "bots, scrapers, spiders, crawlers, Model Context Protocol (MCP), agent-frameworks", UA spoofing and bypassing controls, and makes users responsible for "tools acting for you" | reCAPTCHA on account creation/login if enabled; Cloudflare challenge on jobs.sap.com | **Auto-submit on employer sites; never on jobs.sap.com.** Not supported today |
| LinkedIn | LinkedIn User Agreement (Nov 3, 2025) | §8.2: no "bots or other unauthorized automated methods", no "browser plugins and add-ons", no overriding security, no account sharing. Help centre: extensions that "automate activity" get accounts restricted | Yes, plus rate walls | **Never.** Not for applying, not for discovery. The hiQ injunction is the precedent |
| Indeed (and Glassdoor, now operated by Indeed) | Indeed Terms (Sep 29, 2026) | A.3(5): automation of Indeed Apply "outside of Indeed's official vendors and tooling is prohibited". D.21: no submitting applications "by automated means", no "bots, scrapers, spiders, AI or Agentic AI". D.22(4): third-party agents only through a "Permitted AI Connector" Indeed approves | Persona bot check after applying | **Never.** Only an Indeed-approved connector may automate it, and Indeed sells its own "Apply For Me" |
| ZipRecruiter | ZipRecruiter Terms (Aug 11, 2026) | §1: no "automated means" to view or access, no access "through any technology or means other than those provided", no credential sharing | Not documented | **Do not use** |
| Dice | Dice Terms (Dec 3, 2025) | §8.2(j): no "software, tool … agent … intelligent agents" not approved by Dice; only stock browsers approved. §8.2(p): no responding "on behalf of anyone other than yourself" | Not documented | **Do not use.** The agent clause is written for exactly this kind of tool |
| Handshake | Handshake ToS (Jul 22, 2025) | Only scripted account creation and scraping are banned; applicant tools not addressed | Cloudflare bot checks | Not needed now; if ever, hand-submit |

## What this means for the app

- **Run automatically** on Greenhouse, SmartRecruiters and Workable, and on Workday where the employer's terms
  are silent.
- **Hand-submit** is the lawful way to reach Lever and Ashby: the person presses Submit and answers the captcha
  themselves. The app fills and verifies, then stops.
- **Never touch** LinkedIn, Indeed, Glassdoor, ZipRecruiter or Dice, for applying or for discovery. The earlier
  idea of LinkedIn job-search pages "as a source only" is out: §8.2 bans crawlers and plugins regardless of purpose.
- **Scan the employer's terms.** Read the apply page's consent or certification text before submitting; a sentence
  that forbids automated or third-party submission switches that one job to hand-submit, whatever the vendor
  allows. The wording that was agreed to is kept with the application.
- **Honour every block.** A captcha, a bot wall, a DataDome or Turnstile challenge, a "suspicious activity"
  message: set the job aside and tell the person. No stealth, no proxies, no retries that look different. This
  is what keeps the app on the contract side of the line rather than the circumvention side.
- **Be honest to employers.** Never a false "no tool was used", never an invented fact, never a disguised client.
  If a form asks whether an AI tool was used, the answer is yes.
- **Be a polite client.** One application per company per run, low concurrency, no bulk submissions, no retries
  on a refused submit. Several terms (ZipRecruiter, Dice) measure "more requests than a human".

## Sources

- Workday Website Terms, https://www.workday.com/en-us/legal/site-terms.html (08/13/2026); Workday admin guides
  on career-site terms, https://doc.workday.com/admin-guide/en-us/human-capital-management/recruiting/career-sites/mwk1531772332109.html
- Greenhouse legal hub, https://www.greenhouse.com/legal; My Greenhouse User Agreement, https://my.greenhouse.io/users/agreement
  (Jan 29, 2025); Invisible reCAPTCHA, https://support.greenhouse.io/hc/en-us/articles/115005448066
- Lever / Employ terms, https://www.employinc.com/terms-of-service/ (Feb 19, 2025); hCaptcha observed on jobs.lever.co apply pages
- Ashby terms, https://www.ashbyhq.com/resources/terms (Sep 29, 2025); spam protection, https://docs.ashbyhq.com/job-board-application-spam-protection
- SmartRecruiters Candidate Terms, https://www.smartrecruiters.com/legal/terms-of-use/ (May 14, 2019); DataDome case study,
  https://securityboulevard.com/2026/02/smartrecruiters-crushes-spam-job-applications-without-disrupting-real-users/
- Workable terms, https://www.workable.com/terms (Mar 2, 2026); AI-assisted applications, https://help.workable.com/hc/en-us/articles/35293126257815
- iCIMS Acceptable Use Policy (20 April 2026), https://cdn31.icims.com/wp-content/uploads/2026/03/20120058/iCIMS-Acceptable-Use-Policy.pdf;
  Subscription Agreement, https://cdn31.icims.com/wp-content/uploads/2026/04/20111800/iCIMS-Subscription-Agreement-20APRIL2026.pdf
- Oracle Web Sites Terms of Use, https://www.oracle.com/legal/terms.html (Aug 10, 2024); ORC hCaptcha,
  https://docs.oracle.com/en/cloud/saas/talent-management/faimh/enable-hcaptcha.html
- SAP Terms of Use, https://www.sap.com/corporate/en/legal/terms-of-use.html (Feb 26, 2026); KBA 2082087 on career-site CAPTCHA
- LinkedIn User Agreement, https://www.linkedin.com/legal/user-agreement (Nov 3, 2025); automation policy,
  https://www.linkedin.com/help/linkedin/answer/90586; hiQ settlement, https://www.proskauer.com/blog/hiq-and-linkedin-reach-proposed-settlement-in-landmark-scraping-case
- Indeed Terms, https://www.indeed.com/legal (Sep 29, 2026); job-seeker guidelines,
  https://www.indeed.com/help/job-seekers/articles/360028540531-indeed-job-seeker-guidelines
- ZipRecruiter Terms, https://www.ziprecruiter.com/terms (Aug 11, 2026); Dice Terms, https://www.dice.com/about/terms-and-conditions (Dec 3, 2025);
  Glassdoor Terms, https://www.glassdoor.com/about/terms/ (Jul 1, 2026); Handshake ToS, https://joinhandshake.com/tos/ (Jul 22, 2025)
