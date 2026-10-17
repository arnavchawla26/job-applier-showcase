> Copied from the private `job-applier` repository (`docs/LEGAL-job-boards.md`, written 2026-10-14) with nothing
> removed except this note added on top. It is the research behind `applier/boards.py`, the module that decides
> per hiring system whether the app submits, hands the Submit button to the person, or stays away. "We" and "our"
> below mean the Job Applier product, not any employer. Not legal advice.

# Job boards and ATSs: what an AI-applier company may do on each (2026-10-14)

Written from the operator's side: our servers (Fly machines) or our Mac app act for a paying customer, in their
name, with their data and consent. Not legal advice; every quote is from the platform's own published document,
checked on 2026-10-14. Quotes are at most 15 words.

## How the exposure works

Three layers decide what we may do on a site:

1. **The vendor's terms.** Workday, Greenhouse, Lever, Ashby, SmartRecruiters, Workable, iCIMS, Oracle and SAP
   host the employer's form. None of them publishes terms that a candidate accepts on the hosted apply page; each
   says the employer is the controller and the employer's text governs. A few vendor website terms would bind
   *us* directly if they reached the career sites (Workday: no "applications that interact with our Sites";
   SAP: no "agent-frameworks", no bypassing controls; Oracle: no "automated means"), but each is scoped to the
   vendor's own www site, not the hosted career pages. Job boards (LinkedIn, Indeed, ZipRecruiter, Dice,
   Glassdoor, Handshake) are different: the user accepts the board's own terms, and those terms name automation.
2. **The employer's terms.** On Workday the employer configures a terms checkbox on the application; on Lever,
   Greenhouse, SmartRecruiters and Workable the consent line links the employer's policy. We accept those on the
   customer's behalf (`consents.accept_site_terms_for_me`). If an employer's text forbids automated submission,
   our submit is the breach, even though the vendor is silent.
3. **Law behind the terms.** In the US a terms violation is a contract matter for the account holder (our
   customer), not by itself a computer-crime matter (Van Buren v. United States, 2021). Two things change that:
   circumventing a technical block (CAPTCHA, bot wall, IP ban, user-agent spoofing) and lying to the site. hiQ v.
   LinkedIn ended in 2022 with a $500,000 judgment and a permanent injunction under the User Agreement's
   anti-scraping and fake-account clauses, after the court found those clauses enforceable in contract. Deceiving
   an employer (a false "no tool was used", invented facts) is the customer's misrepresentation and, as the
   service that produced it, our deceptive practice. Our rules already forbid all of these; the point is that they
   are what keeps the exposure contractual and small.

## Verdict per platform, for us as operator

