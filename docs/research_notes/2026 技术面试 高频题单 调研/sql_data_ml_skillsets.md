# Coding skills tested for Data/ML roles in US tech interviews (as of Nov 2026), and the best problem sources: SQL, Python data coding, and ML coding

Research date: 2026-11-22. "Observed 2026-11-22" means I checked it live that day. For LeetCode, I queried the public `leetcode.com/graphql` endpoint without logging in. Older material is marked with its date. Most per-company interview-format claims come from candidate reports (Glassdoor/Blind/LeetCode Discuss) or commercial prep sites, not official company documents, and are flagged as anecdotal.

## Q1. What each role's coding interviews actually test (DA, DS-Analytics, DE, MLE/Applied Scientist, SWE), with company examples

### Takeaway
SQL is the common denominator for Data Analyst, Data Scientist (product analytics) and Data Engineer loops. It is usually live and 45–60 min, with easy-to-medium problems under time pressure. Python shows up as pandas-style data manipulation (DA/DS) or as LeetCode-easy/medium dict/list problems (DE). ML Engineer and Applied Scientist loops are mostly standard LeetCode-style coding plus ML design/breadth. A separate "implement ML from scratch in NumPy" round (k-means, logistic regression, attention, AUC) is reported mainly at AI labs (OpenAI/Anthropic/DeepMind research engineering) and in some Google/Amazon ML loops. SWE is pure DS&A.

### Cited Findings

