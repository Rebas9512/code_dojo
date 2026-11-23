# Learning Science for Teaching Programming: What Gets Learners to Independent Code-Writing Fastest

Scope: evidence on instructional techniques and their order for learning to write Python algorithm code and SQL by hand. The target learner is a rusty adult with past programming experience who studies alone toward US big-tech interview level, on a web app with an editor, instant automated judging, and an AI tutor. Researched 2026-11-22.

**Evidence grades used below**
- **[A]** Meta-analysis, or several replicated RCTs.
- **[B]** At least one controlled experiment or RCT, either in programming or strong in a nearby domain.
- **[C]** A single small, quasi-experimental or correlational study, or a finding I could only verify through a secondary source.
- **[D]** Practitioner opinion, theory, or my own extrapolation.

Where a number comes from prior knowledge and was not re-fetched in this session, it is marked "(not re-verified)".

---

## Q1. Worked examples, fading, completion problems, when to switch from examples to writing, and the expertise reversal effect (detecting when to remove scaffolds)

### Takeaway
Worked examples reliably help people who are new to a procedure, with a medium effect (g ≈ 0.5). The same high-guidance instruction becomes neutral or harmful as expertise grows: the expertise reversal effect is about d ≈ +0.5 for novices and about d ≈ −0.4 for knowledgeable learners, and it is strongest in higher education. For a rusty but experienced learner, the default should therefore be to try the problem first and offer the example on demand, with fast backward fading. Scaffolds should be switched by a quick in-task diagnostic: a first-step or rapid-verification probe, ideally combined with a self-rated effort score. Elapsed time is not a good switching signal.