| Platform | Who governs the apply page | What their text says about automation | Bot check seen | What we may do |
|---|---|---|---|---|
| Greenhouse | Employer (vendor has no board terms; Privacy Policy says the employer is controller) | Nothing for board applicants. The separate My Greenhouse account agreement bans "automated means" (§3(z)); we never use those accounts | Invisible reCAPTCHA Enterprise; fallback to an emailed code or a visible captcha, per the employer's spam setting | **Auto-submit from our servers.** Honour a visible captcha by setting the job aside; the emailed-code path is fine (we read the code for the customer) |
| Workday | Employer's configured terms checkbox (Workday Website Terms cover www.workday.com only) | Vendor: not addressed for career sites. Website Terms §2 forbid "robots" and "applications that interact with our Sites without our prior written consent", scoped to their own site | None observed through account creation; email verification instead | **Auto-submit is allowed by the vendor.** Hand-submit (our current cloud default) is a product choice, not a legal need. The real control is per employer: read the terms text on the apply page and hand-submit where it forbids automation |
| SmartRecruiters | Employer privacy notice; vendor Candidate Terms (2019) only for the optional portal account | "Use automatic means to access content or data from other users" is the only clause, aimed at other users' data | DataDome through Cloudflare on registration and apply flows (vendor case study, Feb 2026) | **Auto-submit.** A DataDome block is a "no": set aside, never retry with tricks |
| Workable | Employer; vendor terms bind customers only | Not addressed. Vendor help centre distinguishes "AI-assisted applications" from "bot-driven spam" and tags the former rather than blocking | Cloudflare Turnstile on apply.workable.com | **Auto-submit.** The vendor's own stance is the most permissive of all |
| Lever | Employer; vendor terms are customer agreements | Not addressed | hCaptcha on every submit (jobs.lever.co) | **No automated submit** (a captcha on every submit is the site saying no). Fill everything and let the customer press Submit in their own browser: Mac app or home runner only |
| Ashby | Employer; vendor terms bind customers | Not addressed; vendor Spam Protection levels documented | reCAPTCHA Enterprise behind the employer's spam-protection level | Same as Lever: **hand-submit on the customer's machine**, nothing from our servers |
| iCIMS | Employer; vendor ToU covers icims.com only | Employer AUP §2(viii): no "robot, spider, automatic device, or technology to act as a headless user", and employers "shall not authorize its Candidates to violate" it | None documented | **Do not auto-submit.** The vendor has told every employer that candidate-side headless automation breaches the employer's contract. Hand-submit only, if ever supported |
| Oracle Recruiting / Taleo | Employer-authored legal disclaimer | Customer sites: not addressed. Oracle's own careers site: Oracle Web Terms §7, no "robot, spider, scraper or other automated means" | hCaptcha on Apply if the employer enables it (ORC) | **Auto-submit on customer sites; never on oracle.com careers.** Not supported by the engine today |
| SAP SuccessFactors | Employer's Data Privacy Consent Statement | Customer sites: SAP ToU §2 excludes cloud solutions. jobs.sap.com: ToU §4 forbids "bots, scrapers, spiders, crawlers, Model Context Protocol (MCP), agent-frameworks", UA spoofing and bypassing controls, and makes users responsible for "tools acting for you" | reCAPTCHA on account creation/login if enabled; Cloudflare challenge on jobs.sap.com | **Auto-submit on customer sites; never on jobs.sap.com.** Not supported today |
| LinkedIn | LinkedIn User Agreement (Nov 3, 2025) | §8.2: no "bots or other unauthorized automated methods", no "browser plugins and add-ons", no overriding security, no account sharing. Help centre: extensions that "automate activity" get accounts restricted | Yes, plus rate walls | **Never.** Not for applying, not for discovery. The hiQ injunction is the precedent. Our terms already promise this |
| Indeed (and Glassdoor, now operated by Indeed) | Indeed Terms (Sep 29, 2026) | A.3(5): automation of Indeed Apply "outside of Indeed's official vendors and tooling is prohibited". D.21: no submitting applications "by automated means", no "bots, scrapers, spiders, AI or Agentic AI". D.22(4): third-party agents only through a "Permitted AI Connector" Indeed approves | Persona bot check after applying | **Never, unless we become an approved connector.** That programme is the only lawful route and Indeed sells its own "Apply For Me" |
| ZipRecruiter | ZipRecruiter Terms (Aug 11, 2026) | §1: no "automated means" to view or access, no access "through any technology or means other than those provided", no credential sharing | Not documented | **Do not use** |
| Dice | Dice Terms (Dec 3, 2025) | §8.2(j): no "software, tool … agent … intelligent agents" not approved by Dice; only stock browsers approved. §8.2(p): no responding "on behalf of anyone other than yourself" | Not documented | **Do not use.** The agent clause is written for exactly this product |
| Handshake | Handshake ToS (Jul 22, 2025) | Only scripted account creation and scraping are banned; applicant tools not addressed | Cloudflare bot checks | Not needed now; if ever, hand-submit on the student's own machine |

## What this means for the product

- **Keep running automatically** on Greenhouse, SmartRecruiters and Workable, and on Workday where the employer's
  terms are silent. Those are the systems the cloud runs on today.
- **Hand-submit, on the customer's own machine,** is the lawful way to reach Lever and Ashby: the customer
  presses Submit and answers the captcha themselves. From our servers they stay excluded.
- **Never touch** LinkedIn, Indeed, Glassdoor, ZipRecruiter or Dice from our servers or in the customer's
  browser, for applying or for discovery. The earlier idea of LinkedIn job-search pages "as a source only" is
  out: §8.2 bans crawlers and plugins regardless of purpose.
- **Honour every block.** A captcha, a bot wall, a DataDome or Turnstile challenge, a "suspicious activity"
  message: set the job aside and tell the customer. No stealth, no proxies, no retries that look different. This
  is what keeps us on the contract side of the line rather than the circumvention side.

## Obligations we carry as the company, beyond any single site

