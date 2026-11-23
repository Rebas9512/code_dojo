# Data-first / data-centric approaches to teaching programming to complete beginners (research notes, as of 2026-11-22)

Scope: evidence and concrete course designs for a first stage, "认识数据" (getting to know data), in a Python + SQL learning platform for an adult starting from zero. Labels used throughout: **[EVIDENCE]** means an empirical study with data. **[RATIONALE]** means an author's design argument or opinion. **[DESIGN]** means a description of a curriculum's actual structure.

Editions and dates checked:
- HtDP 2e online, version 8.15.0.2, released 2024-11-06
- DCIC, version 2025-08-27
- *Computational and Inferential Thinking* (Data 8 textbook), 2nd ed., © 2022
- Bootstrap:Data Science as described in the SIGCSE 2022 paper (PDF metadata dated 2021-12-05)

---

## Q1. How to Design Programs (HtDP 2e): the design recipe, "data shape determines program shape", chapter sequencing, and evaluations

### Takeaway
HtDP starts with atomic values and their operations: numbers, strings, images and booleans, ending with "Predicates: Know Thy Data". It then adds functions and the design recipe, then itemizations with conditionals, then fixed-size structures, and only then lists as "arbitrarily large data". Its design recipe makes the data definition step 1, and the function template is derived mechanically from the data definition. The evidence for HtDP-style instruction is modest and indirect: the Rainfall study of functional-first CS1 courses and the Bootstrap:Algebra transfer studies. There are no randomized comparisons.

