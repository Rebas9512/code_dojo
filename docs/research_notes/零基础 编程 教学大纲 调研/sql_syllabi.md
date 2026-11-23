# Zero-background SQL / database syllabi: how beginner courses start (as of Nov 2026)

Research date: 2026-11-22. Scope: what beginner SQL courses teach before the first `SELECT`, the order of their first units, and the first exercises. The goal is to inform a "认识数据和表" starting stage for a PostgreSQL track built on a fixed "online bookstore" practice database.

Access notes: khanacademy.org (needs JavaScript), runoob.com (HTTP 521 / 16-byte responses on 2026-11-22), edX/Stanford Online/Class Central (403/404) could not be fetched directly. For those courses the findings come from secondary sources and are flagged as such.

---

## Q1. Unit order (first 8–12 units) and what the first 1–3 lessons cover, per course

### Takeaway
Two openings are common. In the first, a short concept intro ("what is a database / table / row / column") is followed immediately by `SELECT * FROM <one table>` on a ready-made dataset (CS50 SQL, SQLBolt, W3Schools, Select Star SQL, Mode/ThoughtSpot, 菜鸟). In the second, "build the table first", the learner meets CREATE TABLE and INSERT (and so data types) before querying (Khan Academy, Codecademy, PostgreSQL tutorial, NCRE 二级 MySQL). DataCamp's *Introduction to SQL* (refreshed Oct 2026) is the clearest example of a full **concept-only chapter before any query writing**. That chapter has 11 exercises on databases, tables, records/fields, unique IDs, naming and data types, all on a library database.

### Cited Findings