1. **Agency and consent.** The customer must be the principal and we the agent acting on their instructions:
   our terms say so, and the onboarding must get an explicit "you authorise Job Applier to accept employers'
   application terms and to create job-site accounts in your name". Keep a copy of what was accepted per
   application (the review page text is already saved; the terms text should be too).
2. **Honesty to employers.** Never a false "no tool was used", never an invented fact, never a disguised client.
   These are already rules that never bend; they are also our main defence against a deceptive-practice claim.
3. **Employer terms scan.** Read the apply page's terms or certification text before submitting; if it forbids
   automated or third-party submission, switch that job to hand-submit. This is the one gap the research found
   that no setting covers today.
4. **Gmail.** We read customers' mail for codes with a restricted scope (`gmail.readonly`). Google requires
   app verification and an annual CASA security assessment before an app with that scope can exceed 100 users,
   and the Limited Use policy restricts what we may do with the data. Until verified, every customer sees the
   "unverified app" screen and the user cap applies.
5. **Personal data.** Resumes, addresses, work authorisation, and the voluntary self-identification answers
   (race, disability, veteran status) are special-category data under GDPR for the UK and EU markets on the beta
   list, and personal information under CCPA. We need a data-processing agreement with each sub-processor (Neon,
   Fly, Cloudflare R2, Resend, Anthropic), a retention and deletion rule (deletion exists), and a privacy notice
   that names them. Store self-identification answers only as the customer's standing choice, not per form.
6. **Job-site accounts.** We create accounts on Workday tenants in the customer's name with a password we hold.
   That is allowed because the customer authorised it and is the account holder; it also means we hold
   credentials and must protect them (they are envelope-encrypted today). Never create accounts on a site whose
   terms say "for yourself" only (My Greenhouse, LinkedIn, Indeed).
7. **AI-in-hiring laws** (NYC Local Law 144, Illinois, Colorado, the EU AI Act's recruitment category) regulate
   employers' selection tools, not applicant-side tools. Nothing found applies to us directly; confirm with
   counsel before marketing in the EU.
8. **Be a polite client.** One application per company per run, low concurrency, no bulk submissions, no
   retries on a refused submit. Several terms (ZipRecruiter, Dice) measure "more requests than a human".

## How other applier companies operate (checked 2026-10-14)

Two camps. **Autofill in the person's own browser, the person clicks Submit** (Simplify, Teal, Huntr, Careerflow,
Jobright Autofill, JobCopilot's extension): no bans, suits or store removals found. Careerflow publishes a named
ATS allow-list and treats LinkedIn and Indeed as save-only sources. **Cloud bots that submit** (Massive, Sonara,
AIApply, JobCopilot, Jobright Agent, Apply Hero): they avoid LinkedIn and Indeed sessions and apply on company
career pages and ATSs; their terms make the user responsible for third-party terms and disclaim platform
restrictions (AIApply: not liable if a platform "suspends, limits or rejects"; Massive: employers "may prohibit
automated access"). Jobright says that when a site blocks bots it tells the user to apply by hand. No enforcement
record found against any of them.

Enforcement clusters where a tool drives the person's logged-in LinkedIn or Indeed session: LazyApply (up to 1,500
a day, Trustpilot 2.1) and LoopCV's LinkedIn extension; LinkedIn's cease-and-desist letters went to extensions
(Browserflow 2023, Kleo 2025). Massive markets "beating CAPTCHAs" and uses a company-owned proxy inbox, the two
patterns Workable and Greenhouse now say they detect. The platforms' own tools keep a human step: Indeed paused the
automatic mode of Apply For Me on 4 Aug 2026 after employer pushback; LinkedIn's Premium Apply Assistant requires
approval of every element before submitting.

What to copy: an explicit third-party-terms clause with indemnity, a published allow-list, review-before-submit
where a site is gated. What never to copy: proxy inboxes, CAPTCHA claims, login-session automation on boards.
Sources: company terms and help pages (lazyapply.com/terms, simplify.jobs/terms, usemassive.com/terms,
aiapply.co/terms-of-service, jobcopilot.com/terms, help.careerflow.ai, help.huntr.co), Indeed newsroom
(indeed.com/news/releases/indeed-tests-apply-for-me-job-search), hrtechfeed.com on the pause, Semafor 12 Sep 2024 on
LinkedIn restrictions, Hacker News item 34583932 (Browserflow), theregister.com 24 Jun 2025 (Jobright).

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
- Google restricted-scope verification and CASA: https://support.google.com/cloud/answer/13465431