### Cited Findings
- **[DESIGN] Edition.** The online HtDP 2e is "version 8.15.0.2", released "Wednesday, November 6th, 2024". The page carries the copyright line "© 1 August 2014, MIT Press" (CC BY-NC-ND). — [HtDP 2e TOC](https://htdp.org/2024-11-6/Book/index.html)
- **[DESIGN] Part I, "Fixed-Size Data", in order:**
  - Ch. 1 "Arithmetic": 1.1 Numbers, 1.2 Strings, 1.3 Mixing It Up, 1.4 Images, 1.5 Booleans, 1.6 Mixing It Up with Booleans, 1.7 "Predicates: Know Thy Data"
  - Ch. 2 Functions and Programs
  - Ch. 3 How to Design Programs (Designing Functions, testing)
  - Ch. 4 Intervals, Enumerations, and Itemizations. Conditionals first appear here, in "4.1 Programming with Conditionals".
  - Ch. 5 Adding Structure (posn, defining structure types, "5.7 The Universe of Data")
  - Ch. 6 Itemizations and Structures (incl. 6.3 Input Errors, 6.5 Equality Predicates)

  Source: [HtDP 2e TOC](https://htdp.org/2024-11-6/Book/index.html)
- **[DESIGN] Part II, "Arbitrarily Large Data":** Ch. 8 Lists, Ch. 9 Designing with Self-Referential Data Definitions, Ch. 10 More on Lists (10.2 "Structures in Lists", 10.3 "Lists in Lists, Files"), Ch. 11 Design by Composition, and Ch. 12 Projects. The projects include "12.1 Real-World Data: Dictionaries" and "12.2 Real-World Data: iTunes". Abstraction comes in Part III, and a short "Nature of Numbers" intermezzo covering overflow and underflow comes after Part IV. — [HtDP 2e TOC](https://htdp.org/2024-11-6/Book/index.html)
- **[DESIGN] The six design-recipe steps** (Preface, Figure 1):
  1. "From Problem Analysis to Data Definitions": "Identify the information that must be represented and how it is represented in the chosen programming language."
  2. Signature, Purpose Statement, Header: "State what kind of data the desired function consumes and produces."
  3. Functional Examples
  4. Function Template: "Translate the data definitions into an outline of the function."
  5. Function Definition
  6. Testing

  Source: [HtDP Preface](https://htdp.org/2024-11-6/Book/part_preface.html)
- **[RATIONALE] Data definitions and examples.** The Preface says "writing down examples proves how real-world information is encoded as data". Part I "starts with atomic data" and then "gradually introduces new ways of describing data". Part II "shows how a subtle generalization gets us from there to data of arbitrary size." — [HtDP Preface](https://htdp.org/2024-11-6/Book/part_preface.html)
- **[DESIGN] Data shape determines program shape, as stated in HtDP's own words:**
  - "the purpose of a template is to express the data definition as a function layout"
  - "all important pieces of the data definition must find a counterpart in the template"
  - "Your template needs as many cond clauses as sub-classes that the data definition distinguishes"
  - "Formulate 'natural recursions' for the template to represent the self-references of the data definition"

  Source: [HtDP Part II](https://htdp.org/2024-11-6/Book/part_two.html)
- **[RATIONALE] Audience and transfer.** The book's stated purpose is "to introduce readers without prior experience to the systematic design of programs". It claims that "if students truly absorb the design recipe, they enhance their articulation skills more than anything else." — [HtDP Preface](https://htdp.org/2024-11-6/Book/part_preface.html)
- **[EVIDENCE] Rainfall study (Fisler, ICER 2014, "The Recurring Rainfall Problem", DOI 10.1145/2632320.2632346).**
  - Data came from five functional-language CS1 courses at four schools.
  - These students chose different high-level program structures and made fewer low-level errors than the imperative-course results in prior studies.
  - The abstract notes that these courses rarely cover interactive I/O and that students "work extensively with lists from the early weeks of a course".
  - Source: [Fisler ICER'14 resources page](https://cs.brown.edu/~kfisler/Pubs/icer14-rainfall), [paper copy](https://typeset.io/pdf/the-recurring-rainfall-problem-4w0k80zfy6.pdf). The resources page later returned 404 to a direct fetch. These details come from the abstract as surfaced by search; I did not read the full results section.
- **[EVIDENCE, preliminary] Bootstrap:Algebra, an HtDP-derived design-recipe curriculum for middle school.**
  - Schanzer et al., SIGCSE 2015, reported statistically significant pre/post gains on function composition and algebra word problems, using paired t-tests. — [Transferring Skills at Solving Word Problems… (SIGCSE 2015)](https://cs.brown.edu/~sk/Publications/Papers/Published/sfkf-trans-word-prob-comp-alg-bs/)
  - A 2018 follow-up found students improved on word problems after the module, including unscaffolded ones. — [Assessing Bootstrap:Algebra Students on Scaffolded and Unscaffolded Word Problems (SIGCSE 2018)](https://cs.brown.edu/people/sk/Publications/Papers/Published/sfk-bsa-scaff-unscaff-wp/), [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/sfk-bsa-scaff-unscaff-wp/paper.pdf)
  - Effect sizes and sample sizes were not visible in what I retrieved.
- **[DESIGN] HtDP in Python (UBC).** A UBC course page says it demonstrates "how to apply the design recipes learned in CPSC 110 [HtDP-based] to the Python programming language", noting that some concepts "will look quite different in Python". — [UBC CS189 page](https://cs.ubc.ca/~pcarter/cs189/cs189_ch1s1.html)
- **[DESIGN, weak source] UBC CPSC 103.** Student-uploaded CPSC 103 notes describe a late-course "How to Design Analysis Programs" recipe that reads CSV files with Python's `csv` library, noting that "the csv library will read each piece of information as a string". Treat this as unverified course detail. — [Studocu CPSC 103 upload](https://www.studocu.com/en-ca/document/vancouver-community-college/computing-science/cpsc-103-intro-to-python-function-design-basics/141672125)
- **[DESIGN] Python design-recipe adaptation.** A Python version of the recipe (Clements, Cal Poly) puts data definitions first. — [The Design Recipe, in Python](https://brinckerhoff.org/clements/2254-csc202/Files/design-recipe.html), [python-design-recipe](https://www.brinckerhoff.org/python-design-recipe/index.html)

### Inferences
- HtDP's Part I is already a "know your data" stage. Each value type is introduced together with its operations ("arithmetic of X") and its type predicates ("Know Thy Data") before any user-defined function or conditional. That maps directly onto a Python stage of: `int` / `float` / `str` / `bool` → operators per type → `type()` / `isinstance()` → conversions.
- HtDP introduces conditionals *as* a consequence of data, because itemizations and enumerations need `cond`. So "control flow" is not postponed. It is motivated by data definitions. This interleaved model fits a data-first stage better than strictly delaying all control flow.
- The template rule ("as many cond clauses as sub-classes"; recursion where the data self-references) is what people paraphrase as "the shape of the data determines the shape of the program". For Python learners it can be restated as:
  - a dict/record → access each field
  - a list → a loop or comprehension over the elements
  - a union (e.g., value-or-None) → an `if` per case

### Gaps
- I did not find the exact sentence "the shape of the data determines the shape of the program" on the HtDP pages fetched (Preface, TOC, first 100k characters of Part II). It appears to be a community paraphrase. Do not quote it as verbatim HtDP text without checking further.
- I found no randomized or controlled study comparing HtDP-style data-first instruction with control-flow-first instruction for adult self-learners. The Rainfall evidence compares against prior published imperative cohorts, not a matched control.
- I found no official UBC CPSC 103 syllabus (it sits on Canvas); the CSV detail comes from a student upload.

---

## Q2. Brown's *A Data-Centric Introduction to Computing* (DCIC): chapter order, rationale, evaluation

### Takeaway
DCIC (Fisler, Krishnamurthi, Lerner, Politz; version 2025-08-27) has a specific order:
1. Basic data: numbers, strings, images, types and contracts, names, functions, conditionals and booleans
2. Tables (filter, order, build columns, cleaning, missing entries, normalizing)
3. Lists, "From Tables to Lists"
4. Recursion, structured data and trees
5. Python: dictionaries, arrays, Pandas, file I/O
6. Mutation, state and memory

The rationale is stated plainly: "data centric = data science + data structures", in that order. I found no published outcome evaluation of DCIC itself. The empirical work around it consists of adjacent studies: data-organization reasoning, mutation misconceptions, and Bootstrap pilots.

### Cited Findings
- **[DESIGN] Version and authors.** "Version 2025-08-27". Authors: Kathi Fisler, Shriram Krishnamurthi, Benjamin S. Lerner, Joe Gibbs Politz. License CC BY-NC-SA 4.0. — [dcic-world.org](https://dcic-world.org/)
- **[DESIGN] Chapter order.** The full table of contents is at [DCIC 2025-08-27 TOC](https://dcic-world.org/2025-08-27/index.html).
  - **Part II, Introduction to Programming:**
    - **3 Basic Data:**
      - 3.1 Getting Started: Numbers, Expressions, Strings, Images, then "3.1.7 Stepping Back: Types, Errors, and Documentation", including "Types and Contracts" and "Format and Notation Errors"
      - 3.2 Naming Values, including "3.2.2.1 Names Versus Strings"
      - 3.3 From Repeated Expressions to Functions, including type annotations
      - 3.4 Conditionals and Booleans
    - **4 Tabular Data:**
      - 4.1 Introduction to Tabular Data: Creating, Extracting Rows and Cell Values, Functions over Rows, Finding/Ordering Rows, Adding New Columns, Calculating New Column Values
      - 4.2 Processing Tables: Loading Data Tables, "Dealing with Missing Entries", Normalizing Data, "Using Programs to Detect Data Errors", Task Plans, bins, Splitting Columns, Visualizations
    - **5 Lists:** 5.1 From Tables to Lists ("Extracting a Column from a Table", built-in list operations, "Combining Lists and Tables"), 5.2 Processing Lists, 5.3 Recursive Data
    - **6 Structured Data**
    - **7 Trees**
  - **Part III, From Pyret to Python:** 9.1 (incl. 9.1.8 `for` loops), 9.2 Dictionaries, 9.3 Arrays, 10 Tables in Python via Pandas, 11 File I/O
  - **Part IV, Programming With State:** 12.1 Mutating Structures, 12.2 Understanding Equality, 12.3 Arrays and Lists in Memory, 13.1 Mutating Variables, 13.2 Mutable Lists
  - **Appendix 30** "Comparing This Book to HtDP"
- **[DESIGN] Table basics in DCIC 4.1:**
  - "A given column has the same type, but different columns can have different types."
  - Rows are a new data type, `Row`.
  - Operations: `filter-with` (described as working "roughly like the `if` statement"), `order-by`, `build-column`, `transform-column`.
  - The book says one of the three table notations it uses is "a SQL-like notation".

  Source: [DCIC 4.1 Introduction to Tabular Data](https://dcic-world.org/2025-08-27/intro-tabular-data.html)
- **[RATIONALE] DCIC 1.3, "Our Perspective on Data":**
  - "Most introductory programming is plagued by artificial data that have no real meaning, interest, or consequence."
  - "programs interrogate data: that is, programs are tools for answering questions."
  - "data centric = data science + data structures"
  - "These limitations, where data science typically ends, are where computer science begins."

  Source: [DCIC Overview](https://dcic-world.org/2025-08-27/booklet_intro.html)
- **[RATIONALE] Notional machines.** DCIC develops "a sequence of them and weaves them through the curriculum". It says its choices are "driven by what we know from the research literature". The intended audience is students "in the early stages of computing education", and the earlier parts are "also suitable for secondary education". — [DCIC Overview](https://dcic-world.org/2025-08-27/booklet_intro.html)
- **[RATIONALE] Language choice.** The authors were "repeatedly frustrated by Python" as an entry point, so they start with Pyret. Python follows because "this will make you learn general programming better than if you had seen only one programming language." They also write: "If we wanted to get rich, we'd have written this book entirely in Python." — [DCIC Overview](https://dcic-world.org/2025-08-27/booklet_intro.html)
- **[RATIONALE] Versus HtDP.**
  - HtDP builds from atomic data → structures → lists → lists of structures. DCIC holds that "the most interesting data are lists of structures" and wants them "near the beginning!"
  - Tables are "ubiquitous" and "even primary school students recognize and use them". Real data (GDPs, populations, sports standings) replaces imagined data.
  - On HtDP's per-datatype recipes: they say the design recipe for lists of structures is complex and that the recipe is "dangerous to ignore" because "Students struggle with blank pages and often fill them up with bad code". DCIC uses "different program design methods that address the same ends through different means".
  - "Pyret and its environment were carefully designed around pedagogic ideas for teaching state"; Python "was not".

  Source: [DCIC Appendix: HtDP vs DCIC](https://dcic-world.org/2025-08-27/htdp-vs-dcic.html)
- **[DESIGN] Course use.** The early booklets correspond to CSCI 0111 at Brown, and a later track to CSCI 0190. The book says Brown students "have been drafted into acting as a crucible for every iteration of this book." The book reports no outcome data. — [DCIC Overview](https://dcic-world.org/2025-08-27/booklet_intro.html)
- **[RATIONALE] CACM Viewpoint (Krishnamurthi & Fisler, "Data-Centricity: A Challenge and Opportunity for Computing Education", Commun. ACM 63(8):24–26, Aug 2020).**
  - It argues introductory computing should be reworked around data to engage more students.
  - "Data-centric computing = data science + data structures (in that order: this + is not commutative)."
  - Tables are an introductory "sweet spot".
  - Source: [Brown paper page](https://cs.brown.edu/~sk/Publications/Papers/Published/kf-data-centric/), [CACM](https://cacm.acm.org/magazines/2020/8/246361-data-centricity/fulltext) (403 on direct fetch; content from the abstract and search snippet), [dblp](https://dblp.dagstuhl.de/rec/journals/cacm/KrishnamurthiF20.html)
- **[EVIDENCE] Adjacent study: data organizations (Gu, Heller, Li, Ren, Fisler, Krishnamurthi, ICER 2020, "Using Design Alternatives to Learn About Data Organizations").**
  - Students were given a pair of alternative organizations of the same data and asked to contrast them, then to interact with both and reflect.
  - Novice college students "handle this task fairly well" and identify differences in access and update operations.
  - They miss performance and privacy differences.

  Source: [Brown paper page](https://cs.brown.edu/~sk/Publications/Papers/Published/ghlrfk-design-alt-data-org/)
- **[EVIDENCE] Adjacent study: mutation misconceptions (Lu & Krishnamurthi, OOPSLA 2024, "Identifying and Correcting Programming Language Behavior Misconceptions", the SMoL Tutor).** Misconceptions about mutable variables and mutable compound data, and their interaction with scope and higher-order functions, are "widespread". An automated tutor "appears to improve understanding". No numbers were visible on the abstract page. — [Brown paper page](https://cs.brown.edu/~sk/Publications/Papers/Published/lk-smol-tutor/), [CEL page](https://cel.cs.brown.edu/paper/identifying-correcting-pl-misconceptions/)
- **[RATIONALE] Talks.** Fisler presented "functional programming: the glue for introducing computing through data science" at Lambda Days. — [Lambda Days slides PDF](https://www.lambdadays.org/static/upload/media/1616398068903863kathifislerfunctionalprogrammingtheglueforintroducingcomputingthroughdatascienceskompresowany.pdf). Krishnamurthi gave a talk on the same theme at an India ACM SIGCSE event. — [iSIGCSE talk PDF](https://www.isigcse.hosting.acm.org/downloads/Shriram-Talk-22ndJan2022.pdf) (neither PDF was read in full)

### Inferences
- DCIC's order is close to what this platform needs:
  1. Atomic types, including the distinction between "Names Versus Strings" and "Types and Contracts"
  2. Tables as the first collection
  3. Columns become lists
  4. Records/structs
  5. Dicts and arrays in Python
  6. Mutation and memory models last

  DCIC does **not** postpone conditionals until after tables: 3.4 Conditionals and Booleans precedes 4 Tabular Data. Loops are postponed. Iteration over a table happens through whole-table operations (`filter-with`, `order-by`, `build-column`) that take a per-row function.
- "From Tables to Lists" inverts the usual Python textbook order (list → dict → list-of-dicts → CSV). It starts from the familiar 2-D table and derives a list as "one column". This may suit an adult who already knows spreadsheets.
- Mutation and aliasing are deliberately deferred to a later booklet with explicit memory diagrams (12.3 "Arrays and Lists in Memory"). The OOPSLA 2024 work suggests these misconceptions are widespread even after instruction. A "认识数据" stage could flag mutability as a list/dict characteristic without yet exercising aliasing.

### Gaps
- I found **no published learning-outcome evaluation of DCIC / CSCI 0111** (pre/post, comparison cohorts). A search summary claimed a SIGCSE 2021 paper with the DCIC title exists, but I could not verify it. Treat it as unconfirmed.
- I could not read the CACM 2020 full text (HTTP 403). The quotes come from the search snippet and abstract.
- The SMoL Tutor prevalence numbers and effect sizes were not retrieved; the full PDF is linked from the paper page.

---

## Q3. Bootstrap:Data Science, Berkeley Data 8, and other data-first intros: ordering of types, tables, filtering, aggregation; relevance for later SQL

### Takeaway
Both Bootstrap:Data Science and Data 8 put **tables first or nearly first** and **defer conditionals and iteration**.
- **Bootstrap:DS** order: basic data/operations → table charts → extracting rows and cells → order/filter rows and compute new columns → functions from examples → the design process → combining table operations. `if`-expressions come only at lesson 10.
- **Data 8** introduces tables in §3.4, before its Data Types chapter (ch. 4). Its order is sequences/arrays (5), tables (6), functions and tables with group/pivot/join (8), and only then conditional statements and iteration (9.1–9.2).

Bootstrap's evaluation is explicitly "very preliminary". I found no Data 8 outcome study.

### Cited Findings
- **[DESIGN] Bootstrap:DS lesson sequence** (Fig. 1 of Schanzer, Pfenning, Denny, Dooman, Politz, Lerner, Fisler, Krishnamurthi, "Integrated Data Science for Secondary Schools: Design and Assessment of a Curriculum", SIGCSE 2022, DOI [10.1145/3478431.3499311](https://doi.org/10.1145/3478431.3499311)), computing column:

  | Lesson | Content |
  |---|---|
  | 1 | Questions that can be asked about datasets, alongside "categorical vs quantitative data" |
  | 2 | Introduction to programming in Pyret, "including basic data/operations" |
  | 3 | "images as datatypes, manipulating basic data with programming operations" |
  | 4 | "expressions to create charts from tables" |
  | 5 | "extracting rows and cells from tables" |
  | 6 | "using programs to order and filter rows, as well as to compute new columns" |
  | 7 | "developing functions from examples (abstraction)" |
  | 8 | "systematic design process" |
  | 9 | "combining multiple table manipulations… (decomposition and planning)" |
  | 10 | "if-else expressions" |
  | 12 | "extracting populations based on precisely-stated criteria" |
  | 18 | "writing tests" |

  Source: [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf), [Brown paper page](https://cs.brown.edu/~sk/Publications/Papers/Published/spddplfk-integ-ds-desn-assm-curric/)
- **[RATIONALE] Why tables only, in bs:ds:**
  - "many important datasets are published as tables (e.g., CSV files)"
  - tables have convenient creation interfaces "such as spreadsheets and even surveys"
  - they "are unambiguous to parse, unlike formats like natural language"
  - so they "do not force the introduction of probabilistic reasoning earlier than necessary".

  Source: [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] Bootstrap datasets.**
  - Curated datasets must have 1000–5000 rows, "at least two categorical columns and at least three quantitative ones", and at least one high correlation.
  - Early lessons use one artificial "animal shelter" dataset; students choose their own dataset from lesson 13.
  - Curated datasets are pre-cleaned, and missing values are deliberately avoided. The authors cite Date: "there can be many interpretations of a missing value, each of which may require different treatment".

  Source: [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] Pyret features.** Pyret has "accurate handling of numbers (rather than directly exposing machine numbers), to reduce numeric surprises", "built-in support for tables", and "a SQL-inspired query language integrated into the language". — [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] Scale.** About 8000 students used bs:ds in 2020–21, in about 50 cities. It is designed for grades 6–10, integrated into other subjects. A simplified 5th-grade version uses Google Sheets, and a CODAP version was in progress. — [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[EVIDENCE, explicitly preliminary] Bootstrap pilot results.**
  - Technical-skills instrument: 11 items. Pilot responses were "only a dozen teacher responses and 23 student responses", "sufficiently small that any detailed interpretations would be meaningless". A clear confusion appeared around data that do not fit the categorical–numeric split, such as studio numbers.
  - Perceptions instrument: 94 students. 96.9% agreed or strongly agreed that "I learned some programming from doing this" (42.6% strongly agree + 54.3% agree), and 100% agreed for data analysis. The authors say the results "do not rise to the level of findings".

  Source: [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] Bootstrap assessment items that double as "know your data" exercises:**
  - Classify each column of a movie table as "categorical, quantitative, or neither", and choose the "programming data type… most suitable to represent the columns".
  - A data-quality item with the column `Likes History?` holding "yes" / "false" / "nope" / "no", and `Height (in.)` holding `5.5` / `"4ft 10in"` / `"61 inches"` / `72`. Students judge whether each column is "ready to use" and fix one.
  - "Table Interpretation": which questions can or cannot be answered from a table.
  - Parsons-style ordering of plan steps.

  Source: [Paper PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] Data 8 textbook.** *Computational and Inferential Thinking*, 2nd ed., Adhikari, DeNero, Wagner, © 2022, CC BY-NC-ND. Chapters: 3 Programming in Python, 4 Data Types, 5 Sequences, 6 Tables, 7 Visualization, 8 Functions and Tables, 9 Randomness. — [inferentialthinking.com](https://inferentialthinking.com/chapters/intro.html)
- **[DESIGN] Data 8 introduces tables in Chapter 3,** before data types. Ch. 3 sections are 3.1 Expressions, 3.2 Names, 3.3 Call Expressions, 3.4 Introduction to Tables. §3.4 uses:
  - `Table.read_table` to load a CSV
  - `show`, `select`, `drop`, `sort` (with `descending=True`), and `where` (exact matching, case-sensitive)

  These methods return new tables and leave the original unchanged. — [Data 8 §3.4](https://inferentialthinking.com/chapters/03/4/introduction-to-tables/)
- **[DESIGN] Data 8 types, arrays and tables.**
  - Ch. 4 covers strings (adding two strings gives a string) and comparisons (strings compare alphabetically). — [Data 8 §4.2 Strings](https://inferentialthinking.com/chapters/04/2/strings/), [Data 8 §4.3 Comparisons](https://inferentialthinking.com/chapters/04/3/comparison/)
  - Ch. 5 arrays "can only contain a single kind of data", and arithmetic with a number applies to each element. — [Data 8 §5.1 Arrays](https://inferentialthinking.com/chapters/05/1/arrays/)
  - Ch. 6 defines a table as named columns, or equivalently as rows that each hold one entry. — [Data 8 Ch. 6 Tables](https://inferentialthinking.com/chapters/06/tables/), [§6.2 Selecting Rows](https://inferentialthinking.com/chapters/06/2/selecting-rows/)
  - Ch. 8 includes "Classifying by One Variable", i.e. group. — [Data 8 §8.2](https://inferentialthinking.com/chapters/08/2/Classifying_by_One_Variable.html)
- **[DESIGN] Data 8 defers conditionals and loops.** Ch. 9 "Randomness" contains 9.1 Conditional Statements and 9.2 Iteration, after Tables (6) and Functions and Tables (8). — [Data 8 Ch. 9](https://inferentialthinking.com/chapters/09/randomness/index.html)
- **[DESIGN] DCIC in Python.** DCIC's Python part puts dictionaries (9.2) before Pandas tables (10) and file I/O (11), after the Pyret table/list foundation. — [DCIC TOC](https://dcic-world.org/2025-08-27/index.html)

### Inferences
- The three designs agree on an order: **atomic types → tables (select/filter/sort/new column) → aggregation and grouping → conditionals and loops as tools inside per-row functions or simulations**. Data 8 goes furthest, using tables before even naming "data types".
- Table operations in Data 8 and Pyret are whole-table and non-mutating, returning new tables. That is the same mental model as a SQL `SELECT` producing a result set, so it is a good bridge to SQL (see Q6).
- Bootstrap's "is this column ready to use?" item is an off-the-shelf design for a "认识数据" exercise on mixed-type columns, which is exactly the `"5"` vs `5` problem.
- For an adult self-learner, Data 8's library (`datascience.Table`) and Pyret are teaching-specific. In plain Python the closest analogs are a list of dicts (or `csv.DictReader`), then pandas, then `sqlite3`. DCIC Part III shows the Pyret-table → Python-dict → Pandas path.

### Gaps
- I found no published learning-outcome evaluation of Data 8, or comparison of tables-first against conventional Python CS1, in this session.
- I could not retrieve the full section lists for Data 8 chapters 4, 5, 6 and 8 from the site navigation. I have only individual section pages found by search, so a "4.1 Numbers" section is not confirmed. I did not verify whether any `if` or `for` appears before Ch. 9 in passing.
- I did not retrieve the current Bootstrap:DS lesson pathway for 2025–26 from bootstrapworld.org. The order above is from the SIGCSE 2022 paper and may have been revised since.
- I did not find a published "Python for Data Science for absolute beginners" course with an explicit data-first rationale and evaluation, beyond Data 8 and DCIC.

---

## Q4. Beginner misconceptions about data types and teaching activities that address them

### Takeaway
There are curated misconception inventories, including progmiscon.org for Python and Sorva's notional-machine review. They document misconceptions about booleans, assignment and references, and mutability/aliasing. Studies show variables and Boolean logic are hard for novices (Grover & Basu 2017), and mutation/aliasing misconceptions are widespread (Lu & Krishnamurthi 2024). For the specific `"5"` vs `5` / `input()`-returns-a-string / str+int problem, I found only teaching materials, not a formal study. Activities with research backing are: making the notional machine an explicit learning objective, memory diagrams, classify/predict items, paired contrasts of data organizations, and refutation-style tutors for mutation.

### Cited Findings
- **[EVIDENCE/RESOURCE] progmiscon.org (Chiodini, Moreno Santos, Gallidabino, Tafliovich, Santos, Hauswirth, ITiCSE 2021, "A Curated Inventory of Programming Language Misconceptions").** It curates 198 misconceptions, defined as statements disprovable from a language's syntax or semantics, and compares them with the Sorva and Lewis collections. — [paper PDF](https://luce.si.usi.ch/assets/publications/chiodiniCuratedInventoryProgramming2021.pdf), [USI page](https://luce.si.usi.ch/publications/2021-06-01-programming-language-misconceptions.html)
- **[RESOURCE] progmiscon Python list (30 entries)** relevant to data:
  - Booleans: `ComparisonWithBoolLiteral` ("must compare to True/False"), `MapToBooleanWithIf`, `NoShortCircuit`
  - Assignment: `AssignCompares`
  - References and copying: `AssignmentCopiesObject`, `VariablesHoldObjects` (a variable contains the object rather than a reference), `VariablesHoldExpressions`
  - Strings: `StringLiteralNoObject` ("must call `str` to create a string")

  The Python list does **not** cover int vs float, division, string concatenation, None, or list/dict-specific items. — [progmiscon Python](https://progmiscon.org/misconceptions/Python/)
- **[EVIDENCE] Grover & Basu, SIGCSE 2017** ("Measuring Student Learning in Introductory Block-Based Programming: Examining Misconceptions of Loops, Variables, and Boolean Logic", pp. 267–272). Items were piloted with 100 6th–8th graders after a Scratch course. Students were largely unfamiliar with variables and held misconceptions about them, and they struggled with loops and Boolean operators. — [DOI 10.1145/3017680.3017723](https://www.doi.org/10.1145/3017680.3017723), [SRI page](https://www.sri.com/publication/education-learning-pubs/measuring-student-learning-in-introductory-block-based-programming-examining-misconceptions-of-loops-variables-and-boolean-logic/)
- **[EVIDENCE/REVIEW] Sorva, "Notional machines and introductory programming education", ACM TOCE 13(2), 2013.** The literature identifies notional machines as a major challenge. Instructors "should acknowledge the notional machine as an explicit learning objective and address it in teaching". — [Crossref DOI 10.1145/2483710.2483713](https://api.crossref.org/works/10.1145%2F2483710.2483713), [dblp](https://dblp.org/rec/journals/jeric/Sorva13)
- **[EVIDENCE] Lu & Krishnamurthi, OOPSLA 2024.** Misconceptions about mutable variables and mutable compound data are widespread. A self-guided tutor built on strategies from the education literature appears to improve understanding. — [paper page](https://cs.brown.edu/~sk/Publications/Papers/Published/lk-smol-tutor/)
- **[DESIGN] DCIC 12.3 and 13.2.** DCIC devotes sections to "Arrays and Lists in Memory" and "Mutable Lists", plus "Understanding Equality" (12.2), all after the functional foundation. — [DCIC TOC](https://dcic-world.org/2025-08-27/index.html)
- **[DESIGN] Early type sections in DCIC and HtDP.** DCIC 3.1.7 "Stepping Back: Types, Errors, and Documentation" covers types and contracts and format/notation errors. 3.2.2.1 "Names Versus Strings" targets the confusion between `x` and `"x"`. — [DCIC TOC](https://dcic-world.org/2025-08-27/index.html). HtDP 1.7 "Predicates: Know Thy Data" teaches type-testing predicates right after the arithmetic of each type. — [HtDP TOC](https://htdp.org/2024-11-6/Book/index.html)
- **[DESIGN] Bootstrap classification items.** Students classify columns as categorical, quantitative or neither, and pick a programming type per column. They also judge whether mixed-format columns ("4ft 10in", "61 inches", 72) are usable and normalize one. The pilot showed clear confusion about values like "studio numbers", which are numeric-looking but categorical. — [Bootstrap SIGCSE 2022 PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[EVIDENCE] Paired contrasts.** Showing two organizations of the same data and asking students to contrast them, then use both and reflect, works for novices on access and update differences. It needs support on performance and privacy. — [Gu et al. ICER 2020](https://cs.brown.edu/~sk/Publications/Papers/Published/ghlrfk-design-alt-data-org/)
- **[TEACHING MATERIAL, not a study] input() and TypeError.**
  - `input()` returns a string, so forgetting to convert gives wrong results. Entering 3 and 4 yields `"34"` rather than 7. — [BU CS111 common errors](https://www.cs.bu.edu/courses/cs111/problem_sets/errors.shtml), [Clark CS120 errors](https://mathcs.clarku.edu/courses/cs120/problem_sets/errors.html)
  - Runestone's *Foundations of Python Programming* lists TypeError among the most common errors in introductory programming. — [FOPP "Know Your Error Messages"](https://runestone.academy/ns/books/published/fopp/Debugging/KnowyourerrorMessages.html)
  - `int("abc")` raises ValueError, not TypeError. — [learnpython: common string and number errors](https://learnpython.netlify.com/02-introduction-to-python/020-basic-data-types/05-common-string-and-number-errors/)
- **[DESIGN] Data 8 array model.** "a single array can only contain a single kind of data", and arithmetic broadcasts over elements. — [Data 8 §5.1](https://inferentialthinking.com/chapters/05/1/arrays/)
- **[DESIGN] Pyret numbers.** Pyret's exact numbers are a deliberate design to "reduce numeric surprises" such as float rounding. Python exposes those surprises directly. — [Bootstrap SIGCSE 2022 PDF](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)

### Inferences
Activity types for a "认识数据" stage, each tied to a source above:
- **Classify-the-value / pick-the-type**, after the Bootstrap column-classification items. Extend to Python literals: `5`, `5.0`, `"5"`, `True`, `"True"`, `None`, `[5]`, `(5,)`, `{"a": 5}`.
- **Predict the result and type before running**, e.g. `"5" + "5"`, `5 + 5`, `"5" * 3`, `7 / 2`, `7 // 2`, `int("5") + 5`, `int("abc")`. This is notional-machine practice in Sorva's sense. Have learners name the error class as well (TypeError vs ValueError).
- **"Is this column ready?" cleaning tasks**, after Bootstrap's data-quality items and DCIC 4.2.1 normalization: mixed `"yes"` / `"no"` / `"false"` strings, numbers stored as text, unit-bearing strings, empty cells.
- **Names vs strings**, after DCIC 3.2.2.1: contrast `x` with `"x"` and `print(x)` with `print("x")`.
- **Booleans as values, not only as `if` conditions.** This targets progmiscon's `ComparisonWithBoolLiteral` and `MapToBooleanWithIf`. Have learners compute and store booleans (`is_adult = age >= 18`) before writing any `if`.
- **Mutability as a property column in a collections comparison table** (ordered? mutable? duplicates allowed? indexed by?). Do the deeper aliasing and memory-diagram work later, as DCIC does, perhaps with an SMoL-style refutation activity.
- **Paired data organizations**, after Gu et al.: the same data as a list of dicts vs a dict of lists vs a list of tuples. Ask "which makes question X easier?"

### Gaps
- I found no peer-reviewed study in this session that specifically measures novice misconceptions about `"5"` vs `5`, int vs float division, string concatenation vs addition, or `None` in Python. Evidence for these is teaching folklore and course materials. Candidate literature to check, not verified here: Kaczmarczyk et al. SIGCSE 2010; Sirkiä & Sorva Koli 2012; Altadmri & Brown SIGCSE 2015 (Java compile errors); Kohn SIGCSE 2019 (Python error messages); Guo SIGCSE 2013 (Python Tutor).
- I found no controlled evidence that memory diagrams improve outcomes specifically for data-type misconceptions. Sorva 2013 is a review and argument. The SMoL tutor numbers were not retrieved.

---

## Q5. A concrete "data first" sequence for Python: values & types → operations → conversion → collections → tabular data → control flow? Strict or interleaved?

### Takeaway
None of the published designs postpone *all* control flow until after collections.
- **HtDP** introduces conditionals when data has variants (itemizations), before structures and lists.
- **DCIC** teaches conditionals and booleans (3.4) before tables, but postpones loops (Python `for` in 9.1.8).
- **Bootstrap:DS** puts if-else at lesson 10, after table filtering and ordering.
- **Data 8** puts if and for in ch. 9, after tables, grouping and joins.

The common pattern is: **values and types (with booleans as values) → names and functions → tables via whole-table operations → columns as lists → aggregation → records/dicts → conditionals as needed → explicit loops and mutation later.**

### Cited Findings
- **[DESIGN] HtDP order:** atomic arithmetic of numbers/strings/images/booleans + predicates (Ch. 1) → functions (2) → design recipe (3) → conditionals via itemizations (4) → structures (5–6) → lists (8–12) → abstraction (III). — [HtDP TOC](https://htdp.org/2024-11-6/Book/index.html)
- **[DESIGN] DCIC order:** numbers/strings/images/types (3.1) → names (3.2) → functions (3.3) → conditionals/booleans (3.4) → tables (4) → lists from table columns (5.1) → recursion (5.2–5.3) → structured data (6) → Python dicts/arrays (9.2–9.3), `for` loops (9.1.8) → Pandas (10) → file I/O (11) → mutation/memory (12–13). — [DCIC TOC](https://dcic-world.org/2025-08-27/index.html)
- **[DESIGN] Bootstrap:DS order:** data types and categorical/quantitative (1–3) → charts from tables (4) → rows and cells (5) → order/filter/new columns (6) → functions from examples (7) → design process (8) → composition and planning (9) → if-else (10). — [Bootstrap SIGCSE 2022](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] Data 8 order:** expressions, names, calls, tables (3) → data types (4) → arrays (5) → tables (6) → visualization (7) → functions and tables, group (8) → conditionals and iteration (9). — [Data 8 §3.4](https://inferentialthinking.com/chapters/03/4/introduction-to-tables/), [Data 8 Ch. 9](https://inferentialthinking.com/chapters/09/randomness/index.html)
- **[DESIGN] DCIC tables use per-row functions.** Tables are processed by passing a per-row function to `filter-with` and `build-column`. `filter-with` is likened to `if`. So functions and booleans are prerequisites for tables, while loops are not. — [DCIC 4.1](https://dcic-world.org/2025-08-27/intro-tabular-data.html)
- **[RATIONALE] Against the blank page.** DCIC's authors say ignoring structured design is dangerous because "Students struggle with blank pages and often fill them up with bad code". That argues for scaffolded, data-driven templates rather than open-ended loops early. — [DCIC vs HtDP](https://dcic-world.org/2025-08-27/htdp-vs-dcic.html)
- **[DESIGN] Python HtDP adaptations** keep "data definitions" as step 1. — [Clements Python design recipe](https://brinckerhoff.org/clements/2254-csc202/Files/design-recipe.html), [UBC CS189](https://cs.ubc.ca/~pcarter/cs189/cs189_ch1s1.html)

### Inferences
A proposed "认识数据" sequence for Python, synthesized from the designs above. This is my inference, not a published curriculum.

| Step | Content | Basis |
|---|---|---|
| D1 | **Values and types:** `int`, `float`, `str`, `bool`, `None`; literals; `type()`; classify-the-value | HtDP Ch. 1, DCIC 3.1, Bootstrap L1–3 |
| D2 | **Operations per type:** arithmetic incl. `/` vs `//` vs `%`; string `+` and `*`, `len`, indexing/slicing, methods; comparisons producing booleans; `and`/`or`/`not`; predict-the-output | HtDP "Arithmetic of X", Data 8 §4.2–4.3 |
| D3 | **Names and conversion:** `x` vs `"x"`; `int()`, `float()`, `str()`, `bool()`; `input()` returns `str`; TypeError vs ValueError | DCIC 3.2.2.1 |
| D4 | **Small functions** with type hints and examples (Python doctest/asserts as "where" examples) | DCIC 3.3, HtDP Ch. 2–3 |
| D5 | **Records:** one row as a `dict` (field names → values of different types) | DCIC 6 / HtDP 5 structures, moved earlier |
| D6 | **Tables:** a list of dicts, loaded from CSV with `csv.DictReader` (everything arrives as `str`, so conversion from D3 is needed); select columns, filter rows, sort, add a computed column, using comprehensions or helper functions | DCIC 4, Data 8 3.4/6, Bootstrap L4–6 |
| D7 | **Columns as lists:** extract a column; `sum`/`len`/`max`/`min`/`sorted`; mean; count by category with a `dict` (group-by) | DCIC 5.1, Data 8 Ch. 8 |
| D8 | **Collections comparison card:** list / tuple / dict / set across ordered? mutable? duplicates? indexed by? literal syntax; JSON as nested dicts/lists | — |
| D9 | **Missing and dirty data:** empty strings, `None`, `"N/A"`, mixed units; normalization functions | DCIC 4.2.1.2–4.2.1.5 |
| D10 | **Then** explicit `for`/`if` patterns over these structures, then mutation and aliasing with memory diagrams | DCIC 9.1.8, 12–13; Data 8 Ch. 9 |

Notes on the table:
- **Interleaving recommendation:** introduce booleans and simple conditional *expressions* in D2/D4, as DCIC and HtDP do. Hold back explicit loops until D6/D7, where list comprehensions or helper functions make "do this for every row" concrete. This mirrors DCIC's `filter-with` / `build-column` and Data 8's `where` / `apply`.
- Data 8's choice to show a table in week one (§3.4, before "Data Types") suggests a motivating preview. Load a small CSV and *look at it* before D1, so types are introduced as "what kinds of values live in these columns?"

### Gaps
- I found no published Python-native course that follows exactly this order *and* reports outcomes. DCIC's Python part assumes the Pyret foundation was learned first.
- I found no evidence on the optimal placement of list comprehensions vs `for` loops for novices in a data-first sequence.

---

## Q6. How data-first prepares for SQL (tables, rows, columns, types, NULL)

### Takeaway
The table operations taught in DCIC, Bootstrap and Data 8 correspond nearly one-to-one to SQL clauses. Pyret explicitly includes a "SQL-inspired query language". Whole-table, non-mutating operations match SQL's declarative result-set model. "A given column has the same type" mirrors SQL column typing, and DCIC's "Dealing with Missing Entries" prefigures NULL. SQL misconception research warns that prior course knowledge is one source of SQL misconceptions. So how the Python stage frames tables matters for later SQL.

### Cited Findings
- **[DESIGN] Pyret query language.** Pyret, used by Bootstrap:DS and DCIC, provides "a SQL-inspired query language integrated into the language". — [Bootstrap SIGCSE 2022](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[DESIGN] DCIC notation and typing.** DCIC uses three notations for table processing, one of which is "a SQL-like notation". It states "A given column has the same type, but different columns can have different types." — [DCIC 4.1](https://dcic-world.org/2025-08-27/intro-tabular-data.html)
- **[DESIGN] DCIC table operations:** row extraction, `filter-with` (rows by predicate), `order-by` (sort by column, ascending or descending), `build-column` / `transform-column` (computed columns). — [DCIC 4.1](https://dcic-world.org/2025-08-27/intro-tabular-data.html)
- **[DESIGN] Data 8 table methods:** `select` / `drop` (columns), `sort` (with `descending=True`), `where` (rows by value). They return new tables, leaving the original unchanged. Grouping comes in Ch. 8 ("Classifying by One Variable"). I believe Ch. 8 also covers cross-classifying (pivot) and joining tables, but did not verify this; check the Ch. 8 navigation. — [Data 8 §3.4](https://inferentialthinking.com/chapters/03/4/introduction-to-tables/), [Data 8 §8.2](https://inferentialthinking.com/chapters/08/2/Classifying_by_One_Variable.html)
- **[DESIGN] Missing data.** DCIC 4.2.1.2 is "Dealing with Missing Entries". 4.2.1.5 is "Using Programs to Detect Data Errors". — [DCIC TOC](https://dcic-world.org/2025-08-27/index.html)
- **[RATIONALE] Bootstrap and missing values.** Bootstrap avoids missing values in early curated datasets because, following Date, "there can be many interpretations of a missing value, each of which may require different treatment". Its lessons do not currently exercise missing-value handling. — [Bootstrap SIGCSE 2022](https://khoury.northeastern.edu/home/blerner/papers/sigcse2022_ds_curriculum.pdf)
- **[EVIDENCE] SQL misconceptions (Miedema, Aivaloglou, Fletcher, ICER 2021, "Identifying SQL Misconceptions of Novices: Findings from a Think-Aloud Study", DOI 10.1145/3446871.3469759).** Four categories: "misconceptions based in previous course knowledge", generalization-based, language-based, and incomplete or incorrect mental model. — [ICER 2021 program page](https://icer2021.acm.org/details/icer-2021-papers/22/Identifying-SQL-Misconceptions-of-Novices-Findings-from-a-Think-Aloud-Study), [TU Delft repository](https://repository.tudelft.nl/record/uuid:9d9f12ee-8474-486a-91b2-4fa4b688dc41)
- **[EVIDENCE] Follow-ups.** A Koli Calling 2023 prevalence study found misconceptions ranging from 1% to 52% of students (DOI 10.1145/3631802.3631821). An ACM TOCE 2023 study had 19 SQL experts propose causes of student errors. — [Expert Perspectives on Student Errors in SQL](https://repository.tudelft.nl/record/uuid:dd23c9b1-247c-4a9e-9ca0-f5e297177686), [Never Work in Theory summary](https://neverworkintheory.org/2021/08/27/errors-in-sql-queries.html)

### Inferences
- **Mapping to teach explicitly** in the Python stage, so the SQL stage is "new syntax for known ideas":

  | Python / table operation | SQL |
  |---|---|
  | select columns | `SELECT col, …` |
  | `where` / `filter-with` | `WHERE` |
  | `sort` / `order-by` | `ORDER BY` |
  | `build-column` | `SELECT expr AS new_col` |
  | group / count-by-category | `GROUP BY` + aggregate |
  | join tables | `JOIN` |
  | per-column type | column type in `CREATE TABLE` |
  | missing entry / `None` | `NULL` |

- **Favor whole-table, non-mutating operations** (comprehensions or helper functions that return a new list of rows) over in-place loops that mutate rows. That matches SQL's declarative result sets and is how Data 8 and Pyret behave. It may also reduce the "previous course knowledge" class of SQL misconceptions, for example thinking procedurally row by row. This is my hypothesis; it has not been tested.
- **Teach `None` vs `""` vs `0` vs `"N/A"` as distinct values in the data stage.** This prepares for SQL's three-valued logic around NULL, where `NULL = NULL` is not true. It also follows DCIC 4.2.1.2 and Bootstrap's caution that missing values have many interpretations.
- **The "one type per column" rule** (DCIC; Data 8 arrays hold "a single kind of data") is the Python-side precursor to SQL schemas. A CSV loaded with `csv.DictReader` yields all strings, so conversion becomes a per-column schema decision.

### Gaps
- I found no study measuring whether data-first or tables-first programming instruction improves later SQL learning.
- I could not confirm whether NULL-specific misconceptions appear in the Miedema et al. inventories; I did not read the full papers.
- DCIC's TOC shows no SQL chapter, and I found no DCIC or Bootstrap material that teaches SQL itself. The SQL connection exists only through Pyret's SQL-like notation.
