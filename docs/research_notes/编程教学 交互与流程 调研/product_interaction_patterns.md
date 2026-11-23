# Interaction Patterns and Lesson Flow in Leading Interactive Coding-Education Products (as of Nov 2026)

Research date: 2026-11-22. Each claim carries a source URL and, where the source gives one, its date. "Product claim" means the vendor describing itself. "Independent" means peer-reviewed or third-party evidence. Several vendor pages (Execute Program, LeetCode, NeetCode) render only through JavaScript and could not be fetched directly. For those, I used secondary sources or search-result excerpts and say so where it happens.

## Q1. Product-by-product lesson anatomy, feedback/hints, gating, and retention mechanics

### Takeaway
The products sort into four families:
1. **Micro-step executable prose** (Execute Program, Brilliant, Mimo/Sololearn): a few paragraphs, then the learner has to act.
2. **Instructions + scaffolded editor + auto-grader** (Codecademy, DataCamp, boot.dev, SQLBolt, Real Python exercises, freeCodeCamp workshops).
3. **Problem sets/projects with tests and mentoring** (CS50P, Exercism, Hyperskill projects, pgexercises, LeetCode/DataLemur).
4. **Explanation-first content plus problems** (Educative/Grokking, AlgoMonster, NeetCode, Select Star SQL).

Only Execute Program, Brilliant, boot.dev (Training Grounds) and Codecademy (Smart Practice) document built-in spaced review. Hint ladders that end in a solution reveal are close to universal, and several products attach a cost to using them.

### Cited Findings

