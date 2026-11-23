# How US Tech Coding Interviews Changed in 2025–2026 (as of Nov 22, 2026) and What It Means for Practice

Scope: US tech-company SWE and data roles. Every finding has a date and a URL. Source labels:
- **[OFFICIAL]**: a company or vendor's own page or press release.
- **[PRESS]**: news reporting, usually based on internal documents or spokesperson statements.
- **[SURVEY]**: survey data, usually from a vendor.
- **[CROWD]**: candidate reports, prep sites or forums. Treat as unverified.
- **[OLDER]**: published before 2025.

Many company-level details reached me only through secondary coverage (paywalled originals: 404 Media, Business Insider, WSJ). Those points are flagged.

---

## 1. AI in interviews: which companies allow AI-enabled coding rounds, what they look like, and who bans AI

### Takeaway
By Nov 2026 the large companies run **two kinds of coding round side by side**. One is the classic no-AI algorithm round. The other is a new AI-enabled round built on an existing, multi-file codebase, where the candidate reads, debugs, extends and verifies code. Meta (from Oct 2025) and Google (pilot from May 2026, expanded by Oct 2026) are the clearest Big Tech cases. Canva and Shopify moved earliest among well-known companies. Amazon and Anthropic officially ban AI unless told otherwise, and so, reportedly, do most banks and quant firms. A vendor survey says most organizations (about 62%) still prohibit AI in technical interviews.

### Cited Findings
**Meta**
- **[PRESS] Late July 2025:** 404 Media reported an internal Meta post saying some coding candidates would be allowed to use an AI assistant during interviews. The post's stated reasons were that this is "more representative of the developer environment that our future employees will work in" and that it makes LLM-based cheating less effective. A Meta spokesperson said the company is testing how to provide these tools to applicants. The post also asked current employees to act as "mock candidates." — [404 Media](https://www.404media.co/meta-is-going-to-let-job-candidates-use-ai-during-coding-tests/) (paywalled; details via [TechRadar](https://www.techradar.com/pro/meta-is-going-to-let-candidates-use-ai-in-job-interviews) and [Business Today, 2025-07-31](https://www.businesstoday.in/technology/news/story/meta-to-test-job-applicants-with-ai-assisted-coding-interviews-amid-ai-expansion-plans-487200-2025-07-31))
- **[SURVEY] 2025:** Interviewers told interviewing.io that Meta was the only FAANG company experimenting with AI-assisted interviews, with a launch planned for Q3. The round would sit in the onsite, possibly replacing one onsite interview, and would *not* replace the algorithmic phone screen. — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot)
- **[CROWD] Format, rolled out Oct 2025:** The round replaces one of the two onsite coding rounds for SWE and EM loops, up to E7/M2. It is about 60 minutes in a three-panel CoderPad layout: file explorer, editor, and an AI chat that can read the project but only answers in chat, so the candidate types all code. The codebase is multi-file and the candidate did not write it. Supported languages are Java, C++, C#, Python, Kotlin and TypeScript. Reported models include GPT-4o mini, GPT-5, Claude Haiku/Sonnet/Opus variants, Gemini 2.5 Pro and Llama 4 Maverick. There are three reported phases: (1) bug fixing, where AI rules vary by interviewer; (2) core implementation, where AI use is expected and problems are "harder than a medium LeetCode"; (3) optimization against tiered test data. The problem pool is reportedly small (about 9 problems, e.g. maze solving). Scoring uses Meta's usual four competencies: problem solving, code quality (including understanding the AI's code), verification, and communication. — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- **[CROWD]** Sources disagree on which levels get the round. Some say mainly E4/E5; others say E5–E7 from Oct 2025. One quote attributed to an internal Meta source and circulating on prep sites reads: "Should use AI, but need to show you understand the code. Explain the output. Test before using. Don't prompt your way out of it." — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding); [copilotinterview.com](https://copilotinterview.com/blog/meta-ai-enabled-coding-interview)
- **[OFFICIAL, vendor]** CoderPad's State of Tech Hiring 2026 material cites Meta replacing one traditional algorithmic round with an AI-assisted round on CoderPad in Oct 2025. — [CoderPad 2026 report blog](https://coderpad.io/blog/hiring-developers/new-research-the-2026-state-of-tech-hiring-what-ai-means-for-developers-and-hiring-teams/) (seen via search summary; full PDF not read)