### Cited Findings
- **[A] Worked-example effect, math meta-analysis (2023).** Average effect on math performance was g = 0.48 (robust variance estimation; 43 studies, mostly middle and high school algebra and geometry). The effect held whether examples were used for first acquisition or for practice. Correct examples alone beat incorrect examples and correct+incorrect mixes. Adding self-explanation prompts was a *negative* moderator compared with examples without prompts. — [Barbieri, Miller-Cotto, Clerjuste & Chawla 2023, *Educ. Psychol. Rev.*, doi:10.1007/s10648-023-09745-1](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf); study count from [Learning & the Brain summary](https://www.learningandthebrain.com/blog/?p=7218)
- **[A] Expertise reversal meta-analysis (2025).** 60 experiments, 176 effect sizes, about 5,924 participants. Low-prior-knowledge learners did better with high-assistance instruction (d ≈ 0.505). High-prior-knowledge learners did better with low assistance (d ≈ −0.428 for high vs. low assistance). The effect grows with learner age and is strongest in higher education. Giving novices assistance mattered more than withholding it from experts. — [Tetzlaff, Simonsmeier, Peters & Brod 2025, *Learning and Instruction* 98:102142, doi:10.1016/j.learninstruc.2025.102142](https://doi.org/10.1016/j.learninstruc.2025.102142); effect sizes via the secondary [Learning & the Brain write-up](https://www.learningandthebrain.com/blog/one-size-doesnt-fit-all-teaching-experts-and-novices/) **[numbers are from a secondary source]**
- **[B] Expertise reversal in a programming task.** In programmable logic controller (PLC) programming, worked examples beat problem solving at first, but the advantage disappeared as trainees gained experience. After intensive training, the more complex tasks were learned better through problem solving than through worked examples (Kalyuga, Chandler, Tuovinen & Sweller 2001). — reviewed in [Kalyuga 2007, *Educ. Psychol. Rev.* 19:509–539, doi:10.1007/s10648-007-9054-3](https://link.springer.com/article/10.1007/s10648-007-9054-3); original statement of the effect in [Kalyuga, Ayres, Chandler & Sweller 2003, *Educational Psychologist* 38(1):23–31](https://ro.uow.edu.au/edupapers/136)
- **[B] Sequencing should depend on prior knowledge** (engineering undergraduates, circuit analysis). Novices benefited more from example→problem pairs. More knowledgeable learners benefited more from problem→example pairs and from backward-faded examples (Reisslein et al. 2006). In Reisslein (2005), high-prior-knowledge learners did significantly better with immediate problem solving or *fast* fading (one solution step removed per example) than with *slow* fading (one step per two examples). Low-prior-knowledge learners showed the opposite pattern. — [Kalyuga 2007 review](https://link.springer.com/article/10.1007/s10648-007-9054-3)
- **[B] Backward fading plus self-explanation prompts.** Fading removes the last solution step first, then the last two, and so on. Combining this with self-explanation prompts improved learning (probability problems). — [Atkinson, Renkl & Merrill 2003, *J. Educ. Psychol.* 95(4):774–783](https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/); the alternative title "Combining fading with prompting fosters learning" is noted in [Cambridge CLT chapter refs](https://cambridge.org/core/books/cognitive-load-theory/learning-from-workedout-examples-and-problem-solving/DBA85CE81E9A7B1B090547D12E2F2A04)
- **[B] Completion strategy, programming (4C/ID precursor).** High-school learners who modified and extended existing programs (completion) beat learners who wrote new programs (generation) on program-construction tests, and fewer of them dropped out. They were *not* better at interpreting programs. Matched groups of 28 and 29 students, 10-lesson COMAL-80 course. — [van Merriënboer 1990, *J. Educ. Comput. Res.* 6:265–285](https://research.utwente.nl/en/publications/strategies-for-programming-instruction-in-high-school-program-com/); sample from [Scilit](https://scilit.com/publications/9d6bb5f9d78b45466ec31bab978e6737)
- **[B] Too much scaffolding in a code-tracing tutor.** With N = 97, interface scaffolding and example placement were varied. The best level of assistance was in the *middle* of the range, and the optimum differed between learner subgroups. — [Jennings & Muldner 2021, *IJAIED* 31(4):784–819, doi:10.1007/s40593-020-00217-z](https://ersearch2.cvtisr.sk/vufind/SummonRecord/FETCH-LOGICAL-c341t-4a849be054c8db6e1704f1b7c1958103b251eaf7820c20679d7169fa0406db763?lng=en); [AIED 2021 companion](https://link.springer.com/10.1007/978-3-030-78292-4_17)
- **[B] Writing code beats tracing worked examples, and both beat video** (preregistered, N = 250 adults on Prolific, about a 30-minute intro lesson, 27% with no prior experience). Writing code with immediate AI-generated elaborated feedback scored highest on a novel code-generation test. Writing vs. tracing: b = 11.99, t(234) = 6.04, p < .001. Practice vs. video: b = 6.15, p < .001. Writing took longer than tracing. — [Gold, Tjaden & Carvalho 2026, *Proc. CogSci* 48, "Less Talk, More Code"](https://escholarship.org/uc/item/6vq9j198)
- **[C] SQL worked examples** (DBQA tool: animated, step-by-step execution of SELECT queries with optional text explanations). Of 587 students enrolled, 131 used it enough to analyze. Pre/post scores did not differ significantly between randomized conditions. Exploring more execution steps was *associated* with higher problem success, fewer query-building attempts, and more persistence. Students given text explanations explored more steps, but only in one open-learner-model condition, and mostly in the first two weeks. Use was voluntary, so self-selection is possible. — [Akhuseyinoglu et al. 2022, ITiCSE, doi:10.1145/3502718.3524813](https://acris.aalto.fi/ws/portalfiles/portal/93553168/A_Study_of_Worked_Examples_for_SQL_Programming.pdf)
- **[D, review scope] Programming-specific review.** The worked-example literature in programming covers mainly code-tracing examples and code-generation examples, plus incomplete examples: completion problems and Parsons puzzles. — [Muldner, Jennings & Chiarelli 2022, *ACM TOCE* 23, doi:10.1145/3560266](https://doi.org/10.1145/3560266)
- **[B] How to detect when scaffolds should go (rapid diagnostics):**
  - **First-step method.** Show a task for a limited time and ask "what is your first step?" Experts skip intermediate steps. Correlation with full traditional tests reached r = .92, and testing time fell by up to 4.9×.
  - **Rapid-verification method.** The learner quickly judges whether proposed intermediate steps are correct. It correlated r = .71 and r = .75 with think-aloud observations and cut testing time by 3.2–3.5×.
  - **Adaptive tutorials built on these probes.** Moving learners through decreasing guidance based on the probes beat non-adapted instruction: ES = 0.46 on knowledge gain (Kalyuga & Sweller 2004). Combining the probes with subjective effort ratings gave ES = 0.55 on knowledge and 0.69 on efficiency (Kalyuga & Sweller 2005). Salden et al. 2006 found ES = 0.58.
  - **A concrete advancement rule** (Kalyuga 2006a): advance when the learner verifies every intermediate step correctly *and* rates difficulty below 5 on a 9-point scale.
  - **Caveat.** All of these studies used high-school math and physics.
  - — [Kalyuga 2007 review, pp. 530–532](https://link.springer.com/article/10.1007/s10648-007-9054-3); [Kalyuga & Sweller 2005, *ETR&D* 53:83–93](https://doi.org/10.1007/bf02504800)

### Inferences
- The learner can program, so the expertise reversal effect implies that full worked examples are likely to be **redundant or harmful for concepts they once knew**, such as loops, dicts, basic SQL SELECT/JOIN. They are likely **useful for concepts that are new or never automated**, such as monotonic stacks, union-find, window functions, DP state design. The platform should decide per concept, not per learner.
- Suggested default for rusty concepts: **problem → example on demand** (Reisslein's problem-example pairing). The first attempt then works as the diagnostic.
- Suggested default for new concepts: **example → problem pairs with fast backward fading**, removing one step per example.
- Practical scaffold-removal signal: first-attempt pass on hidden tests, no hints, and self-rated effort ≤ 4/9 → remove the next scaffold level. A failure, or effort ≥ 7/9, → restore one level. This is a direct port of the Kalyuga performance+effort efficiency rule to code (inference, [D]).
- A cheap programming version of the first-step probe: "Here is the problem. In ≤ 60 s, pick or type the first 1–2 lines / the approach (e.g., 'sort + two pointers', 'GROUP BY customer_id then HAVING')." This is untested in programming ([D]).
- Gold et al. 2026 shows that even novices learn more from *writing* than from *studying* examples when good immediate feedback is available. For an experienced learner on an auto-judged platform, this pushes further toward generation early.

### Gaps
- No meta-analysis of the worked-example effect specific to programming was found. The Barbieri meta-analysis is mostly K-12 math.
- The Tetzlaff 2025 effect sizes come from a blog summary. Moderator tables and the definition of "assistance" were not checked in the original.
- No study was found specifically on *rusty* (previously competent) programmers. Relearning ("savings") is a plausible but untested argument for faster fading.
- The full findings of the Muldner et al. 2022 TOCE review were not retrieved.
- Rapid-diagnostic validation exists only in math and physics. No programming validation was found.

---

## Q2. Parsons problems: as effective as writing code but faster? Adaptive Parsons; where they fit in a sequence

### Takeaway
Across many single-institution studies, Parsons problems are **faster to solve with similar learning gains** to writing the equivalent code, especially adaptive Parsons problems ([B], replicated by one group, plus a systematic review). There are caveats. The speed advantage disappears when the Parsons solution differs from the learner's own natural solution. Evidence on distractors is thin and mixed. Almost all studies cover intro-level constructs. Their best fit is (a) a quick bridge between studying an example and writing from scratch, and (b) an on-demand fallback when a learner is stuck while writing.

### Cited Findings
- **[B] Ericson, Margulieux & Rick 2017.** Parsons problems with distractors took significantly less time than fixing code with the same errors or writing the equivalent code, with no statistically significant difference in learning performance. — [Koli Calling 2017, pp. 20–29](https://escholarship.org/content/qt8794g5s0/qt8794g5s0.pdf?t=qbddoc); summarized in [Codio blog](https://www.codio.com/blog/parsons-problems)
- **[B] Adaptive Parsons (Ericson, Foley & Rick 2018).** Two kinds of adaptation:
  - *Intra-problem*: when a learner struggles, the problem gets easier, e.g., distractors are removed or blocks are combined.
  - *Inter-problem*: the next problem's difficulty depends on performance on the last one.

  Conclusion: adaptive Parsons problems are "a more efficient, but just as effective, form of practice as writing the equivalent code." — [ICER 2018, pp. 60–68, doi:10.1145/3230977.3231000](https://www.bibsonomy.org/bibtex/2b2617611446ed22e870de6f4d75f9ab8/brusilovsky)
- **[B] Boundary condition (Haynes & Ericson 2021).** Novices were significantly more efficient on a Parsons problem built from the *most common student-written solution* than at writing the equivalent code. A Parsons problem with an unusual solution was *not* significantly faster. — [CHI 2021, doi:10.1145/3411764.3445292](https://deepblue.lib.umich.edu/handle/2027.42/174559); see also [arXiv 2512.22407](https://arxiv.org/html/2512.22407)
- **[A−] ITiCSE 2022 working-group systematic review.**
  - **Speed:** 11 papers show Parsons problems are significantly faster than a tutorial, fixing code, writing textual code, or assembling blocks.
  - **Cognitive load:** the reviewers rated this evidence "extremely high quality."
  - **Limitations:** most studies were single-institution with fewer than 500 subjects and covered introductory Python/Java concepts. Multi-institution studies had fewer than 100 participants.
  - **Distractors:** only one study compared learning with and without distractors (Harms et al. 2016, young novices, blocks, a single distractor type), and it found distractors *decreased* learning efficiency. In a separate study, 60% of undergraduates were positive about distractors.
  - **Recommended use point:** after concepts are introduced but before they are mastered.
  - — [Ericson, Denny, Prather et al. 2022, ITiCSE-WGR, doi:10.1145/3571785.3574127](https://acris.aalto.fi/ws/portalfiles/portal/131069230/Parsons_Problems_and_Beyond_-_Systematic_Literature_Review_and_Empirical_Study_Designs_.pdf)
- **[B/C] Parsons as on-demand scaffolding while writing code (Hou, Ericson & Wang 2022).** Novices who could open an equivalent Parsons problem while solving a write-code problem spent significantly less time. Interviews with 11 students indicated it lowered difficulty and taught problem-solving strategies. A 2024 follow-up warns that learners can order blocks correctly "without fully understanding the rationale" and adds multi-level text explanations. — [ICER 2022](https://web.eecs.umich.edu/~xwanghci/papers/ICER22.pdf); [SIGCSE 2024 follow-up, arXiv 2401.03144](https://arxiv.org/pdf/2401.03144)
- **[B] Parsons and subgoals (Morrison, Margulieux, Ericson & Guzdial 2016).** Subgoal-labeled instruction for while loops improved performance on Parsons problems. The authors argue Parsons problems are lower-load and *more sensitive* to learning gains than code-generation items. — [SIGCSE 2016, pp. 42–47](https://dblp.uni-trier.de/rec/conf/sigcse/MorrisonMEG16.html)
- **[C] Place in the skill hierarchy.** The Lopez et al. (2008) hierarchy places Parsons, explaining code, and tracing iterative code as intermediate skills between knowing constructs and writing code. — [Lopez, Whalley, Robbins & Lister 2008, ICER](https://opus.lib.uts.edu.au/handle/10453/10806)

### Inferences
- For this learner, Parsons problems are most useful as **(i) a 1-item bridge for genuinely new algorithm templates**, and **(ii) a "show me the pieces" level in the hint ladder** when the learner is stuck writing (Hou 2022). They should not be a mandatory step for rusty-but-known material.
- Build Parsons blocks from the **canonical / most common solution** (Haynes & Ericson). For interview patterns, distractors should be *meaningful* near-misses, e.g., `while lo < hi` vs. `while lo <= hi`, or `hi = mid` vs. `hi = mid - 1`. Use them sparingly, since distractors are unproven and may cost efficiency.
- A Parsons pass should not count as mastery. Mastery should be judged only on write-from-scratch items, given the "order without understanding" risk.
- SQL: clause-ordering Parsons (SELECT/FROM/JOIN/WHERE/GROUP BY/HAVING/ORDER BY fragments) is a natural fit, but it is untested.

### Gaps
- No Parsons evidence for advanced data-structure or algorithm content, for SQL, or for experienced adults.
- Long-term retention after Parsons practice vs. writing practice has not been established.
- No exact time-savings percentages were retrieved from the 2017/2018 papers, only "significantly less time."

---

## Q3. PRIMM, code tracing / "predict the output" before writing, the tracing → explaining → writing hierarchy, and Xie et al.'s 2019 theory

### Takeaway
Correlational evidence ([C], replicated) shows tracing and explaining ability go with writing ability, and that writing tends to come after them. Structured "read before write" sequences (PRIMM; Xie et al.'s explicit sequencing of skills) improved outcomes in classroom studies ([B], school-age or exploratory). But tracing practice alone is less effective than writing with feedback, and it inflates confidence ([B], 2026). For an experienced learner, prediction items should be short, misconception-targeted checks, not a main learning activity.

### Cited Findings
- **[B] PRIMM (Predict–Run–Investigate–Modify–Make).** 13 secondary schools, 493 students aged 11–14, taught for 8–12 weeks. The PRIMM group scored higher on the post-test than controls. Teachers said it helped all learners progress in mixed-ability classes. The design is grounded in Vygotskian sociocultural theory, emphasizing talk about code. — [Sentance, Waite & Kallia 2019, *Computer Science Education* 29(2–3), doi:10.1080/08993408.2019.1608781](https://qmro.qmul.ac.uk/xmlui/handle/123456789/57800)
- **[C] Reading, tracing and writing are related.** On a first-semester exam, tracing performance and "explain in plain English" performance each correlated with code-writing performance. The authors proposed a hierarchy: knowledge of constructs → (tracing iterative code, explaining, Parsons) → writing. — [Lopez, Whalley, Robbins & Lister 2008, ICER, pp. 101–112](https://opus.lib.uts.edu.au/handle/10453/10806)
- **[C] Replication and caveats.** Fowler et al. reproduced the hierarchy in a non-majors Python course. A 2024 analysis shows the original hierarchy is not the only one that fits purely correlational data. Venables, Tan & Lister (2009) re-examined how the tracing tasks themselves shaped the tracing–writing relationship. — [arXiv 2410.12967 (2024)](https://arxiv.org/html/2410.12967v2); [Venables, Tan & Lister 2009, ICER](https://opus.lib.uts.edu.au/handle/10453/11384)
- **[B-exploratory] Xie et al. 2019 theory of instruction.** The theory separates four skills:
  1. tracing (reading semantics)
  2. writing correct syntax
  3. recognizing templates (reusable code patterns) and their parts
  4. using templates to solve problems

  It argues that teaching them explicitly and in that order reduces cognitive demand. In an exploratory mixed-methods comparison with traditional material, incremental skill teaching improved completion of practice exercises, lowered error rates, and improved post-test understanding. — [Xie, Loksa, Nelson, Davidson, Dong, Kwik, Tan, Hwa, Li & Ko 2019, *CSE* 29(2–3):205–253, doi:10.1080/08993408.2019.1565235](https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf)
- **[B] Tracing vs. writing, head-to-head** (N = 250, preregistered). Tracing beat video, but writing code with AI feedback beat tracing (b = 11.99, p < .001). Learners in the video and tracing conditions *overestimated* their performance. Writers *underestimated* theirs: writing vs. tracing calibration gap b = −15.76, p < .001. The authors read this as ease of processing being mistaken for understanding. Making errors in the writing condition did not lower interest. — [Gold, Tjaden & Carvalho 2026](https://escholarship.org/uc/item/6vq9j198)

### Inferences
- Use "predict the output" as **1–2 items before writing, chosen to target known misconceptions**, not as general warm-up. Examples:
  - Python: aliasing and mutation, mutable default arguments, `//` and `%` with negative numbers, slicing bounds, `range` end, `sorted` vs. `.sort()`, generator exhaustion, closures over loop variables.
  - SQL: NULL in comparisons and aggregates, LEFT JOIN plus a WHERE on the right table, row multiplication from GROUP BY after JOIN, logical evaluation order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY), window frame defaults.
- Require a committed prediction before running; this is PRIMM's P. The mismatch gives the prediction-error signal Gold et al. credit for learning, and it counters the overconfidence that passive reading creates.
- Xie et al.'s "template" skills map closely onto interview patterns (two pointers, sliding window, BFS, binary search on the answer). Explicit "recognize the template" items (which pattern fits this problem?) are a cheap, theory-backed addition for interview prep ([D]).
- Skip tracing items for a concept once the learner predicts correctly on the first item.

### Gaps
- No RCT of PRIMM with adults or university students was found. The 2019 evidence comes from 11–14-year-olds.
- No causal evidence was found that tracing practice *before* writing speeds up writing acquisition for experienced learners. The hierarchy evidence is correlational.
- PLTutor / "comprehension-first" (Nelson, Xie & Ko 2017) was not retrieved in this session.

---

## Q4. Subgoal labeling and self-explanation prompts

### Takeaway
Subgoal labels are short names for the functional steps of a procedure (e.g., "determine whether the condition is true or false"). They improve near-term problem solving in programming with a medium effect on quizzes (d ≈ 0.44) and cut extreme failures; exam effects are small ([B], semester-long quasi-experiment, N = 265). Self-explanation prompts have a medium overall effect (g = 0.55, [A]). However, adding them on top of worked examples did not help in math ([A] moderator), so keep them short and cheap.

### Cited Findings
- **[B] Subgoal-labeled worked examples across a CS1 semester.**
  - **Design:** N = 265 across 5 sections. Subgoal materials replaced worked examples in 2 sections, covering 5 of 15 weeks.
  - **Quizzes:** average 48% vs. 41%, d = 0.44. Total quiz score d = 0.42. More quizzes were taken.
  - **Exams:** average 75% vs. 72%, d = 0.20, not significant. Total exam score d = 0.26. More exams were taken (d = 0.22). Exam variance was lower, meaning fewer very low scores and fewer withdrawals or failures, especially among students at risk.
  - **Example labels** for evaluating a selection statement: "diagram which statements go together", "for if statement, determine whether true or false", "follow the correct branch". The labels were derived by task analysis of expert problem solving (the TAPS protocol).
  - — [Margulieux, Morrison & Decker 2020, *Int. J. STEM Educ.* 7:19, doi:10.1186/s40594-020-00222-7](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-020-00222-7) (data from [NSF PAR full text](https://par.nsf.gov/servlets/purl/10171482))
- **[B] Prior subgoal studies.** Prior studies "consistently found that subgoal-oriented instruction improved problem-solving performance across a variety of STEM domains, such as programming and statistics" (Catrambone 1994–1998; Margulieux & Catrambone 2016; Morrison et al. 2015). Learners who learn subgoals transfer more easily to new problems of the same type. — [Margulieux et al. 2020, background section](https://par.nsf.gov/servlets/purl/10171482); subgoals → Parsons performance: [Morrison et al. 2016](https://dblp.uni-trier.de/rec/conf/sigcse/MorrisonMEG16.html)
- **[A] Self-explanation meta-analysis.** Overall g = 0.55 (69 effect sizes from 64 reports, random effects). Results by prompt type, from a secondary summary: interrogative ("why…?") g = 0.56 (36 studies), imperative g = 0.40 (12), pre-directed g = 0.70 (8). The authors suggest exploring computer-generated prompts. — [Bisra, Liu, Nesbit, Salimi & Winne 2018, *Educ. Psychol. Rev.* 30:703–725, doi:10.1007/s10648-018-9434-x](https://doi.org/10.1007/s10648-018-9434-x); moderators via [TUM Clearing House summary](https://www.clearinghouse.edu.tum.de/wp-content/uploads/2023/09/CHU-KR-25_ENG_Bisra_2018_Selbsterklaerungen.pdf)
- **[A, conflicting] Prompts on top of examples.** In the math worked-example meta-analysis, conditions with self-explanation prompts showed a *smaller* worked-example effect than examples without prompts. — [Barbieri et al. 2023](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf). This contrasts with [Atkinson et al. 2003](https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/), where prompts combined with fading helped.
- **[B] Self-explanation prompts with programming hints.** Next-step hints with text explanations and self-explanation prompts improved immediate performance. Learning gains on later unassisted tasks were reported with self-explanation prompts in an ICER 2019 experiment, but a 2023 classroom study found "no conclusive evidence" that hints improved learning. — [Marwan, Williams & Price 2019, ICER](https://isnap.csc.ncsu.edu/home/public/papers/MarwanICER2019.pdf); [Marwan et al. 2023, IEEE TLT](https://isnap.csc.ncsu.edu/home/public/papers/Marwan2023TLT.pdf)

### Inferences
- Write a **3–6 item subgoal list per algorithm template and per SQL query shape**, and show the labels as comments in the worked example and as headings in completion problems. Examples ([D]):
  - **Sliding window:** "define the window invariant → expand right, update state → while invalid, shrink left → record the answer".
  - **Binary search on the answer:** "define the monotone predicate → set lo/hi bounds → mid and the predicate test → move the bound → return".
  - **SQL aggregation:** "pick the grain (one row per what?) → join sources → filter rows (WHERE) → group → filter groups (HAVING) → project and order".
- Subgoal labels give the AI tutor a shared vocabulary for hints: "Which subgoal are you on? Your shrink step never runs."
- Keep self-explanation prompts **short and structured**: menu choices, or one sentence the AI tutor checks. Use them mainly at fading points and after a bottom-out hint. Long free-text prompts add cost with no consistent benefit on top of examples (Barbieri), and for an experienced learner they risk the expertise reversal effect.
- Subgoal labels mainly helped weaker learners and near-term quizzes. For this learner, expect benefits mostly on genuinely new templates.

### Gaps
- No subgoal-label studies with algorithm or interview-level content or with SQL were found.
- Margulieux et al. 2020 does not report exact DFW percentages (drop, D, F, withdraw) per group in the parts read.
- Effect sizes from the original Margulieux, Guzdial & Catrambone 2012 ICER study were not retrieved.

---

## Q5. Retrieval practice, spacing, interleaving, the testing effect, mastery thresholds, and the "85% rule"

### Takeaway
Retrieval practice, spacing, and (for confusable categories) interleaving are among the best-supported learning techniques ([A]). Programming-specific evidence is limited to course redesigns and quasi-experiments ([C]) that point the same way. Cognitive, accuracy-based skills decay substantially without use, which matches this learner's rustiness. Spaced re-testing is therefore essential. Data across many tutoring systems suggest **about 7–8 practice opportunities per skill** to go from about 65% to 80% correct ([B/C], contested). Treat the "85% rule" as a loose heuristic for item difficulty; it was not derived from human skill learning.

### Cited Findings
- **[A] Testing effect.** Practice tests beat restudy and every other comparison condition. Effects are moderated by test format, feedback, and participant and study features. Most samples were post-secondary. Overall g = 0.61 (not re-verified). The count of 118 articles, 272 effect sizes and 15,472 participants comes from a secondary summary. — [Adesope, Trevisan & Sundararajan 2017, *Rev. Educ. Res.* 87(3):659–701, doi:10.3102/0034654316689306](https://education.wsu.edu/documents/2018/01/rethinking-use-tests.pdf/)
- **[A] Spacing.** More than 1,350 participants, review gaps up to 3.5 months, final tests up to 1 year later. The optimal gap grows with the retention interval but shrinks as a fraction of it: about 20–40% of a 1-week interval and about 5–10% of a 1-year interval. Gaps that are too long hurt less than gaps that are too short. — [Cepeda, Vul, Rohrer, Wixted & Pashler 2008, *Psychol. Sci.* 19(11):1095–1102](https://pubmed.ncbi.nlm.nih.gov/19076480/)
- **[A] Interleaving.** Overall g = 0.42 (59 studies, 238 effect sizes, I² = 77%). Effects were larger when categories look similar to each other, examples within a category vary, and materials are complex. The authors caution against interleaving expository text and words. In math, the effect is small but significant. — [Brunmair & Richter 2019, *Psychol. Bull.* 145(11):1029–1052, doi:10.1037/bul0000209](https://pubmed.ncbi.nlm.nih.gov/31556629/); math note: [Frontiers corrigendum](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6813467/)
- **[A, not re-verified] Technique ratings.** A major review rated practice testing and distributed practice "high utility" and interleaved practice and self-explanation "moderate utility." — [Dunlosky et al. 2013, *Psychol. Sci. Public Interest* 14(1), doi:10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266)
- **[C] Programming-specific spacing and retrieval:**
  - A CS1 "Spiral" redesign built on spacing, interleaving, elaboration, retrieval and reflection. Students later did better in CS2, with a 15% increase in passing grades. A thesis version reports 9% higher CS1 final exam scores. — [Lionelle, Ghosh, Say & Beveridge 2022, SIGCSE, pp. 502–508](https://par.nsf.gov/biblio/10352318); [thesis](https://mountainscholar.org/items/64706ed1-f172-4f24-bc4f-6a2e651d4e48/full)
  - "Retrieval-based teaching" raised course grades by 2.36 percentage points. CS1 quizzes recast as spaced, interleaved low-stakes retrieval practice were linked to higher final, coding-exam and course grades for students who actually spaced and interleaved. This is correlational, with 75 consenting students. — [Moraes, Lionelle, Ghosh & Folkestad 2023, ICETC, doi:10.1145/3629296.3629362](https://par.nsf.gov/servlets/purl/10544324)
- **[A] Skill decay.** A meta-analysis of 53 articles and 189 data points found skill loss ranging from d = −0.01 right after training to d = −1.4 after more than 365 days without use. Cognitive, artificial, accuracy-based tasks decay more than physical or speed-based ones. — [Arthur, Bennett, Stanush & McNelly 1998, *Human Performance*](https://Www.Gwern.net/doc/psychology/spaced-repetition/1998-arthur.pdf). A 2025 meta-analysis of procedural skills found that half the gains from initial training were lost after about 6.5 months for accuracy, 13 months for speed, and 11 months for mixed measures. — [*Psychol. Bull.* 2025, PubMed 40455501](https://pubmed.ncbi.nlm.nih.gov/40455501/)
- **[A, effect size partly unverified] Mastery learning.** A meta-analysis of 108 controlled evaluations found positive effects on exam performance in college and school. A mean ES of about 0.52 (pre-college) and 0.54 (college) is reported for the 1986 version of the analysis. — [Kulik, Kulik & Bangert-Drowns 1990, *Rev. Educ. Res.* 60(2):265–299](https://typeset.io/pdf/effectiveness-of-mastery-learning-programs-a-meta-analysis-45bgwh1byb.pdf); 1986 figures via [Slavin 1987](https://Www.Gwern.net/doc/psychology/1987-slavin.pdf)
- **[B/C] How many practice opportunities.**
  - Across 27 datasets and about 7,000 learners (1.3M interactions in tutors, online courses and games), learners started at about 65% correct on a skill. It took about **7–8 practice opportunities to reach 80%**: under 4 for above-average starters, over 13 for below-average starters.
  - Learning rates varied little: about 2.6 vs. 1.7 percentage points per opportunity for the fastest vs. slowest quartile.
  - — [Koedinger et al. 2023, *PNAS*, doi:10.1073/pnas.2221311120](https://www.cmu.edu/news/stories/archives/2023/march/the-myth-of-the-fast-learner); figures via [KQED MindShift](https://www.kqed.org/mindshift/62750/a-group-of-scientists-set-out-to-study-quick-learners-then-they-discovered-they-dont-exist)
  - **Contested:** a 2026 re-analysis of 26 of these datasets shows that truncating practice sequences inflates the estimated spread in learning rates (+75% at 10 opportunities, +205% at 5), so how sequence length is handled matters. — [Lee, Lichand, Domingue et al. 2026, arXiv 2605.01690](https://arxiv.org/abs/2605.01690)
- **[B, weak transfer to humans] The 85% rule.** For gradient-descent learners on *binary classification*, the optimal training error rate is about 15.87%, i.e., about 85% accuracy. Validated on perceptrons and a perceptual-learning model, and consistent with some animal-learning data. Wilson cautioned that this does not mean students should aim for a B average, and called more complex tasks future work. — [Wilson, Shenhav, Straccia & Cohen 2019, *Nat. Commun.* 10:4646](https://pmc.ncbi.nlm.nih.gov/articles/PMC6831579); [U. Arizona news](https://news.arizona.edu/news/learning-optimized-when-we-fail-15-time)

### Inferences
- **Rustiness is expected decay, not lost knowledge.** Arthur 1998 and the 2025 meta-analysis predict large accuracy loss after more than a year of disuse. Relearning should be faster than first learning (inference; no programming data found). This argues for **diagnose-and-skip** at the start and **heavy spaced re-testing** afterwards.
- **Spacing schedule** for interview-level retention over 2–6 months, derived from Cepeda's 10–20% rule ([D]): first re-test about 1 day after mastery, then about 3–7 days, about 2–3 weeks, and about 1–2 months. Expand on success; on failure, reset to a short interval and go back to a completion item. The *retrieval act* should be writing the solution from a blank editor, not recognizing it.
- **Interleaving fits interview prep best when categories are confusable**, e.g., sliding window vs. two pointers vs. prefix sums, BFS vs. DFS vs. Dijkstra, WHERE vs. HAVING, window functions vs. GROUP BY. Brunmair & Richter found larger effects exactly when categories look similar to each other. Use blocked practice for the first few items of a new concept, then interleave in spaced review sets. Blocked-first-then-mixed is an inference; the meta-analysis does not test the hybrid.
- **Mastery threshold, a practical proposal** ([D], grounded in Kulik's mastery-learning effects, Koedinger's opportunity counts and Kalyuga's efficiency rule): a concept counts as mastered after **2 consecutive unassisted first-submission passes on new (non-isomorphic) problems** within an interview-like time budget, with self-rated effort ≤ 5/9. The rate of hinted or AI-assisted solves should also be low.
- **Difficulty targeting:** aim item selection at roughly **70–85% first-attempt success** in practice. 85% is a heuristic ceiling, not a law. Items that pass at about 100% indicate wasted time; below about 60% indicates frustration and floundering.

### Gaps
- No RCT isolating spaced retrieval of *code writing* (vs. massed) was found. Programming evidence is quasi-experimental or correlational.
- No study was found on "Execute Program"-style spaced-repetition code drills. That product's design is practitioner practice ([D]).
- The headline effect sizes for Adesope (g) and Kulik 1990 could not be confirmed from primary text in this session.
- No programming evidence was found on optimal success rates. The 85% rule has not been tested for complex human skill learning.

---

## Q6. Direct instruction vs. productive failure; how much explanation before first practice; lesson/chunk length; number of practice items per concept

### Takeaway
Problem solving *before* instruction ("productive failure") beats instruction-first for conceptual understanding and transfer in a large meta-analysis ([A], g ≈ 0.36). Programming evidence is tiny ([C], N ≈ 20), and procedural fluency, the main goal here, does not appear to benefit. Learners with low prior knowledge in a domain need structured guidance ([A], expertise reversal). Across designs, the strongest programming-specific signal is **"less talk, more code"**: keep up-front explanation brief and get to generation with feedback quickly ([B]). For a rusty learner, a short "try first" attempt costs little and doubles as a diagnostic.

### Cited Findings
- **[A] Productive failure meta-analysis.**
  - 53 studies and 166 comparisons. Problem solving followed by instruction (PS-I) beat instruction followed by problem solving (I-PS): g = 0.36 [95% CI 0.20, 0.51], or g = 0.87 after a publication-bias adjustment.
  - Effects were larger (g = 0.37–0.58) when designs followed productive-failure principles faithfully.
  - Effects *reversed* (favored I-PS) for young learners (grades 2–5) and for domain-general skills.
  - — [Sinha & Kapur 2021, *Rev. Educ. Res.*](https://ouci.dntb.gov.ua/works/4KnMgZq7)
  - The benefit is mainly for conceptual knowledge and transfer, with no advantage for procedural knowledge (not re-verified; check the moderator tables).
- **[C] Productive failure in intro Python** (Suriyaarachchi, Denny & Nanayakkara). N = 20 (one blog reports 16). The problem-solving-first group got a programming task before a roughly 15-minute instruction unit. Initial learning was equal, but the PF group showed better retention and better performance on delayed, similar tasks, and a larger post-instruction drop in physiologically measured cognitive load. The authors note there has been little PF research in computing. — [arXiv 2411.11227 (SIGCSE 2025)](https://arxiv.org/abs/2411.11227); [Teaching CS substack summary](https://teachingcs.substack.com/p/productive-failure)
- **[B] Practice beats lecture.** Practice-based instruction beat a video lesson on code generation, and writing beat tracing, as already cited in Q1 and Q3. Total instruction time did not differ significantly between practice and lecture conditions. Practice also reduced self-reported distraction (b = −0.16, p = .003) and slightly raised interest. — [Gold, Tjaden & Carvalho 2026](https://escholarship.org/uc/item/6vq9j198)
- **[A] Structured guidance for learners new to a domain** (expertise reversal, as cited in Q1). — [Tetzlaff et al. 2025](https://doi.org/10.1016/j.learninstruc.2025.102142)
- **[B/C] Items per concept:** about 7–8 opportunities from about 65% to 80% correct, fewer for strong starters (Koedinger 2023, as cited in Q5). — [CMU news](https://www.cmu.edu/news/stories/archives/2023/march/the-myth-of-the-fast-learner)
- **[C, not re-verified] Chunk length.** In a large MOOC log analysis, median engagement time topped out at about 6 minutes regardless of video length, so shorter segments are recommended. — [Guo, Kim & Rubin 2014, L@S, doi:10.1145/2556325.2566239](https://doi.org/10.1145/2556325.2566239)
- **[B] Design data points from Margulieux et al. 2020.** Subgoal-labeled examples introduced *new types* of problems, and each quiz tested the previous week's topic. Benefits showed up within about a week of learning a procedure. — [Margulieux et al. 2020](https://par.nsf.gov/servlets/purl/10171482)

### Inferences
- **How much explanation before first practice:** for a known-but-rusty concept, **none**. Start with a capped attempt (about 5–10 minutes), then show a worked example or explanation focused on the specific failure. This is a problem→example pair, which suits higher-knowledge learners (Reisslein, Q1) and is PF-like. For a genuinely new concept, a **≤ 5-minute explanation (about 300–600 words, or one diagram plus the subgoal list)** followed immediately by an example and practice.
- **"Explanation-first" content should be modular and on demand.** Under expertise reversal, a lot of explanation for an experienced learner is mostly extra load.
- **Lesson size:** one concept or template per lesson. About 6–10 practice opportunities total for a new concept, including completion items. About 2–4 for a rusty concept that passes the diagnostic. Then move the concept into the spaced queue rather than over-practicing in one session; over-practice in one session is a massed-practice inefficiency per Cepeda.
- **Keep productive-failure attempts short and expect failure.** A tight time cap avoids unproductive floundering. The learner should see the attempt as diagnostic, not as being graded.

### Gaps
- Only one tiny productive-failure study in text-based programming was found, and none in algorithms or SQL.
- No programming study was found that directly manipulates the *amount* of explanation before practice, or chunk length.
- The Guo et al. 2014 6-minute finding concerns video engagement, not learning outcomes, and was not re-verified here.

---

## Q7. Immediate vs. delayed feedback; quality of error feedback; hint design (including the AI tutor)

### Takeaway
Feedback is among the strongest instructional factors ([A]). For *learning procedures* with an autograder, immediate correctness feedback is standard and supported. The evidence on immediate vs. delayed timing is mixed and mostly from fact learning, where delays can aid retention. Enhanced compiler or error messages show **inconsistent** learning benefits ([B], conflicting). Next-step hints reliably improve *in-task performance*, but learning gains appear mainly when hints carry explanations or self-explanation prompts ([B]). Unrestricted generative AI used as an answer source **harms learning**, while a guardrailed tutor avoids the harm ([B], large field RCT).

### Cited Findings
- **[A, not re-verified] Feedback meta-analysis.** Mean d = 0.48 across 435 studies. Effects were larger for more information-rich feedback (task, process and self-regulation level) than for simple reinforcement. — [Wisniewski, Zierer & Hattie 2020, *Front. Psychol.* 10:3087, doi:10.3389/fpsyg.2019.03087](https://doi.org/10.3389/fpsyg.2019.03087)
- **[C, secondary sources] Timing.** Reviews of feedback timing are mixed. One tally of 39 retention studies: 16 favored delayed feedback, 12 immediate, 11 found no difference. Lab work shows delayed feedback can help retention partly by acting as spaced re-exposure. — [Smith & Kimball 2010, "Learning from feedback: Spacing and the delay-retention effect" (manuscript)](https://www.ou.edu/memorylab/pdfs/SmithKimball_2010_LearningFromFeedback_ms.pdf). One secondary source suggests low-knowledge learners benefit more from immediate feedback and high-knowledge learners from delayed feedback. I found no programming study confirming this.
- **[B, conflicting] Enhanced compiler error messages:**
  - In a CS1 control/intervention study with about 200 students and about 50,000 errors, enhanced Java messages led to fewer errors overall and per student, and 8 specific messages had significant effects. — [Becker 2016, SIGCSE](https://researchrepository.ucd.ie/entities/publication/d4b1c9ce-e7ff-48e7-b9b9-f0ebe0c15e8e)
  - Denny, Luxton-Reilly & Carpenter ("Enhancing syntax error messages appears ineffectual") and Pettit et al. found no conclusive benefit.
  - A 2017 ICER think-aloud study (N = 31) found no substantial learning gain over control, but students did read the messages and generally made effective edits. Conflicting results are acknowledged in the literature. — [core.ac.uk compilation](https://core.ac.uk/download/288100865.pdf); [Frontiers 2021](https://frontiersin.org/articles/10.3389/fpsyg.2021.768962/full)
- **[B] Next-step hints (Marwan & Price).** Textual explanations make hints more useful and help learners explain the hint's purpose. Hints plus self-explanation prompts improved immediate performance, with learning effects in a lab study. A classroom study found enhanced hints (explanations, self-explanation prompts, adaptive display) improved in-class assignment performance, but there was "no conclusive evidence" that they improved learning. — [ICER 2019](https://isnap.csc.ncsu.edu/home/public/papers/MarwanICER2019.pdf); [ITiCSE 2019](https://isnap.csc.ncsu.edu/home/public/papers/MarwanITiCSE2019.pdf); [IEEE TLT 2023](https://isnap.csc.ncsu.edu/home/public/papers/Marwan2023TLT.pdf). LLM-generated next-step hints vary widely in quality, with GPT-4 best among the models tested. — [arXiv 2411.18151](https://arxiv.org/html/2411.18151v1)
- **[B] Generative AI and learning (field RCT, about 1,000 high-school math students).**
  - Practice scores rose 48% with an unrestricted GPT-4 interface (GPT Base) and 127% with a guardrailed tutor (GPT Tutor).
  - On the later exam *without* AI, GPT Base students scored **17% lower than controls**. GPT Tutor students scored the same as controls.
  - Most GPT Base users simply asked for answers, and GPT Tutor users overestimated their own learning.
  - — [Bastani, Bastani, Sungu et al. 2025, *PNAS* 122(26), e2422633122](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html); [Wharton summary](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education/)
- **[B] AI code generator for novice programmers.** N = 69, ages 10–17. The Codex-access group was slightly but not significantly better on a 1-week retention test, and was not harmed. Learners with higher prior competency benefited more (post-hoc). — [Kazemitabaar et al. 2023, CHI, arXiv 2302.07427](https://arxiv.org/abs/2302.07427)
- **[B] AI-generated elaborated feedback** on code submissions (identifying syntax errors and logic issues) produced the best learning in a preregistered N = 250 study. Errors did not reduce interest. The study did not vary feedback features. — [Gold et al. 2026](https://escholarship.org/uc/item/6vq9j198)

### Inferences
- **Correctness feedback: immediate.** Running hidden tests instantly on every submit is justified. The procedural-skill and autograder literature and Gold et al. support it, and delaying correctness on code is impractical.
- **Make the explanation of an error escalate by request or by attempt count, not immediately.** A suggested ladder ([D], combining Marwan, Hou and Bastani):
  1. failing test name or input only;
  2. a minimal counterexample plus a "predict what your code returns" prompt;
  3. a subgoal-level hint ("your shrink step…");
  4. a Parsons or completion version of the solution;
  5. a bottom-out worked solution, which requires a one-sentence self-explanation and **schedules the item for re-test in 1–2 days as a fail**.
- **AI tutor guardrails** (from Bastani 2025):
  - Do not give full code before a minimum attempt or time threshold.
  - Default to Socratic questioning and pointing at a subgoal.
  - Log every AI-assisted solve as "assisted", so it never counts toward mastery.
  - Periodically require unassisted, blank-editor re-solves.
- **Error-message rewriting** (LLM-enhanced Python tracebacks, explaining SQL errors) is cheap UX, but do not expect it to be a learning lever on its own. The evidence is conflicting.
- **Delayed feedback** has one cheap use: in spaced-review sessions, show a batch summary at the end ("what you got wrong across 5 items") on top of the immediate per-item results. This is speculative ([D]).

### Gaps
- No programming RCT was found that isolates immediate vs. delayed *explanatory* feedback.
- The Wisniewski 2020 numbers and the Mullet et al. (2014) engineering study on delayed feedback were not verified this session.
- No RCT was found of a guardrailed LLM tutor for *programming* with an unassisted delayed post-test. Bastani 2025 is math. Kazemitabaar 2023 involved children and an unguarded tool.

---

## Q8. Deliberate practice and fluency drills for hand-writing code (katas, retyping vs. recalling)

### Takeaway
There is **no rigorous programming study** comparing retyping code with recalling it from memory, and none evaluating code katas. The closest evidence is correlational: typing-exercise users had higher grades and fewer compile errors ([C]). The strongest relevant principles come from other domains: retrieval beats re-exposure (testing effect, [A]); generation beats studying examples in programming ([B]); and accuracy-based cognitive skills decay without use ([A]). Together they favor **timed, from-memory, spaced writing of core templates** over copying.

### Cited Findings
- **[C] Typing exercises as interactive worked examples (TYPOS).** Students retype example code. Self-selected students who completed these exercises earned higher course grades and had fewer compilation and build errors on projects. This is correlational. — [Gaweda, Lynch, Seamon, Silva de Oliveira & Deliwa 2020, ACE](https://dblp.org/rec/conf/ace/GawedaLSOD20); [TYPOS project page](https://research.csc.ncsu.edu/arglab/projects/typos/)
- **[A] Testing effect:** retrieval beats restudy, as cited in Q5. — [Adesope et al. 2017](https://education.wsu.edu/documents/2018/01/rethinking-use-tests.pdf/)
- **[B] Generation beats tracing or studying a complete solution** for code-generation outcomes, as cited in Q1 and Q3. — [Gold et al. 2026](https://escholarship.org/uc/item/6vq9j198)
- **[A] Decay of accuracy-based cognitive skills** without practice, as cited in Q5. — [Arthur et al. 1998](https://Www.Gwern.net/doc/psychology/spaced-repetition/1998-arthur.pdf); [Psychol. Bull. 2025](https://pubmed.ncbi.nlm.nih.gov/40455501/)
- **[A, not re-verified] Deliberate practice meta-analysis.** Deliberate practice explained a modest share of performance variance overall and only about 4% in education. Structured practice matters, but it is not the whole story. — [Macnamara, Hambrick & Oswald 2014, *Psychol. Sci.*, doi:10.1177/0956797614535810](https://doi.org/10.1177/0956797614535810)
- **[B] Template knowledge as a distinct skill.** Recognizing and using templates is a separately teachable skill. — [Xie et al. 2019](https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf)

### Inferences
- **Retyping** is defensible only as a *first-exposure syntax* aid, e.g., unfamiliar Python idioms (`collections.deque`, `heapq`, `bisect`, `defaultdict`) or SQL window-function syntax. Switch to **recall** right away: write the snippet from a blank editor after a delay.
- **"Template katas"** ([D]): a list of about 30–60 core snippets.
  - Python examples: BFS/DFS with visited set, binary search variants, union-find with path compression, Dijkstra with `heapq`, top-k with a heap, sliding window, monotonic stack, trie insert/search, backtracking skeleton, 1D/2D DP table, interval merge, topological sort.
  - SQL examples: top-N per group with `ROW_NUMBER`, running totals, anti-join, self-join for consecutive days, pivot via `CASE`, gaps-and-islands.

  Each is drilled as "write from memory and pass the tests in ≤ N minutes", scheduled by spaced repetition, with time-to-pass and error count tracked as fluency measures. This applies the testing effect and spacing to code. It has not been directly tested.
- **Fluency vs. understanding:** pair each template drill with an occasional "apply to a novel problem" item. Recall drills alone risk inflexible, rote templates. Note that van Merriënboer's completion learners were *not* better at interpreting programs.
- **Interview realism:** a final-stage mode with no autocomplete, no running code until submit, and a timer. This is practitioner advice ([D]), consistent with practicing under conditions like the test (Arthur 1998: similar retrieval conditions reduce measured skill loss).

### Gaps
- No peer-reviewed evaluation of code katas, Execute Program, or "blank-page recall" drills in programming was found.
- No study comparing retyping vs. recall for code retention was found.

---

## Q9. Synthesis: an evidence-based sequence for a single concept, with item counts and skip criteria

### Takeaway
For a rusty, experienced learner, the best-supported design is **adaptive**:
- Diagnose first.
- Skip worked examples for concepts that come back quickly.
- For genuinely new templates, use brief explanation → subgoal-labeled worked example → predict → fading or completion (Parsons on demand) → modify → write from scratch with instant judging → spaced, interleaved from-memory re-tests.
- Remove scaffolds on performance-plus-effort signals.
- Count only unassisted, from-scratch solves toward mastery.

Expect about 6–10 practice opportunities per new concept and about 2–4 per rusty concept before spaced review.

### Cited Findings
These are the anchors behind each step; full details are in Q1–Q8.
- **Diagnose and adapt:** expertise reversal is d ≈ +0.5 for novices and ≈ −0.4 for knowledgeable learners, strongest in higher education ([Tetzlaff 2025](https://doi.org/10.1016/j.learninstruc.2025.102142)). Rapid first-step and verification probes correlate up to r = .92 with full tests in up to 4.9× less time. Adaptive guidance gives ES 0.46–0.69, using the rule "all steps verified and effort < 5/9 → advance" ([Kalyuga 2007](https://link.springer.com/article/10.1007/s10648-007-9054-3)).
- **Order of example and problem by prior knowledge:** novices do best with example→problem; knowledgeable learners with problem→example or fast fading (one step per example) ([Reisslein 2005/2006 via Kalyuga 2007](https://link.springer.com/article/10.1007/s10648-007-9054-3)).
- **Worked examples:** g = 0.48 ([Barbieri 2023](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf)). Subgoal labels give d = 0.44 on near-term quizzes plus fewer extreme failures ([Margulieux 2020](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-020-00222-7)). Backward fading with prompts helps ([Atkinson 2003](https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/)).
- **Prediction and tracing** correlate with writing ([Lopez 2008](https://opus.lib.uts.edu.au/handle/10453/10806)). PRIMM beat controls with 11–14-year-olds ([Sentance 2019](https://qmro.qmul.ac.uk/xmlui/handle/123456789/57800)). Tracing alone inflates confidence and is weaker than writing ([Gold 2026](https://escholarship.org/uc/item/6vq9j198)).
- **Completion and Parsons:** completion beats generation for program construction and reduces dropout ([van Merriënboer 1990](https://research.utwente.nl/en/publications/strategies-for-programming-instruction-in-high-school-program-com/)). Adaptive Parsons is as effective as writing and faster ([Ericson 2018](https://www.bibsonomy.org/bibtex/2b2617611446ed22e870de6f4d75f9ab8/brusilovsky); [WG review 2022](https://acris.aalto.fi/ws/portalfiles/portal/131069230/Parsons_Problems_and_Beyond_-_Systematic_Literature_Review_and_Empirical_Study_Designs_.pdf)). Parsons works as on-demand scaffolding while writing ([Hou 2022](https://web.eecs.umich.edu/~xwanghci/papers/ICER22.pdf)).
- **Generation with immediate elaborated feedback** gave the best learning ([Gold 2026](https://escholarship.org/uc/item/6vq9j198)).
- **Number of opportunities:** about 7–8 from about 65% to 80% ([Koedinger 2023](https://www.kqed.org/mindshift/62750/a-group-of-scientists-set-out-to-study-quick-learners-then-they-discovered-they-dont-exist)).
- **Spacing, retrieval and interleaving:**
  - Spacing: optimal gap about 10–20% of the retention interval ([Cepeda 2008](https://pubmed.ncbi.nlm.nih.gov/19076480/)).
  - Testing effect over restudy ([Adesope 2017](https://education.wsu.edu/documents/2018/01/rethinking-use-tests.pdf/)).
  - Interleaving g = 0.42, larger for similar-looking categories ([Brunmair & Richter 2019](https://pubmed.ncbi.nlm.nih.gov/31556629/)).
- **AI guardrails:** unrestricted AI reduced exam scores by 17%, while a guardrailed tutor was neutral ([Bastani 2025](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html)).

### Inferences
The proposed per-concept lesson flow below is my synthesis ([D]), assembled from the findings above. Item counts are design starting points to tune with platform data, not established constants.

| Step | What | Items | Skip / advance criteria | Evidence anchor |
|---|---|---|---|---|
| 0. Diagnose | One timed "write it now" problem for the concept (5–10 min cap), or a 60-second first-step / approach probe for complex templates. Ask for effort on a 1–9 scale after. | 1 (2 if ambiguous) | **Pass hidden tests unassisted with effort ≤ 5 → skip to step 6** (1–2 confirming items) and then spaced review. Partial or fail → step 1. Wrong approach → step 1 with the explanation targeted at the gap. | Kalyuga rapid diagnostics; Reisslein problem→example; Sinha & Kapur PS-I |
| 1. Brief explanation | ≤ 5 min / about 300–600 words: what problem class this template solves, the **3–6 subgoal labels**, and one diagram if useful. On demand for rusty learners. | — | Collapse for rusty concepts and show only the part tied to the diagnostic failure. | Gold "less talk, more code"; Guo 2014; Xie templates |
| 2. Worked example with subgoal labels | Clean, correct solution with subgoal comments. One short structured self-explanation (multiple choice, or one sentence the AI checks). | 1 (2 isomorphic for a fully new concept) | Rusty learner: skip if step 0 produced a near-miss and the worked solution to *their* attempt was shown. | Barbieri 2023; Margulieux 2020; Bisra 2018 |
| 3. Predict / trace | Predict the output or state for a snippet that targets a known misconception (Python mutability or off-by-one, SQL NULL / JOIN fan-out / GROUP BY order). Commit before running. | 1–2 | Correct on the first item → skip the second. | PRIMM; Lopez 2008; Gold 2026 overconfidence |
| 4. Completion / faded example | Backward fading: blank the last subgoal first, then the last two. **Fast fading** (one step per item) for this learner. Adaptive Parsons from the canonical solution *only as fallback* when stuck. | 1–2 | First-try pass with low effort → go straight to step 6. Two failures → go back to step 2 with a second example. | Atkinson 2003; Reisslein; van Merriënboer 1990; Ericson 2018; Hou 2022 |
| 5. Modify | Change a working solution to a variant spec (e.g., "longest window with at most K distinct" → "exactly K"; add HAVING / change the grain). | 1 | Skippable if step 4 was clean. | PRIMM "M"; van Merriënboer completion |
| 6. Write from scratch | Blank editor, instant judge, hint ladder (test → counterexample + predict → subgoal hint → Parsons → bottom-out with self-explanation). Increase variation: isomorphic → near transfer → interview-style. | 3–5 (about 6–10 opportunities total including steps 3–5) | **Mastery = 2 consecutive unassisted first-submission passes on non-isomorphic problems within the time budget, effort ≤ 5/9.** Keep the item mix at about 70–85% first-try success. Any AI bottom-out solve = fail for scheduling. | Gold 2026; Koedinger 2023; Kulik 1990; Wilson 2019 (heuristic); Bastani 2025 |
| 7. Spaced, interleaved retrieval | Re-test by writing from memory on a *new* problem of the type (plus a template kata). Intervals about 1 d → 3–7 d → 2–3 wk → 1–2 mo, expanding on success. Interleave with confusable templates. | 1 per review | Fail → shorten the interval and insert one step-4 completion item before the next write. Two successive passes at ≥ 3 weeks → move to monthly maintenance. | Cepeda 2008; Adesope 2017; Brunmair & Richter 2019; Arthur 1998 |

Further design notes:
- **Time budget:** about 25–40 min for a new concept (steps 1–6) and about 10–15 min for a rusty concept (0 → 6). Review items take about 5–15 min each.
- **Global scaffold controller.** For each concept, track first-try pass rate, hint depth, time-to-pass and self-rated effort. Fade one level when the last two items were clean and low-effort. Restore one level after two failures or any bottom-out hint. This is the Kalyuga efficiency rule applied to code.
- **Keep the mastery signal clean.** Parsons passes, completion passes and AI-assisted solves never count toward mastery. Only blank-editor solves count, since Parsons can be ordered without understanding (Hou 2024) and AI help can act as a crutch (Bastani 2025).
- **SQL specifics.** Use step-by-step execution visualization as an optional worked-example layer (DBQA evidence is correlational) and subgoals following logical evaluation order. Predict-the-result-table items work well as step 3.
- **Interview level.** In later spaced reviews, add constraints: a timer, no running code until submit, and saying the approach out loud before coding (the AI tutor can check the approach statement). This is practitioner-grade advice ([D]).

### Gaps
- No study validates this full sequence end-to-end, or for experienced adults relearning. The counts are extrapolated from tutor-wide averages (Koedinger) and design heuristics.
- No programming-specific evidence on optimal spacing intervals or on mastery thresholds (e.g., 2 vs. 3 consecutive correct) was found.
- Self-rated effort (the 9-point Paas scale) has not been validated as a scaffold-removal signal in programming.
- Whether the AI tutor's elaborated feedback quality is comparable to Gold et al.'s, or to a human tutor, has not been tested. Gold et al. did not vary feedback properties.