**Cross-role / 2026 trends**
- The 2026 DS loop at mid-to-large tech companies has 4–6 rounds over 2–4 weeks. The technical coding round is 45–90 min of SQL and Python in a live shared environment (HackerRank, CoderPad). Live algorithm and SQL rounds at most large companies still prohibit AI tools. A claim that "roughly 25%" of US employers allow AI in at least one round (mid-2026) is unsourced. Interviewers increasingly ask candidates to debug or explain AI-generated code; StrataScratch added a "Debug AI Code" mode for this. Cloud SQL variants (BigQuery/Snowflake/Redshift) may be tested. Take-homes increasingly need a live walkthrough or "defense" call. (KDnuggets, V. Chugani, Nov 4 2026) — [KDnuggets](https://www.kdnuggets.com/the-data-science-interview-in-2026-whats-changed-and-how-to-prepare)
- StrataScratch's paid tier lists "Debug-AI-Code questions" as a feature, which confirms the debugging-AI-code format exists as a practice product (observed 2026-11-22) — [StrataScratch pricing](https://platform.stratascratch.com/pricing)

**Data Analyst**
- At tech companies, SQL dominates the DA technical screen. It is often a timed SQL challenge, async or live, testing joins, window functions and CTEs. Uber reportedly prefers live analysis of a provided dataset. Python matters only if the job description requires it, and then means basic pandas manipulation. Excel rarely gets its own round but shows up in take-homes and cases — [Exponent DA guide](https://www.tryexponent.com/blog/data-analyst-interview-guide); [Exponent top DA questions](https://www.tryexponent.com/blog/top-data-analyst-interview-questions)
- Note: tryexponent.com URLs now 301-redirect to aced.io (observed 2026-11-22 when fetching tryexponent.com course/guide pages).

**Data Scientist, Product Analytics (Meta "DS Analytics")**
- Meta DS process, per a DataLemur guide updated Mar 12 2025:
  - Recruiter screen of 30–45 min.
  - Technical screen of 45–60 min covering SQL plus a product case, on CoderPad, watched live. Any mainstream dialect (MySQL, PostgreSQL, SQL Server) is acceptable. A light product-sense question usually ties to the SQL problem.
  - Onsite of roughly four 45-min sessions: Analytical Execution, Analytical Reasoning, DS Technical Skills (SQL), and Behavioral.
  - Example prompts: pages with zero likes; weekly churn rate with date grouping and rounding. Meta expects fast, accurate SQL, and the screen acts as a filter.
  — [DataLemur Meta DS guide](https://datalemur.com/blog/meta-data-scientist-interview-guide)
- 2026 prep guides still describe the Meta DS screen as SQL plus a related product/case question in a 45–60 min video call (Interview Query 2026 guide, DataInterview 2026 guide, Dataford 2026 guide; summarized via search, and the Interview Query page returned HTTP 429 when fetched) — [Interview Query](https://www.interviewquery.com/guides/meta-data-scientist); [DataInterview](https://www.datainterview.com/blog/meta-data-scientist-interview); [Dataford](https://dataford.io/interview-guides/meta/data-scientist)
- Blind (anecdotal): a Meta DS-analytics thread says the screen is "SQL only. If you choose python then you'll likely need to know pandas", which suggests the language can be chosen — [Blind](https://www.teamblind.com/post/facebook-data-scientist-analytics-live-coding-sbhz5cwn)

**Data Scientist at Google**
- PracHub's Google DS guide (published Mar 17 2026, updated Oct 9 2026) tags its 152-question bank by category. It says public sources "do not establish one universal Google DS round count or duration". — [PracHub Google DS guide](https://prachub.com/interview-guide/google-data-scientist-interview-guide)

  | Category | Share | Questions |
  |---|---|---|
  | Analytics & Experimentation | 26% | 40 |
  | Statistics & Math | 22% | 34 |
  | Machine Learning | 19% | 29 |
  | Coding & Algorithms | 14% | 21 |
  | Data Manipulation (SQL/Python) | 11% | 16 |

  Difficulty split: 8% Easy, 70% Medium, 22% Hard.
- Candidate reports and guides describe Google DS as statistics/experimentation-first, with SQL (window functions, multi-table joins, CTEs) and lighter Python (list processing, cleaning messy data). One report mentions a 45-min DS&A problem. These are anecdotal and summarized via search — [Interview Query Google DS](https://www.interviewquery.com/guides/google-data-scientist); [Exponent Google DS](https://www.tryexponent.com/guides/google-data-scientist-interview)

**Data Scientist at other companies**
- Reddit (the company) DS: guides describe a 60-min live SQL session, and say pandas data manipulation and cleaning come up frequently — [DataInterview Reddit DS](https://www.datainterview.com/blog/reddit-data-scientist-interview); [Dataford Reddit DS](https://dataford.io/interview-guides/reddit/data-scientist)

**Data Engineer**
- Amazon's official university-hiring page says DE and BIE interviews assess "technical acumen through a combination of verbal and coding exercises". DEs are expected to know SQL, ETL and data modeling — [amazon.jobs data roles](https://amazon.jobs/content/en/how-we-hire/university/data)
- Amazon BIE/DE (anecdotal):
  - A timed SQL and data-manipulation online assessment on HackerRank (Medium write-up) — [Medium BIE experience](https://medium.com/@mdmoseena22/my-amazon-bie-interview-experience-a-complete-technical-and-behavioral-guide-0d5de30e3cff)
  - Loops with a live SQL round plus a case study and heavy Leadership Principles behavioral (Glassdoor BIE reviews) — [Glassdoor Amazon BIE](https://static.glassdoor.com.br/Interview/Amazon-Business-Intelligence-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,37_IP7.htm)
- Meta DE (Glassdoor, anecdotal, 2025–2026):
  - 60-min technical screen split into ~25 min SQL (window functions, self-joins) and ~25 min Python (dicts, sets, lists).
  - Onsite rounds combine data modeling with several SQL queries on the same model (KPI/metrics) plus Python.
  - Example: design a housing-marketplace schema, then compute view→lead conversion by location.
  - Questions are "not that hard but extremely time sensitive".
  — [Glassdoor Meta review](https://www.glassdoor.com/Interview/Meta-Interview-E40772-RVW105025258.htm)

**ML Engineer / Applied Scientist**
- Meta MLE (Glassdoor, 2026, anecdotal):
  - Phone screen with LeetCode medium-hard coding.
  - Onsite of about 2 coding rounds, 1 ML system design (ranking/recommendation) and 1 behavioral.
  - Reported problems: LRU cache, Number of Islands variant, trie, graph/DFS.
  - Glassdoor aggregate difficulty is 3.3/5.
  — [Glassdoor Meta MLE review](https://www.glassdoor.com/Interview/Meta-Interview-E40772-RVW103151353.htm)
- Amazon Applied Scientist (Glassdoor/LeetCode Discuss, 2022–2026, anecdotal):
  - Separate ML breadth and ML depth rounds, plus system design, a coding round and a bar raiser.
  - Coding is mostly LeetCode easy-medium, with occasional ML-flavored asks such as "write a program to calculate AUC".
  - Depth rounds probe resume projects, transformers, and LLM training at AGI teams.
  — [Glassdoor Amazon AS](https://www.glassdoor.com/Interview/Amazon-Interview-E6036-RVW104768247.htm); [LeetCode Discuss AS intern](https://leetcode.com/discuss/post/8530116/amazon-applied-scientist-intern-6-months-hdbp/); [igotanoffer Amazon AS](https://igotanoffer.com/en/advice/amazon-applied-scientist-interview)
- From-scratch ML coding (prep-site claims, 2026):
  - k-means, logistic-regression training loops and AUC are typical "ML coding" asks in some MLE loops.
  - Research-engineering roles at Anthropic/OpenAI/DeepMind reportedly include implementing a small attention block from scratch.
  - A Google MLE prep course has an ML-coding module titled "Sampling, k-means, AUC".
  — [DataInterview Google MLE ML coding](https://www.datainterview.com/courses/google-machine-learning-engineer/ml-coding); [techscreen.app MLE guide 2026](https://techscreen.app/articles/machine-learning-engineer-interview-guide-2026); [neuraprep ML coding guide](https://neuraprep.com/blog/ml-coding-interview-guide/)
- OpenAI MLE (Interview Coder blog, May 27 2026 / updated Jun 12 2026; vendor content, no OpenAI source cited):
  - A 60-min live ML-coding round that implements primitives in NumPy without `torch.nn` or autograd. The most-named primitives are attention (scaled dot-product, then multi-head), k-means and conv2d.
  - The SWE loop instead uses practical primitives (LRU cache, rate limiter).
  - Research engineering gets more numerically demanding rounds, plus CUDA where relevant.
  — [Interview Coder OpenAI MLE](https://www.interviewcoder.co/blog/openai-ml-engineer-interview)
- An older data point (2019): a candidate spent about 20 of 45 min of a Google MLE phone screen implementing k-means from scratch (surfaced via search summary; original URL not isolated) — see Gaps.

**SWE**
- At OpenAI the SWE loop uses practical coding primitives rather than ML. SWE coding elsewhere is standard DS&A (see the Meta MLE coding reports above, which are the same SWE-style rounds) — [Interview Coder OpenAI](https://www.interviewcoder.co/blog/openai-ml-engineer-interview); [Glassdoor Meta MLE](https://www.glassdoor.com/Interview/Meta-Interview-E40772-RVW103151353.htm)

### Inferences
- For a personal platform, SQL is the highest-leverage track for DA, DS-Analytics, DE and BIE roles. Python data coding (pandas) is a secondary but real need for DS/DA, and it is often the alternative to SQL in the same screen.
- DE interviews pair SQL with plain-Python (dict/set/list) problems. These overlap with an existing LeetCode-style Python track, so no special DE track is needed beyond SQL plus easy/medium Python.
- "Implement ML from scratch" is a niche but growing format, concentrated at AI labs and some MLE loops. A small curated set (about 15–30 problems: k-means, kNN, linear/logistic regression with GD, softmax/cross-entropy, AUC/ROC, precision/recall, attention/MHA, layer norm, conv2d, backprop for an MLP, sampling) would cover the most-cited prompts. Big-tech MLE loops (Meta, Amazon) still weight LeetCode-style coding more heavily.
- Speed and accuracy under time pressure, often without running the query, is the common theme in DS/DE SQL screens. That argues for timed-mode practice in the platform.

### Gaps
- No official 2026 Meta, Google or Amazon documentation of loop formats. Everything beyond amazon.jobs is candidate-reported or vendor-written.
- Whether Meta's DS screen environment lets candidates execute queries: search summaries said some reports deny it, but I did not isolate a primary URL.
- The 2019 Google MLE k-means anecdote surfaced in a search summary without a resolvable URL. Treat it as unverified.
- No reliable Reddit (r/datascience, r/dataengineering, r/MachineLearning) 2025–2026 threads were surfaced by search, so community sentiment on formats is from Blind and Glassdoor only.
- Airbnb, Netflix and Stripe DE/DS formats were not found.

---

## Q2. Which SQL concepts are tested most often

### Takeaway
Every source puts joins and window functions (ranking, LAG/LEAD, running totals, frames) at the top. They are followed by aggregation with GROUP BY/HAVING and conditional aggregation, CTEs/subqueries, date/time handling, and NULL/duplicate handling. The "business pattern" problems that keep recurring are: top-N per group, consecutive days/streaks, retention/churn, funnels/conversion rates, rolling averages, MoM/YoY growth, pivoting, median/percentiles, and self-joins (manager/employee, pairs). No source gives a rigorous measured frequency distribution.

### Cited Findings
- PracHub says it "reviewed 649 SQL interview questions" and organized a top-50 list into 5 equal sections: joins, window functions, CTEs/subqueries, aggregation, and data manipulation/optimization. It advises "spend it on joins first, then window functions". It publishes no per-topic frequency counts. — [dev.to / PracHub top 50 (2026)](https://dev.to/feng_zhang_cedb4581bee881/top-50-sql-interview-questions-with-answers-2026-27h7)
- KDnuggets lists window functions first among SQL concepts candidates fail. Candidates memorize the functions but do not understand frames, partitions and ordering. — [KDnuggets](https://kdnuggets.com/most-candidates-fail-these-sql-concepts-in-data-interviews)
- In Google DS reports and guides, a 45-min SQL round covers joins, window functions, CTEs and aggregation, with follow-ups that add complexity — [Interview Query Google DS](https://www.interviewquery.com/guides/google-data-scientist)
- Meta DS example prompts include an anti-join ("pages with zero likes") and weekly churn rate (date bucketing, rounding) — [DataLemur Meta guide](https://datalemur.com/blog/meta-data-scientist-interview-guide)
- Meta DS screen prompt (reported): count distinct posts crossing a view threshold within a time window, then join to a violations table to compute a ratio. Prep advice is joins, window functions, aggregations and NULL/duplicate handling (summarized via search) — [Screna Meta DS phone report](https://www.screna.ai/experience/1d1fe7c0-91fa-4798-a99a-8724e57939f9)
- Meta DE: window functions and self-joins in the SQL half of the screen; KPI/metric SQL on a data model you designed; conversion-rate computation — [Glassdoor Meta](https://www.glassdoor.com/Interview/Meta-Interview-E40772-RVW105025258.htm)
- DataLemur's free SQL tutorial covers, in its Advanced section: CTEs vs subqueries, window functions, ranking, LEAD/LAG, self-joins, UNION, execution order, pivoting and string functions. Its Intermediate section covers date functions, CASE, NULL, division/rounding and JOINs. This is a good proxy for an interview concept map. — [DataLemur SQL tutorial](https://datalemur.com/sql-tutorial)
- Retention ("% of users active 7 days after signup") is named as a common question type in DE SQL guides — [Exponent SQL DE questions](https://www.tryexponent.com/blog/top-sql-data-engineering-interview-questions)
- LeetCode's SQL 50 sections (observed 2026-11-22):

  | Section | Problems |
  |---|---|
  | Select | 5 |
  | Basic Joins | 9 |
  | Basic Aggregate Functions | 8 |
  | Sorting and Grouping | 7 |
  | Advanced Select and Joins | 7 |
  | Subqueries | 7 |
  | Advanced String Functions / Regex / Clause | 7 |

  There is no dedicated window-function section. Window-style problems are spread across sections: Consecutive Numbers, Game Play Analysis IV, Last Person to Fit in the Bus, Restaurant Growth (rolling 7-day), Department Top Three Salaries (top-N per group), Product Price at a Given Date. — [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/)
- LeetCode's median, pivot and streak problems are almost all Premium (observed 2026-11-22):
  - Median: Median Employee Salary #569 [P], Find Median Given Frequency of Numbers #571 [P]
  - Pivot: Dynamic Pivoting of a Table #2252 [P]
  - Streak: Longest Winning Streak #2173 [P], Consecutive Transactions… #2701 [P]
  - Free exception: Consecutive Numbers #180 — [LeetCode database problemset](https://leetcode.com/problemset/database/)

### Inferences
Suggested concept checklist (tag taxonomy) for the SQL track:
- SELECT/filter
- Joins: inner/left/anti/semi/self/cross
- Aggregation: GROUP BY/HAVING, conditional `SUM(CASE…)`/`FILTER`, ratios with safe division and `ROUND`
- CTEs, subqueries, correlated subqueries
- Window functions: `ROW_NUMBER`/`RANK`/`DENSE_RANK` for top-N per group, `LAG`/`LEAD`, running and rolling sums/averages with frames, `NTILE`/percentiles
- Dates: `DATE_TRUNC`, intervals, `generate_series` for gap filling, week/month bucketing
- Gaps-and-islands (consecutive days/streaks)
- Retention/cohort
- Funnel/conversion
- Growth (MoM/YoY)
- Pivot/unpivot (`CASE` pivot, `crosstab` not required)
- Median (`PERCENTILE_CONT`)
- Dedup
- NULL semantics
- String/regex

SQL 50 alone under-covers window functions, gaps-and-islands, retention/funnel, median and pivot. A backbone list should be supplemented, for example with DataLemur/StrataScratch-style analytics questions or the newer free LeetCode analytics problems listed in Q3.

### Gaps
- No public, methodologically sound frequency count of SQL concepts across real interviews was found. PracHub's "649 questions" claim has no published breakdown.

---

## Q3. Comparing SQL problem sources: counts, free vs premium, dialects (PostgreSQL?), company tags, standing in 2025–2026, licensing

### Takeaway
- **LeetCode** has the largest free, PostgreSQL-supported, well-known structured list. SQL 50 is 100% free, and every free DB problem offers PostgreSQL. Problems carry no company tags without Premium, and its problems are more puzzle-like than business-analytics.
- **DataLemur** is the most "interview-realistic" and company-attributed free/cheap source. It is small (54 SQL questions in the public catalog) and its editor runs PostgreSQL 14, with MySQL also offered.
- **StrataScratch** is the largest company-tagged bank (1000+ coding questions, paid). It runs PostgreSQL, MySQL, MS SQL Server and Oracle, and has pandas, PySpark and Polars versions, but only 75+ free coding questions.
- **pgexercises** is the only openly licensed (CC BY-SA 3.0) PostgreSQL-native exercise set.

For a platform judged on PostgreSQL, LeetCode SQL 50 plus a PostgreSQL-specific analytics supplement is the most defensible backbone. Link out; do not copy statements.

### Cited Findings

**LeetCode Database problems (primary data, observed 2026-11-22)**
- 323 problems in the Database category: 105 free and 218 Premium.

  | Difficulty | Free | Premium |
  |---|---|---|
  | Easy | 55 | 58 |
  | Medium | 39 | 105 |
  | Hard | 11 | 55 |

  — [LeetCode database problemset](https://leetcode.com/problemset/database/)
- All 105 free DB problems offer the same five languages: MySQL, MS SQL Server, PostgreSQL, Oracle and Pandas. Premium problems' language lists are hidden when logged out. — [LeetCode database problemset](https://leetcode.com/problemset/database/); e.g. [Combine Two Tables](https://leetcode.com/problems/combine-two-tables/)
- LeetCode keeps adding free analytics-style DB problems in 2025–2026. Examples among the 55 free problems outside SQL 50:
  - Medium: #3497 Analyze Subscription Conversion, #3716 Find Churn Risk Customers, #3657 Find Loyal Customers, #3564 Seasonal Sales Analysis, #3580 Find Consistently Improving Employees, #3611 Find Overbooked Employees, #3705 Find Golden Hour Customers
  - Hard: #3673 Find Zombie Sessions, #3832 Find Users with Persistent Behavior Patterns, #3482 Analyze Organization Hierarchy
  - Classic free Hards: #262 Trips and Users, #601 Human Traffic of Stadium

  Classic free Mediums: #177 Nth Highest Salary, #178 Rank Scores, #184 Department Highest Salary, #608 Tree Node, #1158 Market Analysis I, #1393 Capital Gain/Loss — [LeetCode database problemset](https://leetcode.com/problemset/database/)

**LeetCode SQL 50 study plan (observed 2026-11-22)**
- 50 problems, `premiumOnly=false`, 0 Premium problems, so all support PostgreSQL. 32 Easy, 17 Medium, 1 Hard by my count from the list below. Full list (titles and links only) — [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/):
  - **Select** (5): [Recyclable and Low Fat Products](https://leetcode.com/problems/recyclable-and-low-fat-products/) E, [Find Customer Referee](https://leetcode.com/problems/find-customer-referee/) E, [Big Countries](https://leetcode.com/problems/big-countries/) E, [Article Views I](https://leetcode.com/problems/article-views-i/) E, [Invalid Tweets](https://leetcode.com/problems/invalid-tweets/) E
  - **Basic Joins** (9): [Replace Employee ID With The Unique Identifier](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/) E, [Product Sales Analysis I](https://leetcode.com/problems/product-sales-analysis-i/) E, [Customer Who Visited but Did Not Make Any Transactions](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/) E, [Rising Temperature](https://leetcode.com/problems/rising-temperature/) E, [Average Time of Process per Machine](https://leetcode.com/problems/average-time-of-process-per-machine/) E, [Employee Bonus](https://leetcode.com/problems/employee-bonus/) E, [Students and Examinations](https://leetcode.com/problems/students-and-examinations/) E, [Managers with at Least 5 Direct Reports](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/) M, [Confirmation Rate](https://leetcode.com/problems/confirmation-rate/) M
  - **Basic Aggregate Functions** (8): [Not Boring Movies](https://leetcode.com/problems/not-boring-movies/) E, [Average Selling Price](https://leetcode.com/problems/average-selling-price/) E, [Project Employees I](https://leetcode.com/problems/project-employees-i/) E, [Percentage of Users Attended a Contest](https://leetcode.com/problems/percentage-of-users-attended-a-contest/) E, [Queries Quality and Percentage](https://leetcode.com/problems/queries-quality-and-percentage/) E, [Monthly Transactions I](https://leetcode.com/problems/monthly-transactions-i/) M, [Immediate Food Delivery II](https://leetcode.com/problems/immediate-food-delivery-ii/) M, [Game Play Analysis IV](https://leetcode.com/problems/game-play-analysis-iv/) M
  - **Sorting and Grouping** (7): [Number of Unique Subjects Taught by Each Teacher](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/) E, [User Activity for the Past 30 Days I](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/) E, [Product Sales Analysis III](https://leetcode.com/problems/product-sales-analysis-iii/) M, [Classes With at Least 5 Students](https://leetcode.com/problems/classes-with-at-least-5-students/) E, [Find Followers Count](https://leetcode.com/problems/find-followers-count/) E, [Biggest Single Number](https://leetcode.com/problems/biggest-single-number/) E, [Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/) M
  - **Advanced Select and Joins** (7): [The Number of Employees Which Report to Each Employee](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/) E, [Primary Department for Each Employee](https://leetcode.com/problems/primary-department-for-each-employee/) E, [Triangle Judgement](https://leetcode.com/problems/triangle-judgement/) E, [Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/) M, [Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/) M, [Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/) M, [Count Salary Categories](https://leetcode.com/problems/count-salary-categories/) M
  - **Subqueries** (7): [Employees Whose Manager Left the Company](https://leetcode.com/problems/employees-whose-manager-left-the-company/) E, [Exchange Seats](https://leetcode.com/problems/exchange-seats/) M, [Movie Rating](https://leetcode.com/problems/movie-rating/) M, [Restaurant Growth](https://leetcode.com/problems/restaurant-growth/) M, [Friend Requests II: Who Has the Most Friends](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/) M, [Investments in 2016](https://leetcode.com/problems/investments-in-2016/) M, [Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/) H
  - **Advanced String Functions / Regex / Clause** (7): [Fix Names in a Table](https://leetcode.com/problems/fix-names-in-a-table/) E, [Patients With a Condition](https://leetcode.com/problems/patients-with-a-condition/) E, [Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails/) E, [Second Highest Salary](https://leetcode.com/problems/second-highest-salary/) M, [Group Sold Products By The Date](https://leetcode.com/problems/group-sold-products-by-the-date/) E, [List the Products Ordered in a Period](https://leetcode.com/problems/list-the-products-ordered-in-a-period/) E, [Find Users With Valid E-Mails](https://leetcode.com/problems/find-users-with-valid-e-mails/) E
- "Advanced SQL 50" (`premium-sql-50`) exists: 50 questions, `premiumOnly=true`. Its contents are hidden without Premium. — [LeetCode Advanced SQL 50](https://leetcode.com/studyplan/premium-sql-50/)
- LeetCode Premium costs $35/month or $159/year (DataLemur's comparison, last updated Feb 18 2025; it may be outdated) — [DataLemur vs LeetCode](https://datalemur.com/blog/datalemur-vs-leetcode-for-sql-interviews)
- Licensing: LeetCode's Terms state that "All Our Content is copyrighted… protecting it from unauthorized use" and is "owned, controlled, or licensed by us". Statements should not be copied, and titles plus links are the safe approach. — [LeetCode Terms](https://leetcode.com/terms)

**DataLemur (Nick Singh, author of *Ace the Data Science Interview*)**
- Public catalog: 106 questions (54 SQL, 39 Python, 7 Statistics, 5 ML, 1 Probability). Difficulty: 40 Easy, 47 Medium, 19 Hard. 46 company labels, including Amazon, Facebook, Google, Microsoft, Apple, Uber, TikTok, Netflix, Stripe, PayPal, JPMorgan, Visa, Capital One and McKinsey. Individual questions are not marked free or Premium in the catalog. (Observed 2026-11-22.) — [DataLemur questions](https://datalemur.com/questions)
- PracHub (a competitor) independently counted the same catalog on Oct 14 2026: 106 questions, 54 SQL. Company depth: Amazon 11, Facebook 9, Google 7, Microsoft 5. 22 companies have exactly one question, and 28 questions are tagged to the *Ace the DS Interview* book. Self-reported totals conflict ("100+" SQL, "200+", "250+"). The terms say there are no free trials. — [PracHub DataLemur vs PracHub](https://prachub.com/resources/datalemur-vs-prachub)
- Dialect: question pages show "PostgreSQL 14", and the editor dropdown appears to offer PostgreSQL 14 and MySQL (observed 2026-11-22). Reviews describe it as running real PostgreSQL. — [DataLemur question page (Facebook "Page With No Likes")](https://datalemur.com/questions/sql-page-with-no-likes); [boot.dev review](https://www.boot.dev/blog/backend/best-sql-practice-sites)
- Pricing (observed 2026-11-22):

  | Plan | Price | Includes |
  |---|---|---|
  | Monthly | $15 | "100+ SQL Interview questions" and "70+ Data Science questions" |
  | Yearly | $60 (shown struck through from $180) | Same, plus a video course |
  | Lifetime bundle | $300 one-time | 1:1 coaching call, signed book, "250+ interview questions" |

  Free resources: a 9-day crash course, a SQL tutorial and a cheat sheet. — [DataLemur pricing](https://datalemur.com/pricing)
- The boot.dev review (date not confirmed) says 45 of 100 SQL questions are Premium-locked. Treat this as uncertain. — [boot.dev](https://www.boot.dev/blog/backend/best-sql-practice-sites)
- Questions carry a "Sourced from <Company>" tag (e.g. Facebook on "Page With No Likes") — [DataLemur question page](https://datalemur.com/questions/sql-page-with-no-likes)

**StrataScratch**
- Supported environments: SQL dialects PostgreSQL, MySQL, MS SQL Server and Oracle (switchable per question). Python libraries Pandas, PySpark and Polars, plus R. — [StrataScratch homepage (search snippet)](https://stratascratch.com/?via=deal); [StrataScratch SQL lesson](https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-databases-and-sql)
- Pricing and counts (observed 2026-11-22). Paid tiers also add 500+ ML/stats/system-design questions and 60+ interview loops. — [StrataScratch pricing](https://platform.stratascratch.com/pricing)

  | Plan | Price | Coding questions |
  |---|---|---|
  | Free | $0 | "75+ coding questions" with solutions |
  | Monthly | $24/mo | "1000+ coding questions (SQL, Python, R)" |
  | Yearly | $139/yr | Same as Monthly |
  | Lifetime | $289 | Same as Monthly |

- The homepage claims "750,000+ members", "1000+ real coding and concept questions" sourced from real interview loops, and 160+ questions in each of its Comprehensive SQL and Comprehensive Python learning paths (marked free) — [StrataScratch](https://www.stratascratch.com/)
- Company tags: questions are attributed to companies (about page: questions "sourced from actual interview loops"). I could not get a total company count. — [StrataScratch about](https://www.stratascratch.com/about)

**HackerRank**
- Its assessment execution environment supports MySQL 8.0.33, Oracle 11g Express, MS SQL Server 2022, DB2 10.5 and PostgreSQL 14.3, all with a 60 s limit. Python 3.14.2 has pandas 2.2.2 available. — [HackerRank execution environment](https://candidatesupport.hackerrank.com/hc/en-us/articles/4402913877523-Execution-Environment)
- HackerRank's public SQL practice track is widely solved in MySQL, MS SQL Server, Oracle or DB2. I found no confirmation that the practice track (as opposed to the assessment platform) offers PostgreSQL. — [GitHub HackerRank SQL solutions](https://github.com/cuongtrans/hackerrank-sql-challenges)

**pgexercises.com (PostgreSQL Exercises)**
- The repo `AlisdairO/pgexercises` (last push 2026-06-30, 440 stars) holds the site code under a BSD-style license. The `questions/` directory has its own LICENSE: Creative Commons Attribution-ShareAlike 3.0. That directory has 79 files across categories `basic`, `joins`, `aggregates`, `date`, `string`, `recursive` and `updates`. (79 is a file count, not a confirmed exercise count.) — [pgexercises GitHub](https://github.com/AlisdairO/pgexercises); [questions/LICENSE](https://github.com/AlisdairO/pgexercises/blob/master/questions/LICENSE)

**Ace the Data Science Interview (book)**
- By Nick Singh and Kevin Huo (Aug 2021). Subtitle: "201 Real Interview Questions Asked By FAANG, Tech Startups, & Wall Street". Nick Singh also runs DataLemur, where 28 questions are tagged to the book. — [TAMU library record](https://libcat.library.tamu.edu/Record/in00004565357); [DataLemur founder page](https://datalemur.com/nick-singh); [PracHub](https://prachub.com/resources/datalemur-vs-prachub)

**Other / newer aggregators**
- PracHub (self-reported, Oct 2026): 12,000+ visible questions across 500+ companies, including 700+ SQL/Python, 900+ analytics/experimentation and 800+ ML. Over 8,000 are free. It is a 2025–2026 crowd-sourced aggregator, not yet a "classic" list. — [PracHub](https://prachub.com/resources/datalemur-vs-prachub)
- Interview Query is another DS-interview bank with company guides (Meta DS 2026 guide). Its pricing and dialect were not verified (HTTP 429). — [Interview Query](https://www.interviewquery.com/guides/meta-data-scientist)

### Inferences
- Backbone choice for a PostgreSQL-judged SQL track:
  - **LeetCode SQL 50** is the best-known, fully free, PostgreSQL-compatible structured list. It is the natural "SQL Blind-75" equivalent.
  - **The 55 other free LeetCode DB problems**, especially the 2025–2026 analytics ones (#3497, #3716, #3657, #3673, …), can extend it to about 105 problems without Premium.
  - **DataLemur's free SQL questions** (company-attributed, PostgreSQL-native) are the best realism and company-tag supplement.
  - **StrataScratch** is best if the user pays and wants company tags at scale.
- Because LeetCode problems all ship PostgreSQL support and DataLemur uses PostgreSQL 14, a PostgreSQL judge can host user-written solutions for these problems. Statements must be re-authored or linked, not copied.
- pgexercises is the only source whose exercise content could legally be reused with attribution (CC BY-SA 3.0, with share-alike obligations). It is PostgreSQL-native, but less interview-like (a country-club schema).
- Company tags: DataLemur (free, visible), StrataScratch (visible, mostly paid) and LeetCode (company tags Premium-only) — see Gaps.

### Gaps
- Not verified: LeetCode company-tag availability for DB problems (believed Premium-only), and whether the Advanced SQL 50 problems support PostgreSQL. Premium content is hidden when logged out.
- Exact free vs Premium split on DataLemur's 54 SQL questions: the catalog doesn't label them, and the boot.dev "45 of 100 locked" figure is undated.
- StrataScratch's exact SQL vs Python split, company count, and terms of use on reproducing questions were not retrieved.
- sqlzoo was not researched (no time in budget). Its license and current status are unknown.
- The DataLemur and StrataScratch ToS clauses on reproduction were not read directly. Only DataLemur's no-trials/no-update-commitment terms were relayed via PracHub.

---

## Q4. Python data coding (pandas) — what is tested and the sources

### Takeaway
pandas questions appear in DS/DA screens where candidates may choose Python over SQL, and in some DS loops (Reddit, Google "Python data cleaning"). The authoritative free lists are LeetCode's "Introduction to Pandas" (15, all free) and "30 Days of Pandas" (32, 5 Premium). Both mostly reuse SQL-50-style database problems with a Pandas language option. StrataScratch offers pandas, PySpark and Polars versions of its company questions (mostly paid). DataLemur has 39 "Python" questions.

### Cited Findings
- **Introduction to Pandas** (observed 2026-11-22): 15 problems, all free and all Easy — [LeetCode Intro to Pandas](https://leetcode.com/studyplan/introduction-to-pandas/); [LeetCode announcement](https://leetcode.com/discuss/study-guide/4121345/NEW-Study-Plan-for-pandas-Beginners%3A-Introduction-to-pandas/)
  - **Data Structures** (1): [Create a DataFrame from List](https://leetcode.com/problems/create-a-dataframe-from-list/)
  - **Inspection** (2): [Get the Size of a DataFrame](https://leetcode.com/problems/get-the-size-of-a-dataframe/), [Display the First Three Rows](https://leetcode.com/problems/display-the-first-three-rows/)
  - **Selecting** (2): [Select Data](https://leetcode.com/problems/select-data/), [Create a New Column](https://leetcode.com/problems/create-a-new-column/)
  - **Cleaning** (6): [Drop Duplicate Rows](https://leetcode.com/problems/drop-duplicate-rows/), [Drop Missing Data](https://leetcode.com/problems/drop-missing-data/), [Modify Columns](https://leetcode.com/problems/modify-columns/), [Rename Columns](https://leetcode.com/problems/rename-columns/), [Change Data Type](https://leetcode.com/problems/change-data-type/), [Fill Missing Data](https://leetcode.com/problems/fill-missing-data/)
  - **Reshaping** (3): [Concatenate](https://leetcode.com/problems/reshape-data-concatenate/), [Pivot](https://leetcode.com/problems/reshape-data-pivot/), [Melt](https://leetcode.com/problems/reshape-data-melt/)
  - **Advanced** (1): [Method Chaining](https://leetcode.com/problems/method-chaining/)
- **30 Days of Pandas** (observed 2026-11-22): 32 problems (blogs say 32 or 33), 5 Premium. Sections — [LeetCode 30 Days of Pandas](https://leetcode.com/studyplan/30-days-of-pandas/):

  | Section | Problems |
  |---|---|
  | Data Filtering | 4 |
  | String Methods | 5 |
  | Data Manipulation (Nth/Second Highest Salary, Department Highest Salary, Rank Scores, Delete Duplicate Emails, Rearrange Products Table) | 6 |
  | Statistics | 3 |
  | Data Aggregation | 7 |
  | Data Integration | 5 |
  | "Strengthen your learning" extras | 3 |

  The Premium problems are Count Occurrences in Text, The Number of Rich Customers, Immediate Food Delivery I, Ads Performance, and Accepted Candidates From the Interviews.
- Overlap: 30 Days of Pandas largely reuses Database problems. For example, Big Countries, Article Views I, Invalid Tweets and Fix Names in a Table are also in SQL 50, and every free DB problem offers a "Pandas" language. One problem set can therefore serve both tracks. — [LeetCode database problemset](https://leetcode.com/problemset/database/)
- Blogs disagree on the 30 Days of Pandas count (32 vs 33) — [dev.to](https://dev.to/ataseren/leetcode-study-plan-30-days-of-pandas-p7); [Medium](https://medium.com/@ataseren/leetcode-study-plan-30-days-of-pandas-2cea7757fa44)
- StrataScratch supports Pandas, PySpark and Polars for Python solutions. Most of its 1000+ coding questions are paid, with 75+ free. — [StrataScratch](https://stratascratch.com/?via=deal); [StrataScratch pricing](https://platform.stratascratch.com/pricing)
- DataLemur lists 39 "Python" questions in its public catalog, mixed between pandas-style and algorithmic — [DataLemur questions](https://datalemur.com/questions)
- HackerRank's assessment environment has pandas 2.2.2 on Python 3.14.2, so pandas-based assessment questions are technically supported — [HackerRank env](https://candidatesupport.hackerrank.com/hc/en-us/articles/4402913877523-Execution-Environment)
- Interview evidence for pandas:
  - Meta DS-analytics: "If you choose python then you'll likely need to know pandas" — [Blind](https://www.teamblind.com/post/facebook-data-scientist-analytics-live-coding-sbhz5cwn)
  - DA roles test pandas only when the job description requires Python — [Exponent DA](https://www.tryexponent.com/blog/data-analyst-interview-guide)
  - Reddit DS guides cite pandas cleaning as frequent — [DataInterview Reddit DS](https://www.datainterview.com/blog/reddit-data-scientist-interview)

### Inferences
- Adding a pandas mode is cheap: LeetCode's design shows the same table-based problem can be judged as SQL or pandas. If the platform stores tables as fixtures, it can compare a DataFrame result to the expected result set. Intro to Pandas (15) plus 30 Days of Pandas (27 free) is a small, coherent starter list.
- pandas is lower priority than SQL for most roles but valuable for DS (product/analytics) and DA candidates who prefer Python. NumPy-from-scratch belongs in the ML track (Q5), not the pandas track.

### Gaps
- No quantitative data on how often companies offer pandas vs SQL in the same screen.
- StrataScratch's count of pandas-enabled questions (vs SQL-only) was not available.

---

## Q5. ML coding: Deep-ML and other "implement from scratch" sources, and who asks these questions

### Takeaway
Deep-ML (deep-ml.com) is the de facto "LeetCode for ML". Its core problems are free; the site advertises "1,200+" problems and activities, with a paid Premium tier (~$132/yr). Its open GitHub problem repo holds 165 problem folders under an "Educational Use Only" (non-commercial) license. TorchLeet (MIT, 65 problems) and TorchCode (~4.8k stars, no license) are the main PyTorch "from scratch" collections. TensorGym existed but has retired (site says so as of 2026-11-22). From-scratch ML rounds are reported mostly at AI labs and some MLE loops.

### Cited Findings
- Deep-ML site (observed 2026-11-22) — [Deep-ML problems](https://www.deep-ml.com/problems):
  - Advertises "1,200+ machine learning coding challenges"
  - Categories: linear algebra, machine learning, deep learning, NLP and computer vision
  - Difficulty: beginner, intermediate and advanced
  - Also has learning paths, labs, projects, collections, math and "Interview Prep" sections
  - Premium banner: "$118.80 for the first year" (10% off yearly)
- The PracHub review (observed Aug 2 2026; vendor) says — [PracHub Deep-ML review](https://prachub.com/resources/deep-ml-review-2026-is-it-the-leetcode-for-machine-learning):
  - The core challenge page highlights "more than 100 curated coding problems". The 1,200+ figure includes other learning activities.
  - Core problems are free and open source. Free accounts get lower limits on submissions, validations, saved solutions, playlists and PyTorch executions.
  - Premium costs $16/month or $132/year.
  - Solutions are Python, run in-browser, with NumPy and PyTorch.
  - Projects include building GPT, an RL agent and CUDA kernels.
- Deep-ML open problem repo `Open-Deep-ML/DML-OpenProblem` — [GitHub](https://github.com/Open-Deep-ML/DML-OpenProblem):
  - 165 problem folders under `questions/`; 713 stars; last push 2025-11-10
  - The repo builds the JSON the site uses and is open to community PRs
  - Example topics: covariance matrix, SVD, Jacobi method, logistic/softmax regression with GD, masked self-attention, layer/batch/group norm, residual block, GRPO objective, sparse MoE / noisy top-k gating, Q-learning, REINFORCE, KL divergence, METEOR score
- Deep-ML license: "Educational Use Only License, Version 1.0, July 2024". It grants a royalty-free, non-exclusive, **non-transferable** license "to use, reproduce, and distribute the Work for educational purposes only". The licensee "shall not use the Work for any commercial purposes". It may not sublicense or distribute except as permitted. A personal, non-commercial practice platform appears to fit "educational use", but redistribution is restricted. — [Deep-ML LICENSE](https://github.com/Open-Deep-ML/DML-OpenProblem/blob/main/LICENSE)
- TorchLeet (`Exorust/TorchLeet`): MIT license, 2,647 stars, pushed 2026-11-06. It describes itself as "LeetCode for PyTorch — 65 ML/AI interview problems from real interviews at Google, Meta, Anthropic" (self-claim), with Jupyter notebooks and an auto-grader. Exercises include k-means and kNN in PyTorch. — [TorchLeet GitHub](https://github.com/Exorust/TorchLeet); [README](https://raw.githubusercontent.com/Exorust/TorchLeet/main/README.md)
- TorchCode (`duoan/TorchCode`): 4,765 stars, no license declared, pushed 2026-07-31. It covers "implementing softmax, attention, GPT-2 and more from scratch with instant auto-grading", is Jupyter-based, and can be self-hosted or tried online. A fork, `alextfkd/TorchCode`, is MIT-licensed. — [TorchCode (duoan)](https://github.com/duoan/TorchCode); [HF Space](https://huggingface.co/spaces/duoan/TorchCode/blob/main/README.md); [alextfkd fork](https://github.com/alextfkd/TorchCode)
- `alirezadir/Machine-Learning-Interviews` is an MIT-licensed guide with 10,017 stars, pushed 2026-10-08. It is a study guide covering GenAI, agentic and system design, not a judged problem set. — [GitHub](https://github.com/alirezadir/Machine-Learning-Interviews)
- TensorGym, verified:
  - tensorgym.com now shows "TensorGym has retired… The interactive exercises and accounts are no longer available" (observed 2026-11-22) — [tensorgym.com](https://tensorgym.com/)
  - It existed around 2024: a solutions repo created Sep 2024 points to `tensorgym.com/exercises` — [sidsaha-ai/tensor-gym](https://github.com/sidsaha-ai/tensor-gym)
  - An unrelated 0-star repo `apollofps/tensorgym` ("Learn PyTorch by solving problems", Jun 2026) also exists — [GitHub](https://github.com/apollofps/tensorgym)
- Other paid ML-coding courses: Exponent (aced.io) has an ML coding module with an approximately 45-min round format — [Exponent ML coding](https://www.tryexponent.com/courses/ml-engineer/ml-coding/ml-coding-intro). Educative has an "ML coding interview questions" course — [Educative](https://www.educative.io/courses/machine-learning-coding-interview-questions). O'Reilly's *Machine Learning Interviews* (Susan Shu Chang) has a chapter on technical coding interviews — [O'Reilly ch.5](https://oreilly.com/library/view/machine-learning-interviews/9781098146535/ch05.html)
- Who asks from-scratch questions (all vendor or anecdotal):
  - OpenAI MLE: NumPy attention, k-means, conv2d in a 60-min round — [Interview Coder](https://www.interviewcoder.co/blog/openai-ml-engineer-interview)
  - Anthropic, OpenAI and DeepMind research-engineering roles: "implement a small attention block from scratch" — [techscreen.app](https://techscreen.app/articles/machine-learning-engineer-interview-guide-2026)
  - Google MLE: "Sampling, k-means, AUC" ML-coding module — [DataInterview](https://www.datainterview.com/courses/google-machine-learning-engineer/ml-coding)
  - Amazon Applied Scientist: AUC from scratch reported — [Glassdoor Amazon AS](https://www.glassdoor.com/Interview/Amazon-Interview-E6036-RVW104768247.htm)
  - Atlassian ML coding round — [copilotinterview Atlassian](https://copilotinterview.com/blog/atlassian-ml-coding-interview)
- Counterpoint: Meta MLE coding reports are standard LeetCode DS&A (LRU cache, islands, trie), and candidates recommend "Blind75 + Meta top 50" — [Glassdoor Meta MLE](https://www.glassdoor.com/Interview/Meta-Interview-E40772-RVW103151353.htm)
- The KDnuggets 2026 DS-interview article does not discuss from-scratch ML implementation. It describes ML system design and LLM eval/RAG as growth areas. — [KDnuggets](https://www.kdnuggets.com/the-data-science-interview-in-2026-whats-changed-and-how-to-prepare)

### Inferences
- For a personal platform, Deep-ML is the reference list to align with: titles and links, plus self-written statements and tests. Its non-commercial, non-transferable license means the platform should not bulk-import Deep-ML problem text even though the repo is public. TorchLeet (MIT) is the one sizeable ML-coding set whose content could legally be adapted with attribution.
- A Python "ML coding" sub-track is justified only if the user targets MLE, research engineering or AI-lab roles. For DS-analytics or DE targets it is low value. A NumPy-only judge (no torch) covers most cited prompts: k-means, logistic regression, AUC, attention, conv2d and layer norm.

### Gaps
- Deep-ML's exact count of free core "problems" (vs the 1,200+ "activities") on the live site was not confirmed. The repo shows 165, the PracHub review says "100+", and the site says "1,200+".
- No primary (company-official) confirmation of which companies run from-scratch ML coding rounds in 2025–2026. All evidence is from prep vendors or candidate reports.
- Exponent, Educative and O'Reilly ML-coding content was not inspected for size or pricing.

---

## Q6. SQL dialect in interviews (MySQL vs PostgreSQL vs "any") and PostgreSQL support across platforms

### Takeaway
Interviews mostly accept "any mainstream dialect", as at Meta. When an environment is enforced, it is usually CoderPad (MySQL or PostgreSQL) or HackerRank (MySQL, PostgreSQL, Oracle, MS SQL Server, DB2). All four major practice platforms support PostgreSQL: LeetCode on every free DB problem, DataLemur (PostgreSQL 14 default), StrataScratch (4 dialects) and HackerRank assessments (PostgreSQL 14.3). A PostgreSQL-judged track therefore loses little realism. The main friction is MySQL-only idioms in community solutions, such as `DATE_ADD`, `IFNULL`, `LIMIT x,y` and `GROUP_CONCAT`.

### Cited Findings
- Meta DS SQL screen: "any mainstream dialect (MySQL, PostgreSQL, SQL Server) is acceptable" on CoderPad (DataLemur guide, Mar 2025) — [DataLemur Meta guide](https://datalemur.com/blog/meta-data-scientist-interview-guide)
- CoderPad's database interviews support MySQL and PostgreSQL. Search snippets of the docs say its PostgreSQL pad runs PostgreSQL 12.4. A Blind user reports no SQL Server, "only MySQL or PostgreSQL" (anecdotal). — [CoderPad databases docs](https://coderpad.io/resources/docs/interview/databases/); [CoderPad PostgreSQL](https://coderpad.io/languages/postgresql/); [CoderPad MySQL](https://coderpad.io/languages/mysql/); [Blind](https://www.teamblind.com/post/facebook-product-growth-analyst-sql-interview-qg1kwyc8)
- HackerRank's assessment environments are MySQL 8.0.33, Oracle 11g, MS SQL Server 2022, DB2 10.5 and PostgreSQL 14.3 — [HackerRank env](https://candidatesupport.hackerrank.com/hc/en-us/articles/4402913877523-Execution-Environment)
- Amazon BIE online assessments are reported on HackerRank (dialect not reported) — [Medium BIE](https://medium.com/@mdmoseena22/my-amazon-bie-interview-experience-a-complete-technical-and-behavioral-guide-0d5de30e3cff)
- LeetCode: all 105 free DB problems offer PostgreSQL alongside MySQL, MS SQL Server, Oracle and Pandas (observed 2026-11-22). A historical feature-request thread for Postgres support exists. — [LeetCode database problemset](https://leetcode.com/problemset/database/); [LeetCode feedback thread](https://leetcode.com/discuss/feedback/899221/adding-postgres-support-for-sql-questions)
- Community practice: many GitHub SQL 50 solution repos use PostgreSQL, and many use MySQL, the most common choice on LeetCode — [PostgreSQL SQL50 repo](https://github.com/alokshandilya/sql50-leetcode); [HamzaHassanain SQL50](https://github.com/HamzaHassanain/Leetcode_SQL_50_Study_Plan)
- DataLemur question pages show PostgreSQL 14, with MySQL as an option — [DataLemur question](https://datalemur.com/questions/sql-page-with-no-likes)
- StrataScratch offers PostgreSQL, MySQL, MS SQL Server and Oracle, switchable per question — [StrataScratch SQL lesson](https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-databases-and-sql)
- Cloud-warehouse SQL (BigQuery, Snowflake, Redshift) may be tested in 2026 DS interviews — [KDnuggets 2026](https://www.kdnuggets.com/the-data-science-interview-in-2026-whats-changed-and-how-to-prepare)
- pgexercises is PostgreSQL-only by design — [pgexercises GitHub](https://github.com/AlisdairO/pgexercises)

### Inferences
- PostgreSQL support across the surveyed platforms is effectively 100%: LeetCode, DataLemur, StrataScratch, HackerRank assessments, CoderPad and pgexercises. HackerRank's public practice track is the one unconfirmed case. PostgreSQL is a safe single judge dialect.
- Since interviews generally accept any dialect, and PostgreSQL is close to Snowflake, Redshift and BigQuery-style analytic SQL (`DATE_TRUNC`, `FILTER`, `PERCENTILE_CONT`, `generate_series`), practicing in PostgreSQL transfers well.
- A useful platform feature would be MySQL→PostgreSQL "idiom hints" or a lint for common MySQL-isms, because many reference solutions online are MySQL.

### Gaps
- No survey or statistic on what proportion of company SQL interviews mandate a specific dialect. The evidence is per-company and anecdotal.
- CoderPad's current PostgreSQL version (12.4 per snippet) was not confirmed on the live page. Whether HackerRank's public SQL practice domain offers PostgreSQL is unconfirmed.