**Google**
- **[PRESS] Early May 2026:** Business Insider reported, and a Google spokesperson confirmed, a pilot that lets SWE candidates use Gemini in a new "code comprehension" round. Candidates read, debug and optimize an existing codebase. The internal document calls the approach "human-led, AI-assisted" and says "Interviewers will evaluate AI fluency, including prompt engineering, output validation, and debugging skills." The pilot covers select junior and mid-level roles on US teams, starting with Google Cloud and Platforms & Devices. — [Asia Economy, 2026-05-08](https://www.asiae.co.kr/en/article/2026050809233801400); [Entrepreneur](https://www.entrepreneur.com/business-news/google-is-testing-a-new-rule-transform-job-interviews); [Northeastern Careers blog, 2026-05-13](https://careers.northeastern.edu/blog/2026/05/13/googles-ai-assisted-coding-interview-2026-guide/); [Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/asking-kid-math-test-without-151500986.html)
- **[PRESS] Oct 20, 2026:** Business Insider, via Tekedia, reported that internal documents show the formats spreading beyond the first test groups, though Google still calls it a pilot. A Google spokesperson said AI fluency is a requirement for all SWE positions, and the documents say "AI product integration" is required for most roles above entry level. Brian Ong, VP of Recruiting: "We're piloting updates to our interview process for software engineers, including evaluating for AI fluency." — [Tekedia, 2026-10-20](https://www.tekedia.com/google-expands-ai-powered-hiring-tests-making-ai-fluency-mandatory-for-software-engineers/)
- **Conflict:** Secondary sources disagree on whether the code-comprehension round *replaces* a traditional coding round or is *added* alongside the algorithmic rounds. — [byteherald, Oct 2026](https://www.byteherald.com/2026/10/google-changed-coding-interview-ai-is.html); [aced.io](https://www.aced.io/blog/google-ai-coding-interview)

**Canva and Shopify (early adopters)**
- **[OFFICIAL] June 11, 2025:** Canva's "AI-Assisted Coding" interview replaced its Computer Science Fundamentals screen for backend and frontend roles, as a pilot. Canva says "AI assistants can trivially solve traditional coding interview questions." The new problems are "more complex, ambiguous, and realistic." Instead of Conway's Game of Life, a candidate might get "Build a control system for managing aircraft takeoffs and landings at a busy airport." Candidates are evaluated on breaking down ambiguous requirements, judging when to use AI, catching and fixing problems in AI code, and production quality. — [Canva Engineering blog](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews); [The Register, 2025-06-11](https://www.theregister.com/2025/06/11/canva_coding_assistant_job_interviews/)
- **[OFFICIAL]** A companion Canva post says the company cares about "strong engineering fundamentals amplified by AI" and that candidates must be ready to defend their whole solution. — [Canva: AI Interview Success](https://www.canva.dev/blog/engineering/ai-interview-success/) (seen via search summary)
- **[PRESS] Sept 18, 2025:** Shopify has adopted AI-assisted interviews. Its Head of Engineering, Farhan Thawar, said they are "embracing" AI use. Many startups have dropped algorithmic questions and take-homes. — [Pragmatic Engineer, The Pulse #146](https://newsletter.pragmaticengineer.com/p/the-pulse-146)

**Explicit bans (confirmed)**
- **[OFFICIAL] Anthropic, page updated July 10, 2025:** For live interviews, "This is all you–no AI assistance unless we indicate otherwise." Take-homes: "Complete these without Claude unless we indicate otherwise." For applications, write the first draft yourself, then you may refine it with Claude. — [Anthropic candidate AI guidance](https://www.anthropic.com/candidate-ai-guidance)
  - *Contradiction:* a third-party tracker (May 2026, no sources cited) says Anthropic *allows* AI in coding rounds. The official page should win unless a specific round says otherwise. — [techinterview.org tracker](https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/)
- **[PRESS] Amazon, Feb 2025** (Business Insider, internal guidelines): "please do not use GenAI tools during your interview unless explicitly permitted… Failure to adhere to these guidelines may result in disqualification." Candidates must acknowledge they will not use unauthorized tools. Business Insider also reported that one Amazon team was "studying" giving candidates AI assistants. — [ITPro](https://www.itpro.com/business/careers-and-training/amazon-bans-ai-tools-during-job-interviews); [Business Insider (NL mirror)](https://businessinsider.nl/big-tech-wants-everyone-to-use-ai-just-not-when-applying-for-jobs)

**Trackers and other companies (unverified)**
- **[CROWD] May 4, 2026 tracker** (built from candidate reports; cites no official URLs). It lists as AI-prohibited: Apple, Amazon, Netflix, most Microsoft teams, quant firms (Jane Street, Citadel, HRT, etc.), investment banks, and Bloomberg. As allowed or mixed: Cursor, Replit, Vercel, Glean, Linear, Notion, Stripe (some formats), and OpenAI (varies by team). It also lists Meta as "generally prohibited," which is out of date given the AI-enabled round. Its reliability is low. — [techinterview.org](https://www.techinterview.org/post/3233474911/ai-tool-policy-tracker-tech-companies-2026/)
- **[CROWD]** Datadog reportedly allows AI only in interviews designated as "AI coding interviews" and tells candidates in advance. Rippling and Shopify reportedly allow AI copilots in live coding, but the trackers disagree. — [thita.ai](https://thita.ai/ai-in-interviews); [genaidojo](https://www.genaidojo.io/guides/companies-using-ai-in-technical-interviews)
- **[CROWD]** Anysphere/Cursor reportedly bans AI in its first-round coding interview and uses a two-day onsite project for finalists. This contradicts the trackers that say Cursor allows AI. — [Wikipedia: Anysphere](https://en.wikipedia.org/wiki/Anysphere)

**Industry-level numbers**
- **[SURVEY] 2025 (interviewing.io):** 67% of startup respondents said AI meaningfully changed their interview process, versus 0% of FAANG and FAANG-adjacent respondents. CoderPad told interviewing.io that 20–30% of its customers actively use AI in interviews and that it has run more than 35,000 AI-assisted interviews. — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot)
- **[SURVEY, vendor] Karat:** 62% of organizations still prohibit AI in technical interviews, while leaders estimate more than half of candidates use it anyway. — [Interview Query summary](https://www.interviewquery.com/p/technical-interviews-2026-ai-shift); [Karat: Engineering interview trends 2026](https://karat.com/engineering-interview-trends-2026/) (exact survey date and sample unverified; Karat pages cite 400, 157 or 150 leaders)

### Inferences
- The AI-enabled round is a *code-reading and code-extension* round. You debug and extend code you did not write, under time pressure. Even with AI, Meta's assistant cannot write into the editor, and phase 1 (bug fixing) is often done without AI. Fluent hand-coding and reading skills still decide the outcome.
- In every Big Tech loop I found, the AI-enabled round sits next to an AI-free algorithm round, never instead of all of them. A candidate must pass both kinds of round.
- Company policy changes quickly and varies by team. A practice platform should frame a session as "AI-off round" or "AI-on round" instead of assuming one company-wide rule.

### Gaps
- No primary source found for OpenAI's or Rippling's interview AI policy. Trackers say OpenAI "varies by team," without citing anything.
- I could not read the original Business Insider (May and Oct 2026) or 404 Media (July 2025) articles. Details come from secondary coverage.
- No official Meta candidate-facing document on the AI-enabled round was found. Format details are candidate-reported.
- One secondary source estimated that about 25% of US employers permit AI in at least one round as of mid-2026. I could not trace its origin, so I left it out of the findings.

---

## 2. Countermeasures against cheating and AI tools: in-person onsites, proctoring, and more follow-up questions

### Takeaway
From mid-2025, companies fought AI cheating in three ways: (a) at least one in-person round (Google, Cisco, McKinsey), (b) stricter screen-sharing and cheating flags (Meta) and AI proctoring on assessment platforms, and (c) most widely, more probing follow-ups ("why did you do this?", line-by-line questions, re-asking, rapid-fire). All three reward candidates who can produce and explain code fluently without help.

### Cited Findings
- **[PRESS] Google:** Sundar Pichai said Google will "introduce at least one round of in-person interviews for people" to make sure "the fundamentals are there." Coverage peaked in Aug 2025. Outlets attribute the remark to his June 2025 comments, and some name the Lex Fridman podcast as the venue. — [LatestLY](https://www.latestly.com/technology/why-google-is-bringing-back-in-person-interviews-ceo-sundar-pichai-says-we-will-introduce-at-least-one-round-of-in-person-interviews-for-people-7076900.html); [Inshorts](https://inshorts.com/en/news/pichai-reveals-new-interview-process-at-google-to-stop-ai-cheating-1755698986669); [Pragmatic Engineer, 2025-09-18](https://newsletter.pragmaticengineer.com/p/the-pulse-146) (refers to "Pichai's June comments")
- **[SURVEY]** interviewing.io added an edit on Oct 8, 2025 noting Google's pilot of in-person SWE interviews. — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot)
- **[PRESS] Aug 12, 2025:** Axios, citing the WSJ, reported that Google, Cisco and McKinsey brought back face-to-face interviews for some part of hiring. McKinsey asks hiring managers to hold at least one in-person meeting. Cisco's Scott McGuckin said: "Remote work and advancements in AI have made it easier than ever for fake candidates to infiltrate the hiring process." — [Axios](https://www.axios.com/2025/08/12/in-person-job-interview-artificial-intelligence); [Entrepreneur](https://www.entrepreneur.com/business-news/google-mckinsey-reintroduce-in-person-interviews-due-to-ai/496041)
- **[SURVEY, secondary] Gartner, July 31, 2025:** Gartner predicts 1 in 4 candidate profiles worldwide could be fake by 2028. A Gartner survey found 72.4% of recruiting leaders run in-person interviews to combat fraud, and 6% of candidates admitted dishonest AI use in interviews. — [TechSpot](https://www.techspot.com/news/109060-face-face-interviews-making-comeback-age-ai-hiring.html) (secondary; the Gartner original was not read)
- **[SURVEY] Meta, 2025:** Interviewers must flag suspected cheating, with justification, across nearly all interview types and levels. Candidates must share their entire screen and turn off background filters, including blur. Meta was the only Big Tech company making company-wide anti-cheating changes. — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot); [Pragmatic Engineer, 2025-09-18](https://newsletter.pragmaticengineer.com/p/the-pulse-146)
- **[SURVEY] 2025 interviewer survey, 67 responses including 52 FAANG:**
  - 81% suspected AI cheating, about a third had caught someone, and 11% said their company uses cheating-detection software (nearly all at Meta).
  - Share predicting in-person interviews return soon: Apple 100%, Microsoft 78%, Google 67%, Meta 55%, Amazon 50%, Netflix 50%.
  - One Meta interviewer called an earlier in-person attempt "a total failure."
  - — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot)
- **[SURVEY]** Interviewer tactics reported:
  - more follow-up questions, and line-by-line questions about specific code
  - "why" over "how"
  - asking the same question again later to check consistency (AI answers vary; Netflix)
  - rapid-fire questions that leave no time to prompt an AI (DoorDash)
  - fluent explanation of concepts (Microsoft)
  - — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-pulse-146); [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot)
- **[PRESS] Amazon, Feb 2025:** Recruiters received signs of AI use to watch for, such as typing while answering, reading responses, and reacting to AI output. — [ITPro](https://www.itpro.com/business/careers-and-training/amazon-bans-ai-tools-during-job-interviews)
- **[OFFICIAL, vendor] HackerRank, Spring '26 (Apr 2026):** Proctor Mode is "AI-powered" and simulates live human proctoring. The Chakra AI interviewer "flags suspicious behavior." — [HackerRank Spring '26 release](https://www.hackerrank.com/release/apr-2026)
- **[PRESS] Oct 5, 2026:** HackerRank says suspicious-activity flags were 70–80% lower in interviews where candidates had AI access than in comparable traditional assessments. Its CEO argues that giving AI access removes the incentive to use outside tools secretly. — [TechCrunch](https://techcrunch.com/2026/10/05/hackerranks-ai-interviewer-offers-a-glimpse-into-what-job-interviews-could-become/)
- **[OLDER, ~2024] interviewing.io experiment** (small: 37 interviews). Candidates who secretly used ChatGPT passed 73% of the time on verbatim LeetCode problems and 67% on lightly modified ones, versus a 53% baseline. Fully custom questions largely resisted cheating. — [interviewing.io](https://interviewing.io/blog/how-hard-is-it-to-cheat-with-chatgpt-in-technical-interviews)

### Inferences
- Every countermeasure checks *real-time understanding*: talking through code as you write it, answering "why" about any line, and producing working code under live observation or in person. That makes fluent hand-writing of Python and SQL *more* valuable, not less. An in-person whiteboard or laptop round with no autocomplete is the extreme case.
- Because verbatim LeetCode is easy to cheat on, companies moved to *variants and custom problems*. Memorizing solutions is worth less; recognizing patterns and adapting them under twists is worth more.

### Gaps
- No official Google careers-page statement found that defines which rounds are in person, or since when. Evidence is executive comments plus press.
- No public data on the share of US SWE loops that include an in-person round in 2026.
- The details of proctoring in OAs (webcam, screen recording, browser lockdown) on CodeSignal and HackerRank in 2026 are not well documented in what I found.

---

## 3. OA and interview platforms: CodeSignal, HackerRank, CoderPad formats and scoring in 2025–2026

### Takeaway
CodeSignal's **Industry Coding Framework** (one project, 4 progressive levels, e.g. "in-memory database") is the clearest "multi-part, extend-your-own-code" OA format and is widely reported at fintech and AI companies. All three major vendors shipped AI-assisted or agentic modes in 2025–2026: CodeSignal Cosmo (May 2025) and Agentic Assessments (Mar 2026); HackerRank's AI-assisted interviews and the Chakra AI interviewer (GA Oct 2026); CoderPad's AI-enabled pads (used for Meta's round).

### Cited Findings
**CodeSignal**
- **[OFFICIAL]** Industry Coding Framework (ICF): one language-agnostic, project-based task with **4 progressive levels**. Each level adds new methods and entities within a realistic scenario. — [CodeSignal ICF Datasheet](https://discover.codesignal.com/rs/659-AFH-023/images/CodeSignal-Industry-Coding-Framework-Datasheet.pdf); [ICF technical brief](https://discover.codesignal.com/rs/659-AFH-023/images/Industry-Coding-Skills-Evaluation-Framework-CodeSignal-Skills-Evaluation-Lab-Short.pdf)
- **[CROWD]** Reported ICF task: "in-memory database," seen at eBay and Anthropic.
  - Level 1: set/get/delete records, fields and values
  - Level 2: display a record's fields filtered by a condition (prefix filter)
  - Level 3: TTL on records (timestamps)
  - Level 4: look-back at historical values, or backup/restore
  - One secondary source puts the time limit at about 90 minutes; I did not find an official figure.
  - OpenAI has a reported "in-memory database (SQL)" problem.
  - — [LeetCode Discuss, eBay ICF](https://leetcode.com/discuss/post/7316549/ebay-codesignal-oa-industry-coding-asses-8qbn/); [1point3acres, Anthropic OA](https://www.1point3acres.com/interview/thread/1049492); [1point3acres, OpenAI in-memory DB SQL](https://www.1point3acres.com/interview/problems/company/openai/in-memory-database-sql); [Practice repo with level1–level4](https://github.com/PaulLockett/CodeSignal_Practice_Industry_Coding_Framework)
- **[CROWD]** One candidate notes there is "a notable lack of internet resources for preparation for this format." — [Medium: ICF advice](https://medium.com/@thosehippos/advice-preparation-for-codesignal-industry-coding-framework-test-reflections-0260f903ce7f)
- **[OFFICIAL]** The General Coding Assessment (GCA) is reported in four skill areas: Basic Coding, Data Manipulation, Ease of Implementation, Problem-Solving. CodeSignal has moved to an "Assessment Score" with overall and per-skill feedback, after the "Coding Score 2023" recalibration. — [CodeSignal: Understanding Assessment Score](https://support.codesignal.com/hc/en-us/articles/13261190299287-Understanding-Assessment-Score); [CodeSignal: Coding Score / GCA](https://support.codesignal.com/hc/en-us/articles/1500001320521)
- **[OFFICIAL] May 28, 2025:** CodeSignal launched AI-Assisted Coding Assessments and Interviews with **Cosmo**, an in-IDE assistant whose level of help employers can set (from full co-pilot to limited). Hiring teams get transcripts of all AI interactions and session replays. — [CodeSignal press release](https://codesignal.com/newsroom/press-releases/codesignal-launches-ai-assisted-coding-assessments-and-interviews-redefining-technical-hiring-in-the-ai-era/); [CodeSignal blog](https://codesignal.com/blog/codesignal-updates/introducing-ai-assisted-coding-assessments-interviews/)
- **[OFFICIAL] March 2026:** CodeSignal introduced **Agentic Coding Assessments**, where candidates can use tools such as Claude Code, Cursor and Codex. — [CodeSignal Product Updates, March 2026](https://support.codesignal.com/hc/en-us/articles/39883270333591-Product-Updates-March-2026) (seen via search summary)

**HackerRank**
- **[OFFICIAL] Spring '26 (Apr 2026):** Chakra is an AI interviewer that "adapts in real time, probes for depth, flags suspicious behavior" and produces evidence-backed reports. The release also covers the AI-powered Proctor Mode. — [HackerRank Spring '26 release](https://www.hackerrank.com/release/apr-2026)
- **[PRESS] Oct 5, 2026:** Chakra is generally available after about 6 months in beta and more than 500,000 interviews. Candidates get a task based on a **real-world code repository** and work in a canvas with an AI assistant. Chakra asks follow-ups such as why an approach was chosen and how the solution changes under a new constraint. It collapses recruiter screen, take-home and engineer interview into one session, and humans make the final decision. Named customers include Amazon, Nvidia, Snowflake, Replit and Clay. The CEO says: "The previous modality of evaluation was evaluating the output." — [TechCrunch](https://techcrunch.com/2026/10/05/hackerranks-ai-interviewer-offers-a-glimpse-into-what-job-interviews-could-become/)
- **[CROWD]** HackerRank shipped "AI-Assisted Interviews" as a distinct format in 2026. The interviewer, not the candidate, turns on the AI panel. — [aceround.app guide](https://www.aceround.app/blog/hackerrank-ai-assisted-interview-guide/)

**CoderPad**
- **[CROWD]** Meta's AI-enabled round runs in CoderPad: file explorer, editor, AI chat, test runner. — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- **[SURVEY, vendor]** CoderPad State of Tech Hiring 2026 (9th annual, 650+ participants): 82% of developers say GenAI is useful day to day, and 54% say their productivity would drop without it. — [CoderPad 2026 report](https://coderpad.io/survey-reports/coderpad-state-of-tech-hiring-2026/); [CoderPad blog](https://coderpad.io/blog/hiring-developers/new-research-the-2026-state-of-tech-hiring-what-ai-means-for-developers-and-hiring-teams/)

**SQL and data roles**
- **[CROWD/vendor analysis]** Interview Query's review of reports from Jan 2023 to Jun 2025: SQL appears in 39.4% of data-engineer reports and 19.8% of data-scientist reports; ML appears in 25.8% of DS reports. — [Interview Query: Data interview statistics 2026](https://www.interviewquery.com/p/data-interview-statistics-2026)
- **[CROWD/vendor analysis]** Dataford counts SQL questions per loop: Data Analyst 66, Data Engineer 44, Data Scientist 30. — [Dataford SQL Interview Report 2026](https://dataford.io/blog/sql-interview-report-2026)
- **[CROWD/vendor]** DE loops emphasize window functions (PARTITION BY, LEAD, LAG), with Amazon and Uber feedback cited, and add more business-context reasoning. — [DataDriven](https://datadriven.io/blog/sql-is-now-the-1-de-interview-filter-in-2026); [DataDriven DE 2026](https://www.datadriven.io/blog/data-engineering-interview-2026-whats-actually-tested-now)
- **[OFFICIAL, university career blog] July 15, 2026:** A data-analyst candidate was told AI would be available in the SQL round. The post argues that "if AI can write the query, writing the query isn't the test anymore." — [WSU ASCC blog](https://ascc.wsu.edu/blog/2026/07/15/data-analyst-interviews-are-changing-with-ai/)

### Inferences
- ICF-style "build a small stateful system in levels" is the format most worth adding to a Python-only practice platform. It is fully hand-written, needs no AI, and rewards clean class design that later levels can extend without a rewrite.
- Vendors are shifting from "output-only autograded" to "process plus follow-up questions," sometimes asked by an AI interviewer. A tutor that asks "why this approach?" and "what if the constraint changes?" after a correct submission mirrors where the platforms are going.
- For SQL, the live round is still usually no-AI at large companies (per secondary sources). Window functions, multi-step CTEs and business-framed questions are the reported focus.

### Gaps
- I did not find an official 2025–2026 description of the CodeSignal GCA format (question count, time limit, score range). The figures older blogs cite (e.g. a 300–850 or 200–600 scale) could not be verified as current.
- I found no official 2026 description of HackerRank's SQL question types or scoring.
- I could not read Karat's 2026 report or the full CoderPad PDF; numbers come from summaries.

---

## 4. Practical, "real-world" coding rounds: LRU cache, rate limiter, iterators, log parsing, OOP/LLD

### Takeaway
Practical rounds are well established at AI labs and fintech companies (OpenAI and Stripe per candidate reports; Anthropic and eBay via the CodeSignal ICF OA), and Big Tech is moving toward them (Microsoft "extending existing class logic," Apple "more real-world," Google/Meta reading existing codebases). The recurring problems are LRU cache, rate limiter, time-based key-value store, resumable iterator, in-memory database, and multi-part simulations. Each one starts simple and then gets new requirements.

### Cited Findings
- **[CROWD] OpenAI:**
  - LRU cache is described as the most common coding question, and interviewers extend it after the base version works.
  - Four recurring patterns: LRU cache, resumable iterator, time-based key-value store, and a rate limiter with per-key `allow(key)` (token bucket vs sliding-window log, and you defend the choice).
  - Phone screens often run one multi-part simulation for the whole hour (e.g. "Monster Fighting (Multi-part)").
  - — [IGotAnOffer: OpenAI coding interview](https://igotanoffer.com/en/advice/openai-coding-interview); [1point3acres OpenAI problems](https://www.1point3acres.com/interview/problems/company/openai)
- **[CROWD] Stripe:** A reported intern phone screen asked for a rate limiter with sliding and fixed windows, concurrency, and edge cases. — [1point3acres thread](https://www.1point3acres.com/interview/thread/1150333)
- **[CROWD] eBay and Anthropic:** CodeSignal ICF in-memory database in 4 levels (see Q3). — [LeetCode Discuss](https://leetcode.com/discuss/post/7316549/ebay-codesignal-oa-industry-coding-asses-8qbn/); [1point3acres](https://www.1point3acres.com/interview/thread/1049492)
- **[SURVEY] 2025 Big Tech question changes:**
  - Microsoft: "extending existing class logic," systems-level questions, modified LeetCode problems, wording that trips up LLMs.
  - Apple: "more real-world questions and fewer algorithmic ones."
  - Google: multi-part questions with abstract or multiple valid solutions and combined data structures.
  - Meta: longer, more complex setups.
  - — [Pragmatic Engineer, 2025-09-18](https://newsletter.pragmaticengineer.com/p/the-pulse-146)
- **[OFFICIAL] Canva (June 2025):** open-ended system-building prompt (airport takeoff/landing control system) with AI. — [Canva](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews)
- **[PRESS] Google (May 2026):** "code comprehension" round: read, debug and optimize an existing codebase. — [Asia Economy](https://www.asiae.co.kr/en/article/2026050809233801400)
- **[CROWD] Meta (Oct 2025):** fix a bug in a multi-file codebase, then implement and optimize. — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- **[PRESS] HackerRank Chakra (Oct 2026):** tasks based on a real-world repository. — [TechCrunch](https://techcrunch.com/2026/10/05/hackerranks-ai-interviewer-offers-a-glimpse-into-what-job-interviews-could-become/)
- **[CROWD]** Prep courses now sell "incremental coding" and "multi-level coding round" practice as a separate category. — [DataInterview: incremental coding](https://www.datainterview.com/courses/forward-deployed-engineer/incremental-coding); [Educative: multi-level coding round practice](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice)

### Inferences
- These rounds share three traits: (1) state kept across method calls (a class with several methods, not one function); (2) requirements that change mid-interview; (3) a judgement call to defend (which eviction or rate-limit algorithm). A pure "one function, one hidden test" LeetCode format practices none of these.
- Log or text parsing and iterator design fit a hand-written Python platform well: they test the standard library (`collections`, `heapq`, `bisect`, generators) and edge-case handling, not obscure algorithms.

### Gaps
- No primary or press source found for Rippling's machine-coding/LLD round, or for any specific company's "parse logs" question. These are common in prep lore but not verified here.
- No data on what share of loops at a given company are practical versus algorithmic.

---

## 5. Is LeetCode-style difficulty going up or down? Data on difficulty and novel vs. known problems

### Takeaway
At Big Tech, algorithm rounds are **not going away** (0 of 52 FAANG interviewers reported dropping them in 2025), and the evidence points to **harder and less recognizable** questions: variants, custom twists, multi-part setups. Startups moved faster away from algorithm questions. I found no rigorous public dataset measuring the share of novel versus known problems.

### Cited Findings
- **[SURVEY] 2025, interviewing.io (67 responses, 52 FAANG):**
  - 0 of 52 FAANG respondents said their company moved away from algorithmic questions.
  - 58% changed the kinds of algorithmic questions they ask.
  - 21% admit deliberately asking harder questions.
  - 75% believe AI lets weaker candidates pass.
  - Over half expect algorithm interviews to become less prominent in 2–5 years; about 20% think they will never go away.
  - The author says the bar to pass has risen in recent years, based on interviewing.io's own data.
  - — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot)
- **[PRESS/SURVEY] Sept 18, 2025:** A Pragmatic Engineer section is titled "Big Tech interview questions really are tougher." Per-company changes:
  - Meta: variants of popular questions, open-ended questions
  - Amazon: fewer copy-pasted LeetCode questions, more variants
  - Google: no LeetCode-style questions; multi-part questions with unusual terminology
  - Microsoft: modified LeetCode problems, more complex problems
  - Netflix: no change
  - — [Pragmatic Engineer, The Pulse #146](https://newsletter.pragmaticengineer.com/p/the-pulse-146)
- **[OLDER, ~2024]** Verbatim and lightly modified LeetCode questions were about equally easy to cheat on (73% vs 67% pass with secret ChatGPT). Only fully custom questions resisted. interviewing.io predicted companies would invest in more customized questions. — [interviewing.io](https://interviewing.io/blog/how-hard-is-it-to-cheat-with-chatgpt-in-technical-interviews)
- **[CROWD]** Meta's AI-enabled round problems are reportedly "harder than a medium LeetCode." Hello Interview advises practicing LeetCode *hards without AI* and studying backtracking, BFS/DFS, greedy, tries, DP basics and bitmasks. — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- **[OFFICIAL] Canva (June 2025):** "AI assistants can trivially solve traditional coding interview questions," which is why it replaced its CS-fundamentals screen. — [Canva](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews)
- **[SURVEY]** Startups: 67% said AI meaningfully changed their process, including dropping algorithmic questions and take-homes. Many startups have dropped algorithm questions entirely. — [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-pulse-146)

### Inferences
- The trend is two-sided. *Frequency* of pure LeetCode is flat at Big Tech and falling at startups. *Difficulty and novelty* of what remains is rising: variants, twists, multi-part. Memorizing a fixed list of "top 150" problems is less reliable than mastering patterns well enough to adapt to unfamiliar wording.
- The interviewing.io survey covers only interviewers in one company's network (n=67). It is directional, not representative.

### Gaps
- I found no quantitative source (Hello Interview, interviewing.io, Karat or LeetCode) measuring the share of novel versus known or tagged problems asked in 2025–2026, or a year-over-year difficulty index. The claims are surveys and anecdotes.
- No 2026 update of the interviewing.io survey was found; the newest data is 2025.

---

## 6. What this means for how to practice (for a hand-written Python and SQL platform with an AI tutor)

### Takeaway
LeetCode-style drilling should remain **one backbone, not the only one**. Big Tech still runs AI-free algorithm rounds, often with harder variants and more follow-up questions, and in-person rounds are returning, so fluent unaided Python remains essential. But the fastest-growing formats are multi-level, stateful, extend-your-code problems (CodeSignal ICF, OpenAI/Stripe practical rounds) and read/debug/extend-an-existing-codebase rounds (Meta, Google, HackerRank Chakra). Both should be added, along with an AI tutor that cross-examines the candidate the way interviewers now do.

### Cited Findings
**Hand-writing skill still decides the outcome**
- Meta's AI chat cannot write into the editor, so the candidate types every change. Phase 1 bug fixing may be AI-free. Prep advice includes practicing without AI or with a weak AI, reading unfamiliar code before fixing it, managing time (orientation plus phase 1 eat much of the hour), and being able to explain every line. — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- Countermeasures (in-person rounds, line-by-line questions, rapid-fire, re-asking) check real-time understanding. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-pulse-146); [interviewing.io](https://interviewing.io/blog/how-is-ai-changing-interview-processes-not-much-and-a-whole-lot); [Axios](https://www.axios.com/2025/08/12/in-person-job-interview-artificial-intelligence)

**What interviewers now score**
- Meta: problem solving, code quality (understanding the code), verification (running and testing edge cases), communication. — [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- Google: "AI fluency, including prompt engineering, output validation, and debugging skills." — [Asia Economy](https://www.asiae.co.kr/en/article/2026050809233801400)
- Canva: decomposing ambiguous requirements, fixing AI-generated code, production quality, defending the whole solution. — [Canva](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews)
- HackerRank Chakra asks "why this approach" and "how would it change under a new constraint." — [TechCrunch](https://techcrunch.com/2026/10/05/hackerranks-ai-interviewer-offers-a-glimpse-into-what-job-interviews-could-become/)

**Formats and problem types worth practicing**
- Multi-level stateful tasks (in-memory DB with CRUD, filtering, TTL and history; LRU-cache-plus-extensions; rate limiter; time-based KV store; resumable iterator). — [CodeSignal ICF datasheet](https://discover.codesignal.com/rs/659-AFH-023/images/CodeSignal-Industry-Coding-Framework-Datasheet.pdf); [IGotAnOffer OpenAI](https://igotanoffer.com/en/advice/openai-coding-interview); [LeetCode Discuss eBay ICF](https://leetcode.com/discuss/post/7316549/ebay-codesignal-oa-industry-coding-asses-8qbn/)
- SQL: window functions (PARTITION BY, LEAD/LAG) and business-context reasoning for DE and DA. SQL is heaviest in analyst loops (66 questions vs 30 for DS, per Dataford). — [DataDriven](https://datadriven.io/blog/sql-is-now-the-1-de-interview-filter-in-2026); [Dataford](https://dataford.io/blog/sql-interview-report-2026)

### Inferences (recommendations for the platform; not sourced facts)
1. **Keep the LeetCode-style backbone, and make it harder to memorize.**
   - Serve *variants*: renamed entities, extra constraints, a changed objective.
   - After a correct solution, have the tutor add a twist ("now the input streams," "now k queries," "now return all solutions").
   - This matches the variant and custom trend at Meta, Amazon, Microsoft and Google.
2. **Add a "multi-level / incremental" problem type (top priority).**
   - Level 1 through Level 4 specs, revealed one at a time, on the same class.
   - Hidden tests per level; time-box the whole task (~90 minutes, ICF-style).
   - Catalog seeds: in-memory DB (CRUD → filter/scan → TTL → backup/restore or history), LRU/LFU cache with extensions, rate limiter (fixed → sliding window → per-key → burst), time-based KV store, bank/transaction system, file system (mkdir/ls/size → move → quotas), task scheduler, resumable iterator.
   - Score how much code had to be *rewritten* between levels, as a design-quality signal.
3. **Add a "code reading / debug / extend" problem type.**
   - Give the user 2–5 short Python files with a planted bug plus a failing test. The user must find, explain and fix the bug, then add a feature.
   - This mirrors Meta's phase 1–2 and Google's code-comprehension round, and stays hand-written.
   - Optional variant: show "AI-generated" code with subtle bugs for the user to review. This practices the "output validation" skill Google and Canva score.
4. **Make the AI tutor act as interviewer, not only helper.**
   - After submission, require a spoken or written explanation: complexity, why this data structure, edge cases.
   - Ask line-specific "why" questions; re-ask a question later to check consistency; run a short rapid-fire round.
   - These copy documented interviewer tactics and HackerRank Chakra's follow-ups.
5. **Two practice modes.** "AI-off" (no hints, no autocomplete, timer; simulates in-person or proctored rounds) and "AI-on" (tutor available, but the user must type all code and the transcript is graded on verification and ownership, as at Meta and Google). Hints should cost score in AI-off mode.
6. **Time-boxing and narration.** Use realistic timers: about 20–25 min for one medium in a 45-min loop slot; about 60 min for a multi-phase codebase task; about 90 min for a 4-level ICF task. Add a "think aloud" text box graded for clarity.
7. **Debugging without autocomplete.** In AI-off mode, use an editor with no autocomplete, and show only test failure messages, no stack-trace hints. Interviews increasingly run in CoderPad-style pads or in person, where IDE help is minimal.
8. **SQL track.**
   - Add business-framed, multi-step questions (CTE chains, window functions, gaps-and-islands, retention/funnel, dedup with ROW_NUMBER).
   - Have the tutor ask about correctness (NULLs, ties, duplicates) and performance (indexes, join order).
   - Add a "debug this SQL" item type parallel to the Python debug type.
   - Live SQL rounds at most large companies are reportedly still no-AI, so fluent hand-written SQL remains the core skill.

### Gaps
- No controlled evidence links any particular practice method (e.g. multi-level tasks vs LeetCode volume) to interview pass rates. The recommendations above are inferred from format changes, not measured outcomes.
- Recommended timers are based on reported formats (Meta ~60 min, ICF ~90 min per secondary sources). Company time limits vary and are not officially published.
