# How widely used English zero-background Python courses start and sequence data types and data structures (snapshot: 2026-11-22)

Method note: Pages were fetched directly on 2026-11-22. Where possible I used official sites or official GitHub repos: the freeCodeCamp curriculum JSON, the Exercism `config.json`, the py4e book source, the Hyperskill public JSON API and MIT OCW slide PDFs. Real Python blocks automated fetching (HTTP 403), so that course is documented only indirectly. All URLs are given inline.

---

## Q1. Unit/chapter order (first 8–12 units) and what the very first 1–3 lessons cover, per course

### Takeaway
Almost every course opens with output, then values and variables, then input, all within the first unit. The main difference is whether that first unit names the kinds of data explicitly. MIT, py4e, Think Python, Automate the Boring Stuff (ATBS), Hyperskill, freeCodeCamp and Helsinki have a "values and types" or "data types" lesson. CS50P, Codecademy, the official Tutorial and Google meet types only in passing. Collections (list, tuple, dict, set) come in a later, separate unit in every course.

### Cited Findings

#### 1. Harvard CS50P – CS50's Introduction to Programming with Python (OCW site, live Nov 2026; Problem Set 0 deadline shown as 2027-06-30)
- The course has ten weeks plus a final project, in this order: **0 Functions, Variables; 1 Conditionals; 2 Loops; 3 Exceptions; 4 Libraries; 5 Unit Tests; 6 File I/O; 7 Regular Expressions; 8 Object-Oriented Programming; 9 Et Cetera**; then the Final Project. It is "Designed for students with or without prior programming experience." — [CS50P home](https://cs50.harvard.edu/python/)
- Lecture 0 section order: Creating Code with Python, then Functions, Bugs, Improving Your First Python Program, Variables, Comments, Pseudocode, Further Improving Your First Python Program, Strings and Parameters, A small problem with quotation marks, Formatting Strings, More on Strings, **Integers or int**, Readability Wins, **Float Basics**, More on Floats, Def, Returning Values and Summing Up. — [CS50P Lecture 0 notes](https://cs50.harvard.edu/python/notes/0/)
- The first program is `print("hello, world")`. The lecture then uses `name = input("What's your name? ")` and states: "A string, known as a str in Python, is a sequence of text." — [CS50P Lecture 0 notes](https://cs50.harvard.edu/python/notes/0/)
- Lecture 1 (Conditionals) has these sections: if Statements; Control Flow, elif, and else; or; and; Modulo; Creating Our Own Parity Function; Pythonic; match. bool is introduced here: "if statements use bool (Boolean) values (True or False) to decide…" — [CS50P Lecture 1 notes](https://cs50.harvard.edu/python/notes/1/)
- Lecture 2 (Loops) has these sections: While Loops, For Loops, Improving with User Input, **More About Lists**, Length, **Dictionaries**, Mario. — [CS50P Lecture 2 notes](https://cs50.harvard.edu/python/notes/2/)
- Lecture 3 (Exceptions) has these sections: Runtime Errors, try, else, Creating a Function to Get an Integer, pass. — [CS50P Lecture 3 notes](https://cs50.harvard.edu/python/notes/3/)
- Problem Set 0 contains five problems: Indoor Voice, Playback Speed, Making Faces, Einstein and Tip Calculator. — [CS50P Problem Set 0](https://cs50.harvard.edu/python/psets/0/)

#### 2. MIT 6.100L – Introduction to CS and Programming Using Python (Fall 2022, the current OCW edition; it replaces 6.0001 for beginners)
- From the syllabus: "No prerequisites". The course covers the same material as 6.0001, "but the pace is slowed down… give students who have never programmed the time to practice." It uses Python 3 and Guttag's *Introduction to Computation and Programming Using Python*, 3rd ed. — [6.100L Syllabus](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/syllabus/)
- Lecture order from the calendar:
  - **L1** Introduction to Python: knowledge, machines, **objects, types**, variables, bindings, IDEs
  - **L2** Core Elements of Programs: strings, input/output, f-strings, operators, branching, indentation
  - **L3** Program Flow: control flow, loops
  - **L4** Iteration, Simple Programs: guess and check, binary, fractions
  - **L5** Simple Algorithms: approximation method, floats
  - **L6** bisection search, Newton-Raphson
  - **L7** Functions: decomposition, abstraction, specifications
  - **L8** Functions: environments, scope, functions as objects
  - **L9 Tuples and Lists**
  - **L10** List Operations, Mutability
  - **L11** Aliasing and Cloning, List Comprehensions
  - **L12** More Functions as Objects, keyword/default arguments, debugging

  — [6.100L Calendar](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/calendar/)
- The Lecture 1 slides cover OBJECTS (scalar vs non-scalar), then SCALAR OBJECTS: "int – represent integers… float – represent real numbers… bool – represent Boolean values True and False… **NoneType – special and has one value, None**", "Can use type() to see the type of an object". After that come TYPE CONVERSIONS (CASTING), EXPRESSIONS ("An expression has a value, which has a type"), VARIABLES and BINDING VARIABLES to VALUES. — [6.100L Lecture 1 slides (PDF)](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/mit6_100l_f22_lec01.pdf)

#### 3. Python for Everybody (py4e, Dr. Chuck; the book source was updated to Python 3.12 on 2024-Jan-01)
- Lessons list:
  1. Installing Python
  2. Why Program?
  3. **Variables, expressions and statements**
  4. Conditional Execution
  5. Functions
  6. Loops and Iterations
  7. Strings
  8. Files
  9. **Lists**
  10. **Dictionaries**
  11. **Tuples**
  12. Regular Expressions
  13. Network Programming
  14. Using Web Services
  15. Object-Oriented Programming
  16. Databases
  17. Data Visualization

  — [py4e Lessons](https://www.py4e.com/lessons)
- Chapter 2 sections: **Values and types**, Variables, Variable names and keywords, Statements, Operators and operands, Expressions, Order of operations, Modulus operator, String operations, Asking the user for input, Comments, Debugging. The chapter opens with: "A value is one of the basic things a program works with, like a letter or a number… These values belong to different types: 2 is an integer, and 'Hello, World!' is a string". It then demonstrates `type('Hello, World!')`, `type(17)`, `type(3.2)`, `type('17')` and `type('3.2')`. — [py4e Ch.2](https://www.py4e.com/html3/02-variables)
- The 2024-Jan-01 update moved examples to Python 3.12. — [py4e preface source](https://github.com/csev/py4e/blob/master/book3/A0-preface.mkd)

#### 4. freeCodeCamp Python curriculum (v9 "Python Certification", plus a newer "Python Programming Fundamentals" superblock in the repo's main branch)
- `python-v9` ("Python Certification") module order:
  - **python-basics**, with blocks in this order:
    1. lecture-introduction-to-python
    2. **lecture-understanding-variables-and-data-types**
    3. workshop-report-card-printer
    4. lecture-introduction-to-python-strings
    5. workshop-employee-profile-generator
    6. workshop-employee-profile-validator
    7. lecture-numbers-and-mathematical-operations
    8. workshop-bill-splitter
    9. **lecture-booleans-and-conditionals**
    10. workshop-movie-ticket-booking-calculator
    11. lab-travel-weather-planner
    12. lecture-understanding-functions-and-scope
    13. …
    14. lab-rpg-character
  - Then: python-installation, then **python-loops-and-sequences**, then **python-dictionaries-and-sets** (with modules and regex), then lab-user-configuration-manager, python-error-handling, python-classes-and-objects, lab-budget-app, python-object-oriented-programming, python-linear-data-structures, python-recursion, python-algorithms, python-graphs-and-trees, python-dynamic-programming, and finally the certification exam.

  — [python-v9.json](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/superblocks/python-v9.json)
- The newer `python-programming-fundamentals` superblock adds **workshop-first-python-program** as the very first block. It also splits sequences into separate lectures in this order: lecture-working-with-lists, workshop-concert-program-planner, **lecture-working-with-tuples**, workshop-version-checker, lecture-working-with-loops-python, …, list comprehensions & lambdas. Dictionaries and sets are separate lectures (lecture-working-with-dictionaries, lecture-working-with-sets), followed by a "python-modules-and-standard-library" module. Its title is "Python Programming Fundamentals". — [python-programming-fundamentals.json](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/superblocks/python-programming-fundamentals.json); [intro.json](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/client/i18n/locales/english/intro.json)
- Lesson titles in "Understanding Variables and Data Types":
  1. How Do You Declare Variables and What Are Naming Conventions to Name Variables?
  2. How Does the Print Function Work?
  3. **What Are Common Data Types in Python?**
  4. **How Do the type() and isinstance() Functions Work?**

  — [block JSON](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-understanding-variables-and-data-types.json)
- Strings lecture: What Are Strings and What Is String Immutability? / String Concatenation and Interpolation / String Slicing / Common String Methods. — [block JSON](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-introduction-to-python-strings.json)
- Numbers lecture: How Do You Work With Integers and Floating Point Numbers? / Augmented Assignments / Format Numbers in an F-String. — [block JSON](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-numbers-and-mathematical-operations.json)
- Booleans lecture: How Do Conditional Statements and Comparison Operators Work? / **What Are Truthy and Falsy Values, and How Do Boolean Operators and Short-Circuiting Work?** / How Do Identity Operators Work? — [block JSON](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-booleans-and-conditionals.json)
- A separate video superblock, "Learn Python for Beginners", has these blocks in order: Python Setup & First Steps (Mike Dane), then **Core Primitives in Python** ("variables, data types, strings, numbers, and getting input from the user"), Small Python Projects, **Lists and Tuples**, Control Flow and Functions, **Dictionaries and Loops**, Error Handling/Files/Modules, and OOP. — [learn-python-for-beginners.json](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/superblocks/learn-python-for-beginners.json); [intro.json](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/client/i18n/locales/english/intro.json)

#### 5. Codecademy – Learn Python 3 (labelled "Beginner"; "14 lessons • 14 projects • 13 quizzes"; the first lesson lists "Python 3.13")
- Module order:
  1. **Hello World**, with the Hello World lesson and quiz, the projects Block Letters and Receipts for Lovely Loveseats, and the article User Input
  2. **Control Flow**: Control Flow lesson, Match Statements article, Magic 8-Ball, Sal's Shipping, and the Errors in Python lesson
  3. **Lists**: Introduction to Lists, Gradebook, Working with Lists, Len's Slice, the article **Tuples**, and the article Combining Lists: The Zip Function
  4. **Loops** (Carly's Clippers)
  5. **Functions**: Introduction to Functions, plus articles on lambda and map(), and the project Getting Ready for Physics Class
  6. Code Challenges (optional)
  7. **Strings**: Introduction to Strings, String Methods, Thread Shed, Coded Correspondence
  8. **Modules**
  9. **Dictionaries**: Creating Dictionaries, Using Dictionaries, Pythonagrams
  10. **Files**
  11. **Classes** (the lesson slug is `data-types`; the module description reads "Learn about the differences between data types in Python and how to create your own classes")
  12. Code Challenges II
  13. Next Steps

  — [Codecademy Learn Python 3 syllabus](https://www.codecademy.com/learn/learn-python-3)
- Exercises in the "Hello World" lesson: Welcome, Python 3.13, Comments, Print, **Strings**, Variables, Errors, **Numbers**, Calculations, Changing Numbers, Exponents, Modulo, Concatenation, Plus Equals, Multi-line Strings, Review. — [Codecademy Hello World lesson](https://www.codecademy.com/courses/learn-python-3/lessons/python-hello-world/exercises/welcome)

#### 6. JetBrains Academy / Hyperskill (track id 2 is now titled "Python Developer"; this was formerly the "Python Core" course)
- Track metadata: title "Python Developer", topics_count 277, members_count 227,623, is_free false. — [Hyperskill API: tracks/2](https://hyperskill.org/api/tracks/2); [course page](https://hyperskill.org/courses/2-python-core)
- The knowledge-graph order comes from `topological_index`. It begins:
  1. Introduction to Python
  2. Writing first program
  3. Multi-line programs
  4. **Basic data types**
  5. Variables
  6. Integer arithmetic
  7. Taking user's input
  8. Program with numbers
  9. Invoking functions
  10. **Boolean type and operations. True and false**
  11. Comparisons
  12. If statement
  13. Else statement
  14. **List**
  15. Indexes
  16. For loop
  17. …
  18. Declaring functions (144)
  19. …
  20. Elif (383)
  21. Function, arguments and parameters (407)
  22. Operations with list (408)
  23. **Tuple (417)**
  24. Quotes and multi-line strings (434)
  25. String formatting (436)
  26. While loop (451)
  27. …
  28. **Set (674)**
  29. **Dictionary (753)**

  The prerequisites form a chain: Variables requires Basic data types, and Boolean requires Variables. — [Hyperskill API: topics?track=2](https://hyperskill.org/api/topics?track=2)
- The "Basic data types" theory says: "Every data object (a variable or a constant) has a type that describes how to keep it in memory, which operations can be applied to this object… A real-world analogy of types is given by biological species… all dogs you've seen have the type dog". It covers str (single- and double-quoted examples, including `'1234'`), then int vs float (`print(11)` vs `print(11.0)`: "Even though 11 and 11.0 are the same number, the former is an integer, and the latter is a float"), then "Printing types" with `type('hello')`. — [Hyperskill API: steps/5852](https://hyperskill.org/api/steps/5852)

#### 7. Exercism Python track (syllabus = concept tree of "learning exercises", from `config.json` on main)
- The concept exercises are ordered by prerequisite depth (level 0 is the root). Active exercises only; electric-bill is deprecated.
  - **L0** basics (Guido's Gorgeous Lasagna)
  - **L1** bools (Ghost Gobble Arcade Game) and numbers (Currency Exchange)
  - **L2** conditionals (Meltdown Mitigation)
  - **L3** comparisons (Black Jack) and strings (Little Sister's Vocab)
  - **L4** string-methods (Little Sister's Essay) and **lists** (Card Games)
  - **L5** list-methods (Chaitana's Colossal Coaster)
  - **L6** **loops** (Making the Grade)
  - **L7** string-formatting (Pretty Leaflet, wip) and **tuples** (Tisbury Treasure Hunt)
  - **L8** **dicts** (Inventory Management)
  - **L9** dict-methods, unpacking-and-multiple-assignment, and **sets** (Cater Waiter)
  - **L10** classes and **none** (Restaurant Rozalynn, wip)
  - **L11** generators and enums

  — [exercism/python config.json](https://github.com/exercism/python/blob/main/config.json)
- The "basics" introduction covers these topics: Name Assignment (Variables & Constants), Functions (including functions that return **None**), Calling Functions, Comments, Docstrings. — [Lasagna introduction.md](https://github.com/exercism/python/blob/main/exercises/concept/guidos-gorgeous-lasagna/.docs/introduction.md)

#### 8. Official Python Tutorial (docs.python.org/3/tutorial; the page title at fetch time read "Python 3.15.2 documentation")
- Chapters:
  1. Whetting Your Appetite
  2. Using the Python Interpreter
  3. **An Informal Introduction to Python**: 3.1 Using Python as a Calculator, with 3.1.1 **Numbers**, 3.1.2 **Text** and 3.1.3 **Lists**; then 3.2 First Steps Towards Programming
  4. More Control Flow Tools: if, for, range, break/continue, else on loops, pass, match, Defining Functions…
  5. **Data Structures**: More on Lists, del, **Tuples and Sequences**, **Sets**, **Dictionaries**, Looping Techniques, More on Conditions, Comparing Sequences
  6. Modules
  7. Input and Output
  8. Errors and Exceptions
  9. Classes
  10. Brief tour of the standard library
  11. Brief tour of the standard library, part II

  — [Python Tutorial index](https://docs.python.org/3/tutorial/index.html); [Ch.3](https://docs.python.org/3/tutorial/introduction.html)
- The tutorial says it "is designed for programmers that are new to the Python language, not beginners who are new to programming." — [Python Tutorial index](https://docs.python.org/3/tutorial/index.html)

#### 9. Think Python, 3rd edition (Allen Downey; Jupyter notebook edition, site © 2023, print 2024)
- Chapters:
  1. Programming as a way of thinking
  2. Variables and Statements
  3. Functions
  4. Functions and Interfaces
  5. Conditionals and Recursion
  6. Return Values
  7. Iteration and Search
  8. Strings and Regular Expressions
  9. **Lists**
  10. **Dictionaries**
  11. **Tuples**
  12. Text Analysis and Generation
  13. Files and Databases
  14. Classes and Functions
  15. Classes and Methods
  16. Classes and Objects
  17. Inheritance
  18. Python Extras
  19. Final thoughts

  — [Think Python 3e home](https://allendowney.github.io/ThinkPython/)
- Chapter 1 sections: 1.1 Arithmetic operators, 1.2 Expressions, 1.3 Arithmetic functions, 1.4 Strings, **1.5 Values and types**, 1.6 Formal and natural languages, 1.7 Debugging, 1.8 Glossary, 1.9 Exercises. — [Ch.1](https://allendowney.github.io/ThinkPython/chap01.html)
- Chapter 2 sections: Variables, State diagrams, Variable names, The import statement, Expressions and statements, The print function, Arguments, Comments, Debugging. — [Ch.2](https://allendowney.github.io/ThinkPython/chap02.html)
- Section 1.5 text: "So far we've seen three kinds of values: 2 is an integer, 42.0 is a floating-point number, and 'Hello' is a string. A kind of value is called a type. Every value has a type…" It then covers `type(2)` → int, `int(42.9)` → 42, `float(42)` → 42.0, and `'126'` "looks like a number, but it is actually a string", where `'126' / 3` raises TypeError. — [Ch.1](https://allendowney.github.io/ThinkPython/chap01.html)

#### 10. Automate the Boring Stuff with Python, 3rd edition (Al Sweigart, free online)
- Chapters:
  1. **Python Basics**
  2. if-else and Flow Control
  3. Loops
  4. Functions
  5. Debugging
  6. **Lists**
  7. **Dictionaries and Structuring Data**
  8. Strings and Text Editing
  9. Text Pattern Matching with Regular Expressions
  10. Reading and Writing Files
  11. Organizing Files
  12. Designing and Deploying Command Line Programs
  13. Web Scraping
  14. Excel Spreadsheets
  15. Google Sheets
  16. SQLite Databases
  17. PDF and Word Documents
  18. CSV, JSON, and XML Files
  19. Keeping Time, Scheduling Tasks, and Launching Programs
  20. Sending Email, Texts, and Push Notifications
  21. Making Graphs and Manipulating Images
  22. Recognizing Text in Images
  23. Controlling the Keyboard and Mouse
  24. Text-to-Speech and Speech Recognition Engines

  — [ATBS home / TOC](https://automatetheboringstuff.com/)
- Chapter 1 sections: Entering Expressions into the Interactive Shell, **The Integer, Floating-Point, and String Data Types**, String Concatenation and Replication, Storing Values in Variables, Your First Program, Dissecting the Program, How Computers Store Data with Binary Numbers, Summary, Practice Questions. Text: "A data type is a category for values, and every value belongs to exactly one data type", followed by "Table 1-2: Common Data Types". The program-dissection part covers the `str()`, `int()` and `float()` functions. — [ATBS 3e Ch.1](https://automatetheboringstuff.com/3e/chapter1.html)
- Chapter 2 starts with **Boolean Values**, then Comparison Operators and Boolean Operators. — [Ch.2](https://automatetheboringstuff.com/3e/chapter2.html)
- Chapter 4 includes **The None Value**. — [Ch.4](https://automatetheboringstuff.com/3e/chapter4.html)
- Chapter 6 includes The List Data Type, Short-Circuiting Boolean Operators, Sequence Data Types, Mutable and Immutable Data Types, **The Tuple Data Type**, and List and Tuple Type Conversion. — [Ch.6](https://automatetheboringstuff.com/3e/chapter6.html)
- Chapter 7 covers **The Dictionary Data Type**. — [Ch.7](https://automatetheboringstuff.com/3e/chapter7.html)

#### 11. Google's Python Class (intro page "Last updated 2025-08-14 UTC")
- The class is for "people with a little bit of programming experience… enough to know what a 'variable' or 'if statement' is". It is based on Google's internal two-day class. — [Google's Python Class](https://developers.google.com/edu/python)
- Order: Python Set Up, then Python Intro, **Strings**, **Lists**, Sorting, **Dicts and Files**, Regular Expressions, Utilities.
- Videos: 1.1 Introduction, strings; 1.2 Lists and sorting; 1.3 Dicts and files; 2.1 Regular expr; 2.2–2.3 Utilities.
- Exercises: Basic Exercises, Baby Names, Copy Special, Log Puzzle.

  — [Google's Python Class](https://developers.google.com/edu/python)
- Intro page sections: Language Introduction, Python source code, Imports, Command-line arguments, and len(), User-defined Functions, Indentation, Code Checked at Runtime, Variable Names, Modules, help() and dir(). — [Python Introduction](https://developers.google.com/edu/python/introduction)
- Strings page sections: String Methods, String Slices, String formatting, String %, Unicode vs bytes, **If Statement**, Exercise: string1.py. — [Python Strings](https://developers.google.com/edu/python/strings)

#### 12. Real Python – "Python Basics" learning path / book
- The learning-path page returned HTTP 403 to automated fetches. — [Real Python Python Basics path](https://realpython.com/learning-paths/python-basics/)
- Search results show the path is titled "Python Basics: Introduction to Python", with 17–18 resources depending on the snapshot. "Setting Up Python" is the first item under "Getting Started", and the path is built from the *Python Basics* book's chapters. — [Real Python learning path (search result)](https://realpython.com/learning-paths/python-basics); [Python Basics book resources path](https://realpython.com/learning-paths/python-basics-book)
- Chapter folders in the book's official exercise repo:
  - ch03-first-python-program
  - **ch04-strings-and-string-methods**
  - **ch05-numbers-in-python**
  - ch06-functions-and-loops
  - ch08-conditional-logic
  - **ch09-lists-tuples-and-dictionaries**
  - ch10-primer-on-oop
  - ch11-modules-and-packages
  - ch12-file-input-and-output
  - ch14-interact-with-pdf-files
  - ch15-sql-database-connections
  - ch16-interacting-with-the-web
  - ch17-scientific-computing-and-graphing
  - ch18-graphical-user-interfaces

  — [realpython/python-basics-exercises](https://github.com/realpython/python-basics-exercises)

#### 13. University of Helsinki – Python Programming MOOC 2026 (programming-26.mooc.fi; open until the end of 2026)
- Parts 1–7 form the "Introduction to Programming" course (BSCS1001, 5 ECTS). Parts 8–14 form the "Advanced Course in Programming". The Part 1 lecture was on 03.09.2026. — [MOOC 2026 home](https://programming-26.mooc.fi/)
- Section order. Titles come from page H1s for Part 1 and 2.1; the rest are taken from the URL slugs.
  - **Part 1**: 1 Getting started, 2 Information from the user, 3 **More about variables**, 4 **Arithmetic operations**, 5 Conditional statements
  - **Part 2**: 1 **Programming terminology**, 2 else/elif, 3 Combining conditions, 4 Simple loops
  - **Part 3**: Loops with conditions, Working with strings, More loops, Defining functions
  - **Part 4**: VS Code, More functions, **Lists**, Definite iteration, Print statement formatting, Strings and lists
  - **Part 5**: More lists, References, **Dictionary**, **Tuple**
  - **Part 6**: Reading files, Writing files, Errors, Scope of variables
  - **Part 7**: Modules, Randomness, Times and dates, Data processing, Creating modules, More features

  — [Part 1](https://programming-26.mooc.fi/part-1), [Part 4](https://programming-26.mooc.fi/part-4), [Part 5](https://programming-26.mooc.fi/part-5)
- 1.1 "Getting started" has one objective: "You will know how to use the print command". It covers `print("Hi there!")` and the error when the quotes are left out. It contrasts `print(2 + 2 * 10)` with `print("2 + 2 * 10")` and defines strings as "sequences of characters". — [1.1](https://programming-26.mooc.fi/part-1/1-getting-started)
- 1.2 "Information from the user": "You will know how to use variables to store input and print it out". It uses `input`, `+` concatenation, and more than one input. — [1.2](https://programming-26.mooc.fi/part-1/2-information-from-the-user)
- 1.3 "More about variables": "You will understand the difference between strings, integers and floating point numbers". — [1.3](https://programming-26.mooc.fi/part-1/3-more-about-variables)
- 1.4 "Arithmetic operations": "You will know how to cast values into other fundamental data types", using `int(input(...))` and `float(input(...))`. It also notes that `/` always gives a float and `//` gives an int. — [1.4](https://programming-26.mooc.fi/part-1/4-arithmetic-operations)
- 1.5 "Conditional statements" includes the section "Boolean values and Boolean expressions" (the bool type, True/False). — [1.5](https://programming-26.mooc.fi/part-1/5-conditional-statements)
- 2.1 "Programming terminology": "You will be able to find out the data type of an evaluated expression". The section defines Statement, Block, Expression, Function, **Data type** (with `type()`), Syntax and Debugging. — [2.1](https://programming-26.mooc.fi/part-2/1-programming-terminology)

### Inferences
- Most courses meet text and numbers (str, int, float) in their first content unit: CS50P, MIT, py4e, freeCodeCamp, Codecademy, Hyperskill, the Python Tutorial, Think Python, ATBS and Helsinki. The exceptions are Real Python (strings in ch04, numbers in ch05), Exercism (numbers is a separate level-1 concept after "basics") and Google (strings first; numbers not seen in the section list). Only some courses name and compare these types as a topic, and only some put it before variables. Hyperskill ("Basic data types" comes before "Variables") and MIT L1 (objects and types before variables and bindings) are the clearest "types before variables" designs. py4e and Think Python put "Values and types" as the first or a very early section.
- Every course introduces collections in a separate later unit. No course has a "survey of all kinds of data" stage that previews lists, dicts and others together with scalars at the start. MIT L1's mention of "non-scalar objects" is the closest.
- In 2026 the freeCodeCamp repo appears to be shifting its first experience toward an even smaller step: type a bare string literal, then print it. That suggests a "values before statements" trend in at least one major platform.

### Gaps
- Real Python: the exact current course list of the learning path could not be fetched (403). The order shown is the book's, inferred from exercise-repo folder names. Chapters 1, 2, 7 and 13 have no exercise folder, so their titles are not confirmed apart from Ch.2 "Setting Up Python" in search snippets.
- freeCodeCamp: I could not confirm whether `python-programming-fundamentals` is live on freecodecamp.org or still in development. The learn page is a JavaScript shell.
- Hyperskill: `topological_index` is a global dependency order. It may differ from the order a learner's personalised study plan shows. The study-plan API returned empty without login.
- MIT 6.100L: the calendar was read only up to Lecture 12, and the dictionaries lecture number was not captured. MIT 6.0001 (Fall 2016) was not fetched separately; per the syllabus the material is the same.
- CS50P: the recording year of the current lecture videos was not verified. The site's content matches the long-standing 2022 structure.
- Helsinki: section titles for Parts 2–7 are taken from URL slugs, apart from 2.1, and the list of exercise names was not retrieved.

---

## Q2. Which courses introduce types explicitly first vs start with print and variables? When do they teach type conversion, truthiness and None? When do lists and dicts come relative to loops and functions?

### Takeaway
"Types as an explicit topic in the first unit" is now common: MIT, py4e, Think Python, ATBS, Hyperskill, freeCodeCamp and Helsinki all do it. The usual trio is int, float and str, with bool added soon after, often with conditionals. Conversion (`int(input())`) almost always arrives in the first unit because of the "input is a string" problem. Truthiness is early only in freeCodeCamp. `None` is early only in MIT (NoneType listed among the first scalar types) and Exercism (functions that return None). Lists come before loops in Codecademy, Hyperskill, Exercism, the Python Tutorial and freeCodeCamp's video course. Most university and book courses put lists and dicts after loops and functions.

### Cited Findings

| Course | Explicit types lesson in unit 1? | `type()` shown early? | Conversion first appears | bool first appears | Truthiness | `None` first appears | Lists vs loops/functions | Dict / tuple / set |
|---|---|---|---|---|---|---|---|---|
| CS50P | No dedicated lesson. str → int → float are covered as sub-sections of Week 0 "Functions, Variables" ([notes 0](https://cs50.harvard.edu/python/notes/0/)) | Not in Lecture 0 section list | Week 0: `int(x) + int(y)`, called "casting" ([notes 0](https://cs50.harvard.edu/python/notes/0/)) | Week 1, Conditionals ([notes 1](https://cs50.harvard.edu/python/notes/1/)) | Not seen in L0–L1 headings | Week 2, as a dict value ([notes 2](https://cs50.harvard.edu/python/notes/2/)) | Lists in Week 2 *with* for loops, after functions (Week 0) | Dicts in Week 2 ([notes 2](https://cs50.harvard.edu/python/notes/2/)) |
| MIT 6.100L | **Yes.** L1 covers "objects, types" ([calendar](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/calendar/)) | Yes, L1 ([slides](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/mit6_100l_f22_lec01.pdf)) | L1 "TYPE CONVERSIONS (CASTING)" | L1 (as a scalar type) | Not in L1 | **L1: "NoneType… has one value, None"** | Tuples and lists in L9, after loops (L3) and functions (L7–8) | Dict not in L1–12 |
| py4e | **Yes.** Ch.2 §1 "Values and types" ([ch2](https://www.py4e.com/html3/02-variables)) | Yes, `type('17')` etc. | Ch.2 has an "Asking the user for input" section | Ch.3 Conditional Execution ([lessons](https://www.py4e.com/lessons)) | n/a | n/a | Lists Ch.9, after functions (5), loops (6), strings (7) and files (8) | Dict Ch.10, tuple Ch.11, no set chapter ([lessons](https://www.py4e.com/lessons)) |
| freeCodeCamp v9 | **Yes.** Lecture 2 covers "What Are Common Data Types…" (int, float, str, bool) ([md](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/challenges/english/blocks/lecture-understanding-variables-and-data-types/67fe859a00971c34a23abd43.md)) | **Yes, `type()` and `isinstance()` lesson** ([block](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-understanding-variables-and-data-types.json)) | Numbers lecture ([block](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-numbers-and-mathematical-operations.json)) | Basics module, Booleans lecture | **Yes, in the Basics module: "Truthy and Falsy Values… Short-Circuiting"** ([block](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/blocks/lecture-booleans-and-conditionals.json)) | n/a | Lists and tuples in the Loops & Sequences module, after functions (Basics module) ([v9](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/superblocks/python-v9.json)) | Dicts and sets in the next module |
| Codecademy | No. Hello World lesson exercises include "Strings" and "Numbers" ([lesson](https://www.codecademy.com/courses/learn-python-3/lessons/python-hello-world/exercises/welcome)) | n/a (the Classes lesson slug is `data-types`) | "User Input" article in Module 1 | Module 2, Control Flow ("boolean variables and logical operators") ([syllabus](https://www.codecademy.com/learn/learn-python-3)) | n/a | n/a | **Lists (Module 3) before Loops (4) and Functions (5)** | Tuples as an article in Lists; Dicts in Module 9 |
| Hyperskill | **Yes. "Basic data types" comes before "Variables"** ([API](https://hyperskill.org/api/topics?track=2)) | Yes, "Printing types" ([theory](https://hyperskill.org/api/steps/5852)) | "Program with numbers" after "Taking user's input" | "Boolean type and operations. True and false" right after "Invoking functions" | n/a | n/a | **List (idx 131) before For loop (133) and Declaring functions (144)** | Tuple 417, Set 674, Dictionary 753 |
| Exercism | No. The root concept "basics" covers variables and functions ([intro](https://github.com/exercism/python/blob/main/exercises/concept/guidos-gorgeous-lasagna/.docs/introduction.md)) | n/a | "numbers" concept (level 1) | **bools is its own concept at level 1, before conditionals** ([config](https://github.com/exercism/python/blob/main/config.json)) | n/a | **"basics" shows functions returning None**; the dedicated "none" concept is at level 10 (wip) | **Lists (level 4) before loops (level 6)**; functions come first, in basics | Tuples L7, dicts L8, sets L9 |
| Python Tutorial | No. Ch.3 "Using Python as a Calculator" covers Numbers, Text and Lists ([ch3](https://docs.python.org/3/tutorial/introduction.html)) | n/a | n/a | n/a | "More on Conditions" in Ch.5 ([index](https://docs.python.org/3/tutorial/index.html)) | n/a | **Lists in Ch.3, before control flow and functions (Ch.4)** | Tuples, sets and dicts in Ch.5, after functions |
| Think Python 3e | **Yes.** §1.5 "Values and types" ([ch1](https://allendowney.github.io/ThinkPython/chap01.html)) | Yes, `type(2)` | §1.5: `int(42.9)`, `float(42)` | Ch.5 Conditionals (by title) | n/a | n/a | Lists Ch.9, after functions (3–6) and iteration (7) ([home](https://allendowney.github.io/ThinkPython/)) | Dict Ch.10, tuple Ch.11 |
| ATBS 3e | **Yes.** Ch.1 "The Integer, Floating-Point, and String Data Types" ([ch1](https://automatetheboringstuff.com/3e/chapter1.html)) | n/a | Ch.1, `str()` / `int()` / `float()` | Ch.2 opens with "Boolean Values" ([ch2](https://automatetheboringstuff.com/3e/chapter2.html)) | "Short-Circuiting Boolean Operators" in Ch.6 ([ch6](https://automatetheboringstuff.com/3e/chapter6.html)) | **Ch.4 "The None Value"** ([ch4](https://automatetheboringstuff.com/3e/chapter4.html)) | Lists Ch.6, after loops (3) and functions (4) | Tuple in Ch.6, dict in Ch.7 ([ch7](https://automatetheboringstuff.com/3e/chapter7.html)) |
| Google Class | No (assumes prior programming) ([home](https://developers.google.com/edu/python)) | n/a | n/a | If Statement in the Strings page ([strings](https://developers.google.com/edu/python/strings)) | n/a | n/a | Strings, then Lists, then Sorting | Dicts with Files, third section |
| Real Python | Strings chapter (ch04), then Numbers chapter (ch05) ([repo](https://github.com/realpython/python-basics-exercises)) | n/a | n/a | Conditional logic (ch08) | n/a | n/a | Lists, tuples and dicts in ch09, after functions & loops (ch06) and conditionals (ch08) | Same chapter |
| Helsinki MOOC 2026 | **Yes.** 1.3 covers "the difference between strings, integers and floating point numbers" ([1.3](https://programming-26.mooc.fi/part-1/3-more-about-variables)) | **Yes, in 2.1 "Programming terminology"** ([2.1](https://programming-26.mooc.fi/part-2/1-programming-terminology)) | 1.3 `str()`; 1.4 `int()` / `float()` ([1.4](https://programming-26.mooc.fi/part-1/4-arithmetic-operations)) | 1.5 "Boolean values and Boolean expressions" ([1.5](https://programming-26.mooc.fi/part-1/5-conditional-statements)) | n/a | n/a | Lists in Part 4, after loops (Parts 2–3) and functions (3.4) | Dictionary and Tuple in Part 5 |

("n/a" means it was not observed in the fetched material. It does not prove absence.)

- MIT L1 lists four scalar types side by side, including NoneType: "int… float… bool… NoneType – special and has one value, None", and adds "Can use type() to see the type of an object". — [6.100L L1 slides](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/mit6_100l_f22_lec01.pdf)
- freeCodeCamp deliberately limits the starting set: "For now, focus on four data types that you will use throughout this module: Integer… Float… String… Boolean… Python has other data types. You will learn each one when you first need it." It also introduces dynamic typing right away ("Python determines the type from the value assigned"; `age = 25` then `age = 'Twenty-five'`). — [fCC "What Are Common Data Types in Python?"](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/challenges/english/blocks/lecture-understanding-variables-and-data-types/67fe859a00971c34a23abd43.md)
- Helsinki's 2.1 lists each expression with its value, the type in words, and the Python type:

  | Expression | Value | Type | Python type |
  |---|---|---|---|
  | `2 + 4 + 3` | 9 | integer | int |
  | `"abc" + "de"` | "abcde" | string | str |
  | `11 / 2` | 5.5 | floating point number | float |
  | `2 * 5 > 9` | True | Boolean value | bool |

  It also shows `type("Anna")` → `<class 'str'>`. — [Helsinki 2.1](https://programming-26.mooc.fi/part-2/1-programming-terminology)
- CS50P introduces lists as a "new variable type" exactly when it needs them for for-loops: "To best understand a for loop, it's best to begin by talking about a new variable type called a list". It introduces None as "a special None designation where there is no value associated with a key". — [CS50P notes 2](https://cs50.harvard.edu/python/notes/2/)

### Inferences
- There are three common sequencing patterns:
  - **(A) Types-first:** Hyperskill, MIT, py4e, Think Python, ATBS, freeCodeCamp, Helsinki.
  - **(B) Print/strings-first, types implicit:** CS50P, Codecademy, Google, Real Python.
  - **(C) Calculator-first, including lists:** the Python Tutorial.
- Lists come *before* loops in the interactive/platform courses: Codecademy, Hyperskill, Exercism, the Python Tutorial and fCC's video course. Lists come *after* loops and functions in the book- and university-style courses: MIT, py4e, Think Python, ATBS, Helsinki, Real Python. CS50P teaches lists together with loops.
- bool is usually introduced as a by-product of conditionals. Exercism (a standalone bools concept before conditionals) and MIT (bool as a scalar type in L1) are the exceptions. A "recognize kinds of data" stage that treats True/False as data values, independent of if-statements, therefore has precedent but is a minority choice.
- None is the most neglected basic value in beginner syllabi. It appears early only in MIT L1 and in Exercism's basics. A platform that wants None in its first "kinds of data" stage would be going beyond nearly all mainstream courses.
- freeCodeCamp is the only course seen that puts truthy/falsy in the first module.

### Gaps
- The exact first appearance of `type()` in CS50P, Codecademy, Real Python and the Python Tutorial was not confirmed. Only headings and TOCs were checked.
- Where Think Python 3e introduces bool and None, and py4e's treatment of None, were not verified at section level.
- Codecademy beyond the first lesson is mostly paywalled, so exercise-level contents for later modules were not checked.

---

## Q3. What exercises do the very first lessons use (e.g., predicting the type of a value, converting input strings to numbers)?

### Takeaway
The early exercises fall into four groups:
- **"Find or predict the type"** drills: MIT L1, py4e Ch.2 Ex.4, Hyperskill, Helsinki 2.1.
- **"Same-looking but different type"** contrasts: `2 + 2*10` vs `"2 + 2*10"`, `'126'` vs 126, 11 vs 11.0.
- **"Input is a string, so cast it"** bug-fix moments: CS50P calculator, Helsinki birth-year/BMI.
- **Tiny output projects**: receipts, report cards, bill splitter.

### Cited Findings
- **MIT 6.100L L1, "YOU TRY IT!":** "In your console, find the type of: 1234, 8.99, 9.0, True, False". A second drill comes after casting: "find the type of: float(123), round(7.9), float(round(7.2)), int(7.2), int(7.9)". The slides also show `int(3.9)` "(note the truncation!)" and `round(3.9)` returning int 4. — [L1 slides](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/mit6_100l_f22_lec01.pdf)
- **py4e Ch.2, Exercise 4:** "Assume that we execute the following assignment statements: width = 17, height = 12.0. For each of the following expressions, write the value of the expression and the type (of the value of the expression): width//2, width/2.0, height/3, 1 + 2 * 5. Use the Python interpreter to check your answers." Exercise 5 is a Celsius-to-Fahrenheit converter that prompts the user. — [py4e Ch.2](https://www.py4e.com/html3/02-variables)
- **Helsinki 1.1:** contrasts `print(2 + 2 * 10)` with `print("2 + 2 * 10")`; the second "prints out the operation itself, as a string". — [1.1](https://programming-26.mooc.fi/part-1/1-getting-started)
- **Helsinki 1.3:** contrasts `number1 + number1` (int addition) with `number2 + number2` (string concatenation). It shows `TypeError: unsupported operand type(s) for /: 'str' and 'int'` and the fix `"The result is " + str(result)`. — [1.3](https://programming-26.mooc.fi/part-1/3-more-about-variables)
- **Helsinki 1.4:** casts input in the year-of-birth age calculator (`year = int(input("Which year were you born? "))`) and the BMI calculator (`float(input(...))`). — [1.4](https://programming-26.mooc.fi/part-1/4-arithmetic-operations)
- **CS50P Lecture 0 calculator:** the output "12" (from string concatenation) is shown as a bug. "Because your input… comes into the interpreter as text, it is treated as a string… we need to convert this input from a string to an integer", which leads to `int(x) + int(y)` and then `x = int(input("What's x? "))`. — [CS50P notes 0](https://cs50.harvard.edu/python/notes/0/)
- **CS50P Problem Set 0:** Indoor Voice, Playback Speed, Making Faces, Einstein, Tip Calculator. — [Problem Set 0](https://cs50.harvard.edu/python/psets/0/)
- **Think Python 3e §1.5:** shows the `'126'` trap (`'126' / 3` raises TypeError) and fixes it with `int()`. Exercise 1.9.2 asks the reader to work out `round`'s rule from `round(42.5)` → 42 and `round(43.5)` → 44. Section 1.9.1 suggests questions to ask a virtual assistant. — [Ch.1](https://allendowney.github.io/ThinkPython/chap01.html)
- **Hyperskill "Basic data types" theory:** contrasts `print(11)` with `print(11.0)` ("same number… the former is an integer, and the latter is a float"), shows `print('1234')` as a string of digits, and ends with `print(type('hello'))`. — [steps/5852](https://hyperskill.org/api/steps/5852)
- **freeCodeCamp "Build Your First Python Program"** (newest first block) has five steps:
  1. Type only the literal `'Hello'` in the editor.
  2. Learn it is a **string**, then wrap it as `print('Hello')`.
  3. `print('freeCodeCamp')`.
  4. `sentence = 'I am learning Python'`.
  5. `print(sentence)`.

  — [workshop-first-python-program steps](https://github.com/freeCodeCamp/freeCodeCamp/tree/main/curriculum/challenges/english/blocks/workshop-first-python-program)
- **freeCodeCamp's first practice workshops** after the data-types lecture: Report Card Printer, Employee Profile Generator, Employee Profile Validator, then Bill Splitter after the Numbers lecture. — [python-v9.json](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/superblocks/python-v9.json)
- **Codecademy's first projects:** Block Letters, and Receipts for Lovely Loveseats: "Use strings and numbers to save a catalog of furniture, then perform concatenation and math calculations to create a receipt." — [Codecademy syllabus](https://www.codecademy.com/learn/learn-python-3)
- **Exercism's first exercise** is Guido's Gorgeous Lasagna (concept "basics": variables, constants, functions, return, comments, docstrings). The next two exercises are Ghost Gobble Arcade Game (bools) and Currency Exchange (numbers). — [config.json](https://github.com/exercism/python/blob/main/config.json); [Lasagna intro](https://github.com/exercism/python/blob/main/exercises/concept/guidos-gorgeous-lasagna/.docs/introduction.md)

### Inferences
- The most reusable exercise patterns for a "recognize kinds of data" stage are:
  1. "Find or predict the type of this literal", with mixed int, float, str and bool, including look-alikes such as `9.0`, `'17'` and `True` (MIT, py4e).
  2. "Predict the value *and* type of an expression" (py4e Ex.4, Helsinki 2.1 table).
  3. "Same characters, different type, different behaviour": `2+2` vs `"2+2"`, `11` vs `11.0`, `+` on int vs str (Helsinki, Hyperskill, Think Python).
  4. "Why did this TypeError happen?" (Helsinki 1.3, Think Python §1.5).
  5. "Input is always text, so convert it" (CS50P, Helsinki 1.4).
- freeCodeCamp's step 1 (type a bare `'Hello'` literal before any `print`) is the closest existing precedent for a "data before statements" first lesson.

### Gaps
- Exact task statements for CS50P PS0 problems, ATBS 3e Ch.1 practice questions, Helsinki Part 1 exercises and Think Python 1.9.3–1.9.5 were not extracted.

---

## Q4. Explicit rationale authors give for their ordering

### Takeaway
Few authors justify where data types go. The rationales found are about pacing (MIT), being driven by what the application needs (py4e, freeCodeCamp's "learn each type when you first need it", CS50P introducing lists "to understand a for loop"), building programming vocabulary (Think Python), and why types matter (Helsinki, Hyperskill). The Python Tutorial and Google state outright that they are not for absolute beginners.

### Cited Findings
- **py4e (Severance):** "Number-oriented examples and exercises have been replaced with data-oriented exercises. Topics are presented in the order needed to build increasingly sophisticated data analysis solutions. Some topics like try and except are pulled forward… Functions are given very light treatment until they are needed to handle program complexity rather than introduced as an early lesson in abstraction." — [py4e preface source](https://github.com/csev/py4e/blob/master/book3/A0-preface.mkd)
- **Think Python 3e (Downey):** "In this chapter, we'll see how Python represents numbers, letters, and words… You will also start to learn the vocabulary of programming, including terms like operator, expression, value, and type. This vocabulary is important." — [Ch.1](https://allendowney.github.io/ThinkPython/chap01.html)
- **Think Python 3e preface:** "The first six chapters introduce basic elements like arithmetic, conditionals, and loops. They also introduce the most important concept in programming, functions… Chapters 9 through 12 introduce Python's core data structures – lists, dictionaries, and tuples". Also: "the sequence of topics is almost the same, but I rearranged a few of the chapters and compressed two short chapters into one", and "Each chapter… builds on the previous ones." — [Preface](https://allendowney.github.io/ThinkPython/chap00.html)
- **MIT 6.100L:** "The material covered is the same [as 6.0001], but the pace is slowed down. Our goal with this course is to give students who have never programmed the time to practice the concepts." — [Syllabus](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/syllabus/)
- **freeCodeCamp:** "For now, focus on four data types that you will use throughout this module… Python has other data types. You will learn each one when you first need it." This is an explicit just-in-time rationale. — [fCC data types lesson](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/challenges/english/blocks/lecture-understanding-variables-and-data-types/67fe859a00971c34a23abd43.md)
- **Helsinki:** "So, why does it matter that variables have a type…? Variable types matter because different operations affect different types of variables in different ways." — [1.3](https://programming-26.mooc.fi/part-1/3-more-about-variables)
- **Hyperskill:** "Every data object… has a type that describes how to keep it in memory, which operations can be applied to this object… A real-world analogy of types is given by biological species." — [steps/5852](https://hyperskill.org/api/steps/5852)
- **ATBS 3e:** "A data type is a category for values, and every value belongs to exactly one data type." — [Ch.1](https://automatetheboringstuff.com/3e/chapter1.html)
- **ATBS 3e changes:** the stated changes are about projects and topics (16 new projects, SQLite, PDF, Playwright, Whisper and others), not about reordering the fundamentals. — [Introduction](https://automatetheboringstuff.com/3e/chapter0.html)
- **CS50P:** "To best understand a for loop, it's best to begin by talking about a new variable type called a list". — [notes 2](https://cs50.harvard.edu/python/notes/2/)
- **Exercism:** "Concept Exercises are exercises designed to teach specific (programming) concepts. The concepts taught by the concept exercises form a syllabus", ordered through `prerequisites`. — [Exercism docs: concept exercises](https://github.com/exercism/docs/blob/main/building/tracks/concept-exercises.md)
- **Python Tutorial:** "designed for programmers that are new to the Python language, not beginners who are new to programming." — [Tutorial](https://docs.python.org/3/tutorial/index.html)
- **Google:** "geared for people who have a little bit of programming experience in some language, enough to know what a 'variable' or 'if statement' is." — [Google's Python Class](https://developers.google.com/edu/python)

### Inferences
- No mainstream course gives a pedagogical argument for a dedicated, extended "kinds of data and their characteristics" stage before statements and control flow. The existing rationales either favour just-in-time introduction (freeCodeCamp, CS50P, py4e) or treat types as vocabulary to be met briefly (Think Python, MIT).
- A platform that builds a fuller "recognize data" stage would therefore be filling a gap rather than copying a precedent. It can still borrow concrete pieces:
  - Hyperskill's species analogy
  - Helsinki's expression → value → type table
  - MIT's NoneType-as-scalar framing
  - freeCodeCamp's "literal before print" first step

### Gaps
- No explicit ordering rationale was found for CS50P as a whole, Codecademy, Real Python, Google or Helsinki beyond the quotes above. ATBS 3e's reasons for splitting Loops and Debugging into their own chapters were not stated in the fetched intro, and the 2nd-edition TOC was not fetched for comparison.