#### Execute Program (Gary Bernhardt): TypeScript, JS, Python, SQL, regex
- Lessons interleave prose with live programming problems, and **the prose unfolds in response to reader interaction**. Readers answer prompts **by executing a program**. There are **no non-executable prompts** (no multiple choice), and each prompt serves as both an application prompt and a recall prompt. Andy Matuschak's research notes (third-party analysis, partly based on conversations with Bernhardt in 2020): [Matuschak – Execute Program](https://notes.andymatuschak.org/Execute_Program)
- Lessons are "quite short": a few minutes each. You read a few paragraphs, try the concept right away, and repeat a few times. They are short because the interactive prompts carry much of the explanation and because lessons "assume solid recall of prior material": [Matuschak – lessons are quite short](https://notes.andymatuschak.org/zLnMMGiCT6xDjMfMurTzKjs)
- Several examples can share a code "preamble" (setup code reused across prompts). The Python course has a "dynamic reference": [Matuschak – Execute Program](https://notes.andymatuschak.org/Execute_Program)
- **Gating:** lessons don't unlock until the learner has successfully reviewed their prerequisites (Matuschak note; Bernhardt said this formalizes how he already preferred to write): [Matuschak – lessons don't unlock until prerequisites reviewed](https://notes.andymatuschak.org/zHLWyC5LVXZLWE9RmoC1gua)
- **Review mechanics** (Matuschak note, sourced from a 2020-03-24 conversation and a 2020-04-07 email with Bernhardt):
  - Prompts are machine-graded, so harmless typos produced false negatives. In early 2020 the SQL course's false-negative rate was high enough to force a change: wrong attempts no longer count as failures if the student eventually answers correctly, retries are unlimited, and the next interval still grows on the SRS curve.
  - After the change, later lessons unlock regardless of performance.
  - A student who can't answer after several tries can **"give up"** to see the answer, which shortens that item's interval.
  - Source: [Matuschak – missed answers don't penalize unless they give up](https://notes.andymatuschak.org/zX7RdiHGbHYnkFznUr9VZx7). This partly conflicts with the "unlock only after successful review" note above. My reading is that a review must be *completed*, not aced.
- Execute Program's own spaced-repetition page (product claim; JS-rendered, so this comes from a search-result excerpt and the page is undated) says:
  - fully completing an item's reviews takes **90 days** if every review is on time and passed;
  - it uses fewer review levels than comparable SRS systems, because programming topics reinforce each other;
  - on a miss it takes a "middle ground" and **halves the item's level** rather than resetting it.
  - Source: [Execute Program – Spaced Repetition](https://www.executeprogram.com/spaced-repetition)
- Progress mechanics emphasize completing new lessons over increasing recall duration. In Matuschak's description, a lesson reaches "Learned" after a single review: [Matuschak – Execute Program](https://notes.andymatuschak.org/Execute_Program)
- Tagline: "Learn it. Code it. Remember it." [Changelog person page](https://changelog.com/person/garybernhardt)

#### Codecademy
- **Smart Practice / personalized practice** (blog, 2023-09-20):
  - Tracks when a concept was last seen, when it was last practiced, and the scores, weighing "hundreds of facts" to "prioritize things that you might be forgetting" (spaced repetition).
  - Mobile flashcards were added in a June app update.
  - An early version held practice back for the first week after a concept was learned. Learner feedback got that delay removed.
  - Item selection time fell from about 20 s to under 2 s.
  - The post gives **no usage or outcome numbers**.
  - Source: [Codecademy – Behind the Build: Smart Practice](https://www.codecademy.com/resources/blog/behind-the-build-smart-practice/)
- **AI Learning Assistant** (blog, 2024-05-09):
  - Aware of the current checkpoint and lesson, and stays in that scope.
  - Engineers used examples to make it **give a hint first, and the answer only if the learner keeps pressing**.
  - "Explain code" button works on highlighted code.
  - RAG over Codecademy articles and cheatsheets; prototyped in Streamlit with LangChain.
  - No outcome numbers reported.
  - Source: [Codecademy – Behind the Build: AI Learning Assistant](https://www.codecademy.com/resources/blog/behind-the-build-ai-learning-assistant)
- Help-center pages (undated; from search excerpts):
  - The assistant is available in lessons, projects and articles, and can be switched off under Tools.
  - Free learners are limited (one page says 5 prompts/day). Pro/Plus is unlimited.
  - Project steps have a "Get a hint" option that reviews your code.
  - An older article says solutions come via "Get Unstuck → Get Code Solution", and freeform projects have no solution.
  - Sources: [AI Features available on Codecademy](https://help.codecademy.com/hc/en-us/articles/23400751016859-AI-Features-available-on-Codecademy); [AI Assistance for free learners](https://help.codecademy.com/hc/en-us/articles/25381511803035-AI-Assistance-for-free-learners); [Understanding Your Code](https://help.codecademy.com/hc/en-us/articles/220914987-Understanding-Your-Code)
- Independent analysis (SIGCSE 2017, 30 tutorials): Codecademy and Khan Academy organize content hierarchically, with "many sub-stages", e.g. a conditionals module containing many sub-stages on writing `if`/`while` correctly. The popular interactive tutorials used lecture-based contexts heavily: [Kim & Ko 2017](https://faculty.washington.edu/ajko/papers/Kim2017CodingTutorialEvaluation.pdf)

#### boot.dev (Go/Python/backend; "Boots" AI)
- Concepts are taught through "bite-sized coding challenges". After a set of micro-concepts, learners build a full project. The site positions itself against long video courses whose feedback loops are "too long". Product claim, undated about page: [boot.dev – About](https://www.boot.dev/about)
- **Boots** is a chatbot meant to guide rather than answer, using the **Socratic method**. Using him is **"penalized (in game terms)"** so that learners turn to him only when really stuck. The same page tells learners to avoid AI as a crutch that skips the needed struggle, and to work in the "zone of proximal development": [boot.dev – About](https://www.boot.dev/about)
- Boots originally worked only on code-completion and multiple-choice lessons and was extended to all lesson types in January 2024. Search-result excerpt of [Boot.dev Beat Jan 2024](https://boot.dev/blog/news/bootdev-beat-2024-01)
- **Training Grounds** (launched 2025-08-27):
  - "Next Challenge" chooses a topic, difficulty and challenge type from completed courses, recent topics, **recent struggles, and spaced repetition** (time since last seen).
  - It starts from hand-written examples, has an LLM (GPT-5 or Claude Sonnet 4 at the time) generate a new challenge, then **runs it on the backend to check that it's valid and has a correct solution** before serving it. Generation takes about 45 s.
  - Skipping with a reason makes that kind of challenge less frequent.
  - Over 2,500 hand-written lessons exist, and **every challenge ships with a solution** for learners who are still stuck. The team had handled 21,219 learner reports on lessons.
  - Source: [boot.dev – Training Grounds launch](https://www.boot.dev/blog/news/training-grounds-launch)
- I could not verify the specifics of XP, gems, chests or streaks from a primary source (see Gaps).

#### Brilliant (problem-first, no video)
- Lessons are sequenced into short sections, one idea each, starting from the simplest useful case. They **often open with a question before showing the procedure**, so the learner's first attempt gives the explanation a purpose.
- Interaction relies on manipulables: dragging a tangent line, rearranging pieces, adjusting a graph.
- Feedback arrives "while reasoning is still fresh" so the learner can revise.
- **Koji** (AI tutor, supported courses only) can see the problem, the on-screen interactive elements and what the learner has tried. It asks guiding questions, highlights part of a diagram, or breaks the problem into steps. Support is heavy when an idea is new and tapers off for independent practice.
- **A skill check ends each lesson.** Unit checks mix in earlier material. If a miss traces back to an earlier idea, **review lessons are added to the learner's plan**. Practice picks problems from learning history and uses new surface contexts, spacing and interleaving.
- Product claim; page updated 2026-11-20: [Brilliant – How Brilliant teaches math](https://brilliant.org/resources/choosing-brilliant/how-brilliant-teaches-math/)
- "Action first. Theory later." (Brilliant blog, 2024-11-08): [Brilliant blog – Solving equations](https://blog.brilliant.org/solving-equations/)
- Brilliant's llms.txt states there are no videos and that everything is interactive: [brilliant.org/llms.txt](https://brilliant.org/llms.txt)

#### Exercism (test-driven, mentoring)
- The v3 design (launched September 2021) splits exercises into two kinds:
  - **Concept Exercises**: language-specific, each with a clear learning goal. They explain a concept, then ask the learner to apply it, with **stubs/boilerplate** to cut out unnecessary code.
  - **Practice Exercises**: story-based, no approval step.
- Unlocking is concept-graph based. Concept Exercises are tagged with the concepts they teach, and a Practice Exercise unlocks once its prerequisite concepts are covered.
- Automated **analyzers and representers** were expected to auto-analyze about 95% of iterations. Approvable solutions are auto-approved with tips. Solutions that can't be analyzed are auto-approved so the student isn't blocked, and a mentor reviews them later, with that feedback reused for similar solutions.
- Source: [Exercism v3 rationale (GitHub)](https://github.com/exercism/v3/blob/master/docs/rationale-for-v3.md)
- "Independent Mode" was renamed "Practice Mode", and the guided path is "Mentored/Learning Mode": [Exercism blog – Independent mode becomes Practice mode](https://exercism.io/blog/independent-mode-becomes-practice-mode)

#### freeCodeCamp
- The newer full-stack curriculum is made of **workshops, labs, review pages and quizzes**. At launch it listed 64 workshops, 62 review pages and 66 quizzes, of which 42/46/46 were live. A 2026 third-party review counts 64 workshops, 513 lectures, 83 labs, 66 quizzes and 6 prep exams, ending in a capstone and a final exam. Counts come from different dates; sources: [freeCodeCamp turns 10 – curriculum updates](https://www.freecodecamp.org/news/freecodecamp-turns-10-major-curriculum-updates) (search excerpt); [SkillScouter freeCodeCamp review 2026](https://skillscouter.com/freecodecamp-review/)
- The full-stack coursework was still being built out in mid-2025: [freeCodeCamp mid-2025 update](https://www.freecodecamp.org/news/learn-react-in-your-browser-freecodecamp-full-stack-curriculum-mid-2025-update/)
- Legacy model (2018-08-09): each certification requires 5 projects. Each project has its own test suite you can run to check readiness. All other challenges are optional preparation: [freeCodeCamp – new curriculum is live (2018)](https://www.freecodecamp.org/news/freecodecamps-new-coding-curriculum-is-now-live-with-1400-coding-lessons-and-6-developer-certifications-you-can-earn/)

#### Scrimba (interactive screencasts)
- Lessons ("scrims") are recorded live-coding sessions. The learner can **pause and edit the instructor's code** in the browser; the player doubles as the IDE. Third-party descriptions and reviews, 2026: [tooldirectory.ai – Scrimba (reviewed 2026-07-25)](https://tooldirectory.ai/tools/scrimba); [G2 Scrimba reviews](https://www.g2.com/products/scrimba/reviews)
- I found no completion or retention data. Scrimba's comparison articles are vendor marketing: [Scrimba vs Codecademy](https://scrimba.com/articles/scrimba-vs-codecademy-which-is-better-for-learning-to-code/)

#### Educative (text + embedded runnable code)
- Text-first. Lessons are assembled from **widgets** (Markdown, Code, Quiz) and code runs in the browser: [Educative author quick start](https://www.educative.io/courses/author-quick-start/RL538wz3B6E); [Dev.to review 2025 (third-party)](https://dev.to/alex_hunter_44f4c9ed6671e/is-educativeio-worth-it-in-2025-a-comprehensive-review-1n7j)
- **"Evaluate with AI"** launched March 2026 in the Grokking Coding Interview Patterns courses. It gives on-demand evaluation of edge cases, logic gaps and time/space complexity. Product claim: [Educative blog – AI-assisted feedback](https://www.educative.io/blog/educative-ai-assisted-feedback)

#### Mimo / Sololearn (mobile, Duolingo-like)
- Mimo lessons run a **learn → quiz → practice loop**: read a short concept, answer a quiz, write code in a built-in editor, repeat. Vendor comparison page, undated: [Mimo vs Sololearn (Mimo blog)](https://mimo.org/blog/mimo-vs-sololearn)
- A 2025 user complaint about Mimo: "You have to click 5x on the same button per exercise." [Trustpilot – Mimo](https://ie.trustpilot.com/review/mimo.org)
- Sololearn:
  - Added **hearts**, which are lost on mistakes and refill over time or with Pro.
  - Made practice a **mandatory** part of lessons "since all of the feedback we've seen shows how valuable and necessary practice is". Staff reply on a forum, ~2022: [Sololearn forum – why are there hearts now](https://www.sololearn.com/Discuss/3100662/why-are-there-hearts-now)
  - **Code Coach** gives a task description with sample input/expected output and hidden test cases. The task counts as solved once all tests pass. Community answer, Jan 2025: [Sololearn forum – how code coaches work](https://sololearn.com/de/Discuss/3314960/how-core-coaches-work)

#### CS50x / CS50P (lectures + problem sets + CS50 Duck)
- CS50P runs 10 weeks (0–9). Each week is **lecture → optional "Shorts" → problem set**, followed by a final project: [CS50P](https://cs50.harvard.edu/python/)
- **CS50 Duck** (SIGCSE 2024 paper; deployed Summer/Fall 2023, first to about 70 summer students, then thousands online, then about 500 on campus). It is GPT-4 based, "designed to guide students toward solutions rather than offer them outright". The suite includes:
  - **"Explain Highlighted Code"**, a VS Code extension;
  - **style50 "Explain Changes"**, which turns style diffs into natural-language explanations;
  - the Duck itself, on the web, in VS Code and on the Ed forum, where its answers are subject to staff endorsement.
  - **Throttling with hearts:** 10 hearts, one regained every 3 minutes, one spent per interaction. The paper presents this as both cost control and pedagogy: it makes students think about their questions and take reflective breaks.
  - Source: [Liu et al., "Teaching CS50 with AI", SIGCSE 2024](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)

#### Real Python
- Interactive coding exercises have **Instructions / Hints / Solution tabs** and a **sidebar of test results** (click a failed test for details).
  - Hints are **progressive**, "from a gentle nudge to more specific guidance". Some individual tests carry their own hints.
  - The **solution unlocks after your first test run**.
  - Reading the solution does **not** complete the exercise. Learners are told to rebuild it from memory and run the tests.
  - Help article updated 2026-07-02: [Real Python – Using hints and solutions in coding exercises](https://support.realpython.com/article/111-using-hints-and-solutions-in-coding-exercises)

#### Learn Python the Hard Way (Zed Shaw)
- The method: do each exercise, **type it in exactly**, make it run. The 5th edition describes "read, type, run, fix mistakes, repeat" across 60 exercises. The publisher listing says "No copying and pasting!": [LPTHW intro – "The Hard Way Is Easier"](https://learnpythonthehardway.org/python3/intro.html); [InformIT listing](https://www.informit.com/store/learn-python-3-the-hard-way-9780138270575)
- Criticism: Goodreads reviewers call the tone condescending and the drills tedious or too simple: [Goodreads](https://goodreads.com/book/show/8341335.Learn_Python_The_Hard_Way)

#### Hyperskill / JetBrains Academy
- A topic is a **theory segment plus code challenges and multiple-choice quizzes**. Topics form a **knowledge map** whose areas link to prerequisites in other groups. A topic finished in one project doesn't need repeating in another. Help center, undated: [Hyperskill – Getting started](https://support.hyperskill.org/hc/en-us/articles/8770808176404-Getting-started-with-Hyperskill); [Hyperskill – Knowledge map](https://support.hyperskill.org/hc/en-us/articles/4406586984468-Knowledge-map-and-what-it-is-for)
- Manifesto (product claim, undated):
  - every piece of theory is followed by practice;
  - learners solve **several similar problems per topic** until they master it, then use the concept in a **project stage**;
  - stages grow in complexity and reuse earlier code ("reverse decomposition");
  - it claims reading or watching without applying "has proved to be enjoyable but ineffective", citing no source.
  - Source: [Hyperskill – How we teach](https://home.hyperskill.org/how-we-teach)
- Code challenges can be solved in the browser or the IDE. Projects are IDE-based (JetBrains plugin): [Hyperskill – Getting started](https://support.hyperskill.org/hc/en-us/articles/8770808176404-Getting-started-with-Hyperskill)

#### SQLBolt
- Each lesson is about three short paragraphs plus syntax snippets. Below that are the dataset table (e.g., "Table: movies"), a **pre-filled query editor** (default selects all columns) with RESET, and **one exercise of ~5 checklist tasks** (e.g., "find the title of each film", "find the director", …).
  - Each task has a "Stuck? Read this task's Solution" link.
  - **"Solve all tasks to continue to the next lesson."**
  - The course has about 18 numbered lessons plus review lessons and extra topics (subqueries, unions).
  - Undated page: [SQLBolt – Lesson 1](https://sqlbolt.com/lesson/select_queries_introduction)

#### Select Star SQL
- A free interactive **book**: front matter plus 5 chapters, about 30 min each, all built around **one real dataset** (Texas death-row executions/last statements).
  - Ch1 query structure, Ch2 whole-table aggregation, Ch3 group aggregation, Ch4 joins, Ch5 closing remarks and user-added challenge questions.
  - The stated aim is to convey "a mental model for writing SQL", more than a reference page.
  - Undated: [Select Star SQL](https://selectstarsql.com/)

#### PostgreSQL Exercises (pgexercises)
- Seven categories: Basic, Joins & Subqueries, Modifying data, Aggregates, Date, String, Recursive. The author built it because there were few places to "learn by *doing* in a structured manner" for databases.
- Execution design:
  - read-only access, `statement_timeout`, and PgBouncer pooling;
  - for data-modification questions, users change a `cd` schema that is **deleted and recreated after each operation**, with rotating databases so each serves one user at a time.
  - Source: [pgexercises – About](https://pgexercises.com/about.html)

#### DataCamp SQL (and DataCamp exercises generally)
- **Exercise anatomy:**
  - Title, then **Context** (objective and motivation; no instructions here), then **Instructions** (brief, but meant to make the learner plan), then **sample code** in a `script.py`/script window.
  - **Hint** via "Show Hint" or Ctrl+H. **Solution** via a second Ctrl+H/"Show Answer". Submitting from the solution window completes the exercise but **awards no XP**.
  - **SCTs** (submission correctness tests) grade the code. An incorrect submission shows "Incorrect Submission" and **highlights the faulty portion in the editor; only the first error is reported**.
  - The success message should focus "on insights, not praise".
  - Source: [DataCamp instructor guide – Coding exercise anatomy](http://instructor-support.datacamp.com/en/articles/2347523-coding-exercise-anatomy)
- **Hint design:** "Hints should get students ~50% of the way to the answer": [same](http://instructor-support.datacamp.com/en/articles/2347523-coding-exercise-anatomy). The target hint rate is "below 35%". When it is high, instructors should clarify the instructions and use extra scaffolding "only as a last resort". Article dated 2021-03-15: [DataCamp – high hint ratio](https://instructor-support.datacamp.com/en/articles/4058594-what-do-i-do-if-an-exercise-has-a-high-hint)
- Exercises follow short videos. Instructors are told to check whether the preceding video covers what the exercise needs: [same](https://instructor-support.datacamp.com/en/articles/4058594-what-do-i-do-if-an-exercise-has-a-high-hint)

#### DataLemur SQL tutorial
- Three tiers:
  - Basic 101–109: SELECT, WHERE, AND/OR/NOT, BETWEEN, IN, LIKE, filtering review, ORDER BY.
  - Intermediate 201–212: aggregates, GROUP BY, HAVING, DISTINCT, NULLs, CASE, JOINs, dates.
  - Advanced 301–312: CTEs vs subqueries, window functions, ranking, LEAD/LAG, self-joins, UNION, execution order, pivoting, strings, an Instacart case study.
- The site links to an interview-question bank (SQL, company-specific). Page ©2026: [DataLemur SQL tutorial](https://datalemur.com/sql-tutorial)

#### LeetCode SQL 50, NeetCode, AlgoMonster, VisuAlgo, Python Tutor
- LeetCode SQL 50 is 50 problems grouped by topic: SELECT, basic joins, aggregates, sorting/grouping, advanced select/joins, subqueries, advanced string functions/regex. Topics are reconstructed from community repos because the official page didn't render: [GitHub – Leetcode_SQL_50_Study_Plan](https://github.com/HamzaHassanain/Leetcode_SQL_50_Study_Plan); official URL [leetcode.com/studyplan/top-sql-50](https://leetcode.com/studyplan/top-sql-50/)
- NeetCode is a "Roadmap (video)" and AlgoMonster is "Patterns (text)". AlgoMonster has about 230 problems, NeetCode a curated 150–300. Third-party comparison posts disagree on prices and counts: [Dev.to – NeetCode vs AlgoMonster](https://dev.to/alex_hunter_44f4c9ed6671e/neetcode-vs-algomonster-which-is-better-for-coding-interviews-2m90)
- **VisuAlgo:**
  - 24 visualization modules.
  - **e-Lecture Mode opens automatically for first-time/non-logged-in visitors**, and users can enter their own inputs.
  - Each module has a **"Training" quiz with questions randomly generated from rules and auto-graded**; a test mode is used for NUS exams.
  - Conceived 2011; mobile lite version since April 2022.
  - Source: [VisuAlgo](https://visualgo.net/en)
- **Python Tutor:** step-by-step execution visualization. UCSD reports 25M+ users in 180+ countries, 500M+ visualizations and 10k–20k daily users (institutional claim): [UCSD Today](https://today.ucsd.edu/story/a-uc-san-diego-tool-teaching-code-to-25-million-is-even-more-critical-in-age-of-ai); original paper [Guo, SIGCSE 2013](https://pg.ucsd.edu/publications/Online-Python-Tutor-web-based-program-visualization_SIGCSE-2013.pdf)

### Inferences
- The strongest fit for "teach first, then practice, hand-written fluency" combines three products' patterns:
  - **Execute Program's** micro-lesson shape: a few paragraphs, then an executable prompt, prose revealed on interaction, every prompt answered by typing code or output, never multiple choice.
  - **Real Python's / DataCamp's** hint ladder: progressive hints, then the solution only after a first attempt, with a cost or no credit for solution use.
  - **Exercism's / Hyperskill's** concept-graph unlocking: practice problems unlock once their prerequisite concepts are done.
- Single-dataset SQL teaching (SQLBolt per lesson, Select Star SQL for the whole book, pgexercises' one club schema) lets learners carry schema knowledge from lesson to lesson and look at results instead of decoding new tables. This suggests one or two well-known schemas for the whole SQL track.
- Several products share a pattern: ration help (boot.dev's game penalty, CS50 hearts, DataCamp's lost XP, Sololearn hearts) and steer the AI toward hints first (Codecademy, CS50, boot.dev, Brilliant/Koji). For a learner aiming at independent writing, the AI tutor should be scoped to the current step, hint-first, and somewhat rationed.

### Gaps
- Execute Program's own design essays and blog are JS-rendered and returned no content via fetch or curl. The 90-day / "halve the level" details come from a search excerpt of its spaced-repetition page, and the rest from Matuschak's 2020 notes. Current (2026) behavior is unverified.
- I found no primary documentation of boot.dev's XP/gems/chests/streak mechanics or its exact solution-unlock rule (e.g., whether a solution requires a failed attempt). The Sept 2025 "Beat" post mentions spaced repetition only in a search snippet.
- No primary source for the exact anatomy of Mode/ThoughtSpot's SQL tutorial (mode.com now redirects to thoughtspot.com/sql-tutorial, whose landing page gives no structure), LeetCode Explore cards, NeetCode's per-problem page, or AlgoMonster's template pages.
- Codecademy's exact hint/solution unlock thresholds in the 2026 UI are unconfirmed; help-center wording varies between articles.
- Mimo: no official documentation of step types (fill-in-blank, reorder) was found. Sololearn's AI features in 2025–26 are known only from user forum claims.
- I didn't find official CS50P documentation of check50/submit50/style50 in this pass (the CS50P landing page doesn't describe them).

## Q2. Which patterns have evidence behind them, and which are criticized?

### Takeaway
Independent evidence is strongest for:
- **active practice with immediate feedback** (Freeman 2014, cited by Brilliant);
- **retrieval/spacing** (Roediger & Karpicke; Rohrer & Taylor);
- **Parsons problems** as an *efficient* exercise (same learning in less time);
- **PRIMM** (predict-run-investigate-modify-make).

Vendor data on completion or learning is almost absent. Codecademy, Execute Program, boot.dev, Scrimba and Mimo publish no outcome numbers. The best-documented vendor numbers are CS50 Duck self-report surveys and Duolingo's streak A/B tests.

Common criticisms:
- shallow, right/wrong-only feedback;
- no personalization for prior experience;
- "tutorial hell" / "blank editor syndrome" from over-scaffolding;
- weak transfer from standard Parsons/fill-in exercises to unscaffolded writing;
- false negatives from strict machine grading;
- punitive throttles (hearts) that frustrate learners.

### Cited Findings
- **Kim & Ko, SIGCSE 2017 (independent, 30 popular tutorials including Codecademy and Khan Academy):**
  - most teach bottom-up and require learners to write programs;
  - most give immediate feedback, "but this feedback is shallow", and "almost half of the tutorials did not provide feedback when learners made errors";
  - few explain when and why a concept is useful, and few give guidance on common errors;
  - **none personalize based on prior coding experience or learner goals**;
  - educational games scored best on structure, immediate feedback and active writing;
  - the analysis was analytical, not a measurement of learning outcomes.
  - Source: [Kim & Ko 2017 PDF](https://faculty.washington.edu/ajko/papers/Kim2017CodingTutorialEvaluation.pdf); [Ko's blog summary](https://medium.com/bits-and-behavior/coding-tutorials-the-good-the-bad-and-the-ugly-b45afc8821f6)
- **Parsons problems (reorder lines):**
  - Ericson, Margulieux & Rick (Koli Calling 2017) compared Parsons with distractors, fixing code and writing code. Later papers summarize the result as Parsons problems being **faster than code-writing with similar learning gains**: [Ericson et al. 2022 summary via eScholarship](https://escholarship.org/content/qt8794g5s0/qt8794g5s0.pdf?t=qbddoc); [Parsons Problems and Beyond – systematic review](https://acris.aalto.fi/ws/portalfiles/portal/131069230/Parsons_Problems_and_Beyond_-_Systematic_Literature_Review_and_Empirical_Study_Designs_.pdf)
  - Hou, Ericson & Wang (ICER 2022): learners given Parsons problems **as optional scaffolding inside write-code tasks** spent significantly less time, with no significant difference in learning: [ICER22 PDF](https://web.eecs.umich.edu/~xwanghci/papers/ICER22.pdf)
  - A 2023 follow-up: the "Parsons as Help" group had higher practice performance and efficiency with the **same posttest scores**: [arXiv 2311.18115](https://arxiv.org/pdf/2311.18115)
  - **Transfer caveat:** a CS1 pilot study surfaced in search found that **standard Parsons problems did not produce short-term near-transfer to code writing**, and it proposed harder "Blank-Variable Parsons". The excerpt came from NSF-PAR-hosted papers whose authorship I couldn't confirm: [par.nsf.gov 10510493](https://par.nsf.gov/servlets/purl/10510493); [par.nsf.gov 10510497](https://par.nsf.gov/servlets/purl/10510497)
- **PRIMM:**
  - Introduced by Sentance & Waite (WiPSCE 2017). The stages are Predict → Run → Investigate → Modify → Make, and the first three map to "Use" in Use-Modify-Create: [Sentance PRIMM slides 2020](https://www.slideshare.net/slideshow/the-i-in-primm-code-comprehension-and-questioning/233967029); [Raspberry Pi PRIMM summary 2023](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)
  - Sentance, Waite & Kallia (Computer Science Education 29(2–3), 2019) reported the experimental group outperforming the control on the post-test. That result comes from an abstract summary on an aggregator and is not verified in the full text: [QMRO record](https://qmro.qmul.ac.uk/xmlui/handle/123456789/57800); [X-MOL abstract page](https://www.x-mol.com/paper/1403736023379705856)
- **CS50 Duck (SIGCSE 2024; self-reported, non-anonymous surveys, Fall 2023, ~500 on-campus students):**
  - Usage mid-semester: 17% used it >10×/week, 32% 5–10×, 26% 2–5×, 25% <2×.
  - Helpfulness: 47% "very helpful", 26% "helpful", 21% "somewhat", 6% "not helpful".
  - Effectiveness: 35% very effective, 35% effective, 25% somewhat, 5% not.
  - End of semester (73% responded): 50% "frequently" and 28% "constantly" used; 53% "loved" and 33% "liked".
  - Accuracy: 22/25 (88%) of curricular Ed answers were correct in Summer 2023. Fall 2023 endorsement was only 70/180, which the authors think understates accuracy.
  - **Ed forum questions per student fell from 0.89 (Fall 2022) to 0.28 (Fall 2023).**
  - Some students asked for less throttling; the course kept it.
  - Source: [Liu et al. 2024](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)
- **DataCamp hint data (vendor-internal):**
  - Target hint rate is <35% ([2021-03-15](https://instructor-support.datacamp.com/en/articles/4058594-what-do-i-do-if-an-exercise-has-a-high-hint)).
  - A search excerpt of DataCamp's "Hints best practices" guide states that across DataCamp **86% of learners who take the hint go on to ask for the solution**, against a 50% target. This suggests hints often fail to unblock. Not re-verified on the fetched page: [DataCamp – Hints best practices](https://instructor-support.datacamp.com/en/articles/2379164-hints-best-practices)
- **Streaks (Duolingo, vendor A/B data):** separating the daily goal from the streak produced +3.3% Day-14 retention, +1% daily active learners and +10.5% learners on a streak within 20 days (relative changes). The share of daily learners with a 7+ day streak rose from about a third to just over half in a year. Learners can now equip up to two Streak Freezes. Blog undated in the excerpt: [Duolingo – Improving the streak](https://blog.duolingo.com/improving-the-streak)
- **Python Tutor:** the evidence is correlational. In one CS1 course, students who interacted more with embedded visualizations scored higher on midterms: [Guo SIGCSE 2013](https://pg.ucsd.edu/publications/Online-Python-Tutor-web-based-program-visualization_SIGCSE-2013.pdf). A 2018 log study of 78,369 users found cross-country differences in back-stepping: [Guo et al. VL/HCC 2018](https://pg.ucsd.edu/publications/impact-of-culture-on-visual-debuggers_VLHCC-2018.pdf)
- **Learning-science citations used by Brilliant** (vendor citing independent work): Freeman et al. 2014 (active learning beats lecture), Roediger & Karpicke 2006 (retrieval > rereading), Rohrer & Taylor 2007 (spacing/interleaving), Hattie & Timperley 2007 (feedback). Brilliant's App Store "6x more effective than lecture videos" claim has no source I could find: [Brilliant – How Brilliant teaches math](https://brilliant.org/resources/choosing-brilliant/how-brilliant-teaches-math/); [App Store listing](https://apps.apple.com/vg/app/id913335252?l=en-gb)
- **Criticisms:**
  - **"Tutorial hell" / "blank editor syndrome":**
    - Al Sweigart (2026-01-14) argues the standard advice ("build your own projects", "contribute to open source") is oversimplified. He recommends slowing down, hand-written notes, **memorizing basic syntax**, and **tiny projects that you finish and then rebuild from memory**: [Sweigart – tutorial hell bad advice](https://inventwithpython.com/blog/tutorial-hell-bad-advice.html)
    - daily.dev frames the problem as recognition versus recall and suggests closing the tutorial and rebuilding from scratch: [daily.dev – How to escape tutorial hell](https://daily.dev/blog/how-to-escape-tutorial-hell/)
  - **Machine-grading false negatives:** Execute Program's early-2020 SQL reviews were strict enough that the review policy changed: [Matuschak note](https://notes.andymatuschak.org/zX7RdiHGbHYnkFznUr9VZx7)
  - **Mentor bottleneck:** Exercism v2 tracks "pretty reliably fail as soon as a complex exercise like Bob is introduced", with long waits that break flow. This drove v3's automation: [Exercism v3 rationale](https://github.com/exercism/v3/blob/master/docs/rationale-for-v3.md)
  - **Hearts/paywalls:** Sololearn learners complain about losing hearts and having to wait or pay: [Sololearn forum – hearts](https://www.sololearn.com/pl/Discuss/3333771/when-your-heart-are-gone)
  - **Mobile micro-lessons too shallow for depth:** competitor Coddy's (biased) view of Mimo: [coddy.tech vs Mimo](https://coddy.tech/vs/mimo)
  - **Codecademy Smart Practice:** an early forced one-week delay was removed after negative learner feedback: [Codecademy Smart Practice](https://www.codecademy.com/resources/blog/behind-the-build-smart-practice/)
  - **AI over-reliance:** boot.dev warns AI can become a crutch that bypasses the needed struggle: [boot.dev About](https://www.boot.dev/about)

### Inferences
- For a rusty adult aiming at hand-written fluency, the evidence supports a particular role for scaffolding. Parsons and fill-in-the-blank work best as **optional help offered inside a write-from-scratch task** (the "Parsons as Help" design), not as the main exercise type, given the weak transfer from standard Parsons to writing.
- Machine-graded "type the output" prompts need **lenient normalization and unlimited retries** (Execute Program's 2020 fix). Otherwise false negatives erode trust in spaced reviews.
- DataCamp's 86% hint-to-solution figure suggests a single static hint rarely unblocks learners. A progressive ladder (Real Python) or a context-aware Socratic AI (CS50/Codecademy/Koji) is the better bet. This is a hypothesis; no head-to-head data was found.
- The fall in CS50 forum questions alongside high Duck usage suggests the AI absorbs routine help-seeking. For a solo learner, that argues for building in "explain highlighted code" and "explain this error" affordances.

### Gaps
- I found no published completion or retention numbers for Codecademy, Execute Program, boot.dev, Scrimba, Mimo, Sololearn, Educative, Hyperskill or freeCodeCamp. I also found no controlled evaluation of any commercial coding platform's learning outcomes beyond Kim & Ko's analytical review.
- I couldn't retrieve the exact time savings in Ericson et al. 2017 or the effect sizes in Sentance et al. 2019.
- No independent study of spaced repetition specifically for programming syntax or concepts (as opposed to general retrieval-practice literature) turned up in this pass.
- There is no evidence on whether CS50-style throttling improves learning, as opposed to just cutting cost; the paper's argument is a rationale only.

## Q3. How do products move learners from guided to independent writing, and how do they handle learners who already know part of the material?

### Takeaway
Products fade scaffolding with fairly consistent ladders:
- **Exercism:** stubbed concept exercises → story-based practice exercises.
- **freeCodeCamp:** step-by-step workshops → independent labs → certification projects with test suites.
- **Hyperskill:** theory → several similar problems → project stage that reuses your code.
- **boot.dev:** micro-challenges → full project → "build and deploy your own".
- **Brilliant:** heavy tutor support → independent practice without visuals or tutoring.
- **CS50P:** lecture → problem sets → final project.
- **PRIMM:** Predict → Run → Investigate → Modify → Make.

Placement/test-out is rare. Hyperskill's "skip a topic by solving one problem" plus a personalization quiz is the clearest implementation. Kim & Ko found none of 30 tutorials personalized for prior experience (2017).

### Cited Findings
- **Exercism:** Concept Exercises use stubs and boilerplate and teach one concept. Practice Exercises are story-based, have no approval step, and unlock once prerequisite concepts are covered. Practice Mode is for languages you already know and contains only Practice Exercises: [Exercism v3 rationale](https://github.com/exercism/v3/blob/master/docs/rationale-for-v3.md)
- **Hyperskill:**
  - Theory, then "a few similar problems in each topic" until mastery, then the concept applied in project stages that "grow in complexity" and reuse earlier code: [Hyperskill – How we teach](https://home.hyperskill.org/how-we-teach)
  - Test-out: **"If you feel that a topic is familiar, you can Skip it: you will need to solve one problem to verify your knowledge."**
  - **Project personalization** asks you to solve several problems and marks topics as known (graduation-cap badge), which can be skipped without solving anything; "Unskip" reverses it.
  - Help-center articles, undated: [Hyperskill support 4407035732500](https://support.hyperskill.org/hc/en-us/articles/4407035732500); [Hyperskill – Getting started](https://support.hyperskill.org/hc/en-us/articles/8770808176404-Getting-started-with-Hyperskill)
- **freeCodeCamp:** guided workshops and independent labs, plus review pages and quizzes, culminating in exams and a capstone ([SkillScouter 2026](https://skillscouter.com/freecodecamp-review/)). Since 2018, certification projects come with runnable test suites ([freeCodeCamp 2018](https://www.freecodecamp.org/news/freecodecamps-new-coding-curriculum-is-now-live-with-1400-coding-lessons-and-6-developer-certifications-you-can-earn/)).
- **boot.dev:** bite-sized challenges, then a full project combining the micro-concepts. Learners are then urged to build their own projects from scratch and deploy them or publish them to GitHub: [boot.dev About](https://www.boot.dev/about). Training Grounds adapts topic and difficulty to completed courses and recent struggles: [Training Grounds](https://www.boot.dev/blog/news/training-grounds-launch)
- **Brilliant:**
  - Koji's support "is heavier while an idea is new and decreases for independent practice". Independent practice removes scaffolding, visual aids and tutoring.
  - Unit checks mix in earlier material. Misses that trace back to earlier ideas add review lessons to the plan, an adaptive remediation path rather than a placement test.
  - Source: [Brilliant – How Brilliant teaches math](https://brilliant.org/resources/choosing-brilliant/how-brilliant-teaches-math/)
- **CS50P:** lecture → Shorts → problem set each week, then a final project: [CS50P](https://cs50.harvard.edu/python/)
- **DataCamp:** instructors are told to avoid extra scaffolding and use it "only as a last resort": [DataCamp high-hint article](https://instructor-support.datacamp.com/en/articles/4058594-what-do-i-do-if-an-exercise-has-a-high-hint)
- **Real Python:** after reading a solution, learners are told to **rebuild it from memory** and rerun the tests: [Real Python support](https://support.realpython.com/article/111-using-hints-and-solutions-in-coding-exercises)
- **Sweigart (2026):** finish tiny projects, then **rebuild them from memory**: [inventwithpython](https://inventwithpython.com/blog/tutorial-hell-bad-advice.html)
- **PRIMM:** Predict → Run → Investigate → Modify → **Make** (a new program applying the same ideas to a new problem): [Sentance slides](https://www.slideshare.net/slideshow/the-i-in-primm-code-comprehension-and-questioning/233967029)
- **Execute Program:** the gate is retention, not placement. Lessons stay locked until prerequisite reviews are done, and lessons assume solid recall: [Matuschak notes](https://notes.andymatuschak.org/zHLWyC5LVXZLWE9RmoC1gua)
- **No personalization in 2017-era tutorials:** "None provide personalization based on prior coding experience or learner goals": [Kim & Ko 2017](https://faculty.washington.edu/ajko/papers/Kim2017CodingTutorialEvaluation.pdf)

### Inferences
- A rusty adult needs a **per-lesson test-out**: Hyperskill-style "solve one representative write-from-scratch problem to skip". Combined with Execute Program-style prerequisite gating, the learner skips what they still know but still gets spaced reviews on it. This could be implemented as "skip = pass the lesson's final 'Make' exercise cold".
- A concrete fading ladder within one lesson, synthesized from PRIMM, Exercism, freeCodeCamp and Real Python:
  1. read an example;
  2. predict its output (typed);
  3. modify given code;
  4. write a small function from a stub;
  5. write from a blank editor (no stub);
  6. later, a spaced review asks for the blank-editor version again.
- Across a course, a "project stage" every few lessons that reuses earlier code (Hyperskill, boot.dev) is the most common bridge to independence.

### Gaps
- I found no published data comparing skip/test-out designs, or showing how often learners use Hyperskill's skip or how accurate its personalization is.
- I didn't confirm whether Execute Program, boot.dev, Codecademy, DataCamp or Mimo offer placement tests or test-out in 2026.
- How freeCodeCamp's workshops differ from labs in step granularity (e.g., one instruction per step) was not confirmed from a primary source in this pass.

## Q4. UI specifics worth copying

### Takeaway
The most reusable concrete UI patterns:
1. **Prose that reveals step by step on interaction** (Execute Program).
2. **Instructions / Hints / Solution tabs with a clickable test-results sidebar and per-test hints** (Real Python).
3. **Highlight-to-explain code** and **explain-the-diff for style feedback** (CS50, Codecademy).
4. **Report only the first error and highlight its location in the editor** (DataCamp SCTs).
5. **Hint, then solution on the same hotkey (Ctrl+H twice), with no credit for solution-submitted work** (DataCamp).
6. **Dataset table shown above a pre-filled SQL editor with a per-lesson task checklist** (SQLBolt).
7. **Sandboxed per-user schema reset for DML exercises** (pgexercises).
8. **Step-through execution visualization with back-stepping** (Python Tutor).
9. **Auto-opening "e-Lecture" for first-time visitors plus auto-generated, auto-graded quizzes** (VisuAlgo).
10. **Pause-and-edit the instructor's code** (Scrimba).

### Cited Findings
- Execute Program: prose unfolds in response to reader interaction, prompts are answered by executing a program, examples share a code preamble, and the Python course has a dynamic reference: [Matuschak – Execute Program](https://notes.andymatuschak.org/Execute_Program)
- Real Python: Instructions/Hints/Solution tabs, a failed-tests sidebar (click for details), progressive hints, per-test hints, solution unlocking after the first run: [Real Python support (2026-07-02)](https://support.realpython.com/article/111-using-hints-and-solutions-in-coding-exercises)
- DataCamp: Context kept separate from Instructions; Ctrl+H gives the hint and pressing again gives the solution; "Incorrect Submission" highlights the offending code and shows only the first error; success messages focus on insight rather than praise; solution-submitted exercises get no XP: [DataCamp exercise anatomy](http://instructor-support.datacamp.com/en/articles/2347523-coding-exercise-anatomy)
- CS50: "Explain Highlighted Code" (select lines, get a plain-English explanation); style50 "Explain Changes" button; heart-based AI rate limit shown visually: [Liu et al. 2024](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)
- Codecademy: highlight code, then the "Explain code" button; the AI assistant is aware of the current checkpoint; it can be switched off under Tools: [Codecademy AI Learning Assistant blog (2024-05-09)](https://www.codecademy.com/resources/blog/behind-the-build-ai-learning-assistant); [Codecademy AI features help](https://help.codecademy.com/hc/en-us/articles/23400751016859-AI-Features-available-on-Codecademy)
- SQLBolt: table display, pre-filled default query, RESET, task checklist, per-task "Solution" link, "Solve all tasks to continue": [SQLBolt Lesson 1](https://sqlbolt.com/lesson/select_queries_introduction)
- pgexercises: read-only plus `statement_timeout`; a writable `cd` schema dropped and recreated after each modification; rotating DBs, one user at a time: [pgexercises About](https://pgexercises.com/about.html)
- Sololearn Code Coach: sample input/expected output shown, hidden tests, solved when all tests pass: [Sololearn forum (Jan 2025)](https://sololearn.com/de/Discuss/3314960/how-core-coaches-work)
- VisuAlgo: e-Lecture Mode auto-opens for new visitors; learners can enter their own inputs; the "Training" button gives randomly generated, auto-graded quizzes: [VisuAlgo](https://visualgo.net/en)
- Python Tutor: step-through visualization embeddable in textbooks; back-step behavior logged at scale: [Guo SIGCSE 2013](https://pg.ucsd.edu/publications/Online-Python-Tutor-web-based-program-visualization_SIGCSE-2013.pdf); [Guo VL/HCC 2018](https://pg.ucsd.edu/publications/impact-of-culture-on-visual-debuggers_VLHCC-2018.pdf)
- Brilliant: question before procedure; manipulable diagrams; an AI tutor that sees on-screen state and what the learner tried; a skill check at the end of each lesson: [Brilliant (updated 2026-11-20)](https://brilliant.org/resources/choosing-brilliant/how-brilliant-teaches-math/)
- boot.dev Training Grounds: one-click "Next Challenge"; AI-generated challenges validated by actually running a reference solution server-side; "skip with reason" tunes future items: [Training Grounds (2025-08-27)](https://www.boot.dev/blog/news/training-grounds-launch)
- Educative: "Evaluate with AI" button on practice problems, giving edge-case and complexity feedback (March 2026): [Educative blog](https://www.educative.io/blog/educative-ai-assisted-feedback)
- Scrimba: pause the screencast and edit the instructor's code in place: [tooldirectory.ai – Scrimba](https://tooldirectory.ai/tools/scrimba)

### Inferences
- With Monaco plus server-side judging plus an AI tutor, the cheapest high-value features to copy are:
  1. "Explain highlighted code" and "explain this error" context actions in Monaco;
  2. test-results panel with per-test hints;
  3. first-error-only feedback with an inline editor decoration;
  4. a hint ladder on one keyboard shortcut (e.g., Ctrl+H repeated) ending in a solution that gives no credit and must be retyped;
  5. for SQL, a result-grid diff of expected vs. actual rows, plus a schema/table panel always visible above the editor.
- boot.dev's Training Grounds suggests a safe way to generate AI practice items: generate, run the reference solution against the judge, and only then serve the item. This fits a platform that already has server-side judging.

### Gaps
- I found no primary-source screenshots or descriptions of an **output-diff UI** (expected vs. actual) for LeetCode, DataLemur or Codecademy SQL in this pass, and no documentation of keyboard-flow shortcuts (e.g., run/submit hotkeys) beyond DataCamp's Ctrl+H.
- No usability or A/B data on side-by-side versus stacked explanation/editor layouts was found for any product.
