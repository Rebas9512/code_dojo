# Coding-interview formats and high-frequency problems: Uber, TikTok/ByteDance, Oracle, Infosys, Goldman Sachs, Salesforce, LinkedIn, IBM, Visa, Walmart Global Tech, Nvidia, Snowflake, Airbnb, Pinterest (as of Nov 2026)

Method and source notes (read first):
- **Problem-frequency data** comes from the GitHub repo `liquidslr/leetcode-company-wise-problems` (35.7k stars; last commit "Update Problem [Oct 20]" on 2026-10-21; README still says "updated as of 1 June 2025"). It has per-company CSVs (30 days / 3 months / 6 months / >6 months / All) with a 0–100 "Frequency" score, difficulty and topics — [repo](https://github.com/liquidslr/leetcode-company-wise-problems). The data is crowd-scraped LeetCode company-tag data, not official. I downloaded the CSVs on 2026-11-22 and computed the rankings, difficulty mix, topic counts and overlap myself. I mapped LeetCode IDs from the public LeetCode GraphQL problem list on the same day (4,123 problems). "$" marks a Premium-only problem.
- The repo's "All" sizes are close to, but not exactly, the counts the user saw on leetcode.com: Uber 336 (user saw 326), TikTok 317 (290), Oracle 282 (272), Infosys 254 (263), Goldman Sachs 246 (245), Salesforce 196 (185), LinkedIn 171 (173), IBM 166 (161), Visa 150 (148), Walmart Labs 135 (131), Nvidia 131 (120), Snowflake 100 (97), Airbnb 62 (61), Pinterest 41 (39). There is also a separate ByteDance tag with 59 problems. Per-company folders: [Uber](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Uber), [TikTok](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/TikTok), [ByteDance](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/ByteDance), [Oracle](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Oracle), [Infosys](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Infosys), [Goldman Sachs](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Goldman%20Sachs), [Salesforce](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Salesforce), [LinkedIn](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/LinkedIn), [IBM](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/IBM), [Visa](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Visa), [Walmart Labs](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Walmart%20Labs), [Nvidia](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Nvidia), [Snowflake](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Snowflake), [Airbnb](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Airbnb), [Pinterest](https://github.com/liquidslr/leetcode-company-wise-problems/tree/main/Pinterest).
- **Process information** is almost entirely crowd-sourced (Glassdoor, LeetCode Discuss, 1point3acres, Blind) or from commercial prep sites (interviewing.io, Hello Interview, aced.io/TryExponent, Interview Query, Lodely). Several official pages (Uber's engineering blog, Goldman Sachs' HackerRank guide, Infosys' HackWithInfy page) appeared in search results but returned 404/403 when fetched on 2026-11-22. Those claims rely on search snippets and are marked as such.
- Tags used below: **[official]**, **[crowd]** (candidate self-reports), **[prep-site]** (commercial guide, partly crowd-derived), **[data]** (my computation from the GitHub CSVs).

---

## 1. Process and OA format per company (2025–2026): platform, number of coding rounds, time limits, difficulty

### Takeaway
Most companies here start with a timed OA. Uber and Visa use CodeSignal, typically about 4 questions in about 70 minutes. TikTok, Goldman Sachs, Salesforce, Oracle and Walmart use HackerRank. A live loop of 2–4 coding rounds follows. Four formats stand out:
- **Airbnb:** practical, multi-part problems. Since 2024 a code-review round has replaced the second coding round.
- **Uber:** machine-coding/LLD rounds, mostly in India SDE-2 reports.
- **Goldman Sachs:** the HackerRank OA includes a "Software Diagnostics" exercise that has candidates debug a Django, Node.js or Spring Boot app.
- **Infosys:** HackWithInfy is a 3-hour, 3-problem contest-style test (India only).

### Cited Findings

**Uber (US + India)**
- OA: candidates describe a proctored CodeSignal General Coding Assessment with 4 questions in 70 minutes [crowd] — [Glassdoor review](https://www.glassdoor.com/Interview/Uber-Interview-E575263-RVW98951783.htm); [1point3acres "Uber 2025 New Grad Online Test Review: 4 Coding Questions on CodeSignal"](https://www.1point3acres.com/interview/thread/1134971). A Toronto new-grad report (June 2025) says the OA must be finished within 3 days of the invite [crowd] — [Taro](https://www.jointaro.com/interviews/companies/uber/experiences/swe-new-grad-toronto-on-june-1-2025-no-offer-positive-214e1f33). One reported difficulty mix is 2 easy, 1 medium and 1 hard [crowd] — [Glassdoor](https://www.glassdoor.co.in/Interview/Uber-Interview-E575263-RVW97575516.htm).
- Variant: "a customized CodeSignal OA with two medium-level algorithm/data-structures problems, not standard LeetCode questions" [crowd] — [Glassdoor question](https://www.glassdoor.ca/Interview/The-screen-was-a-customized-CodeSignal-OA-with-two-medium-level-algorithm-data-structures-problems-not-standard-leetcode-qu-QTN_8541384.htm). A Blind thread says the new CodeSignal scores are "out of like 600" [crowd, secondhand] — [Blind](https://www.teamblind.com/post/uber-codesignal-assessment-update-passed-frjrzgso).
- Official: Uber's engineering blog says candidates solve coding problems on CodeSignal or a whiteboard, and that the phone screen uses a shared CodeSignal editor [official, search snippet only; URL returned 404 on fetch] — [Uber blog](https://www.uber.com/en-EG/blog/engineering-interview-process).
- Loop: interviewing.io describes a second coding round "focused on depth in a specialization" that is sometimes "not an algorithmic question at all" [prep-site] — [interviewing.io Uber](https://interviewing.io/uber-interview-questions). A 2025 new-grad account describes a 1-hour LeetCode screen followed by a 3-round loop [crowd] — [Glassdoor](https://www.glassdoor.com/Interview/Uber-Interview-E575263-RVW92179321.htm).
- Machine coding/LLD (mostly India SDE-2, 2020–2025) [crowd; I did not verify each thread individually]:
  - Candidates get a problem statement, design OO classes, then implement and run the code on CodeSignal or CoderPad.
  - Reported prompts: a multithreaded job scheduler with task prerequisites (2022), an in-memory Kafka-like queue with producers and consumers (2020), a parking lot, and file-system APIs (mkdir/pwd/cd). Candidates stress preparing concurrency.
  - Sources: [LC Discuss 2396265](https://leetcode.com/discuss/interview-experience/2396265/), [LC Discuss 2463807](https://leetcode.com/discuss/interview-experience/2463807/), [LC Discuss 943350](https://leetcode.com/discuss/interview-experience/943350/uber-sde-ii-bangalore-oct-nov-2020-offer), [LC Discuss 7182332](https://leetcode.com/discuss/post/7182332/uber-sde-2-interview-experience-l4-banga-fd1d/), [LC Discuss 7300207](https://leetcode.com/discuss/post/7300207/uber-software-engineer-ii-se-2-bangalore-wyl8/).
- Tag difficulty [data]: 12% easy, 57% medium, 30% hard (336 problems). Uber's hard share is among the highest of these 14 companies (only Pinterest at 36% and Airbnb at 33% are higher). Top topics: Array, String, Hash Table, BFS, DFS, DP, Graph, Heap.

**TikTok / ByteDance (US)**
- OA: HackerRank for recent grads, due 5–7 days after the invite, 120 minutes with the camera on. Reported formats are 3 medium DS&A questions, or 5 questions mixing SQL, array/string and OOP. Experienced hires generally skip the OA [prep-site, page © 2026] — [aced.io (formerly TryExponent) TikTok SWE guide](https://www.aced.io/guides/tiktok-software-engineer-interview).
- An August 2025 internship OA had 4 questions in 70 minutes: 2 easy and 2 LeetCode medium [crowd] — [Glassdoor](https://static.glassdoor.de/Interview/TikTok-Software-Engineer-Internship-Interview-Questions-EI_IE2230881.0,6_KO7,35_IP5.htm).
- Loop: 2–3 technical interviews of 45 minutes each on CoderPad or HackerRank, usually on the same day, plus system design for experienced hires. The guide says the loop takes at least 2 months and that TikTok rotates questions once many candidates pass them [prep-site] — [aced.io](https://www.aced.io/guides/tiktok-software-engineer-interview). Interview Query notes the process "is not standardized and varies significantly by role" [prep-site, 2026] — [Interview Query TikTok](https://www.interviewquery.com/interview-guides/tiktok).
- Tag difficulty [data]: 8% easy, 70% medium, 20% hard (317 problems), the most medium-heavy tag in the set. The ByteDance tag (59 problems) is 81% medium.

**Oracle (US OCI + India)**
- The usual first step is a HackerRank OA, with aptitude + coding in campus/India reports. One source describes a two-hour challenge on HackerRank or CoderPad [crowd] — [Glassdoor](https://www.glassdoor.com/Interview/Oracle-Interview-E1737-RVW98327066.htm).
- OCI IC3/SMTS screen: "two random coding problems on HackerRank… similar to Codeforces A/B level", all tests must pass, followed by distributed-systems basics [crowd] — [LC Discuss 6814795](https://leetcode.com/discuss/interview-experience/6814795).
- Another report describes 5 rounds. Round 1 is DSA on HackerRank/CodePair with 2 medium problems (arrays, hashmaps, sliding window) [crowd] — [LC Discuss 7330761](https://leetcode.com/discuss/interview-experience/7330761). See also the [1point3acres "Oracle OCI SWE: 6 rounds" thread](https://www.1point3acres.com/interview/thread/1165134).
- OCI uses "Bartender" rounds, run by an engineer from a different team, focused on behavior and projects. Typical loops have 4–6 rounds [prep-site] — [TryExponent Oracle guide](https://www.tryexponent.com/guides/oracle-software-engineer-interview).
- Tag difficulty [data]: 18% easy, 64% medium, 17% hard.

**Infosys (India-specific; mass hiring)**
- HackWithInfy (HWI) Round 1: a 3-hour online test with 3 problems and no negative marking. The reported cut-off is about 1.5–2 problems solved. Sources disagree on difficulty ("Medium" vs "High"). Topics: DP, greedy, backtracking, stack/queue, graphs, trees, strings/arrays [prep-site] — [placementpreparation.io HWI pattern 2025](https://www.placementpreparation.io/hackwithinfy/syllabus-and-test-pattern/).
- Round 2 (Grand Finale) is a 48-hour or multi-day hackathon; sources conflict on the length [prep-site] — same source; [PrepInsta HWI](https://prepinsta.com/hackwithinfy/).
- Official: HWI gives pre-placement interviews for the **Specialist Programmer** role and other specialised-unit roles [official, search snippet; page returned 403] — [infosys.com HWI](https://infosys.com/careers/hackwithinfy.html). An official 2026 edition terms PDF exists — [HWI 2026 T&C](https://www.infosys.com/careers/hackwithinfy/2026/hwi-terms-conditions.pdf).
- Reported packages: Specialist Programmer ₹9.5 LPA and Digital Specialist Engineer ₹6.25 LPA [third-party campus page] — [Acharya campus drive page](https://www.acharya.ac.in/events/placement/infosys-campus-drive). Other sources give different figures.
- Tag difficulty [data]: 21% easy, 54% medium, 24% hard. The pool is split: very easy classics (1 Two Sum, 9, 20, 70, 242, 283, 860) sit alongside contest-hard problems (3336, 2940, 1872), which matches HWI's "easy + medium + hard" three-problem shape.

**Goldman Sachs (US + India)**
- OA platform: HackerRank. All applicants take a "Software Fundamentals" challenge. Engineering applicants also take a "Software Diagnostics" challenge that has them debug a Django, Node.js or Spring Boot application. Duration varies: one SWE reported a 75-minute DS screen, another got 2 questions in 90 minutes. Sample problems are labelled Easy/Medium [prep-site, page dated 2026-10-24] — [Lodely GS OA](https://www.lodely.com/companies/goldman-sachs/online-assessment).
- A 2025 Engineering Analyst OA was a 90-minute HackerRank test with 2 DSA questions [crowd] — [1point3acres 1082289](https://www.1point3acres.com/interview/thread/1082289). A 2025 India Analyst report describes 60 minutes with 3 coding problems plus MCQs on DSA, OOP and quant [crowd; search snippet; probably this thread] — [LC Discuss 7289995](https://leetcode.com/discuss/interview-experience/7289995).
- In a CoderPad round (2025), the reported problems were House Robber (198) and Car Pooling (1094) [crowd] — [1point3acres 7235919](https://www.1point3acres.com/interview/post/7235919).
- Official: GS publishes a "guide to HackerRank" on its careers blog [official; returned 403 on fetch, content not verified] — [GS careers blog](https://www.goldmansachs.com/careers/blog/guide-to-hackerrank).
- Tag difficulty [data]: 17% easy, 64% medium, 18% hard. GS has notably more math/simulation problems than the others: 166 Fraction to Recurring Decimal, 1823 Find the Winner of the Circular Game, 1648 Sell Diminishing-Valued Colored Balls, 1086 High Five.

**Salesforce (US + India AMTS)**
- OA: HackerRank, 90 minutes, 3 coding problems. An India campus AMTS candidate called it easier than earlier Salesforce OAs [crowd] — [LC Discuss 8514030](https://leetcode.com/discuss/post/8514030/salesforce-amts-interview-experience-ind-ijyg/); a New Grad 2026 AMTS report also mentions 3 OA questions — [LC Discuss 8488321](https://leetcode.com/discuss/post/8488321/salesforce-amts-interview-experience-new-csmd/).
- Loop: 2 technical rounds plus a hiring-manager round [crowd] — same sources. Glassdoor rates AMTS difficulty 3/5 [crowd] — [Glassdoor](https://www.glassdoor.com/Interview/Salesforce-Interview-E11159-RVW99280293.htm).
- Tag difficulty [data]: 12% easy, 61% medium, 26% hard. The top of the list is dominated by recent contest-numbered problems: 2571, 2380, 3398/3399, 3488, 3035, 3607, 3613, 3893$. This pattern usually means the tag is fed by HackerRank OA questions that candidates matched to LeetCode equivalents (inference).

**LinkedIn (US)**
- Phone screen: 1 hour, often with two interviewers [prep-site] — [interviewing.io LinkedIn](https://interviewing.io/linkedIn-interview-questions). Several reports describe 2 coding questions in the screen, at easy-to-medium level [crowd] — [Glassdoor](https://www.glassdoor.ca/Interview/LinkedIn-Software-Engineer-Interview-Questions-EI_IE34865.0,8_KO9,26.htm).
- Onsite (2025–26 report): a standard coding round, a **"coding with AI" round**, a hiring-manager round, system design, and a project deep dive [crowd; search snippet; page returned 403] — [LC Discuss 8359456](https://leetcode.com/discuss/post/8359456/linkedin-software-engineer-interview-exp-dp7a/).
- Difficulty: "mostly medium… medium LeetCode problems with follow-ups" [prep-site] — [Interview Query LinkedIn](https://www.interviewquery.com/guides/linkedin-software-engineer).
- Tag [data]: 14% easy, 64% medium, 21% hard. It is the most Premium-heavy pool after Airbnb and Pinterest (32 of 171 are Premium), built on LinkedIn "classics": 716$, 364$, 339$, 244$, 277$, 366$, 156$.

**IBM (US + India)**
- The coding assessment includes SQL: one report describes a PostgreSQL question (joins + GROUP BY + HAVING + ORDER BY on customer/site resource usage) [crowd] — [LC Discuss 8504767](https://leetcode.com/discuss/post/8504767/ibm-coding-assesment-question-customer-r-a9yl/). A January 2026 Glassdoor reviewer says questions "focused on SQL and LeetCode-style problem solving" [crowd] — [Glassdoor](https://www.glassdoor.co.uk/Interview/They-asked-questions-focused-on-SQL-and-LeetCode-style-problem-solving-mainly-testing-logical-thinking-data-handling-and-QTN_8806577.htm). See also the 2024 OA SQL discussion — [1point3acres 1023174](https://www.1point3acres.com/interview/thread/1023174).
- Platform: I could not confirm whether IBM's current assessment runs on HackerRank (gap).
- Tag [data]: 30% easy, 59% medium, 10% hard, the easiest of these 14 companies. Top problems: 412 Fizz Buzz, 12/13 Roman conversions, 56, 3, 121, 1, 20.

**Visa (US + India)**
- OA: CodeSignal, 4 questions in about 70–75 minutes. Reported mixes are "2 easy, 1 medium, 1 hard" or "2 easy, 2 medium-hard" [crowd] — [Glassdoor](https://www.glassdoor.com/Interview/Visa-Inc-Interview-E3035-RVW100890407.htm), [Glassdoor UK](https://www.glassdoor.co.uk/Interview/Visa-Inc-Interview-E3035-RVW99849879.htm).
- Variant: a Bellevue new-grad candidate (October 2025) had 3 HackerRank questions (2 easy, 1 medium) [crowd] — [Glassdoor](https://static.glassdoor.com.br/Interview/Visa-Inc-New-Grad-Software-Engineer-Interview-Questions-EI_IE3035.0,8_KO9,35_IP2.htm). An India SWE report is at [LC Discuss 6817721 (Bangalore, May 2025)](https://leetcode.com/discuss/post/6817721/visa-software-engineer-bangalore-may-202-qcpc/).
- Tag [data]: 22% easy, 61% medium, 16% hard. The top-20 contains many CodeSignal-style grid and simulation tasks: 68 Text Justification (#1), 3459 V-Shaped Diagonal, 1861 Rotating the Box, 3071 Letter Y on a Grid, 2768 Number of Black Blocks, 2672 Adjacent Elements Same Color, 3161 Block Placement Queries.

**Walmart Global Tech (US + Bengaluru)**
- OA: HackerRank, with a LeetCode-style problem plus a **debugging task done with an AI assistant**. Another candidate reports one coding question, one SQL query and 2 MCQs [crowd; Glassdoor, individual attribution via search snippets] — [Glassdoor (Feb 2026 intern)](https://static.glassdoor.ca/Interview/Walmart-Global-Tech-Software-Engineer-Internship-Interview-Questions-EI_IE3293060.0,19_KO20,48.htm), [Glassdoor (Nov 2024)](https://www.glassdoor.com/Interview/Walmart-Global-Tech-Interview-E3293060-RVW99558187.htm).
- Several reports describe a **Karat** third-party first technical round: LeetCode easy, then medium [crowd] — [Glassdoor](https://www.glassdoor.com/Interview/Walmart-Global-Tech-Interview-E3293060-RVW91885501.htm).
- Senior/India loops include LLD, HLD, coding and a hiring-manager round. A Bengaluru SDE3 had a DSA round with 2 LeetCode mediums plus an order-schema design [crowd] — [Glassdoor (Bengaluru, May 2025)](https://www.glassdoor.com/Interview/Walmart-Global-Tech-Interview-E3293060-RVW103608610.htm).
- Tag [data]: 15% easy, 66% medium, 17% hard. The top-20 is almost entirely universal classics (3, 200, 20, 22, 42, 56, 146, 1, 49, 33, 139).

**Nvidia (US)**
- Process (based on 2024 conversations): recruiter, technical phone screen, hiring-manager call, then an onsite with two coding rounds, system design and a domain-specific coding round [prep-site] — [interviewing.io Nvidia](https://interviewing.io/nvidia-interview-questions).
- Reported topics [prep-site, crowd-derived] — [Interview Query Nvidia](https://www.interviewquery.com/guides/nvidia-software-engineer):
  - Merge k sorted lists with complexity follow-ups, and linked lists in C.
  - Threads vs processes, fork, mutex vs semaphore, C++ destructor/exception behaviour, bit manipulation, and false sharing.
  - A 16-byte-aligned `malloc16`.
- OA: a CodeSignal or HackerRank link with "low-level nuances such as bit manipulation"; the sample given is Bitwise AND of a Range (LC 201) [prep-site] — [Lodely Nvidia OA](https://www.lodely.com/companies/nvidia/online-assessment). A 2026 Glassdoor OA report lists 3 DSA questions: easy array, hard heap, medium 2D DP [crowd; search snippet].
- Questions "vary greatly depending on the role and team" [prep-site] — [TryExponent Nvidia](https://www.tryexponent.com/guides/nvidia-software-engineer-interview).
- Tag [data]: 22% easy, 64% medium, 12% hard. Bit manipulation appears (190 Reverse Bits, 761 Special Binary String at #1), and design problems appear (146, 622 Design Circular Queue).

**Snowflake (US)**
- Process: recruiter call (30 min), optional hiring-manager screen, a **2-hour technical phone screen** (DSA + system design) on CoderPad, then an onsite with presentation, coding, "expertise" (coding, design or a language deep dive), behavioral and close rounds. A December 2025 edit notes some candidates went through team matching [prep-site] — [interviewing.io Snowflake](https://interviewing.io/snowflake-interview-questions).
- Coding is "around a LeetCode medium" with a Snowflake twist and a database-internals flavour. Example: aggregating log files efficiently. System design focuses on data systems, e.g. storing time-stamped events for fast insert and retrieval [prep-site] — same source.
- One candidate titled their write-up "Snowflake SDE 5 round interview experience, very hard" [crowd] — [LC Discuss 6930095](https://leetcode.com/discuss/post/6930095/snowflake-sde-5-round-interview-experien-ytqe/). A Glassdoor report mentions log parsing with concurrency plus Linux, networking and container questions [crowd; search snippet, review not individually verified] — [Glassdoor Snowflake](https://www.glassdoor.com/Interview/Snowflake-Interview-E928471-RVW97608629.htm).
- Tag [data]: 14% easy, 65% medium, 21% hard. Design (18 problems) and DFS/graph topics are unusually prominent: 588$ Design In-Memory File System, 1600 Throne Inheritance, 2050 Parallel Courses III, 210/207 Course Schedule, 212 Word Search II.

**Airbnb (US)**
- Senior (G9) loop: recruiter (30 min), coding screen (60 min, CoderPad), system design screen (60 min), then an onsite with coding (60 min in a laptop IDE, screen-shared), **code review** (60 min; "introduced in 2024 to replace the second traditional coding interview"), system design, technical experience and behavioral [prep-site, updated 2026-02-11] — [Hello Interview Airbnb G9](https://www.hellointerview.com/guides/airbnb/g9).
- Screen problems "resemble everyday engineering work", such as an LRU cache, a time-series iterator or a stateful class, and come with layered follow-ups. Most-asked: 1298, 631$, 1235, plus non-LeetCode problems (URL query-string parser, payment management system). One candidate says "Airbnb asks 1 hard problem per coding interview" [prep-site] — same source.
- No pseudocode: the solution must be correct, clean and pass test cases [prep-site] — [TryExponent Airbnb](https://www.tryexponent.com/guides/airbnb-software-engineer-interview). Problems arrive "wearing Airbnb clothes (bookings, listings, availability windows, itineraries)" and DP is over-represented [prep-site] — [techinterview.org Airbnb](https://www.techinterview.org/post/3233476842/airbnb-interview-guide/).
- Tag [data]: 17% easy, 48% medium, 33% hard (62 problems).

**Pinterest (US)**
- Format: a coding screen followed by 4 rounds (2 coding, 1 system design, 1 behavioral). One candidate had a 90-minute OA with two medium-to-hard algorithm questions, then a phone screen with one problem [crowd; Glassdoor, via search snippets] — [Glassdoor](https://www.glassdoor.com/Interview/Pinterest-Interview-E503467-RVW98686991.htm), [Glassdoor](https://www.glassdoor.co.in/Interview/Pinterest-Interview-E503467-RVW95828613.htm).
- Reported problems: reconstruct a route from unordered tickets (= 332), overlapping intervals, a DP medium, a sparse-matrix class (March 2025), and building a GitHub-style contribution heatmap from an API. Glassdoor rates difficulty 3.3/5, with 46% positive experiences and about 40 days to hire [crowd] — same Glassdoor set.
- Tag [data]: 2% easy, 60% medium, 36% hard (41 problems), the hardest pool in this set.

### Inferences
- **Platform grouping for OA-simulation features:**
  - CodeSignal GCA-style (4 tasks / 70 min; simulation and grid-heavy): Uber, Visa, and sometimes Nvidia.
  - HackerRank (2–3 problems / 90–120 min): TikTok, Goldman Sachs, Salesforce, Oracle, Walmart, and likely IBM.
  - Contest-style (3 problems / 3 hours): Infosys HWI.
  - Live CoderPad or IDE without an OA: Airbnb, Snowflake, LinkedIn (experienced hires).
- **Non-LeetCode formats a practice platform could tag:**
  - Code review/debugging: Airbnb code-review round; GS Software Diagnostics; Walmart AI-assisted debugging.
  - Machine coding/LLD with concurrency: Uber (India).
  - AI-assisted coding: LinkedIn "coding with AI" (2025–26).
  - Systems/C++ trivia: Nvidia.
  - Database-internals-flavoured coding: Snowflake.
  - Contest-style 3-hour test: Infosys HWI.

### Gaps
- No official 2025–26 process page could be fetched for any of the 14 companies: the Uber blog returned 404, and the GS and Infosys pages returned 403. Round counts and timings are therefore crowd or prep-site level.
- IBM's OA platform, Nvidia's standard OA format, and Snowflake's new-grad OA (if any) could not be confirmed.
- The LinkedIn "coding with AI" round comes from a single report; its prevalence is unknown.
- I found no reliable US data on Uber's machine-coding round. The evidence is predominantly India SDE-2, much of it from 2020–2024.

---

## 2. Top reported problems and patterns per company; what recurs across companies

### Takeaway
A small core of about 20 universal problems appears in nearly every list: 200, 1, 146, 56, 20, 3, 49, 42, 23, 121, 53, 33, 5, 15, 347. Each company's distinctive signal is in a handful of "signature" problems:
- Uber: 815, 269, 305, 1438, 427
- LinkedIn: 716, 364, 244, 432
- Snowflake: 588, 2050, 1600
- Airbnb: 68, 1235, 1298, 631, 251, 755
- Pinterest: 332, 465, 282, 1055
- Visa: 68 plus CodeSignal grid/simulation problems
- Goldman Sachs: 42, 4, 1086, 166, 1648
- Nvidia: 761, 93, 190

### Cited Findings

Top problems by all-time frequency [data] — source: [liquidslr repo](https://github.com/liquidslr/leetcode-company-wise-problems) (per-company links in the header). "Recent" = the repo's 6-month list.

- **Uber** — All-time: 815 Bus Routes (H), 269 Alien Dictionary (H$), 1438 Longest Continuous Subarray w/ Abs Diff ≤ Limit (M), 305 Number of Islands II (H$), 427 Construct Quad Tree, 200 Number of Islands, 977, 1429 First Unique Number$, 230, 564 Find the Closest Palindrome (H), 2858 Min Edge Reversals (H), 79, 362 Design Hit Counter$, 380, 146, 729 My Calendar I, 2791 (H), 121, 238, 3161 Block Placement Queries (H). Recent: 1429$, 305$, 977, 2858, 815, 1475, 1101$, 427, 871, 200, 1438, 269$. Patterns: graph BFS/union-find (815, 305, 1101, 200), topo sort (269), monotonic deque/sliding window (1438), design with hash maps (362, 380, 146, 1429, 729).
- **TikTok** — All-time: 146 LRU, 200, 253$ Meeting Rooms II, 300 LIS, 694$ Distinct Islands, 3, 207, 56, 68 Text Justification, 42, 51 N-Queens, 827 Making a Large Island, 33, 54, 76, 394 Decode String, 210, 560, 79, 322. Recent: 146, 200, 253$, 394, 432 All O`one, 827, 56, 207, 787, 694$, 25, 3161. Patterns: grid DFS/BFS (islands family), intervals, topo sort, DP (300, 322), stack parsing (394).
- **ByteDance** (separate tag, 59 problems): 146, 200, 316/1081 (monotonic-stack duplicates), 1997, 207, 56, 934, 39, 198, 2502, 127, 33, 394, 227 Basic Calculator II.
- **Oracle** — All-time: 146, 1, 3, 200, 49, 347, 239 Sliding Window Max, 23, 20, 253$, 33, 460 LFU Cache, 56, 206, 1209, 5, 11, 15, 54, 394. Recent: 200, 1, 33, 23, 253$, 394, 49, 18, 721 Accounts Merge, 787, 1209, 3. Patterns: generic classics, with cache design (146/460) prominent.
- **Infosys** — All-time: 1, 3, 176 Second Highest Salary (SQL), 121, 560, 53, 134 Gas Station, 860 Lemonade Change, 3336 (H), 9, 5, 198, 11, 20, 70, 2940 (H), 1872 (H), 242, 283, 3467. Recent: 860, 1, 3, 176, 121, 53, 72 Edit Distance, 875 Koko, 70, 200, 11, 56. Patterns: DP is the #2 topic (78 problems), plus greedy, prefix sum and math.
- **Goldman Sachs** — All-time: 42 Trapping Rain Water, 4 Median of Two Sorted Arrays, 387, 1086$ High Five, 166 Fraction to Recurring Decimal, 64 Min Path Sum, 11, 146, 3, 443 String Compression, 56, 200, 33, 49, 1823, 121, 1648, 1, 153, 516. Recent: 42, 1648, 516, 2791, 2948, 4, 1086$, 166, 790, 11, 64, 387. Lodely's 2026 list of GS OA problems matches the tag: 42, 64, 443, 11, 125, 49, 20, 3, 62, 146 [prep-site] — [Lodely](https://www.lodely.com/companies/goldman-sachs/online-assessment). Patterns: arrays/two pointers, grid DP, string compression/parsing, math.
- **Salesforce** — All-time: 2571, 443, 460 LFU, 2380, 3488, 3398/3399, 628, 713, 3035, 146, 2957, 1297, 3607, 210, 115, 3613, 56, 1221, 3540$. Recent: 2571, 443, 2380, 3893$, 56, 2551, 460, 210, 2366, 2858, 735, 628. Patterns: string manipulation, greedy, heap, cache design.
- **LinkedIn** — All-time: 716$ Max Stack, 364$ Nested List Weight Sum II, 432 All O`one, 1004, 244$ Shortest Word Distance II, 53, 339$, 277$ Find the Celebrity, 20, 127, 605, 366$, 380, 17, 200, 152, 34, 156$, 50, 319. Recent: 364$, 716$, 605, 319, 17, 53, 381, 152, 244$, 20, 272$, 200. Patterns: data-structure design (716, 432, 380/381, 244), nested lists/trees, binary search.
- **IBM** — All-time: 412 Fizz Buzz, 56, 12, 3, 121, 1, 13, 20, 2580, 5, 560, 3159, 3402, 845, 49, 3175, 2545, 242, 2907$, 2921$. Recent: 3820, 20, 1648, 56, 1797, 412, 12, 11, 242, 2645, 324, 5. Patterns: easy string/array, sorting, two pointers.
- **Visa** — All-time: 68 Text Justification, 3459, 3, 1, 1861 Rotating the Box, 3071, 15, 146, 3043, 3046, 121, 56, 3161, 2768, 49, 1389, 2672, 42, 71 Simplify Path, 5. Recent: 526, 636 Exclusive Time of Functions, 3, 2484, 3919, 2964$, 56, 2680, 1963, 32, 928, 924. Patterns: matrix/grid simulation, string formatting, stack.
- **Walmart Labs** — All-time: 3, 200, 20, 22, 42, 56, 146, 1, 49, 33, 139 Word Break, 2406, 876, 740 Delete and Earn, 11, 15, 1977, 2072$ (SQL), 2179, 2449. Recent: 740, 56, 1200, 870, 49, 239, 347, 20, 200, 716$, 210, 139.
- **Nvidia** — All-time: 761 Special Binary String (H), 146, 121, 1, 3, 23, 49, 20, 93 Restore IP Addresses, 1046, 2592, 33, 53, 200, 2571, 412, 42, 1610, 11, 190 Reverse Bits. Recent: 49, 146, 93, 743, 875, 121, 347, 200, 394, 23, 622 Design Circular Queue, 138. Patterns: classics plus bit manipulation, linked lists and queue/cache design.
- **Snowflake** — All-time: 202 Happy Number, 2050 Parallel Courses III, 588$ In-Memory File System, 210, 76, 212 Word Search II, 2303, 42, 1600 Throne Inheritance, 2096, 2742, 438, 1235, 2062, 3155$, 2856, 3176/3177, 207, 23. Recent: 2050, 588$, 42, 2062, 2303, 202, 1600, 243$, 2096, 3092, 427, 347. Patterns: topological sort/DAG scheduling, tree/file-system design, trie + DFS.
- **Airbnb** — All-time: 68 Text Justification, 1235 Max Profit in Job Scheduling, 251$ Flatten 2D Vector, 1298 Max Candies from Boxes, 1257$, 631$ Design Excel Sum Formula, 160, 755$ Pour Water, 42, 773 Sliding Puzzle, 219, 269$, 336 Palindrome Pairs, 2043 Simple Bank System, 3076, 1557, 751$ IP to CIDR, 759$ Employee Free Time, 1, 2. Recent: 631$, 1235, 3076, 68, 1125, 973, 1257$, 1298. This agrees with the Hello Interview "most asked" list (1298, 631, 1235) — [Hello Interview](https://www.hellointerview.com/guides/airbnb/g9). Patterns: simulation/implementation (68, 755, 631, 2043), interval DP (1235), BFS state search (773, 1298).
- **Pinterest** — All-time: 332 Reconstruct Itinerary (H), 465$ Optimal Account Balancing (H), 815 Bus Routes (H), 282 Expression Add Operators (H), 1055$, 322, 2302, 494 Target Sum, 410 Split Array Largest Sum, 642$ Design Search Autocomplete, 392, 571$ (SQL), 720, 1293, 2402 Meeting Rooms III, 1110, 43, 1723, 1580$, 1564$. Patterns: backtracking (282, 465, 1723), graph/Euler path (332), binary search on answer (410), heap scheduling (2402). The 332 entry matches a Glassdoor report ("reconstructing a route from unordered travel tickets") [crowd] — [Glassdoor](https://www.glassdoor.com/Interview/Pinterest-Interview-E503467-RVW98686991.htm).

**Cross-company recurrence** [data]. Counts are how many of the 14 company "All" lists contain the problem, and in how many it ranks in the top 50:

| Problem | In N lists | In top 50 of N lists |
|---|---|---|
| 200 Number of Islands | 13 | 11 |
| 56 Merge Intervals | 12 | 11 |
| 146 LRU Cache | 12 | 10 |
| 1 Two Sum | 13 | 10 |
| 49 Group Anagrams | 10 | 9 |
| 3 Longest Substring Without Repeating Characters | 11 | 9 |
| 20 Valid Parentheses | 12 | 9 |
| 121 Best Time to Buy and Sell Stock | 11 | 8 |
| 23 Merge k Sorted Lists | 12 | 8 |
| 42 Trapping Rain Water | 12 | 8 |
| 53 Maximum Subarray | 11 | 8 |
| 33 Search in Rotated Sorted Array | 11 | 7 |
| 15 3Sum | 9 | 7 |
| 347 Top K Frequent Elements | 10 | 7 |
| 5 Longest Palindromic Substring | 11 | 7 |
| 11 Container With Most Water | 10 | 6 |
| 54 Spiral Matrix | 10 | 5 |
| 210 Course Schedule II | 11 | 5 |
| 68 Text Justification | 7 | 5 |
| 253 Meeting Rooms II | 10 | 5 |
| 560 Subarray Sum Equals K | 11 | 5 |
| 198 House Robber | 9 | 5 |

Other problems present in at least 10 lists but rarely in a top 50: 994 Rotting Oranges, 76, 215, 75, 238, 17, 207, 322, 735, 155, 84, 239.

### Inferences
- **146 LRU Cache** is the strongest cross-company "design" signal. It sits at #1 for TikTok, Oracle and ByteDance and in the top 20 at Uber, GS, Salesforce, Walmart, Nvidia and Visa. Its relatives 460 LFU Cache (Oracle, Salesforce) and 432 All O`one (LinkedIn, TikTok) extend it.
- **68 Text Justification** is a distinctive "implementation-heavy" problem shared by Airbnb, Visa and TikTok (each has it in the top 10). It is a good proxy for practical, spec-following problems.
- **815 Bus Routes** links Uber (#1) and Pinterest (#3). **3161 Block Placement Queries** appears in Uber, TikTok and Visa, a likely shared OA-sourced problem. **2858** appears in Uber and Salesforce, and **1648** in GS and IBM. These overlaps suggest OA-bank reuse across companies (speculative).
- A company tag adds little beyond a generic top-150 list where its top 20 is mostly classics: Oracle, Walmart and IBM, and partly Nvidia. Tags are distinctive and worth drilling for Uber, LinkedIn, Airbnb, Pinterest, Snowflake and Visa.

### Gaps
- The GitHub data is crowd-scraped from LeetCode Premium. Its "Frequency" score is relative within each company, so it cannot be compared across companies.
- I did not cross-check per-company top lists against a second frequency repo, such as snehasishroy/leetcode-companywise-interview-questions (last push 2026-08-21), within the tool budget.
- Interview reports rarely name LeetCode IDs. The IDs above come from tag data plus my slug→ID mapping, except where a report names the problem (e.g., GS 198/1094, Airbnb 1298/631/1235).

---

## 3. Which companies emphasize SQL or data-manipulation coding?

### Takeaway
SQL shows up in **IBM**, **Walmart**, **Infosys** and sometimes **TikTok** SWE OAs, and in **Visa** data-engineering loops (SQL window functions plus PySpark). I found no evidence of SQL in Goldman Sachs' SWE OA. Snowflake's SWE interviews are database-internals-flavoured algorithm and design work, not SQL-writing (its LeetCode tag has zero Database problems). LeetCode's company tags under-represent SQL relative to these reports.

### Cited Findings
- Database-tagged problems in each company's LeetCode tag [data] — [liquidslr repo](https://github.com/liquidslr/leetcode-company-wise-problems):

  | Company | Database problems | Examples |
  |---|---|---|
  | Infosys | 6 | 176, 197, 175, 1341, 185, 181 (176 ranks #3 in Infosys' entire tag) |
  | Uber | 5 | 262 Trips and Users, 1635/1645/1651 Hopper Company, 601 |
  | IBM | 5 | 1355, 3521, 627, 181, 196 |
  | LinkedIn | 4 | 1107, 1127, 1148, 1149 |
  | Walmart Labs | 4 | 2072, 197, 550, 1164 |
  | TikTok | 2 | 601, 185 |
  | Oracle | 2 | 176, 1633 |
  | Pinterest | 1 | 571 |
  | Goldman Sachs, Salesforce, Visa, Nvidia, Snowflake, Airbnb | 0 | — |

- IBM: the coding assessment includes a PostgreSQL question (JOIN/GROUP BY/HAVING) [crowd] — [LC Discuss 8504767](https://leetcode.com/discuss/post/8504767/ibm-coding-assesment-question-customer-r-a9yl/); a January 2026 Glassdoor reviewer reports "SQL and LeetCode-style problem solving" [crowd] — [Glassdoor](https://www.glassdoor.co.uk/Interview/They-asked-questions-focused-on-SQL-and-LeetCode-style-problem-solving-mainly-testing-logical-thinking-data-handling-and-QTN_8806577.htm). DataLemur has IBM-tagged SQL practice problems [prep-site] — [DataLemur IBM SQL](https://datalemur.com/blog/ibm-sql-interview-questions).
- Walmart Global Tech: one OA had one coding question, one SQL query and 2 MCQs; another OA covered Java, Python, C, SQL and C# [crowd; via search snippets] — [Glassdoor Walmart GT](https://www.glassdoor.com/Interview/Walmart-Global-Tech-Interview-E3293060-RVW99558187.htm).
- TikTok: some OA variants include a SQL question alongside array/string coding [prep-site] — [aced.io](https://www.aced.io/guides/tiktok-software-engineer-interview).
- Visa (data engineer): candidates who solve at least 2 of 4 CodeSignal tasks get basic SQL and Python questions. Reported topics: SQL window functions, a "count each letter, alphabetical output" Python task, and Spark questions (inferSchema on 1 TB files, lazy evaluation, wide vs narrow transformations). Glassdoor shows 40% positive ratings for Data Engineer interviews [crowd; Glassdoor, mostly Bengaluru] — [Glassdoor](https://www.glassdoor.com/Interview/Visa-Inc-Interview-E3035-RVW101184114.htm), [Glassdoor](https://www.glassdoor.com/Interview/Visa-Inc-Interview-RVW58400194.htm).
- Goldman Sachs: the SWE OA is described as Software Fundamentals plus Software Diagnostics (app debugging), with no SQL or math section mentioned [prep-site, 2026-10-24] — [Lodely](https://www.lodely.com/companies/goldman-sachs/online-assessment). A 2025 India Analyst report mentions quant MCQs [crowd; search snippet] — [LC Discuss 7289995](https://leetcode.com/discuss/interview-experience/7289995).
- Snowflake SWE: coding has a "database internals" focus and system design centres on data systems; SQL-writing is not mentioned [prep-site] — [interviewing.io Snowflake](https://interviewing.io/snowflake-interview-questions).

### Inferences
- For a "SQL" company tag on a practice platform:
  - **Strong:** IBM, Walmart Global Tech and Infosys (SWE/OA level), and Visa (data roles).
  - **Moderate:** TikTok (some OAs) and Uber (LeetCode SQL tag only: 262 and Hopper Company are classic hard SQL problems, though I found no 2025–26 Uber SWE report of SQL).
  - **No signal:** Goldman Sachs SWE and Snowflake SWE.
- Snowflake is better tagged "data-systems / DB-internals design" than "SQL".

### Gaps
- I did not research Snowflake data/analytics-engineer roles or Goldman Sachs data-engineer roles; SQL emphasis there is likely but unverified.
- Walmart data-role SQL formats beyond the SWE OA were not found.

---

## 4. Which LeetCode tag pools are small or concentrated enough that practicing the tag is efficient?

### Takeaway
The efficient pools are **Pinterest (39–41)**, **Airbnb (61–62)** and **Snowflake (97–100)**, then **Nvidia (120–131)** and **LinkedIn (171–173)**. Their recent problems are mostly drawn from the existing all-time top 50, i.e. stable. **Infosys, Salesforce and TikTok** churn heavily, so drill only their recent window. **Uber, Oracle and Goldman Sachs** are large. Oracle, Walmart and IBM pools are largely generic classics already covered by a standard top-150 list.

### Cited Findings
Sizes are from the repo, with the user's leetcode.com counts in parentheses. "Recent in top 50" means the share of the 6-month list that is already in the company's all-time top 50 (a stability indicator). Source: [liquidslr repo](https://github.com/liquidslr/leetcode-company-wise-problems).

| Company | Pool size | 6-month list | Recent in top 50 | Notes |
|---|---|---|---|---|
| Pinterest | 41 (39) | 12 | 12/12 (100%) | 36% hard; 10 Premium |
| Airbnb | 62 (61) | 8 | 7/8 (88%) | 33% hard; 13 Premium |
| Walmart Labs | 135 (131) | 14 | 12/14 (86%) | |
| LinkedIn | 171 (173) | 19 | 16/19 (84%) | 32 Premium |
| Snowflake | 100 (97) | 17 | 14/17 (82%) | 17 Premium |
| Nvidia | 131 (120) | 20 | 15/20 (75%) | |
| Oracle | 282 (272) | 14 | 10/14 (71%) | |
| Uber | 336 (326) | 33 | 22/33 (67%) | 51 Premium |
| IBM | 166 (161) | 24 | 12/24 (50%) | |
| Visa | 150 (148) | 24 | 12/24 (50%) | |
| Goldman Sachs | 246 (245) | 35 | 17/35 (49%) | |
| TikTok | 317 (290) | 36 | 16/36 (44%) | |
| Salesforce | 196 (185) | 33 | 9/33 (27%) | |
| Infosys | 254 (263) | 119 (77 in the 3-month list) | 25/119 (21%) | |

- Within every company, about 35–44% of the pool accounts for half of the summed frequency score. The scores are normalized per company, so "concentration" is better judged by pool size and recent-list stability than by score mass [data].

### Inferences
**Recommended tag strategy for the practice platform:**
- **Practice the whole tag:**
  - Pinterest: about 40 problems, hard-skewed, very stable.
  - Airbnb: about 60, but pair it with practical/implementation and code-review practice, since some asked problems are not on LeetCode ([Hello Interview](https://www.hellointerview.com/guides/airbnb/g9)).
  - Snowflake: about 100, stable, design/graph heavy.
- **Practice the top 50 plus the 6-month list:** LinkedIn (signature Premium design problems), Nvidia (classics plus bit manipulation; add C++/concurrency fundamentals outside LeetCode), Walmart (classics), Uber (large but stable top; add LLD/machine coding).
- **Practice the 3–6-month window only:**
  - Infosys: 119 recent problems with little overlap with its all-time top. HWI rotates and is India-only; contest-hard DP/greedy practice transfers better than the tag.
  - Salesforce and TikTok: recent OA-sourced and contest-numbered problems dominate.
  - Visa: the OA is CodeSignal-style, so practise CodeSignal-format simulation/grid tasks.
  - Goldman Sachs: its stable core (42, 4, 166, 443, 64, 11, 1086) is well known; the rest churns.
- **Low marginal value over a generic list:** Oracle and IBM (top problems are universal classics, with IBM skewed easy).

### Gaps
- I could not access LeetCode's live company-tag pages, which need Premium, so the "user saw" counts could not be reconciled exactly. Differences of up to about 10% (TikTok 317 vs 290, Nvidia 131 vs 120) probably reflect timing or scrape differences.
- The "recent in top 50" stability metric is my own heuristic. No external source validates it as a predictor of interview questions.
