# AI (LLM) Tutor Pedagogy for "Teach First, Then Practice" Python + SQL Lessons

Research cutoff: 2026-11-22. Evidence labels used throughout:
- **[RCT]** randomized controlled trial / randomized experiment
- **[Quasi]** quasi-experimental or non-randomized comparison (e.g., propensity-adjusted, diff-in-diff, condition-by-module)
- **[Obs]** observational / deployment / survey / log analysis
- **[Lab-qual]** small lab or qualitative study
- **[Bench]** offline evaluation of model outputs (no learners' learning measured)
- **[Vendor]** company-run study or product claim
- **[Preprint]** not peer reviewed (arXiv, NBER/EdWorkingPaper, SSRN)

---

## 1. Do LLM tutors help or harm learning? (headline evidence, 2023–2026)

### Takeaway
The best evidence through Nov 2026 shows one pattern again and again: **unrestricted, answer-giving AI raises performance while the AI is available but does not raise, and often lowers, independent performance afterward.** Purpose-built tutors that are grounded in correct solutions, scaffold step by step and withhold answers can remove that harm, and in one well-designed physics RCT they produced large gains. The programming-specific RCTs show "better scores, same learning". The newest large field RCTs (UMD 2026, Khanmigo 2026) found null-to-negative effects when the tutor defaulted to direct answers or when learners barely used it.

### Cited Findings

**Harm from unguarded AI; guardrails mitigate (math, general evidence)**
- [RCT] Bastani et al., *PNAS* 122(26):e2422633122 (2025). ~1,000 students in grades 9–11, ~50 classrooms at one Turkish high school, Fall 2023, four 90-minute practice sessions. Arms: control (textbook/notes), "GPT Base" (ChatGPT-like) and "GPT Tutor" (hidden teacher-written prompt that required incremental hints rather than answers and **supplied the correct solutions to the model**). Practice performance: GPT Base +48%, GPT Tutor +127% vs control. Unassisted exam: GPT Base **−17%** vs control; GPT Tutor not significantly different from control. — [PNAS DOI](https://doi.org/10.1073/pnas.2422633122); [Knowledge at Wharton, 2024-08-27](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education); [PsyPost summary, 2026-04-21](https://www.psypost.org/unrestricted-generative-ai-harms-high-school-math-learning-by-acting-as-a-crutch/)
- Bastani mechanism: GPT Base gave correct answers only **51%** of the time. Chat logs showed most GPT Base users just asked for the answer and copied it. GPT Tutor users asked for help and attempted problems. Students in both AI arms **overestimated** how much they had learned (GPT Tutor students felt they did significantly better, but their exam scores matched control). — [PsyPost](https://www.psypost.org/unrestricted-generative-ai-harms-high-school-math-learning-by-acting-as-a-crutch/); [Wharton](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)
- Note: GPT Tutor **removed the harm but did not produce exam gains over textbook practice**. — [Wharton](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)

**Large gains from a carefully engineered tutor (physics, general evidence)**
- [RCT, crossover] Kestin, Miller, Klales, Milbourne & Ponti, *Scientific Reports* 15:17458 (June 2025). Harvard intro physics for life-science majors, Fall 2023, N=194 analyzed. Each student had one week with the AI tutor at home and one week of in-class active learning (randomized by peer group). Median post-test 4.5 (AI) vs 3.5 (class); pre-test median 2.75. Effect 0.63 SD (linear regression), 0.73–1.3 SD (quantile regression); Mann-Whitney z=−5.6, p<10⁻⁸. Median AI time-on-task was 49 min vs ~60 min in class. — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- Kestin design details relevant to us: the system prompt encoded active engagement, cognitive-load management and growth mindset. **Step-by-step worked solutions were placed in the prompt for accuracy** (the authors avoided relying on GPT-4 to solve problems). **Sequential scaffolding was enforced by the platform because the prompt alone did not reliably enforce it.** Learners were self-paced. The authors say the tutor complements rather than replaces instruction, and that results may not hold for higher-order synthesis. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)

**Programming-specific controlled evidence**
- [RCT] Bassner, Lenk-Ostendorf, Beinstingel, Wasner & Krusche, "Less stress, better scores, same learning: The dissociation of performance and learning in AI-supported programming education," *Computers & Education: AI* (listed as 2026). TUM CS1, N=275 (Iris n=91, ChatGPT n=88, No-AI n=96), 90-min Java concurrency task. Exercise score: ChatGPT 71.8%, Iris (hint-first, context-aware tutor) 57.5%, No-AI 29.9% (ChatGPT vs No-AI d=1.10; Iris vs No-AI d=0.76; ChatGPT vs Iris d=0.38, p=.031). **Post-test without AI: no significant group differences** (knowledge p=.311; code comprehension p=.136). Both AI arms reduced frustration (d≈−0.8). Only Iris raised intrinsic motivation (d=0.55). Students rated ChatGPT easier and more helpful, which the authors call a "comfort trap". — [Iris research results page](https://ls1intum.github.io/edutelligence/iris/docs/research/study-results); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666920X25001778); [TUM portal](https://portal.fis.tum.de/en/publications/less-stress-better-scores-same-learning-the-dissociation-of-perfo/)
  - Conflict note: one search-engine summary claimed the ChatGPT arm did *worse* than controls on later exams. The developers' results page reports **no significant post-test differences**, so I report the primary version.
- [RCT, Vendor] Shen & Tamkin (Anthropic), "How AI Impacts Skill Formation," published 2026-01-29. 52 mostly junior developers who already knew Python learned the unfamiliar async library Trio (35-min task, then a 25-min quiz). AI group quiz ≈50% vs hand-coding ≈67% (Cohen's d=0.738, p=0.01). Time saved (~2 min) was not significant. **The largest gap was on debugging questions.** — [Anthropic research post](https://www.anthropic.com/research/AI-assistance-coding-skills); [arXiv 2601.20245](https://arxiv.org/abs/2601.20245)
  - Interaction patterns and quiz scores (small n per pattern, descriptive): AI delegation ~39% (n=4); progressive reliance ~35% (n=4); **iterative AI debugging ~24%** (n=4); conceptual inquiry only ~65% (n=7); hybrid code+explanation ~68% (n=3); **generation-then-comprehension ~86%** (n=2). — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)
  - Authors: "Cognitive effort—and even getting painfully stuck—is likely important for fostering mastery." They measured immediately after the task only, not retention. — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)
- [Quasi] Pankiewicz & Baker, ITiCSE 2024, "Navigating Compiler Errors with AI Assistance." Intro programming. GPT-4 (gpt-4-0613) hints appeared automatically on compiler errors, for the **first half of each module only**. Results with hints on were mixed across the six most common error types, but **once hints were switched off, the experimental group outperformed control on 5 of 6 error types**. Students rated the hints highly. — [arXiv 2403.12737](https://arxiv.org/abs/2403.12737); [PDF](https://learninganalytics.upenn.edu/ryanbaker/ITICSE2024%20-%20Navigating%20Compiler%20Errors%20with%20AI%20Assistance.pdf)
- [RCT, Preprint] Heickal & Lan, "A Classroom Study of LLM-Generated Feedback Intervention in Introductory Programming," arXiv 2606.08807 (June 2026; IRAISE 2026). Intro Python, 215 students, 17 labs, 6,693 submissions. Randomized arms on incorrect submissions: natural-language hint / AI-generated failing test case / none. NL hints were associated with higher completion and faster convergence. **Test-case feedback had heterogeneous effects that depended on whether the generated test was valid.** — [arXiv 2606.08807](https://arxiv.org/abs/2606.08807)
- [RCT, Preprint] Eastwood, Narne, Hilby, Denny, Aggarwal & Kapoor, "Guardrails or Roadblocks?" arXiv 2609.29995 (Sept 2026). 132 intro-programming students, 2×2 design: Socratic vs direct × no-context vs full context (problem + student code). **The Socratic + full-context TA was rated least favorably**, with significantly lower perceived support for task completion. Descriptively (not significant) it also had the highest stress, the most external-LLM use and the fewest full-comprehension post-task explanations. — [arXiv 2609.29995](https://arxiv.org/abs/2609.29995)
- [Lab-qual] Prather et al., "The Widening Gap," ICER 2024. 21 novices, observation + interviews + eye tracking. Students who were already doing well used GenAI to speed up code they already intended to write. Struggling students' metacognitive difficulties persisted or compounded, and they finished with an **"illusion of competence"**. — [arXiv 2405.17739](https://arxiv.org/abs/2405.17739); [ICER 2024 program](https://icer2024.acm.org/details/icer-2024-papers/26/The-Widening-Gap-The-Benefits-and-Harms-of-Generative-AI-for-Novice-Programmers)
- [RCT lab + field, Preprint] Lehmann, Cornelius & Sting, "AI Meets the Classroom: When Do LLMs Harm Learning?" (arXiv 2409.09047, v2 March 2025; coding exercises). Two pre-registered, incentivized lab experiments found **no net effect** of LLM access on learning. Students who used LLMs to *substitute* for practice covered more topics but understood each less. Students who used them to *complement* practice (asking for explanations) understood more. **LLMs widened the gap between low and high prior-knowledge students.** — [arXiv 2409.09047](https://arxiv.org/abs/2409.09047)

**Large 2026 field RCTs (general, not programming-specific)**
- [RCT, Preprint] Liu et al. (University of Maryland), "The Effects of Course-Integrated AI Tutoring on Student Performance and Engagement," EdWorkingPaper 26-1598 (Oct 2026). 2,379 undergraduates, 30 instructors, multiple disciplines including CS, Fall 2025. The GPT-4o RAG tutor **reduced final grades by 0.27–0.37 SD** (0.37 SD in exact-match course blocks) and LMS participation by 0.90 SD. First-generation students lost about twice as much. Only 14.6% of treated students ever used it. 73.8% of requests sought information, explanations or solutions; **0.7% sought feedback on the student's own work**. Instructors mostly left the **default "direct instruction" mode** on (only two ended the term in "tutor mode"), so the result concerns a direct-answer configuration. — [EdWorkingPaper PDF](https://edworkingpapers.com/sites/default/files/ai26-1598.pdf); [DOI 10.26300/y3f8-vh05](https://doi.org/10.26300/y3f8-vh05)
- [RCT, Preprint] Oreopoulos & Low, "One Click Away: AI Tutoring with Khanmigo in a Two-Year School Experiment," NBER w35620 (2026). 18 Tennessee middle schools. Khanmigo was set to coach rather than give answers. Effect: about 0.06–0.08 SD per school year, similar to Khan Academy practice without AI. 96% of students messaged it at least once, but they used it on only about a third of practice days. The authors call **engagement the binding constraint** and cite a **non-proactive interface** plus help-seeking barriers. — [NBER w35620](https://www.nber.org/papers/w35620); [Chalkbeat, 2026-08-25](https://www.chalkbeat.org/2026/08/25/ai-tutoring-students-khanmigo-khan-academy-engagement-study/)
- [RCT, Preprint] Oreopoulos, Liut, Sungu & Low, "Making AI Tutoring Productive: Evidence from a Mastery-Based Math Practice Experiment," NBER w35621 (Aug 2026). >6,000 middle-schoolers, factorial design: AI vs plain CAL × mastery vs non-mastery progression. AI students progressed more slowly and attempted fewer questions, but were more accurate per attempt, recovered faster after mistakes and spent more time on structured support. Mastery alone did not improve the delayed test. **AI + mastery gave the best delayed results** (marginally significant, concentrated on practiced material; ~3 pp per Hechinger). — [NBER w35621](https://www.nber.org/papers/w35621); [Hechinger Report](https://hechingerreport.org/proof-points-ai-mastery-learning/)
- [RCT, Vendor, Preprint] Google LearnLM × Eedi, "AI tutoring can safely and effectively support students: An exploratory RCT in UK classrooms," arXiv 2512.23633 (Dec 2025; trial May–June 2025). N=165 UK secondary math students. Human tutors supervised every AI-drafted message and approved 76.4% with little or no edits. Supervised LearnLM was at least as effective as human tutors on all measured outcomes. A larger follow-up (1,179 students, 10 schools, 10 weeks) is reported in a Google PDF dated Oct 2026; I did not verify its results. — [arXiv 2512.23633](https://arxiv.org/abs/2512.23633); [Stanford SCALE summary](https://scale.stanford.edu/news/research-notes-two-emerging-strategies-using-ai-tutoring); [Google follow-up PDF](https://services.google.com/fh/files/misc/learnlm_oct26.pdf)
- [Quasi, Preprint] Thomas, Borchers, …, Koedinger, "LLM-Generated Feedback Supports Learning If Learners Choose to Use It," EC-TEL 2025 (arXiv 2506.17006). 885 learners in tutor-training lessons (not programming). Optional gpt-3.5 explanatory feedback, propensity-adjusted. Significant benefits in 2 of 7 lessons (ES 0.28, 0.33), with no significant time cost. — [arXiv 2506.17006](https://arxiv.org/abs/2506.17006)
- Other studies cited in Liu et al.'s literature review (I did not verify them independently): Barcaui (2025) RCT, "ChatGPT as a cognitive crutch," *Social Sciences & Humanities Open* 12:102287, reports lower knowledge retention with unrestricted ChatGPT. Strömberg, Lei & Wu (2026, SSRN 6868618) use diff-in-diff on Chinese secondary schools and find GenAI adoption raised homework scores but lowered exam scores. — as cited in [Liu et al. 2026](https://edworkingpapers.com/sites/default/files/ai26-1598.pdf)

**Usage/observational and vendor data**
- [Obs, Vendor] Anthropic Education Report (2025-04-08). 574,740 academic conversations from higher-ed accounts. ~47% were "Direct" (resolve as fast as possible) rather than "Collaborative". Computer Science was 36.8% of conversations. Anthropic notes that even collaborative conversations can have questionable learning outcomes. — [Anthropic](https://www.anthropic.com/news/anthropic-education-report-how-university-students-use-claude)
- [Obs] CS50 Duck (Liu, Zenke, Liu, Holmes, Thornton & Malan, SIGCSE 2024, DOI 10.1145/3626252.3630938). Rolled out Summer–Fall 2023 to ~70 summer students, then thousands online, then ~500 on campus. Mid-semester survey: 47% "very helpful", 26% "helpful"; 17% used it >10×/week. Staff review: 22/25 (88%) curricular answers correct and 30/39 (77%) administrative answers correct. **No learning-outcome data.** — [paper PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)

### Inferences
- The evidence agrees on a "performance ≠ learning" gap (Bastani; Iris RCT; Anthropic Trio; Strömberg; UMD). **The platform must never treat in-session success with AI help as evidence of mastery.**
- Tutors that helped (GPT Tutor, Kestin, Iris on motivation, LearnLM supervised) shared three features. They had **access to verified correct solutions**, they **withheld direct answers**, and they **enforced structure outside the prompt**. Tutors that hurt or did nothing (GPT Base, UMD's default direct mode, ChatGPT arms) gave answers on demand.
- For a rusty adult who once could code, the closest analogue is the Anthropic Trio study (experienced Python users learning something new). There, AI delegation and AI-driven debugging cut comprehension, and conceptual questioning or "generate, then interrogate" preserved it. Prior knowledge does not protect against offloading; *how* the AI is used does.
- Restricting answers is not enough. Over-restrictive Socratic tutoring can backfire (Eastwood 2026: rated worst, more off-platform LLM use), and under-use is a real failure mode (Khanmigo, UMD). The tutor has to be useful enough that the learner does not go to an unrestricted chatbot.

### Gaps
- No RCT I found measures **delayed retention (weeks later)** for an LLM programming tutor. Programming RCTs measure immediately or within the same session.
- I could not access the full Iris RCT paper (ScienceDirect returned 403), so its numbers come from the developers' results page.
- An unverified search snippet described a Pankiewicz & Baker GPT-4o compiler-error RCT (248 students: faster error resolution, no post-test difference). I could not locate the primary source, so it is excluded from the findings.
- No study isolates adult self-learners on a personal platform. All the evidence comes from K-12, university or lab samples.

---

## 2. Which tutor behaviors produce learning? (Socratic questioning, hint ladders, self-explanation, error explanation, timing, guardrails)

### Takeaway
The behaviors with the best evidence are these:
- graduated hints that start at "where to look" and end, only if needed, at concrete code;
- tutoring that gets the learner to correct their own error (Socratic or scaffolded) rather than handing over an explanation or the fix;
- forced engagement with any AI-produced code ("explain each step before reveal", "trace and predict");
- fading help as skill grows.

Guardrails that live only in the prompt leak, which is why CS50's Duck still emits code blocks up to a quarter of the time. Effective systems also enforce rules in code: ordering, output screening and rate limits.

### Cited Findings

**Hint ladders: levels and content**
- [Lab-qual] Xiao, Hou & Stamper, "Exploring How Multiple Levels of GPT-Generated Programming Hints Support or Disappoint Novices" (CHI EA 2024; arXiv 2404.02213). "LLM Hint Factory" with **4 levels**: (1) orientation, i.e. where to focus; (2) next step in concise words; (3) a *similar* example code snippet; (4) the exact code for the next step. Learners could move freely between levels. 12 novices, think-aloud + pre/post. **High-level natural-language hints alone were often unhelpful or misleading**, especially for next-step and syntax questions. Adding lower-level hints such as commented example code helped most. — [arXiv 2404.02213](https://arxiv.org/abs/2404.02213)
- [Bench + user study] Heickal & Lan, "Generating Feedback-Ladders for Logical Errors in Programming using LLMs" (EDM 2024; arXiv 2405.00302). GPT-4 ladder for one buggy submission: L0 correct/incorrect verdict → L1 failing test case → L2 high-level explanation → L3 location hint → L4 concrete code change. Recommended use is to start high and move down only while the student is still stuck. Rated effectiveness was lower for the higher (vaguer) levels and for higher-scoring submissions. — [arXiv 2405.00302](https://arxiv.org/abs/2405.00302)
- [Expert judgement study] Brown, Weill-Tessier, Leinonen, Denny & Kölling, "Howzat? … Human and AI Next-Step Hints for Novice Programmers" (arXiv 2411.18151, Nov 2024). 44 Java educators ranked hints by comparative judgement. With a good multi-stage prompt, GPT-4 hints beat hints written by expert humans. The best hints were **80–160 words** at a **US grade-9 reading level or below**. **Offering alternative approaches was judged bad.** Sentiment did not matter. — [arXiv 2411.18151](https://arxiv.org/abs/2411.18151)
- [Bench] Phung et al., LAK 2024, "GPT-4 Tutor Model for Hint Generation and GPT-3.5 Student Model for Hint Validation." GPT-4 hints were grounded by putting **failing test cases and fixes in the prompt**. A weaker model then acted as a simulated student to *validate* each hint before release (hints that fail validation are withheld). The paper's motivation cites prior benchmarking in which GPT-4's hint quality was ~60% vs >90% for human tutors. Using GPT-4 as the validator lowered precision, so a weaker "student" model was the better validator. Python datasets covered basic algorithms, regex and pandas. — [arXiv 2310.03780](https://arxiv.org/abs/2310.03780); [LAK PDF](https://machineteaching.mpi-sws.org/files/papers/lak2024_GPT4Hints-GPT3.5Val.pdf)

**Socratic / scaffolded self-correction vs explanations**
- [Experiment, Preprint] Asher, Cao & Carvalho, "Turning Errors into Successes: Designing LLM Tutoring Around Scaffolded Error Correction," arXiv 2611.20061 (2026-11-15). Pre-registered, 400 adults, constraint-equation task (not code). After each error, participants got one of: the correct answer, a generic explanation, a personalized LLM explanation, or Socratic tutoring. Socratic tutoring resolved **64% of errors through dialogue** and scored **+0.24 SD** on practice-aligned post-test items vs both explanation arms. It was rated more interesting and less frustrating but **took nearly 2× as long**. **Personalized LLM explanations were no better than generic ones, and neither reliably beat simply seeing the correct answer.** The abstract does not state the assignment method. — [arXiv 2611.20061](https://arxiv.org/abs/2611.20061)
- [RCT, Preprint] Eastwood et al. 2026 (see §1): Socratic + full context was the *least* favored configuration in a CS1 RCT. Socratic style can become a roadblock. — [arXiv 2609.29995](https://arxiv.org/abs/2609.29995)
- [Vendor] OpenAI ChatGPT "study mode" (launched 2025-07-29) combines Socratic questioning, hints and self-reflection prompts, and can be toggled off mid-conversation. — [OpenAI](https://openai.com/index/chatgpt-study-mode/); [TechCrunch](https://techcrunch.com/2025/07/29/openai-launches-study-mode-in-chatgpt). Anthropic launched Claude "Learning mode" for Claude for Education in April 2025 and extended it to all users plus Claude Code learning/explanatory output styles in Aug 2025. — [Engadget](https://engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html). **I found no published learning-outcome evaluation of either vendor mode.**

**Forced engagement with AI code / self-explanation**
- [Controlled user study] Kazemitabaar, Huang, Suh, Henley & Grossman, IUI 2025, "Exploring the Design Space of Cognitive Engagement Techniques with AI-Generated Code." Study 1: n=82 novices. **Lead-and-Reveal**: the AI walks through the solution step by step, and the learner must explain each step's action or decision before the next is revealed. **Trace-and-Predict**: the learner traces code on a sample input and predicts variable values. These two were the most balanced techniques. Lead-and-Reveal brought perceived and actual coding ability closer together without raising cognitive load. — [arXiv 2410.08922](https://arxiv.org/abs/2410.08922)
- [Obs deployment] Kazemitabaar et al., "CodeAid," CHI 2024. ~700 students in a C/systems course over 12 weeks, >8,000 interactions. Guardrails **block direct code solutions even on request**; the tool uses interactive pseudo-code and annotations of the student's own code instead. Students mainly used it for concepts and debugging, and a minority tried to extract code. Educators worried about occasional incorrect feedback and students defaulting to ChatGPT. — [arXiv 2401.11314](https://arxiv.org/abs/2401.11314)
- [RCT, Vendor] Anthropic Trio study (§1): the highest-scoring pattern was generation-then-comprehension (asking follow-up "why" questions after receiving code). Conceptual-only inquiry also preserved learning. — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)
- [Vendor doc] Claude Code's "Learning" output style inserts a `TODO(human)` marker in the code, asks the user to write that piece, then **stops and waits**. It gives one "Insight" on the user's code before continuing. — [Claude Code docs: output styles](https://code.claude.com/docs/en/output-styles). A third-party system-prompt dump (unofficial) says it requests **2–10-line pieces** where design decisions exist and allows only one TODO(human) at a time. — [GitCode blog (unofficial)](https://blog.gitcode.com/a56c721a8d8daa095fa41ca39e61ae40.html)
- "Explain in Plain English" (EiPE) code-explanation questions can now be auto-graded. In Smith & Zilles's code-generation-based grading, an LLM writes code *from the student's explanation* and unit tests check whether the explanation was accurate. — [NSF PAR 10644112](https://par.nsf.gov/biblio/10644112); 2026 work on LLM-as-judge vs similarity scoring for EiPE: [AIME-Con 2026](https://aclanthology.org/2026.aimecon-main.10/); Denny et al., "Explaining Code with a Purpose" [arXiv 2403.06050](https://arxiv.org/abs/2403.06050)

**Error-message explanation without the fix**
- [Bench] Leinonen et al., SIGCSE 2023 (DOI 10.1145/3545945.3569770). Codex enhanced 9 Python error messages, 81 outputs. 88% comprehensible; correct explanation in 48% of inputs; correct fix in 33%; better than the original message 54% of the time. Temperature 0 was clearly better than 0.7. Wrong outputs sounded as confident as right ones, and the authors judged it "not yet ready for production". — [arXiv 2210.11630](https://arxiv.org/abs/2210.11630)
- [Quasi] Pankiewicz & Baker 2024 (§1): auto-shown GPT-4 compiler-error hints that were **faded out mid-module** left the learners better than control on 5 of 6 error types once hints were off. — [arXiv 2403.12737](https://arxiv.org/abs/2403.12737)

**Guardrails in production: what worked and what leaked**
- [Obs] CS50 Duck guardrails (SIGCSE 2024): system prompt to act as a TA that guides rather than gives solutions; RAG over lecture captions to reduce hallucination; prompt-injection screening; **"hearts" rate limit (10 hearts, +1 every 3 min, 1 per interaction)**, which the course justifies on both cost and pedagogical grounds (formulate better questions, take reflective breaks). Students asked for fewer limits, and staff kept them. — [paper PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)
- [Obs/interview] Harvard Gazette, "Taming the Duck, for starters" (2026-09-25). The Duck is designed to "ask more questions than it answers". **Custom code screens responses before students see them and rejects or retries non-constructive ones.** The interviewer states that the Duck **still emits code blocks up to a quarter of the time** despite instructions, and Malan did not dispute it. One student asked ~200 questions, prompting the heart system. — [Harvard Gazette](https://news.harvard.edu/gazette/story/2026/09/taming-the-duck-for-starters/)
- [RCT] Kestin 2025: prompt alone did not enforce step order, so the platform enforced sequential scaffolding. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- [Obs] A 2026 deployment of a course-aware AI tutor in intro programming found students agreed it avoided full solutions. Some reported that turning hints into a working solution stayed hard. — [arXiv 2604.11836](https://arxiv.org/html/2604.11836)

**Feedback timing / proactivity**
- [Controlled user study] Chen, Zhu, et al., "Need Help? Designing Proactive AI Assistants for Programming," CHI 2025. Proactive suggestions raised tasks completed by 12–18%. 80–90% preferred proactive over chat-only, but **only about half preferred the high-frequency variant**. Good timing depended on recent editor activity and the user's reactions to earlier suggestions. Outcome was productivity, not learning. — [arXiv 2410.04596](https://arxiv.org/abs/2410.04596)
- [Controlled user study] Pu, Chen, et al., "Assistance or Disruption?" CHI 2025. Applies interruption-management theory to proactive AI programming support and finds trade-offs in **user control, ownership and code understanding**. — [arXiv 2502.18658](https://arxiv.org/abs/2502.18658)
- [RCT] Khanmigo trial: low use was attributed partly to a **non-proactive interface**. — [NBER w35620](https://www.nber.org/papers/w35620). UMD trial: only 0.7% of requests sought feedback on the student's own work. — [EdWorkingPaper](https://edworkingpapers.com/sites/default/files/ai26-1598.pdf)

### Inferences
- **Number of hint levels:** the convergent evidence supports **one platform-generated level plus four LLM levels**: L0 verdict + failing test from running code; L1 location/orientation; L2 conceptual next step in words; L3 analogous worked example; L4 bottom-out concrete fix. Both Xiao (4 levels) and Heickal & Lan (5 incl. verdict) landed here. Xiao shows L2 alone is often not enough, so L3 (an analogous example, not the learner's own solution) is the key bridge before giving the answer.
- **Gate full solutions** behind (a) at least one genuine attempt, (b) reaching L3 first and (c) an explicit request. After a bottom-out, require retyping (not paste) plus an explain-or-predict check. This mirrors Lead-and-Reveal and the generation-then-comprehension pattern.
- **Socratic, but bounded:** use 1–2 guiding questions per stuck point, then escalate a hint level. Do not run open-ended questioning loops; Eastwood shows they become roadblocks and push learners to other LLMs. Asher shows scaffolded self-correction is worth ~2× the time when it resolves the error.
- **Error explanations:** explain *what the error means and where* (L1/L2) and leave out the fix. Ground every claim in the platform's actual run output. Leinonen shows ungrounded fix suggestions are unreliable and confidently wrong.
- **Fade help:** Pankiewicz & Baker's "hints for first half of module, then off" design is a cheap fading rule with positive evidence.

### Gaps
- No RCT directly compares **different numbers of hint levels**, or **gating rules for full solutions**, in an LLM programming tutor. The level design above is synthesized from lab and expert-judgement studies.
- No learning-outcome evaluation was found for ChatGPT Study Mode or Claude Learning Mode, only product descriptions.
- Kazemitabaar IUI 2025 Study 2 details and the full Asher et al. methods (randomization) were not verified.
- No study specifically on **SQL** tutoring with LLMs turned up in this search.

---

## 3. AI-generated exercises and explanations: quality, failure modes, verification

### Takeaway
LLMs produce mostly sensible, novel programming exercises. Without execution-based checks, though, a large share have **broken or mismatched tests, print-vs-return mismatches, unstated edge cases and ambiguous statements**, and invalid generated tests measurably hurt learners. Running the reference solution is necessary but not sufficient. Generated tests should be cross-validated, and the problem statement should be checked for ambiguity, for example by having an independent model or a "simulated student" solve it from the statement alone.

### Cited Findings
- [Bench] Sarsa, Denny, Hellas & Leinonen, ICER 2022 (DOI 10.1145/3501385.3543957), Codex-generated exercises. 120 of 240 manually assessed: **75.0% sensible, 81.8% novel, 76.7% matched their sample solution**. 84.6% had a sample solution, of which 89.7% ran. 70.8% had tests. **Only 30.9% (51/165) of solution+test pairs passed all tests.** Passing test sets averaged 98% statement coverage. Failure modes: **solution printed where tests expected a return value** (the most common), impossible test expectations, missing tests, under-specified boundary cases, and wrong code explanations (e.g., `speed > 100` explained as "less than 100"). Code explanations covered all parts 90% of the time, but only **67.2% of lines were explained correctly**. — [arXiv 2206.11861](https://arxiv.org/abs/2206.11861); [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2206.11861)
- [User study] Contextually personalized exercises generated with GPT-4 in an intro course were rated generally high quality by researchers and students, and students found them engaging. — [arXiv 2407.11994](https://arxiv.org/abs/2407.11994)
- [Bench, ongoing] ICPEC 2024: an OpenAI-API exercise pipeline yielded only **120 correct of 562 generated items (~21%)**. Failures were malformed JSON (35%) and code errors (44%), with difficulty producing matching test cases. — [Dagstuhl OASIcs ICPEC 2024](https://drops.dagstuhl.de/storage/01oasics/oasics-vol122-icpec2024/OASIcs.ICPEC.2024.21/OASIcs.ICPEC.2024.21.pdf)
- [Bench] "Automating Autograding: LLMs as Test Suite Generators for Introductory Programming" (arXiv 2411.09261, 2024). GPT-4 test suites built from the statement + reference solution identified most valid solutions and were usually at least as comprehensive as instructor suites. **Generating tests also exposed ambiguities in some problem statements.** — [arXiv 2411.09261](https://arxiv.org/abs/2411.09261)
- [RCT, Preprint] Heickal & Lan 2026 (ProgFeed): the effect of AI-generated failing-test feedback **depended on the test's validity**. Invalid generated tests are a real hazard for learners, not just a quality metric. — [arXiv 2606.08807](https://arxiv.org/abs/2606.08807)
- [Bench] Phung et al. 2024: generate-then-validate with a simulated weaker "student" model raised hint precision. The same pattern applies to checking whether a statement is solvable. — [arXiv 2310.03780](https://arxiv.org/abs/2310.03780)
- [Obs] CS50: 88% of curricular answers were correct with RAG over course materials, vs 77% for administrative answers where the model's training data was stale. Grounding in authoritative course content matters. — [CS50 SIGCSE 2024 PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)
- [RCT] Bastani: ungrounded GPT-4 was correct only 51% on high-school math. GPT Tutor supplied solutions to the model. — [PsyPost](https://www.psypost.org/unrestricted-generative-ai-harms-high-school-math-learning-by-acting-as-a-crutch/). Kestin likewise put verified step-by-step solutions in the prompt. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)

### Inferences
- A verification pipeline for generated items that matches the observed failure modes:
  1. The structured output must validate against a JSON schema (the ICPEC failures were mostly malformed JSON). Claude's structured outputs address this directly.
  2. The reference solution executes and passes all tests (Sarsa: only ~31% did with Codex).
  3. Tests check *return values or result sets*, not stdout, unless the statement says print (the print-vs-return failure).
  4. A second, independent solve: a separate model call sees only the statement plus examples, writes a solution, and must pass the hidden tests. Failure flags ambiguity (from Phung's simulated student and 2411.09261's ambiguity finding).
  5. Mutation/wrong-solution check: a few plausible buggy variants must *fail* at least one test, so the suite is not vacuous.
  6. Edge cases (empty input, zero, None/NULL, ties) are stated explicitly in the statement.
- SQL-specific (inference; no direct evidence found): results should be compared as order-insensitive multisets unless the statement requires `ORDER BY`. Fixtures need to include NULLs, duplicates and ties, since these are the SQL analogue of unstated boundary cases.
- When the tutor gives hints or explanations on a generated item, **pass it the verified reference solution and the actual test results.** Never let it re-derive the answer.

### Gaps
- No study found on the quality of **LLM-generated SQL exercises** or SQL test fixtures specifically.
- Most exercise-quality data is from Codex or GPT-4 (2022–2024). I found no 2025–2026 benchmark of frontier-model (e.g., Claude 4-class) exercise-generation error rates, so current error rates are likely lower but unmeasured.

---

## 4. AI for adaptive pacing: diagnosing missing prerequisites, remediation, knowledge tracing

### Takeaway
LLMs can tag knowledge components, propose misconceptions in student code (~82% accuracy on one Python benchmark) and support test-case-level knowledge tracing. **There is no controlled evidence yet that LLM-driven prerequisite diagnosis or LLM knowledge tracing improves learning outcomes.** The strongest pacing evidence is that AI support works best combined with a mastery requirement (NBER 2026). Classic ITS literature warns that the way hint use enters mastery estimates changes learner behavior.

### Cited Findings
- [RCT, Preprint] Oreopoulos et al. NBER w35621 (Aug 2026): AI support slowed progression but improved accuracy and recovery after mistakes. **Mastery progression + AI gave the best delayed-test result** (marginal, concentrated on practiced material). Mastery alone did not help. — [NBER](https://www.nber.org/papers/w35621)
- [Bench, Preprint] McMining (arXiv 2510.08827): LLM discovery of misconceptions in Python student code, **82.0% accuracy** on a 1,063-sample benchmark, with 41 novel misconceptions proposed. The benchmark assumes one primary misconception per sample. — [arXiv 2510.08827](https://arxiv.org/abs/2510.08827)
- [Bench, Preprint] TIKTOC: test-case-informed knowledge tracing for open-ended coding predicts per-test pass/fail and beats correctness-only coding KT. — [arXiv 2410.10829](https://arxiv.org/abs/2410.10829)
- [Bench, Preprint] An LLM pipeline that generates and tags knowledge components for open-ended programming problems, then runs KT on CodeWorkout data. — [arXiv 2502.18632](https://arxiv.org/abs/2502.18632)
- [Bench, Preprint] "Can LLMs Simulate Novice Programmers' Misconceptions?" (arXiv 2610.10656, 2026): larger models simulate misconceptions better and generate diagnostic code-tracing questions. **Code-specialized models tend to default to correct answers**, which is a risk when asking an LLM to "think like the student". — [arXiv 2610.10656](https://arxiv.org/abs/2610.10656)
- [Quasi] Pankiewicz & Baker 2024: fading hints (on for the first half of a module, off for the second) left learners better than control when unassisted. — [arXiv 2403.12737](https://arxiv.org/abs/2403.12737)
- **Hint usage in mastery models (classic ITS literature):**
  - Traditional KT either scores a hint request as *incorrect* or drops it. EDM 2018 argues this conflates two different learning events. — [EDM 2018 paper 100](https://educationaldatamining.org/files/conferences/EDM2018/papers/EDM2018_paper_100.pdf)
  - Standard "first attempt" rollups ignore later attempts and hints, so a student who needed one small hint looks the same as one who needed the full answer. — [EDM 2021 paper 105](https://educationaldatamining.org/EDM2021/virtual/static/pdf/EDM21_paper_105.pdf)
  - In ASSISTments, binary first-attempt scoring that penalizes hints **made students afraid to use hints** (help avoidance). — [EDM 2015 short paper](https://www.educationaldatamining.org/EDM2015/proceedings/short404-407.pdf)
- [Obs] Prather 2024 and Bastani 2025 both document **illusions of competence and overconfidence** after AI help, so self-assessment cannot stand in for measured mastery. — [arXiv 2405.17739](https://arxiv.org/abs/2405.17739); [Wharton](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)

### Inferences
- Use the LLM to **propose** a diagnosis (likely misconception or missing prerequisite) as structured JSON with confidence. **Confirm it with a short targeted diagnostic item** (e.g., a predict-the-output or one-concept micro-problem) before rerouting the learner to remedial content. Treat LLM diagnosis as a hypothesis generator, given ~82% benchmark accuracy and no outcome evidence.
- Log hint use as **graded evidence** rather than binary right/wrong, and keep the penalty modest so the learner is not discouraged from asking. Suggested weights:
  - unassisted first-try pass = strong mastery evidence;
  - L1–L2 = partial credit;
  - L3–L4 / bottom-out = no mastery credit for that item, and schedule an **isomorphic fresh item later** (spaced).
- Declare mastery only on **unassisted** success (no hints, AI panel closed) on a new item. This is the platform's version of "AI + mastery" (NBER) and the remedy for the performance/learning dissociation (§1).
- Use per-test-case results as KT inputs (TIKTOC-style). The platform already runs tests, so this is free signal.

### Gaps
- No RCT or field experiment found showing that **LLM-based prerequisite diagnosis or LLM knowledge tracing improves learning** in programming. Everything found is offline prediction or benchmark accuracy.
- No head-to-head study found comparing mastery estimates under different hint-scoring rules (binary-incorrect vs graded vs dropped).
- No evidence found specific to remediation for **rusty adult re-learners** (e.g., whether to re-teach or just re-practice).

---

## 5. AI as interviewer (mock-interview follow-up questioning)

### Takeaway
Evidence is thin and mostly qualitative. Small studies report that LLM interviewers with adaptive follow-up questions feel realistic and raise confidence, and that LLM follow-up questions are roughly as good as human ones in a neighboring domain (requirements elicitation). I found no controlled study showing that AI mock interviews improve real technical-interview performance.

### Cited Findings
- [Lab-qual, Preprint] Gomez, Batham, Volonte & Do, "Virtual Interviewers, Real Results: Exploring AI-Driven Mock Technical Interviews on Student Readiness and Confidence," arXiv 2506.16542 (June 2025; CSCW Companion '25). N=20, formative and qualitative, no control group. Participants found whiteboarding with real-time feedback "realistic and helpful" and reported more confidence and better articulation of decisions. **Problems with conversational flow and timing** were noted. — [arXiv 2506.16542](https://arxiv.org/abs/2506.16542)
- [User study] An LLM-simulated interview study (ACM DOI 10.1145/3701188) found that participants valued **adaptive follow-up questions** for realism and deeper thinking. — [ACM DOI](https://doi.org/10.1145/3701188) (via search summary; full text not read)
- [System + study, Preprint] Conversate (arXiv 2410.05570): LLM interview simulation that generates contextual follow-ups and gives dialogic feedback for reflective learning. — [arXiv 2410.05570](https://arxiv.org/abs/2410.05570)
- [Bench, Preprint] In requirements-elicitation interviews, GPT-4o follow-up questions were neither better nor worse than human-written ones overall. Good follow-ups had to be clear, relevant and informative. — [arXiv 2507.02858](https://arxiv.org/abs/2507.02858)
- [Bench, Preprint] "LLM-as-an-Interviewer" (arXiv 2412.10424): multi-turn interviews with feedback and follow-ups reveal behaviors that static Q&A misses, such as how the subject responds to feedback and clarification. — [arXiv 2412.10424](https://arxiv.org/abs/2412.10424)
- Related learning evidence: requiring the learner to articulate decisions (Lead-and-Reveal, EiPE) has controlled support (§2). Debugging comprehension is the skill most damaged by AI delegation (Anthropic Trio). — [arXiv 2410.08922](https://arxiv.org/abs/2410.08922); [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)

### Inferences
- Interviewer mode should be a **separate, no-help mode**: no hints, no code. Follow-up questions about complexity, edge cases, alternative approaches, testing strategy and "what would break if…" probe understanding. In tutor mode, alternatives are discouraged (Brown et al.); in interview mode they are the point.
- Follow-ups should be anchored to the learner's actual code and the platform's test results, to avoid generic questions. Turn-taking should be explicit (learner signals "done"), given the reported flow and timing problems.
- Interviewer-mode transcripts can be graded with a rubric as a **self-explanation signal** for mastery.

### Gaps
- No RCT or controlled study found showing that AI mock interviews improve real interview outcomes or coding-interview performance.
- No credible practitioner reports with data (e.g., from interview-prep companies) turned up in this search pass. The Berkeley MIDS capstone (2026) is a student project only. — [Berkeley MIDS](https://www.ischool.berkeley.edu/projects/2026/interviewpro-agentic-ai-mock-interviewer)

---

## 6. Synthesized concrete rules for the code-dojo AI tutor (Claude, structured JSON, "teach first, then practice")

### Takeaway
Run the tutor as a **grounded, ladder-gated coach**:
- It sees the verified reference solution and real test output.
- It speaks unprompted only at a few defined moments.
- It never writes the learner's code into the editor.
- It escalates hints one level at a time, then requires re-typing and explanation after any bottom-out.
- It feeds hint depth into a mastery model that counts only unassisted success on a fresh item.

These rules are inferences from the evidence above. Each cites its primary support.

### Cited Findings
(Each rule's supporting evidence is cited inline; see §§1–5 for full details.)
- Grounding the tutor in correct solutions removed harm and/or produced gains — [Bastani PNAS 2025](https://doi.org/10.1073/pnas.2422633122); [Kestin Sci Rep 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- Prompt-only guardrails leak (CS50 Duck emits code up to ~25% of the time), so enforcement in code is needed — [Harvard Gazette 2026-09-25](https://news.harvard.edu/gazette/story/2026/09/taming-the-duck-for-starters/); [Kestin](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- Direct-answer default configuration lowered grades — [Liu et al. 2026](https://edworkingpapers.com/sites/default/files/ai26-1598.pdf)
- AI debugging/delegation hurts comprehension, and conceptual or follow-up questioning preserves it — [Anthropic 2026](https://www.anthropic.com/research/AI-assistance-coding-skills)
- Hint level design and length/readability — [Xiao 2024](https://arxiv.org/abs/2404.02213); [Heickal & Lan 2024](https://arxiv.org/abs/2405.00302); [Brown et al. 2024](https://arxiv.org/abs/2411.18151)
- Bounded Socratic dialogue helps, unbounded hurts — [Asher 2026](https://arxiv.org/abs/2611.20061); [Eastwood 2026](https://arxiv.org/abs/2609.29995)
- Proactivity: helps completion, but frequency and ownership trade-offs exist, and passivity reduces use — [Chen CHI 2025](https://arxiv.org/abs/2410.04596); [Pu CHI 2025](https://arxiv.org/abs/2502.18658); [Khanmigo NBER w35620](https://www.nber.org/papers/w35620)
- Fading and mastery gating — [Pankiewicz & Baker 2024](https://arxiv.org/abs/2403.12737); [Oreopoulos NBER w35621](https://www.nber.org/papers/w35621)
- Hint scoring in KT and help avoidance — [EDM 2015](https://www.educationaldatamining.org/EDM2015/proceedings/short404-407.pdf); [EDM 2018](https://educationaldatamining.org/files/conferences/EDM2018/papers/EDM2018_paper_100.pdf)
- Learner writes the code (TODO(human), 2–10 line pieces) — [Claude Code output styles docs](https://code.claude.com/docs/en/output-styles)
- Forced engagement with revealed code — [Kazemitabaar IUI 2025](https://arxiv.org/abs/2410.08922)

### Inferences

**A. Grounding and enforcement (architecture)**
1. Every tutor call receives the **verified reference solution, the test suite, the learner's current code and the actual run output** (stdout/stderr/traceback/failed-test diff, SQL result-set diff) in hidden context. The tutor must never compute expected outputs itself. *(Bastani, Kestin, Phung, Leinonen.)*
2. Enforce pedagogy **in code, not just in the prompt**. The JSON schema has fields such as `hint_level`, `contains_code`, `code_line_count`, `asks_question`, `reveals_solution`. A validator rejects and retries (or truncates) any response whose code exceeds the cap for its level. For example: L1–L2 = 0 lines of learner-solution code; L3 = example code only, which must not textually match the reference solution (check by similarity); L4 = minimal diff. *(CS50 screening layer; ~25% leak rate.)*
3. Lesson flow (teach → worked example → practice) and hint escalation order are **state-machine controlled by the platform**, and the model cannot skip levels. *(Kestin: prompt alone did not enforce sequencing.)*
4. Use low temperature for diagnostic or explanatory calls. *(Leinonen: temperature 0 was much more accurate.)*

**B. Hint ladder (how many levels, where solutions are gated)**
5. **5 levels (L0 from the platform + 4 from the LLM):**
   - L0 verdict + first failing test, produced by the platform without the LLM;
   - L1 *where* to look (line or region, concept name);
   - L2 *what* to do next in words (80–160 words, plain language, no code, no alternative approaches);
   - L3 an **analogous** worked example (different data or names, commented);
   - L4 bottom-out: a minimal concrete fix for the next step only, not the whole solution.

   *(Xiao; Heickal & Lan; Brown.)*
6. **Gating:** L1 needs one submitted attempt. Each further level needs a new attempt or an explicit "still stuck" plus a short statement of what the learner tried. L4 needs L3 first and explicit confirmation. **A full solution is shown only after the problem is abandoned or ended**, never as a hint. A Lead-and-Reveal walkthrough is required (the learner explains each step before the next appears). *(Bastani; Kazemitabaar IUI 2025; CodeAid.)*
7. Socratic budget: at most **1 question per turn and 2 Socratic turns per stuck point**, then escalate one level automatically. Always offer an "explain it directly" escape that costs one hint level. The tutor must be useful enough that the learner doesn't open an unrestricted chatbot instead. *(Asher; Eastwood; Iris "comfort trap".)*
8. **Fade:** for a skill already demonstrated unassisted, cap hints at L2 on later items of that skill. In the final "check" problem of a lesson, hints are off. *(Pankiewicz & Baker.)*
9. Optional soft budget (visible "hearts" per problem or session) to encourage forming a question before asking. For a single self-motivated adult this should be gentle and adjustable. *(CS50 hearts: 10, +1 every 3 min.)*

**C. When the tutor speaks unprompted vs waits**
10. **Speak unprompted only at these triggers:**
    - (a) after a failed run/submission: offer L0 automatically, plus a one-line *offer* of help (not the help itself);
    - (b) the same error class repeats ≥2 times: offer a targeted micro-explanation of the error *meaning* (not the fix);
    - (c) no edits and no runs for N minutes (e.g., 3–5) after a failure: one check-in question;
    - (d) after a correct submission: one short explain/predict question or one "insight" (generation-then-comprehension), at most once per problem;
    - (e) during the teach phase: comprehension checks at designed points.

    *(Chen/Pu proactivity trade-offs; Khanmigo non-proactive under-use; UMD 0.7% own-work feedback.)*
11. **Never interrupt while the learner is typing or before their first run.** Never volunteer the next step, and never give more than one unprompted message per trigger.

**D. Hard "never" rules**
12. Never insert or overwrite code in the learner's editor. Never offer a copy/paste button on tutor code. Bottom-out code must be **retyped** (render it as an image or disable copying, or show it, hide it, then have the learner type from memory). *(TODO(human) pattern; Anthropic Trio delegation harm.)*
13. Never debug *for* the learner: no "here is the corrected function". Point to the symptom and the evidence (failing input, actual vs expected) and ask for a hypothesis first. *(Anthropic Trio: iterative AI debugging was the worst pattern at ~24%, and debugging questions showed the biggest gap.)*
14. Never state that code is correct, or predict an output, without the platform having run it. Never invent test results.
15. Never offer alternative approaches during practice hints (save them for post-solve review or interview mode). *(Brown et al.)*
16. Never give a full solution before a genuine attempt, and never during the final check problem.
17. Never inflate praise or confidence. Show the learner objective calibration ("solved with L3 hint; mastery not yet credited"). *(Illusion of competence: Prather; overconfidence: Bastani.)*

**E. Keeping the learner typing their own code**
18. Practice items are "learner writes all solution code". In teach-phase worked examples, use **completion problems** in which the learner fills 2–10-line `TODO` gaps (Claude Code learning-mode pattern), moving from more given code to less across the lesson.
19. After any L3/L4 hint or post-mortem solution reveal, require **(i)** retyping the relevant lines and **(ii)** one Trace-and-Predict or explain-in-plain-English answer. Auto-grade it (LLM judge, or code-generation-based grading where the LLM writes code from the explanation and the tests check it). *(Kazemitabaar; Smith & Zilles.)*

**F. Logging hint usage into mastery**
20. Log per attempt: `max_hint_level`, `n_hints`, `socratic_turns`, `time_to_first_run`, `n_runs`, `per_test_pass_vector`, `bottom_out_used`, `explanation_score`, `error_classes`.
21. Mastery credit, as a suggestion. Avoid binary "hint = wrong", which causes help avoidance.
    - Unassisted first-try pass = 1.0.
    - Pass after L0 only = 0.8.
    - L1–L2 = 0.5.
    - L3 = 0.2.
    - L4 or solution reveal = 0, and schedule an **isomorphic new item** after a spacing delay.
22. A skill is "mastered" only after **≥2 unassisted passes on different generated items, separated in time**. In-session assisted success never counts alone. *(Oreopoulos AI+mastery; performance/learning dissociation in Bastani, Iris and Strömberg.)*
23. Use LLM error diagnosis to **propose** a missing prerequisite (JSON: `suspected_kc`, `evidence`, `confidence`). Confirm it with one diagnostic micro-item before branching to remediation. *(McMining ~82% benchmark accuracy; no outcome RCTs.)*

**G. Generated problems**
24. Accept a generated problem only if all of these hold:
    - schema-valid;
    - the reference solution passes;
    - tests check returns or result sets rather than prints;
    - an **independent blind solve** from the statement passes (ambiguity check);
    - ≥1 plausible buggy variant fails;
    - edge cases (empty, NULL, ties, duplicates) appear explicitly in the statement.

    Never show learners an AI-generated failing test that hasn't been validated against the reference solution. *(Sarsa; ICPEC 2024; 2411.09261; ProgFeed.)*

**H. Interview mode**
25. Separate mode: no hints, no code from the AI. 2–4 follow-ups anchored to the learner's code and complexity, plus one edge-case probe. Explicit turn-taking. Rubric-scored. *(Thin evidence: Gomez et al. N=20; follow-up quality ≈ human in a related domain.)*

### Gaps
- The specific numbers above (5 levels, 2 Socratic turns, credit weights, 3–5 min idle trigger, ≥2 unassisted passes) are **design choices synthesized from heterogeneous evidence, not values tested in RCTs**. They should be treated as tunable defaults and A/B-tested on the learner's own data where possible.
- No evidence found on how these rules should differ for a **single adult re-learner** vs students. The Anthropic Trio study (developers with prior Python) is the closest analogue, and it was short-term.
- No evidence found specific to **SQL** tutoring behaviors.