**Harvard CS50 SQL (CS50's Introduction to Databases with SQL)**
- Course weeks in the site navigation: 0 Querying, 1 Relating, 2 Designing, 3 Writing, 4 Viewing, 5 Optimizing, 6 Scaling, then Final Project. The navigation also has a "What's new for 2024?" link, and the dataset covers the 2018–2023 longlists. — [CS50 SQL Lecture 0 notes](https://cs50.harvard.edu/sql/notes/0/)
- Lecture 0 section order: Introduction → What is a Database? → SQL → Getting Started with SQLite → Terminal Tips → SELECT → LIMIT → WHERE → NULL → LIKE → Ranges → ORDER BY → Aggregate Functions → Fin. — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- Before the first query, the lecture covers these topics. A table stores related information, with each row one item and each column one attribute. The examples are an ancient temple worker-stipend table and a modern book-title table. It then covers why databases beat spreadsheets (scale, update frequency, speed of lookup) and defines a database as a way to organize data for CRUD. A DBMS is defined, with MySQL, Oracle, PostgreSQL, SQLite, Access and MongoDB as examples and cost, support and weight as selection factors. SQL is introduced as an ANSI/ISO standard that DBMSs implement in subsets. — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- The first queries, in order, are `SELECT * FROM "longlist";`, `SELECT "title" FROM "longlist";` and `SELECT "title", "author" FROM "longlist";`. — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- Week 1 (Relating) section order: Entity Relationship Diagrams → Keys (Primary Keys, Foreign Keys) → Subqueries → IN → JOIN → Sets → Groups. — [CS50 SQL notes 1](https://cs50.harvard.edu/sql/notes/1/)
- Week 2 (Designing) section order: Creating a Database Schema (Normalizing, Relating) → CREATE TABLE → Data Types and Storage Classes → Type Affinities → Adding Types to our Tables → Table Constraints → Column Constraints → Altering Tables. — [CS50 SQL notes 2](https://cs50.harvard.edu/sql/notes/2/)
- A CS50 Extension School offering (Spring 2025) of the SQL course exists with its own sections pages. — [CS50 Extension SQL 2025 Spring, section 0](https://cs50.harvard.edu/extension/sql/2025/spring/sections/0) (seen in search results only, not opened)

**Khan Academy: "Intro to SQL: Querying and managing data"** (official page could not be rendered; secondary sources)
- Five segments: (1) SQL basics: creating tables and selecting data in different ways; (2) More advanced SQL queries: AND/OR, IN, LIKE, HAVING; (3) Relational queries in SQL: related data across multiple tables, inner/outer/self joins; (4) Modifying databases with SQL: updating and deleting data, ALTER/DROP; (5) Further learning in SQL. OpenCourser says the course is about 2 hours and lists it as "discontinued". It is not clear whether that refers to Khan Academy itself or to the OpenCourser listing. — [OpenCourser listing](https://opencourser.com/course/829g5z/intro-to-sql-querying-and-managing-data); official URL [khanacademy.org/computing/computer-programming/sql](https://www.khanacademy.org/computing/computer-programming/sql) (would not load: "A required part of this site couldn't load")
- The SQL basics order is video/talk-through then challenge. "Creating a table and inserting data" leads to a challenge building a book database (id, name, rating). "Querying the table" leads to a box-office challenge (movies after 2000, sorted by year). "Aggregating data" leads to a TODO-list challenge using SUM. Each module ends with a project, and module 2's write-up is a store-database design project. — [Daniel Corcoran blog, 2016 write-up of Khan SQL basics](https://danielcorcoranssql.wordpress.com/2016/11/28/khan-academy-part-18-sql-basics/) (old third-party source)
- The "Challenge: Box office hits database" starter creates a `movies` table (id, name, release_year) and inserts six films, Avatar and Titanic among them. Learners select all movies, then movies from 2000 onward ordered by year. — [community solution repo (koyokowolf)](https://github.com/koyokowolf/KA-IntroToSQLChallengeSolutions/blob/master/Challenge:%20Box%20office%20hits%20database.sql); [KATRINAHIGH repo](https://github.com/KATRINAHIGH/sql-khan-academy-challenges/blob/master/challenge2_box_office.sql) (seen via search snippets)
- "Welcome to SQL" is also reused as the opener of Khan's Hour of Code "Hour of SQL". — [Khan Academy Hour of SQL: Welcome to SQL](https://en.khanacademy.org/computing/hour-of-code/hour-of-code-lessons/hour-of-sql/v/welcome-to-sql) (search result title only)

**SQLBolt**
- Full lesson order: Introduction to SQL → 1 SELECT queries 101 → 2 Queries with constraints (Pt. 1) → 3 Queries with constraints (Pt. 2) → 4 Filtering and sorting Query results → Review: Simple SELECT Queries → 6 Multi-table queries with JOINs → 7 OUTER JOINs → 8 A short note on NULLs → 9 Queries with expressions → 10–11 Queries with aggregates → 12 Order of execution of a Query → 13 Inserting rows → 14 Updating rows → 15 Deleting rows → 16 Creating tables → 17 Altering tables → 18 Dropping tables → X To infinity and beyond! It also has extra topics on subqueries and unions/intersections/exceptions. — [SQLBolt Introduction](https://sqlbolt.com/lesson/introduction)
- The intro page defines a relational database as "a collection of related (two-dimensional) tables". A table is like a spreadsheet with a fixed number of named columns (its attributes/properties) and any number of rows. The example is a DMV "Vehicles" table (Id, Make/Model, # Wheels, # Doors, Type) with five rows. Data types and primary keys are not discussed on the intro page. — [SQLBolt Introduction](https://sqlbolt.com/lesson/introduction)

**Stanford Databases (Jennifer Widom; StanfordOnline/edX "Databases: Relational Databases and SQL")** (official pages returned 403/404; secondary sources only)
- The material is now packaged as five self-paced edX courses. "Databases: Relational Databases and SQL" is the first and covers "the relational model and concepts in relational databases and relational database management systems" plus comprehensive SQL. Relational algebra sits in a separate course, "Databases: Modeling and Theory". — [edX: databases-1-introduction-to-relational-databases](https://edx.org/course/databases-1-introduction-to-relational-databases); [Class Central listing](https://classcentral.com/course/relational-databases-stanford-university-database-1006) (both from search-result summaries; not fetched)
- The original Lagunita platform was retired on March 31, 2020, and one edX listing marks the intro course as archived. — [s7oev/db GitHub notes](https://github.com/s7oev/db) (search snippet)

**DataCamp "Introduction to SQL"** (page dated 2026-10-16)
- Chapter 1 "Relational Databases" has 11 exercises: 1 Databases (video), 2 What is inside a database?, 3 Data organization, 4 Tables (video), 5 Picking a unique ID, 6 Table and field naming, 7 Our very own table, 8 Data types (video), 9 Understanding servers, 10 Finding data types, 11 Selecting data types. — [DataCamp campus, ch.1 ex.4](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=4)
- Chapter 2 "Querying": 1 Introducing queries (video), 2 SQL strengths, 3 Developing SQL style, 4 Querying the books table, 5 Writing queries (video), 6 Making queries DISTINCT, 7 Aliasing, 8 VIEWing your query, 9 SQL flavors (video), 10 Comparing flavors, 11 Limiting results, 12 Translating between flavors, 13 Congratulations!. — [DataCamp campus, ch.1 ex.4 (nav lists both chapters)](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=4)
- Course page facts: the chapter 1 description says it uses "a database for a local library" and covers database and table organization, data types and storage, and best practices. Chapter 2 uses a books database. Other facts listed:
  - datePublished 2026-10-16
  - ~2 hours, although one header says "30 min – 1 hr", which conflicts
  - rating 4.8 from 68,252 reviews
  - 1,626,692 historical enrollments
  - the visible outline also shows three "AI Tutor" lessons: "Meet Databases & SQL", "Write Your First SQL" and "Complete Your SQL Foundation"

  — [DataCamp course page](https://www.datacamp.com/courses/introduction-to-sql)

**Codecademy "Learn SQL"**
- Syllabus: 4 lessons, 5 projects and 4 quizzes, about 5 hours. The lessons are (1) Manipulation, "Learn how to use SQL to access, create, and update data stored in a database"; (2) Queries; (3) Aggregate Functions; (4) Multiple Tables, "creating and manipulating databases with multiple related tables". The named projects include "New York Restaurants" and "Analyze Hacker News Trends". Rating is 4.57 from 27,720, and the page footer reads © 2026. — [Codecademy Learn SQL](https://www.codecademy.com/learn/learn-sql)
- The Manipulation cheatsheet covers, in order: Column Constraints (PRIMARY KEY, UNIQUE, NOT NULL, DEFAULT), CREATE TABLE, INSERT (by column order and by column name), ALTER TABLE ... ADD COLUMN, DELETE ... WHERE, UPDATE ... SET ... WHERE. Its example table is `student` (id, name, grade, age). — [Codecademy Manipulation cheatsheet](https://www.codecademy.com/learn/learn-sql/modules/learn-sql-manipulation/cheatsheet)

**Select Star SQL** (free interactive book)
- Chapters: Front Matter → 1 Beazley's Last Statement (query structure, row operations) → 2 Claims of Innocence (whole-table aggregation) → 3 The Long Tail (group aggregation) → 4 Execution Hiatuses (joins) → 5 Closing Remarks and Challenge Questions. It targets readers with "little to no coding knowledge", with each chapter taking about 30 minutes. — [selectstarsql.com](https://selectstarsql.com/)
- Chapter 1 section order: The Beazley Case (narrative) → A First SQL Query → The SELECT Block (SQL Comments) → The FROM Block (Capitalization, Whitespace) → The WHERE Block (Quotes) → Recap. — [Select Star SQL ch.1](https://selectstarsql.com/beazley.html)

**Mode SQL Tutorial → now ThoughtSpot**
- `mode.com/sql-tutorial/introduction-to-sql` now returns 301 to `thoughtspot.com/sql-tutorial/introduction-to-sql`. That page is titled "SQL Tutorial for Data Analysis: Beginner's Guide (2026)". Its sections are Basic SQL (15 lessons), Intermediate SQL (20), SQL Analytics Training (8) and Advanced SQL (9). — [Mode URL (redirect)](https://mode.com/sql-tutorial/introduction-to-sql); [ThoughtSpot SQL tutorial intro](https://www.thoughtspot.com/sql-tutorial/introduction-to-sql)
- Intro content: a database is "an organized collection of data", and tables resemble spreadsheets but are stricter (each column has a unique name). Tables live in schemas tied to usernames, as in `databass3000.fish_food_sales`. SQL is compared to Excel pivot tables but works on larger data across tables. A sample table of 2010 Academy Awards data illustrates structure. — [ThoughtSpot SQL tutorial intro](https://www.thoughtspot.com/sql-tutorial/introduction-to-sql)

**W3Schools SQL tutorial**
- Navigation order: SQL Home → Intro → Syntax → Select → Select Distinct → Where → Order By → And → Or → Not → Insert Into → **Null Values** → Update → Delete → Select Top → Aggregate Functions (Min/Max/Count/Sum/Avg) → Like → Wildcards → In → Between → Aliases → Joins (Inner/Left/Right/Full/Self) → Union → Group By → Having → Exists → Any/All → Select Into → Insert Into Select → Case → Null Functions → Stored Procedures → Comments → Operators.
- A separate "SQL Database" section comes after that list: Create DB → Drop DB → Backup DB → **Create Table** → Drop Table → Alter Table → **Constraints → Not Null → Unique → Primary Key → Foreign Key** → Check → Default → Create Index → Auto Increment → Dates → Views → Injection → … SQL Data Types is under "SQL References".

  — [W3Schools SQL Intro](https://www.w3schools.com/sql/sql_intro.asp)
- The intro defines SQL (ANSI 1986, ISO 1987) and the RDBMS. Tables are made of columns (e.g. CustomerName) and records/rows, illustrated by the "Customers" table (CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country; 91 records). — [W3Schools SQL Intro](https://www.w3schools.com/sql/sql_intro.asp)

**PostgreSQL official tutorial (Docs Part I; "PostgreSQL 19.0 Documentation", 19 = current)**
- Part I contents:
  - Ch.1 Getting Started: 1.1 Installation, 1.2 Architectural Fundamentals, 1.3 Creating a Database, 1.4 Accessing a Database
  - Ch.2 The SQL Language: 2.1 Introduction, 2.2 Concepts, 2.3 Creating a New Table, 2.4 Populating a Table With Rows, 2.5 Querying a Table, 2.6 Joins Between Tables, 2.7 Aggregate Functions, 2.8 Updates, 2.9 Deletions
  - Ch.3 Advanced Features: Views, **Foreign Keys**, Transactions, Window Functions, Inheritance

  — [PostgreSQL docs: Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- Audience (preface): "We assume some general knowledge about how to use computers and no particular Unix or programming experience is required." — [PostgreSQL docs: Tutorial](https://www.postgresql.org/docs/current/tutorial.html)

**菜鸟教程 SQL / MySQL** (runoob.com returned HTTP 521 on 2026-11-22; findings from search-result summaries of runoob pages)
- The SQL tutorial basic part runs SQL 简介 → SQL 语法 → SELECT → SELECT DISTINCT → WHERE → AND & OR → ORDER BY → INSERT INTO → UPDATE → DELETE. The 高级教程 part then covers SELECT TOP, LIKE, 通配符, IN, BETWEEN, 别名, JOIN …, followed later by UNION, 视图, 约束, 日期, NULL 值 and 函数. — [runoob SQL quiz page (nav)](https://www.runoob.com/quiz/sql-quiz.html); [runoob.com/sql](https://www.runoob.com/sql) (search summary)
- Examples are tested on MySQL, using a downloadable `Websites` table in a `RUNOOB` database. The SQL 语法 page introduces the Websites table and the first SELECT. — [runoob SQL 语法](https://www.runoob.com/sql/sql-syntax.html) (search summary)

**全国计算机等级考试（NCRE）二级 MySQL 数据库程序设计 考试大纲（2025年版）** (PDF by NEEA, created 2024-12-27, hosted by 遵义师范学院继续教育学院)
- 基本要求: 1 掌握数据库的基本概念和方法；2 熟练掌握MySQL的安装与配置；3 熟练掌握MySQL平台下使用SQL语言实现数据库的交互操作；4 熟练掌握MySQL的数据库编程；5 熟悉PHP…；6 掌握MySQL数据库的管理与维护技术。
- 考试内容 order:
  - **一、基本概念与方法**: 1 数据库基础知识（基本概念；数据库系统的特点与结构；数据模型）；2 关系数据库、关系模型；3 数据库设计基础（设计步骤；关系数据库设计方法）；4 MySQL概述（系统特性与工作方式；MySQL编程基础：SQL、MySQL语言结构）
  - **二、MySQL平台下的SQL交互操作**:
    - 1 数据库（数据库对象概念；创建/选择/修改/删除/查看）
    - 2 数据表: (1) 数据表、表结构、表数据的基本概念与作用 → (2) 创建/更新/重命名/复制/删除/查看数据表 → (3) 插入/删除/更新表数据 → (4) 简单查询、聚合查询、连接查询、条件查询、嵌套查询、联合查询 → (5) 数据完整性约束的基本概念、分类与作用 → (6) 定义/命名/更新完整性约束
    - 3 索引；4 视图
  - 三、数据库编程（触发器、事件、存储过程和存储函数）
  - 四、管理与维护（服务器、用户账号、权限、备份与恢复、二进制日志）
  - 五、应用编程（PHP，B/S）
- Exam format: 上机 120 分钟; 单选 40 分 (含公共基础 10 分) + 操作题 60 分. Environment: WAMP 5.0+, MySQL 5.5.

  — [NCRE 二级 MySQL 大纲 2025年版 (PDF copy at yznu.edu.cn)](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/93fbb5d7-5fad-4868-a11d-a0b253751745.pdf)

### Inferences
- No course listed here opens with keys, NULL or relationships. Every one opens with "a database is a set of tables; a table is rows × named columns", then goes straight to one table.
- The split runs along audience lines. Analyst-oriented courses (CS50 week 0, SQLBolt, Select Star, Mode/ThoughtSpot, W3Schools, DataCamp ch.2) assume the data already exists and start with reading it. Developer- and exam-oriented ones (Codecademy, Khan, PostgreSQL tutorial, NCRE) start by defining a table's structure with CREATE TABLE and INSERT. For an adult beginner on a fixed bookstore DB, the reading-first ordering matches the setup better. DataCamp's concept chapter on a fixed library DB is the closest analogue to the planned "认识数据和表" stage.
- NCRE is a syllabus of exam content, not a lesson order. Even so, it explicitly puts "表、表结构、表数据的基本概念" before any SQL operation on tables, and puts 完整性约束 after queries.

### Gaps
- The Khan Academy lesson list and the content of its first talk-through came only from third-party and old sources, because khanacademy.org did not render. Its current status ("discontinued" per OpenCourser) is unconfirmed. I recall a "groceries" CREATE TABLE example (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER), but no fetched source confirmed it.
- Stanford/Widom: no official module list was retrievable (403/404). From memory, the course opens with "Introduction", "Relational Model" and "Querying Relational Databases" videos built on a college-admissions example (College/Student/Apply). This is unverified.
- Codecademy: the per-exercise content of lesson 1 (I recall a `celebs` table and an opening "Relational Databases" exercise) was not visible without login. Only the cheatsheet was verified.
- SQLBolt Lesson 1's dataset (I recall a `Movies` table) and Lesson 16's data-type list were not fetched.
- ThoughtSpot/Mode: individual Basic SQL lesson titles and the first dataset were not extractable from the page.
- 菜鸟教程: the MySQL tutorial order could not be retrieved because the site was down. SQL tutorial details come from search summaries, not the live page.
- NCRE: the 2025年版 is the latest I found. I did not check whether a 2026 revision exists on ncre.neea.edu.cn.

---

## Q2. How table, columns and data types, primary keys, NULL and relationships are introduced (before or after SELECT?), and with which datasets

### Takeaway
"Table = rows (records) + columns (fields)" always comes before SELECT. **Data types** come before SELECT only in DataCamp (VARCHAR/INT/NUMERIC + schema), Khan, Codecademy and PostgreSQL (via CREATE TABLE). CS50 defers them to week 2, and SQLBolt and W3Schools defer them to the end or the reference section. A **unique ID / key** comes before SELECT only in DataCamp ("Picking a unique ID") and in Codecademy's constraints. CS50 teaches PK/FK in week 1 together with JOIN. **NULL** is almost always taught after WHERE (CS50 week 0 after WHERE, W3Schools item 12, SQLBolt lesson 8, 菜鸟 高级). **Relationships / foreign keys** are taught with JOINs (CS50 week 1, SQLBolt 6, PostgreSQL 3.3). DataCamp is the exception: it shows that tables relate through shared columns in its first video, before any join.

### Cited Findings
- **DataCamp, video 1 "Databases"**: tables organize data into rows and columns, with each row a record and each column one attribute. Relational databases connect several tables through shared columns: "The card number column relates checkouts to patrons." Querying doesn't change stored data. The library dataset has three tables, `books`, `patrons` (card number, name, year joined, fines owed) and `checkouts` (linked by card number and book ID). — [DataCamp ch.1 ex.1](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=1)
- **DataCamp, video "Tables"** covers several points:
  - Table names should be clear, lowercase and use underscores.
  - "rows are often referred to as records and columns as fields".
  - "Each record contains the data for an individual observation", e.g. a patrons table with four records.
  - Unique identifiers: "Tables include a special field containing a unique identifier for each record, sometimes called a key… In the patrons table, the card_num field is the unique identifier… as opposed to the name field, because it's possible that two patrons might have the same name."
  - The video then moves on to "Multiple tables": several well-organized tables are often better than one.

  — [DataCamp ch.1 ex.4 "Tables"](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=4)
- **DataCamp, video "Data types"** covers strings, integers, floats and schemas:
  - Strings: a "string" is a sequence of characters, and VARCHAR is commonly used for its flexibility (patron names).
  - Integers: INT stores whole numbers from below −2 billion to above +2 billion (card_num).
  - Floats: NUMERIC stores numbers with a fractional part, up to 38 digits (Jasmin's $2.05 fine).
  - Schemas are "blueprints" that show tables, relationships and each field's data type. In the library schema, patrons relate to checkouts but not to books.

  — [DataCamp ch.1 ex.8 "Data types"](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=8)
- **CS50 SQL**: NULL appears in week 0 right after WHERE, before LIKE, ranges and ORDER BY. — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- **CS50 SQL week 1** uses books and authors to illustrate one-to-one, one-to-many and many-to-many relationships, and ER diagrams with crow's-foot notation. A primary key is "an identifier that is unique for every item in a table" (the ISBN example). A foreign key is a primary key from another table that links the two, and `authored` is a junction table for many-to-many. The `longlist.db` tables are books, authors, publishers, translators, ratings, authored and translated. — [CS50 SQL notes 1](https://cs50.harvard.edu/sql/notes/1/)
- **CS50 SQL week 2**: SQLite storage classes NULL, INTEGER, REAL, TEXT and BLOB, plus type affinities (TEXT, NUMERIC, INTEGER, REAL, BLOB; e.g. "25" inserted into an INTEGER column becomes 25). The lecture weighs integer vs text vs real for storing fares. Table constraints PRIMARY KEY and FOREIGN KEY; column constraints CHECK, DEFAULT, NOT NULL and UNIQUE. The dataset is MBTA (Boston subway) `mbta.db`. — [CS50 SQL notes 2](https://cs50.harvard.edu/sql/notes/2/)
- **CS50 dataset**: `longlist`, International Booker Prize longlisted books (13 per year, from Booker Prize site + Goodreads), with columns title, author, translator, format, year, rating, votes, pages and publisher. — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- **PostgreSQL 2.2 Concepts** (before any table is created): "Relation is essentially a mathematical term for table… Each table is a named collection of rows. Each row of a given table has the same set of named columns, and each column is of a specific data type. Whereas columns have a fixed order in each row, … SQL does not guarantee the order of the rows within the table in any way (although they can be explicitly sorted for display). Tables are grouped into databases, and a collection of databases managed by a single PostgreSQL server instance constitutes a database cluster." — [PostgreSQL docs 2.2](https://www.postgresql.org/docs/current/tutorial-concepts.html)
- **PostgreSQL 2.3**: the `weather` (city varchar(80), temp_lo int, temp_hi int, prcp real, date date) and `cities` (name varchar(80), location point) tables. varchar(80) "can store arbitrary character strings up to 80 characters", int "is the normal integer type", real is single-precision floating point, date "should be self-explanatory", and point is a PostgreSQL-specific type. `--` comments are explained here. NULL and primary keys are not mentioned in 2.3, and foreign keys wait until 3.3. — [PostgreSQL docs 2.3](https://www.postgresql.org/docs/current/tutorial-table.html); [Tutorial TOC](https://www.postgresql.org/docs/current/tutorial.html)
- **SQLBolt**: the intro covers table, rows and columns (Vehicles example). NULL comes only in Lesson 8, after JOINs. Table creation (where types and constraints would appear) comes in Lesson 16. — [SQLBolt Introduction](https://sqlbolt.com/lesson/introduction)
- **W3Schools**: tables, records and columns in the Intro (Customers table). NULL Values at item 12 (after INSERT INTO). Primary Key and Foreign Key are deep in the "SQL Database" section. Data Types appear only in the References. — [W3Schools SQL Intro](https://www.w3schools.com/sql/sql_intro.asp)
- **Codecademy**: column constraints (PRIMARY KEY, UNIQUE, NOT NULL, DEFAULT) and CREATE TABLE appear in lesson 1 "Manipulation", alongside INSERT, ALTER, UPDATE and DELETE (student table). — [Codecademy Manipulation cheatsheet](https://www.codecademy.com/learn/learn-sql/modules/learn-sql-manipulation/cheatsheet)
- **Select Star SQL**: no up-front definition of table, rows or types. The ch.1 recap only mentions string, numeric and boolean-valued columns, and NULL is not discussed in ch.1. Dataset: Texas death-row executions since 1976, from the Texas Department of Criminal Justice website (pre-1995 data partly hand-extracted from paper-document images). — [Select Star SQL ch.1](https://selectstarsql.com/beazley.html); [Front matter](https://selectstarsql.com/frontmatter.html)
- **Mode/ThoughtSpot**: the intro defines database, table (spreadsheet-like but stricter, with unique column names) and schema before any lesson. — [ThoughtSpot SQL tutorial intro](https://www.thoughtspot.com/sql-tutorial/introduction-to-sql)
- **NCRE**: 关系模型/数据模型 and 表结构 concepts come first; 数据完整性约束 (PK/FK/NOT NULL etc.) is listed after the query items. — [NCRE 二级 MySQL 大纲 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/93fbb5d7-5fad-4868-a11d-a0b253751745.pdf)

**Example datasets used at the start**

| Course | First dataset |
|---|---|
| CS50 SQL | International Booker Prize longlist (books) |
| DataCamp | Local library: books / patrons / checkouts |
| SQLBolt | DMV Vehicles (intro illustration) |
| W3Schools | Customers (91 rows) |
| PostgreSQL | weather + cities |
| Select Star | Texas executions |
| Codecademy | student table (cheatsheet) |
| Khan | book list / movies / TODO (challenges) |
| 菜鸟 | Websites table |
| Mode/ThoughtSpot | 2010 Academy Awards (illustration) |

Sources: see the per-course citations above.

### Inferences
- Book-themed data is common in the courses closest to this platform's setup (CS50, DataCamp, Khan's first challenge). An online-bookstore DB fits this convention well. DataCamp's library schema (books, patrons, checkouts, with card_num as key and VARCHAR/INT/NUMERIC) maps almost one-to-one onto a bookstore's books, customers and orders.
- These courses support a 认识数据和表 stage that covers database → table → row/record → column/field → each column has one type → one column uniquely identifies a row → tables link through shared columns (concept only). NULL and formal FK/JOIN mechanics would be deferred until after WHERE and JOIN respectively. That is the majority practice: CS50, SQLBolt, W3Schools and PostgreSQL all defer them.
- For PostgreSQL specifically, the official doc's beginner type set is varchar, int, real and date. For an adult bookstore context, text, integer, numeric (price), date/timestamp and boolean (e.g. in_stock) would be the natural five to show. DataCamp's "price 63.75 → which type?" item illustrates this exact choice.

### Gaps
- None of the fetched pages showed an introduction of **boolean** columns before SELECT. Select Star's ch.1 recap mentions boolean-valued columns only in passing.
- I did not verify how Khan's or Codecademy's first lesson explains types, because their lesson pages were not renderable.

---

## Q3. Which first exercises are used (reading a table by eye, predicting results, SELECT * first, etc.)

### Takeaway
The most "zero-background-friendly" sequence found is DataCamp's chapter 1. It opens with **non-coding multiple-choice items about the structure of a shown database**, then **running provided code (`SELECT * FROM books;`) without writing anything**, then type-picking questions. Only after that does the learner fill in `SELECT ___ FROM ___;`. The other courses make `SELECT *` (or a fill-in SELECT) the very first hands-on task. Khan and Codecademy instead have learners build a table themselves first.

### Cited Findings
- DataCamp ch.1 exercise prompts, in order:
  - "What is inside a database?": "What is a component of a database?" (multiple choice). — [ex.2](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=2)
  - "Data organization": "Understanding the organization of a database is an important first step when using SQL. Look at the database below. Which statement best describes its structure?" — [ex.3](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=3)
  - "Picking a unique ID": "A unique identifier distinguishes a record from others in the same table." The learner picks the best key for `books` (id, title, author, genre, pub_year). — [ex.5](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=5)
  - "Table and field naming": "Here are two versions of a table… Which table uses the correct naming format?" — [ex.6](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=6)
  - "Our very own table": "Run the code provided to explore what data books holds! You don't need to write anything new yet." The provided code is `SELECT * FROM books;`. — [ex.7](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=7)
  - "Understanding servers": choose the true statement about database storage (non-coding). — [ex.9](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=9)
  - "Finding data types": "You want to familiarize yourself with a new database by understanding the data type—such as VARCHAR, INT, or NUMERIC—corresponding to each field in a table. Where could you find this information?" The hint is that looking at values gives a clue, and the answer theme is the schema. — [ex.10 (embedded in ex.8 page data)](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=8)
  - "Selecting data types": "When creating a table, it's important to specify the appropriate data type for each field… Here is an example of a field: price 63.75. What data type would you specify for this field?" — [ex.11](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=11)
  - First query-writing exercise (ch.2 ex.4, "Querying the books table"): the scaffold is `-- Return all titles from the books table` / `SELECT ___ FROM ___;`, with "Feel free to explore books in the exercise." — [ch.2 ex.4](https://campus.datacamp.com/courses/introduction-to-sql/querying?ex=4)
- CS50 SQL: the first query typed is `SELECT * FROM "longlist";`, then single and multiple columns. Lecture sections are interleaved with "Questions" (student Q&A). — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- Select Star SQL: the first query is `SELECT * FROM executions LIMIT 3`, framed as "three Lego blocks: `SELECT *` `FROM executions` `LIMIT 3`… each block has a fixed format and the different blocks have to fit together in particular ways." The chapter has "Show Solution" exercises, a quick quiz, and ends with a project to retrieve Beazley's last statement using WHERE. — [Select Star SQL ch.1](https://selectstarsql.com/beazley.html)
- Select Star SQL's mental-model goal: "Learning to program is learning a mental model" so that after writing a query you can predict its output, and "Programming is best learnt by doing". — [Select Star SQL front matter](https://selectstarsql.com/frontmatter.html)
- Khan Academy: the first challenge after "Creating a table and inserting data" is to build a book list table (id, name, rating). Next comes "Querying the table" with a movies challenge (select all, then filter ≥ 2000 and order by year). — [Corcoran write-up](https://danielcorcoranssql.wordpress.com/2016/11/28/khan-academy-part-18-sql-basics/); [community solution](https://github.com/koyokowolf/KA-IntroToSQLChallengeSolutions/blob/master/Challenge:%20Box%20office%20hits%20database.sql)
- PostgreSQL tutorial: learners create `weather` and `cities` (2.3), insert rows (2.4), then query (2.5). — [PostgreSQL Tutorial TOC](https://www.postgresql.org/docs/current/tutorial.html); [2.3](https://www.postgresql.org/docs/current/tutorial-table.html)

### Inferences
- A beginner stage can be built from DataCamp's question types, swapped onto the bookstore DB, before any typed SQL:
  1. "Which statement describes this database's structure?"
  2. "Which column is the best unique ID for `books`?"
  3. "Which name follows the convention?"
  4. "Run this provided `SELECT * FROM books;` and look."
  5. "Where would you find each column's type?" (schema)
  6. "price 39.80 → which type?"

  Select Star's "predict the output" goal is a natural next step once SELECT begins.
- "Answer a question by reading the table by eye" and "predict the result rows" were not found as explicit exercise types in the fetched pages, though Select Star states prediction as the learning goal. These would be the platform's own additions, not copied practice.

### Gaps
- I could not confirm whether any course uses explicit "count the rows by eye" or "predict which rows come back" items before SELECT. Khan's and Codecademy's exercise texts were not accessible.
- I did not research SQLBolt's interactive exercise format beyond the lesson list (Lesson 1 content not fetched).

---

## Q4. Author rationale on ordering, and evidence for teaching "what is a table" before queries

### Takeaway
The only explicit rationale found for "concepts before queries" is DataCamp's chapter 1 description: "Before writing any SQL queries, it's important to understand the underlying data." It adds, "Understanding the organization of a database is an important first step when using SQL." Select Star SQL's author argues the other way, for learning by doing on a real dataset and building a predictive mental model. CS50 places "What is a Database?" before SELECT without stating a reason. No empirical study comparing these orderings was found.

### Cited Findings
- DataCamp ch.1 description: "Before writing any SQL queries, it's important to understand the underlying data. In this chapter, we'll discover the role of SQL in creating and querying relational databases. Using a database for a local library, we will explore database and table organization, data types and storage, and best practices for database construction." — [DataCamp campus ch.1](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=4)
- DataCamp ex.3 prompt: "Understanding the organization of a database is an important first step when using SQL." — [DataCamp ch.1 ex.3](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=3)
- DataCamp's first video states the two course goals in order: learn how databases store and organize data, then query it in Chapter 2. — [DataCamp ch.1 ex.1](https://campus.datacamp.com/courses/introduction-to-sql/relational-databases?ex=1)
- Select Star SQL rationale: "Programming is best learnt by doing". Most time should go to exercises the learner struggles with. "Learning to program is learning a mental model" so that one can predict a query's output. The exercises are "realistic and substantial", and the book adds techniques gradually on data people find interesting. It is not a reference page; "it conveys a mental model for writing SQL." — [Select Star SQL front matter](https://selectstarsql.com/frontmatter.html); [selectstarsql.com](https://selectstarsql.com/)
- Select Star SQL chapter progression: single-row operations → whole-table aggregation → group aggregation → joins (stated in chapter descriptions). — [selectstarsql.com](https://selectstarsql.com/)
- CS50 SQL motivates databases against spreadsheets on scale, update frequency and lookup speed before SQL syntax. — [CS50 SQL notes 0](https://cs50.harvard.edu/sql/notes/0/)
- Mode/ThoughtSpot motivates SQL for analysts: easy to understand, queries data where it lives, and is more auditable and repeatable than spreadsheet formulas. — [ThoughtSpot SQL tutorial intro](https://www.thoughtspot.com/sql-tutorial/introduction-to-sql)
- PostgreSQL tutorial's stated purpose: "to give an introduction to PostgreSQL, relational database concepts, and the SQL language". It puts a short Concepts section (2.2) before table creation and querying. — [PostgreSQL docs: Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- NCRE 2025 lists "基本概念与方法" (数据库基础知识, 关系模型, 数据库设计基础) as the first content block, ahead of all SQL operations. — [NCRE 二级 MySQL 大纲 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/93fbb5d7-5fad-4868-a11d-a0b253751745.pdf)

### Inferences
- The current mainstream practice, as of the Oct 2026 DataCamp refresh, is a short, interactive, non-coding orientation to the data itself before typing SQL. It stays short (DataCamp ch.1 has 3 short videos and 8 quick items) and still lets the learner run a provided `SELECT *` to see real rows. Combined with Select Star's "learn by doing, predict output" stance, this suggests a "认识数据和表" stage that is brief, tied to the actual bookstore tables, and quickly handed over to SELECT.
- Deferring NULL and foreign keys is consistent across courses. Introducing them conceptually in the first stage would go against every course found, so the evidence favours only a light preview ("some cells can be empty"; "orders point to customers by customer_id").

### Gaps
- No peer-reviewed or empirical evidence was found on whether teaching "what is a table" before queries improves beginner outcomes. I did not run a dedicated academic-literature search (e.g. SIGCSE papers on SQL misconceptions) within this task's budget, so that is a recommended follow-up.
- No explicit ordering rationale from CS50 (Carter Zenke / David Malan), SQLBolt, W3Schools, Khan or Codecademy authors was found on the fetched pages.
