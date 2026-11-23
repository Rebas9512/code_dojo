# Mainstream General-Purpose Coding-Interview Problem Lists (state as of 2026-11-22)

> **How the data was gathered.** Wherever possible, counts come from the live data the official sites serve. They were retrieved on **2026-11-22** and tallied by the researcher. They are not taken from third-party summaries.
> - **NeetCode:** the problem objects in neetcode.io's front-end bundle (`https://neetcode.io/main.d3bcb00a2330ecc4.js`, loaded by [neetcode.io/practice](https://neetcode.io/practice)). There are 1,127 problem objects with flags `blind75`, `neetcode150`, `neetcode250`, `premiumAlgo100` and `pro`.
> - **Grind 75 / 169:** the question JSON embedded in the Grind 75 page's JS chunk (`/grind75/_next/static/chunks/c5797dfbd9aea01f.js` on [techinterviewhandbook.org/grind75](https://www.techinterviewhandbook.org/grind75)). The default 75 were reproduced by running the site's own selection algorithm, as described under Q1.
> - **LeetCode study plans:** LeetCode's public GraphQL `studyPlanV2Detail` query, the same data the [study plan pages](https://leetcode.com/studyplan/top-interview-150/) render.
> - **LeetCode metadata (difficulty, `paidOnly`):** LeetCode's `questionList` GraphQL, which reports **4,123 problems** in total ([leetcode.com/problemset](https://leetcode.com/problemset/)).
> - **Overlaps:** computed by exact LeetCode slug matching.

---

## Q1. Which lists are current in 2025–2026, and what are their exact counts, topic mixes, difficulty mixes, maintainers, update dates and premium status?

### Takeaway
All of the major lists are still live in November 2026.

**Algorithms lists:**

| List | Problems | Easy / Medium / Hard | Notes |
|---|---|---|---|
| Blind 75 | 75 | 19 / 49 / 7 | 6 are LeetCode Premium |
| NeetCode 150 | 150 | 28 / 101 / 21 | 7 premium; contains all of Blind 75 |
| NeetCode 250 | 250 | 60 / 155 / 35 | 7 premium; contains all of NeetCode 150; launched 2024-12-29 |
| Grind 75 (default) | 75 | 24 / 42 / 9 | 0 premium |
| Grind 169 (full set) | 169 | 41 / 102 / 26 | 12 premium |
| LeetCode 75 | 75 | 22 / 53 / 0 | 0 premium |
| Top Interview 150 | 150 | 39 / 93 / 18 | 0 premium |
| Top 100 Liked | 100 | 20 / 68 / 12 | 0 premium |

**SQL / pandas lists:**

| List | Problems | Easy / Medium / Hard | Notes |
|---|---|---|---|
| SQL 50 | 50 | 32 / 17 / 1 | 0 premium |
| Introduction to Pandas | 15 | 15 / 0 / 0 | 0 premium |
| 30 Days of Pandas | 33 | 25 / 8 / 0 | 5 premium |

The only significant new list in 2025–2026 is NeetCode 250, plus the growth of "NeetCode All", which went from 584 to 793 problems in March 2025 and is now 1,127. Grind 75 has not changed since 2022, according to its own changelog.

### Cited Findings

**Blind 75**
- **Origin:** posted on Blind on **Dec 30, 2018**, titled "New Year Gift - Curated List of Top 75 LeetCode Questions to Save Your Time". The author's flair was a Facebook tech lead ([Teamblind best of Dec 2018](https://www.teamblind.com/best/2018/december)). The widely used LeetCode Discuss repost is [leetcode.com/discuss/post/460599](https://leetcode.com/discuss/post/460599/blind-75-leetcode-questions-by-krishnade-9xev/).
- **Author:** Yangshun Tay. The Tech Interview Handbook says: "I'm Yangshun, an ex-Meta Staff Engineer, author of this handbook and Blind 75" ([TIH best practice questions](https://www.techinterviewhandbook.org/best-practice-questions/), page "Last updated on Aug 7, 2026").
- **Difficulty:** 19 Easy, 49 Medium, 7 Hard ([neetcode.io/practice](https://neetcode.io/practice), researcher tally). AlgoMind independently reports 75 problems, "10 topics" in the original grouping, and 6 needing Premium ([AlgoMind, 2026-10-30](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)).
- **Premium problems (6):** encode-and-decode-strings, graph-valid-tree, number-of-connected-components-in-an-undirected-graph, alien-dictionary, meeting-rooms, meeting-rooms-ii ([LeetCode problemset](https://leetcode.com/problemset/)). NeetCode hosts free versions of these on its own site ([neetcode.io/practice](https://neetcode.io/practice)).
- **Breakdown by NeetCode pattern** (Easy/Medium/Hard per pattern) ([neetcode.io/practice](https://neetcode.io/practice)):

  | Pattern | Total | E / M / H |
  |---|---|---|
  | Arrays & Hashing | 8 | 3 / 5 / 0 |
  | Two Pointers | 3 | 1 / 2 / 0 |
  | Sliding Window | 4 | 1 / 2 / 1 |
  | Stack | 1 | 1 / 0 / 0 |
  | Binary Search | 2 | 0 / 2 / 0 |
  | Linked List | 6 | 3 / 2 / 1 |
  | Trees | 11 | 4 / 5 / 2 |
  | Heap | 1 | 0 / 0 / 1 |
  | Backtracking | 2 | 0 / 2 / 0 |
  | Tries | 3 | 0 / 2 / 1 |
  | Graphs | 6 | 0 / 6 / 0 |
  | Advanced Graphs | 1 | 0 / 0 / 1 |
  | 1-D DP | 10 | 1 / 9 / 0 |
  | 2-D DP | 2 | 0 / 2 / 0 |
  | Greedy | 2 | 0 / 2 / 0 |
  | Intervals | 5 | 1 / 4 / 0 |
  | Math & Geometry | 3 | 0 / 3 / 0 |
  | Bit Manipulation | 5 | 4 / 1 / 0 |

- **Thin areas:** Stack, Heap and Backtracking are under-represented (1, 1 and 2 problems). AlgoMind makes the same comparison against NeetCode 150: Stack 1 vs 6, Heap 1 vs 7, Backtracking 2 vs 10, Binary Search 2 vs 7, Advanced Graphs 1 vs 6, 2-D DP 2 vs 11 ([AlgoMind](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)).
- **The author's distilled 50:** Yangshun later "further distilled the list down into only 50 questions and spread them across a 5-week schedule" ([TIH best practice questions](https://www.techinterviewhandbook.org/best-practice-questions/)). The weeks are:
  - Week 1, Sequences: 10 questions + 2 optional
  - Week 2, Data structures: 11
  - Week 3, Non-linear data structures: 9 + 4 optional
  - Week 4, More data structures: 10 + 5 optional
  - Week 5, Dynamic programming: 10

**NeetCode 150**
- **Size and difficulty:** 150 problems, 28 Easy / 101 Medium / 21 Hard, in 18 patterns ([neetcode.io/practice](https://neetcode.io/practice)). AlgoMind reports the same 28/101/21 ([AlgoMind](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)).
- **Breakdown by pattern** ([neetcode.io/practice](https://neetcode.io/practice)):

  | Pattern | Total | E / M / H |
  |---|---|---|
  | Arrays & Hashing | 9 | 3 / 6 / 0 |
  | Two Pointers | 5 | 1 / 3 / 1 |
  | Sliding Window | 6 | 1 / 3 / 2 |
  | Stack | 6 | 1 / 4 / 1 |
  | Binary Search | 7 | 1 / 5 / 1 |
  | Linked List | 11 | 3 / 6 / 2 |
  | Trees | 15 | 6 / 7 / 2 |
  | Heap / Priority Queue | 7 | 2 / 4 / 1 |
  | Backtracking | 10 | 0 / 9 / 1 |
  | Tries | 3 | 0 / 2 / 1 |
  | Graphs | 13 | 0 / 12 / 1 |
  | Advanced Graphs | 6 | 0 / 3 / 3 |
  | 1-D DP | 12 | 2 / 10 / 0 |
  | 2-D DP | 11 | 0 / 7 / 4 |
  | Greedy | 8 | 0 / 8 / 0 |
  | Intervals | 6 | 1 / 4 / 1 |
  | Math & Geometry | 8 | 2 / 6 / 0 |
  | Bit Manipulation | 7 | 5 / 2 / 0 |

- **Premium on LeetCode (7):** the 6 Blind 75 premium problems plus walls-and-gates ([LeetCode problemset](https://leetcode.com/problemset/)). None is flagged NeetCode `pro`, so all 150 are free to practise on neetcode.io ([neetcode.io/practice](https://neetcode.io/practice)).
- **Maintainer:** NeetCode (neetcode.io, @neetcode1 on X). The open-source solutions repo [neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode) is MIT-licensed and was last pushed 2026-11-16. Its `.problemSiteData.json` (450 problems) carries only the `blind75` and `neetcode150` flags, not `neetcode250`. That file was last changed 2025-08-03 ([GitHub commits](https://github.com/neetcode-gh/leetcode/commits/main/.problemSiteData.json)).

**NeetCode 250 (new since late 2024)**
- **Launch:** announced by NeetCode on X on **2024-12-29**: "It's almost 2025 and tech companies are still asking LeetCode style interview questions. So I just added a new list of problems … 🦄 NeetCode 250. This list is very beginner friendly. Each topic has a few extra easy problems." ([X post](https://x.com/neetcode1/status/1873322718013362516); the date is decoded from the tweet ID).
- **Official description:** "The Neetcode 250 is the Neetcode 150 plus 100 more problems. It's the most beginner friendly list, intended for people completely new to algorithms" ([neetcode.io/practice/practice/neetcode250](https://neetcode.io/practice/practice/neetcode250), as quoted in [ShiveshK09/NeetCode250](https://github.com/ShiveshK09/NeetCode250)).
- **Size and difficulty:** 250 problems, 60 Easy / 155 Medium / 35 Hard. The 100 problems added on top of NeetCode 150 are 32 Easy / 54 Medium / 14 Hard ([neetcode.io/practice](https://neetcode.io/practice)).
- **Breakdown by pattern** ([neetcode.io/practice](https://neetcode.io/practice)):

  | Pattern | Total | E / M / H |
  |---|---|---|
  | Arrays & Hashing | 22 | 9 / 12 / 1 |
  | Two Pointers | 13 | 6 / 6 / 1 |
  | Sliding Window | 9 | 2 / 5 / 2 |
  | Stack | 14 | 4 / 8 / 2 |
  | Binary Search | 14 | 4 / 7 / 3 |
  | Linked List | 14 | 3 / 8 / 3 |
  | Trees | 23 | 9 / 12 / 2 |
  | Heap | 12 | 2 / 8 / 2 |
  | Backtracking | 17 | 1 / 13 / 3 |
  | Tries | 4 | 0 / 3 / 1 |
  | Graphs | 21 | 3 / 17 / 1 |
  | Advanced Graphs | 10 | 0 / 4 / 6 |
  | 1-D DP | 17 | 3 / 13 / 1 |
  | 2-D DP | 16 | 0 / 12 / 4 |
  | Greedy | 14 | 1 / 12 / 1 |
  | Intervals | 7 | 1 / 4 / 2 |
  | Math & Geometry | 13 | 6 / 7 / 0 |
  | Bit Manipulation | 10 | 6 / 4 / 0 |

- **Premium:** 7 are LeetCode Premium, the same 7 as in NeetCode 150; none of the 100 additions is premium. 0 are NeetCode-`pro`-locked ([neetcode.io/practice](https://neetcode.io/practice)).
- **NeetCode's later recommendation (2025-03-30):** "For most people, I would recommend just going through the NeetCode 150 or even better, the NeetCode 250 to learn the main patterns. After that, you can probably solve problems at random from the All list." The same post announced "NeetCode All" growing from 584 to 793 problems ([X post](https://x.com/neetcode1/status/1906204613583544625)).

**Other NeetCode lists in the live site code (Nov 2026)**
- **List names in the code:** "🧠 Blind 75", "🚀 NeetCode 150", "🦄 NeetCode 250", "🌎 NeetCode All", "📚 Core Skills" (`coreSkills`), "🌸 System Design", and a `companyTagged` mode ([neetcode.io/practice](https://neetcode.io/practice); also [Core Skills page](https://neetcode.io/practice/practice/coreSkills)).
- **NeetCode All:** now 1,127 problems. 309 carry a `pro` flag, meaning they are locked behind NeetCode Pro. 1,097 have a NeetCode-hosted problem page (`ncLink`) ([neetcode.io/practice](https://neetcode.io/practice)).
- **Unlabelled `premiumAlgo100` flag:** marks 100 problems, of which 99 are LeetCode-Premium problems and 93 are NeetCode-Pro-locked; difficulty 20 Easy / 63 Medium / 17 Hard ([neetcode.io/practice](https://neetcode.io/practice)). This looks like a paid "premium problems" set, but no public label was found (see Gaps).

**Grind 75 / Grind 169**
- **Positioning:** "A better Blind 75 you can customize, by the author of Blind 75" ([techinterviewhandbook.org/grind75](https://www.techinterviewhandbook.org/grind75)).
- **How it was built, per the About page:** "I looked at all the top LeetCode questions (by popularity, frequency, topics covered, like rating) and picked the top 169 questions … assigned a priority … selected the top 75 to be the new Blind 75." Also: "No premium questions in the initial list of 75" and "You probably don't need to do beyond the 169 questions." Credits go to AlgoMonster, Sean Prashad's LeetCode Patterns, Elements of Programming Interviews and LeetCode ([Grind 75 About](https://www.techinterviewhandbook.org/grind75/about)).
- **Design rationale (FAQ):** Easy problems come first, Hard problems get lower priority, and Premium problems are pushed "as far back as possible". The list mixes topics across weeks on purpose, for spaced repetition ([Grind 75 FAQ](https://www.techinterviewhandbook.org/grind75/faq)).
- **Last change:** the changelog's newest entry is **2022/09/11**, "Changed difficulty of 'Maximum Subarray' to 'Medium'". Earlier entries are 2022/07/03, 2022/05/02 and 2022/05/01. On 2022/05/01 the default order was changed to "by Difficulty" ([Grind 75 Changelog](https://www.techinterviewhandbook.org/grind75/changelog)). **The list content is therefore pre-2025 (2022) and unchanged.**
- **Grind 169 full set:** 41 Easy / 102 Medium / 26 Hard, 12 premium ([techinterviewhandbook.org/grind75](https://www.techinterviewhandbook.org/grind75)). The premium titles are Meeting Rooms, Shortest Path to Get Food, Graph Valid Tree, Inorder Successor in BST, Number of Connected Components, Minimum Knight Moves, Design In-Memory File System, Employee Free Time, Design Hit Counter, Alien Dictionary, Meeting Rooms II, and Encode and Decode Strings.
  - Grind's own topic tags: array 24, graph 21, binary-tree 18, stack 14, linked-list 14, string 14, dynamic-programming 12, binary-search 8, heap 8, binary 7, recursion 6, binary-search-tree 5, matrix 5, math 5, trie 4, hash-table 3, queue 1.
- **Default Grind 75 (8 weeks × 8 h/week):** reproduced with the site's own code. The code sorts questions by `priority`, then adds them while the budget 60 × 64 min minus Σ(1.96 × duration) stays non-negative, then orders by difficulty ([Grind 75 page JS](https://www.techinterviewhandbook.org/grind75)). The result:
  - 24 Easy / 42 Medium / 9 Hard, 0 premium.
  - Topics: array 11, graph 10, binary-tree 9, string 8, stack 7, linked-list 5, binary-search 5, dynamic-programming 5, heap 4, binary-search-tree 3, recursion 3, trie 2, hash-table 1, binary 1, matrix 1.
  - AlgoMind independently reports the same 24/42/9 default and "26 weeks at 40 hours a week, which covers all 169" ([AlgoMind](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)).
- **Default week grouping (useful as a ready-made progressive order):**
  - **W1 (13):** Two Sum, Valid Parentheses, Merge Two Sorted Lists, Best Time to Buy and Sell Stock, Valid Palindrome, Invert Binary Tree, Valid Anagram, Binary Search, Flood Fill, LCA of BST, Balanced Binary Tree, Linked List Cycle, Implement Queue using Stacks.
  - **W2 (12):** First Bad Version, Ransom Note, Climbing Stairs, Longest Palindrome, Reverse Linked List, Majority Element, Add Binary, Diameter of Binary Tree, Middle of the Linked List, Maximum Depth of Binary Tree, Contains Duplicate, Maximum Subarray.
  - **W3 (8):** Insert Interval, 01 Matrix, K Closest Points to Origin, Longest Substring Without Repeating Characters, 3Sum, Binary Tree Level Order Traversal, Clone Graph, Evaluate Reverse Polish Notation.
  - **W4 (8):** Course Schedule, Implement Trie, Coin Change, Product of Array Except Self, Min Stack, Validate BST, Number of Islands, Rotting Oranges.
  - **W5 (8):** Search in Rotated Sorted Array, Combination Sum, Permutations, Merge Intervals, LCA of Binary Tree, Time Based Key-Value Store, Accounts Merge, Sort Colors.
  - **W6 (9):** Word Break, Partition Equal Subset Sum, String to Integer (atoi), Spiral Matrix, Subsets, Binary Tree Right Side View, Longest Palindromic Substring, Unique Paths, Construct Binary Tree from Preorder and Inorder.
  - **W7 (7):** Container With Most Water, Letter Combinations of a Phone Number, Word Search, Find All Anagrams in a String, Minimum Height Trees, Task Scheduler, LRU Cache.
  - **W8 (10):** Kth Smallest Element in a BST, Minimum Window Substring, Serialize and Deserialize Binary Tree, Trapping Rain Water, Find Median from Data Stream, Word Ladder, Basic Calculator, Maximum Profit in Job Scheduling, Merge k Sorted Lists, Largest Rectangle in Histogram.
- **Licensing:** the Grind 75 site is "© 2026 Tech Interview Handbook. All rights reserved" ([Grind 75 Changelog](https://www.techinterviewhandbook.org/grind75/changelog)). Its question data was not found in the MIT-licensed [yangshun/tech-interview-handbook](https://github.com/yangshun/tech-interview-handbook) repo tree, which was last pushed 2026-08-07.

**LeetCode official study plans (maintained by LeetCode)**
- **LeetCode 75** ([leetcode.com/studyplan/leetcode-75](https://leetcode.com/studyplan/leetcode-75/)): "75 Essential & Trending Problems … Best for 1~3 month of prep time".
  - 22 Easy / 53 Medium / **0 Hard**, 0 premium.
  - 22 sections, in order: Array/String 9, Two Pointers 4, Sliding Window 4, Prefix Sum 2, Hash Map/Set 4, Stack 3, Queue 2, Linked List 4, Binary Tree DFS 6, Binary Tree BFS 2, BST 2, Graphs DFS 4, Graphs BFS 2, Heap/PQ 4, Binary Search 4, Backtracking 2, DP 1D 4, DP Multidimensional 4, Bit Manipulation 3, Trie 2, Intervals 2, Monotonic Stack 2.
  - Originally announced on LeetCode Discuss as "🆕 Study Plan - 75 Questions till Interview Ready" ([LeetCode Discuss 2163754](https://leetcode.com/discuss/post/2163754/new-study-plan-75-questions-till-interview-ready/)); no launch date was confirmed.
- **Top Interview 150** ([leetcode.com/studyplan/top-interview-150](https://leetcode.com/studyplan/top-interview-150/)): "150 Original & Classic Questions … Best for 3+ months of prep time … Problems support high-quality editorials".
  - 39 Easy / 93 Medium / 18 Hard, 0 premium.
  - 23 sections: Array/String 24, Two Pointers 5, Sliding Window 4, Matrix 5, Hashmap 9, Intervals 4, Stack 5, Linked List 11, Binary Tree General 14, Binary Tree BFS 4, BST 3, Graph General 6, Graph BFS 3, Trie 3, Backtracking 7, Divide & Conquer 4, Kadane's 2, Binary Search 7, Heap 4, Bit Manipulation 6, Math 6, 1D DP 5, Multidimensional DP 9.
- **Top 100 Liked** ([leetcode.com/studyplan/top-100-liked](https://leetcode.com/studyplan/top-100-liked/)): "100 most liked problems by LeetCoders".
  - 20 Easy / 68 Medium / 12 Hard, 0 premium.
  - 15 sections: Backtracking 8, Binary Search 7, Binary Tree 14, DP 15, Graph 3, Greedy 4, Hashing 4, Heap 3, Linked Lists 14, Matrix 4, Sliding Window 4, Stack 5, Two Pointers 4, Trie 1, Misc 10.
- **SQL 50** ([leetcode.com/studyplan/top-sql-50](https://leetcode.com/studyplan/top-sql-50/)): "Basic to intermediate SQL topics … Best for 1 month of prep time".
  - 32 Easy / 17 Medium / 1 Hard, 0 premium.
  - 7 sections, each listed with its E/M/H split and LeetCode problem IDs:
    - **Select** (5; 5/0/0): 1757, 584, 595, 1148, 1683.
    - **Basic Joins** (9; 7/2/0): 1378, 1068, 1581, 197, 1661, 577, 1280, 570 (M), 1934 (M).
    - **Basic Aggregate Functions** (8; 5/3/0): 620, 1251, 1075, 1633, 1211, 1193 (M), 1174 (M), 550 (M).
    - **Sorting and Grouping** (7; 5/2/0): 2356, 1141, 1070 (M), 596, 1729, 619, 1045 (M).
    - **Advanced Select and Joins** (7; 3/4/0): 1731, 1789, 610, 180 (M), 1164 (M), 1204 (M), 1907 (M).
    - **Subqueries** (7; 1/5/1): 1978, 626 (M), 1341 (M), 1321 (M), 602 (M), 585 (M), 185 Department Top Three Salaries (H, the only Hard).
    - **Advanced String Functions / Regex / Clause** (7; 6/1/0): 1667, 1527, 196, 176 (M), 1484, 1327, 1517.
  - A third-party summary gave about 64% Easy / 34% Medium / 2% Hard, which matches 32/17/1 ([Scribd summary](https://www.scribd.com/document/746335033/1-Leetcode-SQL-50-Challenge)).
- **Introduction to Pandas** ([leetcode.com/studyplan/introduction-to-pandas](https://leetcode.com/studyplan/introduction-to-pandas/)): "Learn Basic Pandas in 15 Qs … Designed for absolute beginners".
  - 15 problems, all Easy, 0 premium; IDs 2877–2891.
  - Sections: Data Structures 1, Inspection 2, Selecting 2, Cleaning 6, Reshaping 3 (concat/pivot/melt), Method Chaining 1.
- **30 Days of Pandas** ([leetcode.com/studyplan/30-days-of-pandas](https://leetcode.com/studyplan/30-days-of-pandas/)): "Essential for pandas Interviews".
  - **33** problems (30 + 3 "Strengthen Your Learning" items), 25 Easy / 8 Medium.
  - **5 premium:** 2738 Count Occurrences in Text, 2082 The Number of Rich Customers, 1173 Immediate Food Delivery I, 1322 Ads Performance, 2041 Accepted Candidates From the Interviews.
  - Sections: Data Filtering 4, String Methods 5, Data Manipulation 6, Statistics 3, Data Aggregation 7, Data Integration 5.

**Other lists that appear in 2025–2026 comparisons**
- **Sean Prashad's LeetCode Patterns** ([seanprashad/leetcode-patterns](https://github.com/seanprashad/leetcode-patterns)): **179** problems, 41 Easy / 112 Medium / 26 Hard, 13 premium. It contains all of Blind 75. Its `questions.json` is refreshed automatically by a cron workflow (`updated: 2026-11-22`); the repo license is listed as NOASSERTION ([questions.json](https://raw.githubusercontent.com/seanprashad/leetcode-patterns/main/src/data/questions.json)).
- **Striver A2Z** (popular mainly in India): "495 items in 20 modules, some of them theory lessons", about 131.4 hours. Striver's shorter sheets have 75, 150 and 180 items ([AlgoMind, 2026-10-30](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)).
- **Size of LeetCode itself:** 4,123 problems as of 2026-11-22 ([LeetCode problemset](https://leetcode.com/problemset/)).

### Inferences
- **NeetCode lists are pure supersets** (Blind 75 ⊂ NC150 ⊂ NC250), and the 100 added for NC250 are free and Easy-heavy (32 E). That makes NC250 the most natural single backbone for a learner restarting from beginner level, since its categories already follow the stage sequence the platform wants.
- **LeetCode 75 has no Hard problems** and is internally progressive (22 small sections). It works as an on-ramp, but it is a weak interview-coverage list (see Q4).
- **Grind 75's content is frozen at 2022.** Its value is the priority/duration metadata and the week-by-week mixed ordering, not freshness.
- **SQL 50 is the only mainstream curated SQL list from an official source,** and its 7 sections are already progressive. 30 Days of Pandas shares 16 of its 33 problems with SQL 50 (researcher tally by problem ID), so a pandas track can reuse SQL 50 problems.

### Gaps
- **NeetCode 250 changes since launch:** no official changelog was found, and the counts above reflect the live bundle on 2026-11-22.
- **What `premiumAlgo100` is:** no public label was found in the site code.
- **Launch and update dates of the LeetCode study plans** (LeetCode 75, Top Interview 150, Top 100 Liked, SQL 50, Pandas plans): not found. The API shows no "last updated" field. They are widely referenced since about 2023, but no primary source was confirmed.
- **The "Core Skills" list contents:** not retrieved.

---

## Q2. How much do the lists overlap?

### Takeaway
- **Nesting:** Blind 75 ⊂ NeetCode 150 ⊂ NeetCode 250, and Grind 75 ⊂ Grind 169 (all exact).
- **Across families, overlap is moderate:**
  - Grind 75 ∩ Blind 75 = 40
  - NC150 ∩ Top Interview 150 = 77
  - NC250 ∩ Top Interview 150 = 102
  - Grind 169 ∩ NC250 = 122
- **LeetCode 75 is the outlier:** it shares only 10 problems with Blind 75, and 37 of its 75 problems appear in none of NC250, Grind 169 or Top Interview 150.
- **Size of the union:** all the major algorithm lists combined contain 375 unique problems.

### Cited Findings

**Pairwise overlap |A∩B|** (researcher computation by LeetCode slug from [neetcode.io/practice](https://neetcode.io/practice), [techinterviewhandbook.org/grind75](https://www.techinterviewhandbook.org/grind75), and [LeetCode study plans](https://leetcode.com/studyplan/top-interview-150/)):

| | B75 | NC150 | NC250 | G75 | G169 | LC75 | TI150 | T100L |
|---|---|---|---|---|---|---|---|---|
| **Blind 75** | 75 | 75 | 75 | 40 | 70 | 10 | 50 | 46 |
| **NeetCode 150** | | 150 | 150 | 58 | 106 | 20 | 77 | 73 |
| **NeetCode 250** | | | 250 | 64 | 122 | 30 | 102 | 83 |
| **Grind 75** | | | | 75 | 75 | 10 | 48 | 48 |
| **Grind 169** | | | | | 169 | 21 | 85 | 83 |
| **LeetCode 75** | | | | | | 75 | 16 | 19 |
| **Top Interview 150** | | | | | | | 150 | 67 |
| **Top 100 Liked** | | | | | | | | 100 |

- **Blind 75 vs Grind 169:** 5 Blind 75 problems are not in Grind 169: house-robber-ii, longest-common-subsequence, palindromic-substrings, sum-of-two-integers, top-k-frequent-elements.
- **Blind 75 vs Grind 75:** 35 Blind 75 problems are not in default Grind 75. In the other direction, Grind 75 adds 35 problems Blind 75 lacks, for example Flood Fill, Min Stack, LRU Cache, Rotting Oranges, Permutations, Subsets, Task Scheduler, Trapping Rain Water, Word Ladder, Largest Rectangle in Histogram, Basic Calculator, Accounts Merge, Time Based Key-Value Store, Maximum Profit in Job Scheduling ([Grind 75](https://www.techinterviewhandbook.org/grind75)).
- **LeetCode 75 ∩ Blind 75 (10):** container-with-most-water, counting-bits, house-robber, implement-trie, longest-common-subsequence, maximum-depth-of-binary-tree, non-overlapping-intervals, product-of-array-except-self, reverse-linked-list, unique-paths ([LeetCode 75](https://leetcode.com/studyplan/leetcode-75/)).
- **LeetCode 75 problems found in no other major list:** 37 of 75 are in none of NC250, Grind 169 or Top Interview 150, for example can-place-flowers, kids-with-the-greatest-number-of-candies, find-pivot-index, removing-stars-from-a-string, keys-and-rooms, number-of-provinces, successful-pairs-of-spells-and-potions, domino-and-tromino-tiling, total-cost-to-hire-k-workers ([LeetCode 75](https://leetcode.com/studyplan/leetcode-75/)).
- **What other lists add on top of NC250:** Top Interview 150 has 48 problems not in NC250, and Grind 169 has 47. Of Top Interview 150, 37 are in neither NC250 nor Grind 169 ([Top Interview 150](https://leetcode.com/studyplan/top-interview-150/)).
- **Combined sizes:**
  - NC250 ∪ Grind 169 = 297 problems (13 premium)
  - NC250 ∪ Top Interview 150 = 298 (7 premium)
  - NC250 ∪ Grind 169 ∪ Top Interview 150 = 334 (13 premium)
  - Adding Top 100 Liked brings it to 338
- **Problems in many lists:** across the 8 lists in the table, membership counts are: 148 problems are in exactly 1 list, 78 in 2, 35 in 3, 31 in 4, 27 in 5, 20 in 6, 32 in 7, and only 4 in all 8 (container-with-most-water, implement-trie-prefix-tree, maximum-depth-of-binary-tree, product-of-array-except-self). 56 are in at least 6 of 8. These counts are inflated by the nested lists.
- **Sean Prashad's LeetCode Patterns (179) vs other lists:** shares 75 with Blind 75 (all of it), 102 with NC150, 117 with NC250, 54 with Grind 75, 118 with Grind 169, 79 with Top Interview 150, 75 with Top 100 Liked, and 23 with LeetCode 75 ([questions.json](https://raw.githubusercontent.com/seanprashad/leetcode-patterns/main/src/data/questions.json)).
- **SQL 50 vs 30 Days of Pandas:** they share 16 problem IDs (595, 1757, 1148, 1683, 1667, 1517, 1527, 176, 196, 1907, 2356, 596, 1484, 1378, 1280, 570) ([SQL 50](https://leetcode.com/studyplan/top-sql-50/), [30 Days of Pandas](https://leetcode.com/studyplan/30-days-of-pandas/)).
- **Published third-party overlap claims:**
  - A DEV post claims "two 75-problem lists overlap by only nine problems" without clearly naming which two ([DEV](https://dev.to/alex_hunter_44f4c9ed6671e/grind-75-vs-blind-75-vs-neetcode-150-which-list-should-you-use-pja)). The computed figures are Grind 75 ∩ Blind 75 = 40 and LeetCode 75 ∩ Blind 75 = 10, so "nine" most plausibly refers to LeetCode 75 vs Blind 75 and is off by one, or reflects an older plan version.
  - techinterview.org's "LeetCode Patterns by Frequency" (2026-04-27, updated 2026-07-13) gives "Blind 75" category counts that add up to 128 and names no data source. **It is unreliable** ([techinterview.org](https://www.techinterview.org/post/3233474682/leetcode-patterns-by-frequency/)).

### Inferences
- **A union of NC250 and Grind 169 (297 problems) captures almost all of the "classic" consensus problems.** Adding Top Interview 150 contributes 37 mostly Array/String, Matrix, Math and Divide & Conquer items.
- **LeetCode 75 is a largely separate pool** of newer, easier problems. For a progressive bank it is a source of warm-up items rather than overlap.

### Gaps
- **No independent, published overlap matrix from 2025–2026 was found.** The table above is the researcher's own computation from live data on 2026-11-22.

---

## Q3. Which list fits which situation, and which lists provide a recommended order that maps onto progressive stages?

### Takeaway
Consensus in 2025–2026 commentary:

| Situation | Recommended list |
|---|---|
| Short timeline, basics in place | Blind 75 or Grind 75 |
| About 2 months | Grind 75 (default plan) |
| 2–3 months | NeetCode 150 |
| Beginner or long runway | NeetCode 250 (or Striver A2Z) |

Lists with a built-in stage order:
- **NeetCode** (18 categories, from Arrays & Hashing to Bit Manipulation): matches the target stage sequence almost exactly.
- **LeetCode 75** (22 small sections).
- **Top Interview 150** (23 sections).
- **SQL 50** (7 sections).
- **Grind 75:** orders by week (Easy first, mixed topics) rather than by topic.

### Cited Findings
- **AlgoMind (2026-10-30) recommendations by situation** ([AlgoMind](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)):
  - "Under a month, basics in place": Blind 75, then NeetCode 150 problems for stacks, heaps and backtracking.
  - "About two months": Grind 75 at its default plan.
  - "Two to three months": NeetCode 150, in order.
  - "Starting from scratch or about six months away": Striver A2Z, or NeetCode 250.
  - NeetCode 250 is described as "the most beginner-friendly NeetCode list. Blind 75 assumes you already know the basics."
- **NeetCode's own advice (2025-03-30):** go through NC150 "or even better, the NeetCode 250" to learn the patterns, then practise at random from NeetCode All ([X post](https://x.com/neetcode1/status/1906204613583544625)).
- **Reddit r/leetcode (2025, via redlib mirror; search snippets only, threads not fully read):** for a short timeline, the top advice was to cover the topics with a 75 list, then move to 150, "then 250 if time permits" ([r/leetcode thread](https://redlib.hbubli.cc/r/leetcode/comments/1kketcz/which_is_better_to_prepare_neetcode_150_or)). There is also a 2025 thread comparing NeetCode 150 vs Top Interview 150 ([r/leetcode thread](https://redlib.hbubli.cc/r/leetcode/comments/1l10hh5/neetcode_150_vs_top_interview_150_on_leetcode/mvhml4a)).
- **2026 SEO-style comparison pages** agree on Blind 75 = shortest, NeetCode 150 = most complete of the short lists, and Grind 75 = adjustable ([interviewchamp.ai](https://interviewchamp.ai/learn/leetcode-75-vs-blind-75-vs-neetcode-150-2026), [copilotinterview.com](https://copilotinterview.com/blog/blind-75-leetcode-guide)). These are low-authority sources.
- **LeetCode's own guidance in the plan descriptions** ([LeetCode 75](https://leetcode.com/studyplan/leetcode-75/), [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/), [SQL 50](https://leetcode.com/studyplan/top-sql-50/), [Intro to Pandas](https://leetcode.com/studyplan/introduction-to-pandas/)):
  - LeetCode 75: "Best for 1~3 month of prep time"
  - Top Interview 150: "Best for 3+ months of prep time"
  - SQL 50: "Best for 1 month of prep time"
  - Introduction to Pandas: "Designed for absolute beginners"
- **Grind 75's flexible plan:** the weeks and hours per week are adjustable. The default is 8 weeks × 8 h (the code defaults are `weeks ?? 8`, `hours ?? 8`), and the maximum of 26 weeks × 40 h covers all 169 ([AlgoMind](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/); [Grind 75](https://www.techinterviewhandbook.org/grind75)). Each problem has a suggested time of 15–45 min ([AlgoMind](https://www.algomind.app/blog/blind-75-vs-neetcode-150-vs-grind-75-vs-striver-a2z/)). The FAQ explains that "for each question, I have assigned a recommended duration" because interviews allow "less than half an hour per algorithm question" ([Grind 75 FAQ](https://www.techinterviewhandbook.org/grind75/faq)).
  - The FAQ argues for **mixed-topic weeks**, citing spaced repetition and the fact that interviews can come from any topic. It adds that grouping by topic "can be helpful if you're just starting out" ([Grind 75 FAQ](https://www.techinterviewhandbook.org/grind75/faq)).
- **NeetCode category order in the live site data** ([neetcode.io/practice](https://neetcode.io/practice); same order in [.problemSiteData.json](https://github.com/neetcode-gh/leetcode/blob/main/.problemSiteData.json)):
  1. Arrays & Hashing
  2. Two Pointers
  3. Sliding Window
  4. Stack
  5. Binary Search
  6. Linked List
  7. Trees
  8. Heap / Priority Queue
  9. Backtracking
  10. Tries
  11. Graphs
  12. Advanced Graphs
  13. 1-D DP
  14. 2-D DP
  15. Greedy
  16. Intervals
  17. Math & Geometry
  18. Bit Manipulation

  A separate constant in the same code lists Tries before Backtracking. A third-party guide gives the roadmap reading order as "arrays and hashing, two pointers, sliding window, stack, binary search, linked list, trees, tries, heap, backtracking, graphs, advanced graphs, 1D DP, 2D DP, greedy, intervals, math and geometry, bit manipulation". It explains that hashing comes first because hash lookups recur later, and that trees precede graphs because tree DFS/BFS is a simpler form of graph traversal (search-result summary of guides including [Educative NeetCode roadmap](https://www.educative.io/blog/neetcode-roadmap)).
- **Within-category order in NeetCode lists** generally runs Easy, then Medium, then Hard. For example, NC250's Arrays & Hashing has 9 E, 12 M and 1 H ([neetcode.io/practice](https://neetcode.io/practice)).
- **SQL 50 section order** is a beginner-to-intermediate progression: Select, Basic Joins, Basic Aggregate Functions, Sorting & Grouping, Advanced Select & Joins, Subqueries, Advanced String Functions/Regex/Clause ([SQL 50](https://leetcode.com/studyplan/top-sql-50/)).
- **The Tech Interview Handbook's own guidance (updated Aug 7, 2026)** recommends its 12-week study plan built on a distilled 50-question, 5-week core. It presents Grind 75 as "a modern version of Blind 75 that you can customize" ([TIH best practice questions](https://www.techinterviewhandbook.org/best-practice-questions/)).

### Inferences
- **Beginner restarting, fixed progressive bank:**
  - **Algorithms backbone:** NeetCode 250 in NeetCode category order, Easy to Medium to Hard within each stage. It maps one-to-one onto the target stages: arrays & hashing → two pointers → sliding window → stack → binary search → linked list → trees → tries → heap → backtracking → graphs → DP → greedy → intervals → math/bit.
  - **Mark subsets as milestones:** the Blind 75 / NC150 members within NC250 can be flagged as "core" checkpoints.
  - **Optional on-ramp:** LeetCode 75's easy items (no Hards) can serve as a "Stage 0".
  - **Late extension:** add the Grind 169 and Top Interview 150 extras (47 + 37 problems) as a review or "interview mix" stage that mimics Grind's mixed-topic weeks.
- **SQL track:** SQL 50 in section order is the natural backbone. Introduction to Pandas (15, all Easy) can precede 30 Days of Pandas if a pandas sub-track is wanted.
- **Timeline guidance for the platform's UI:**

  | Prep time | Suggested list |
  |---|---|
  | Under 1 month | Blind 75 / Grind 75 |
  | 1–3 months | NC150 or LeetCode 75 + NC150 |
  | 3+ months / beginner | NC250 (+ Top Interview 150 extras) |

### Gaps
- **The exact edges of the NeetCode roadmap tree** (prerequisite arrows) could not be retrieved. neetcode.io/roadmap is rendered client-side, and the edge data was not found in the main bundle. Only the linear category order is verified.
- **No 2025–2026 study measured which list works best for beginners;** all of the guidance above is expert or vendor opinion.

---

## Q4. Is there evidence on which lists best match what big US tech companies actually ask in 2025–2026?

### Takeaway
No independent, published analysis was found, so the researcher computed coverage against the most-used public company-tag dataset ([liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems), last commit 2026-10-21).

Measured against each company's top 50 problems from the last six months:

| List | Coverage of top-50 (6 mo) |
|---|---|
| NeetCode 250 | 82–88% at Google, Meta, Amazon, Microsoft, Bloomberg |
| Grind 169 | 74–82% |
| NC150 / Top Interview 150 / Top 100 Liked | about 60–74% |
| Blind 75 / Grind 75 | about 36–52% |
| LeetCode 75 | 10–16% |

Per problem, Top 100 Liked and Grind 75 are the most efficient.

### Cited Findings
- **The dataset:** the README says "Curated lists of Leetcode questions group by companies, updated as of 1 June 2025", but commits continue ("Update Problem [Oct 20]", 2026-10-21; earlier 2026-08-16 and 2026-06-26). The repo has 35.7k stars and **no license** ([liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)). Each company folder has "Thirty Days / Three Months / Six Months / More Than Six Months / All" CSVs with a 0–100 `Frequency` column ([Google CSV](https://github.com/liquidslr/leetcode-company-wise-problems/blob/main/Google/3.%20Six%20Months.csv)).
- **Coverage of each company's top 50 by frequency, "Six Months" CSV** (researcher computation; list data from Q1 sources). The "All-time top-100" line under each company is the same metric for the all-time top 100.

  | Company | B75 | G75 | LC75 | NC150 | TI150 | T100L | G169 | NC250 |
  |---|---|---|---|---|---|---|---|---|
  | Google | 44% | 42% | 12% | 64% | 68% | 66% | 74% | **86%** |
  | Google, all-time top-100 | 35 | 36 | 14 | 58 | 59 | 56 | 67 | 75 |
  | Meta | 42 | 42 | 16 | 60 | 72 | 62 | 74 | **82** |
  | Meta, all-time top-100 | 25 | 31 | 9 | 40 | 46 | 38 | 50 | 52 |
  | Amazon | 48 | 52 | 16 | 70 | 70 | 72 | 80 | **88** |
  | Amazon, all-time top-100 | 37 | 42 | 18 | 65 | 64 | 64 | 74 | 82 |
  | Microsoft | 40 | 48 | 14 | 70 | 68 | 74 | **82** | **82** |
  | Microsoft, all-time top-100 | 42 | 44 | 17 | 66 | 70 | 67 | 74 | 79 |
  | Bloomberg | 44 | 36 | 10 | 60 | 74 | 60 | 76 | **84** |
  | Bloomberg, all-time top-100 | 35 | 34 | 13 | 53 | 57 | 54 | 63 | 70 |
  | Apple (top 50) | 32 | 30 | 12 | 48 | 46 | 42 | 54 | 62 |
  | Uber (only 33 in window) | 18 | 15 | 6 | 21 | 21 | 15 | 30 | 27 |
  | LinkedIn (only 19 in window) | 26 | 26 | 21 | 37 | 42 | 37 | 37 | 37 |

  Source: [liquidslr dataset](https://github.com/liquidslr/leetcode-company-wise-problems) × [neetcode.io](https://neetcode.io/practice) / [Grind 75](https://www.techinterviewhandbook.org/grind75) / [LeetCode study plans](https://leetcode.com/studyplan/top-interview-150/).
- **Frequency-weighted coverage of each company's full six-month list** is much lower because of long tails (Google has 793 problems in that window, Amazon 733):
  - NC250: 39–48% (Google 39, Amazon 41, Meta 48, Microsoft 48, Bloomberg 47)
  - Grind 169: 31–41%
  - NC150: 27–35%
  - Blind 75: 15–20%
  - LeetCode 75: 9–11%

  ([liquidslr dataset](https://github.com/liquidslr/leetcode-company-wise-problems))
- **Union of the six-month top-50s for Google, Meta, Amazon, Microsoft and Bloomberg:** 94 distinct problems ([liquidslr dataset](https://github.com/liquidslr/leetcode-company-wise-problems)).

  | List | Covered (of 94) | List size | Covered per 100 list problems |
  |---|---|---|---|
  | Blind 75 | 31 (33%) | 75 | 41 |
  | Grind 75 | 33 (35%) | 75 | 44 |
  | LeetCode 75 | 17 (18%) | 75 | 23 |
  | NC150 | 50 (53%) | 150 | 33 |
  | Top Interview 150 | 53 (56%) | 150 | 35 |
  | Top 100 Liked | 52 (55%) | 100 | **52** |
  | Grind 169 | 62 (66%) | 169 | 37 |
  | NC250 | 70 (74%) | 250 | 28 |
  | NC250 ∪ Grind 169 | 78 | 297 | |
  | NC250 ∪ Grind 169 ∪ Top Interview 150 | 81 | 334 | |
  | All 8 lists combined | 83 | 375 | |

- **Problems in the six-month top-50 at 3 or more of those 5 companies (44 problems):**
  - Covered: NC250 39, Grind 169 37, Top Interview 150 34, Top 100 Liked 32, NC150 31, Blind 75 22, Grind 75 21, LeetCode 75 5.
  - Only max-consecutive-ones is in none of the lists.

  ([liquidslr dataset](https://github.com/liquidslr/leetcode-company-wise-problems))
- **Vendor and anecdotal context:**
  - Educative asserts that Grind 75 "was designed around the most common problems between 2021–2022" and that company trends have shifted by 2025. This is a vendor claim without data ([Educative](https://www.educative.io/blog/grind-75-vs-leetcode-patterns-for-meta-coding-interviews)). It is consistent with the Grind changelog stopping in 2022 ([Grind 75 Changelog](https://www.techinterviewhandbook.org/grind75/changelog)).
  - Anecdotal Blind posts from Sept 2025 report that list problems appear less often verbatim, with new or modified problems instead ([Teamblind](https://www.teamblind.com/post/starting-to-feel-like-lc-sets-dont-really-show-up-in-interviews-anymore-jynit841), [Teamblind](https://www.teamblind.com/post/kinda-feel-lc-question-doesnt-seem-to-appear-in-real-interviews-anymore-ztymostk)). These are individual reports, not measurements.

### Inferences
- **NeetCode 250 gives the best absolute coverage** of current big-tech high-frequency problems among single lists. Grind 169 is close, with fewer problems.
- **For a tight problem budget,** Top 100 Liked and Grind 75 / Blind 75 give the most coverage per problem.
- **LeetCode 75 should not be counted as interview-frequency coverage.**
- **Combining NC250 with Grind 169 (297 problems) reaches 78 of 94 of the union top-50,** which is a reasonable ceiling for a fixed bank. The rest is company-specific long tail.
- **The data reflects verbatim frequency only;** pattern transfer to modified problems is the main argument for pattern-ordered lists over chasing frequency.

### Gaps
- **The dataset's provenance is uncertain.** It appears to mirror LeetCode Premium company-tag frequency, which LeetCode crowdsources and does not publish openly. Its exact collection method and time window semantics (the six-month window is relative to the last update, around Oct 2026) are not documented, and it has no license.
- **No peer-reviewed or independent 2025–2026 analysis** comparing these lists against company data was found. Third-party "frequency" articles (for example techinterview.org) give no data source.
- **Possible bias:** the frequency data is self-reported by LeetCode users and may over-represent classic problems that people already practise.

---

## Q5. Licensing and reuse: can the lists (titles + links) be reused freely, and what is the status of reusing LeetCode problem statements?

### Takeaway
- **Problem statements:** LeetCode's Terms (last modified **2024-04-05**, still current as fetched in Nov 2026) claim all content, including "questions" and "solutions", as LeetCode's copyrighted property. They forbid crawling and scraping and grant no reuse licence. Reproducing problem statements is therefore not permitted. LeetCode has filed DMCA notices against repositories that exposed its paid content.
- **The lists themselves:** NeetCode's list flags for Blind 75 and NC150 are in an MIT-licensed repo. Grind 75 is "All rights reserved". The company-frequency dataset is unlicensed.
- **Safest approach:** store problem IDs, slugs and titles plus outbound links, and write original statements and test cases.

### Cited Findings
- **LeetCode Terms of Service** ([leetcode.com/terms](https://leetcode.com/terms/)), "Last modified: 04/05/2024":
  - Content is defined to include "all software, images, questions, communications, solutions, and any related material".
  - "Unless otherwise specified in writing, all Our Content is owned, controlled, or licensed by us."
  - "You agree that all Content is our sole and exclusive property."
  - "All Our Content is copyrighted under United States copyright laws."
  - Activities such as "crawling," "scraping," or "spidering" any part of the Service are "strictly forbidden".
  - Users must not "directly compete with LeetCode".
  - "You … are authorized to use our Services for your sole benefit."
  - No clause grants users reproduction or commercial-use rights.
- **LeetCode DMCA notices on GitHub's public archive:**
  - A notice against "Leetcode-Premium-Bypass" / "Leetcode-Premium-Unlocker", stating LeetCode "uses a subscription-based access method to restrict access to certain copyrighted material". It is dated around 2024-02-01 in a mirror.
  - An earlier notice dated 2021-03-25 against a site "copying premium problems".
  - Sources: mirrors of [github/dmca](https://github.com/github/dmca), e.g. [mirror commit](https://source-hub.etos-pro.ru/github/dmca/commit/a286358a334b6e1b5445f89a5ba21f2f34c3c813) and [mirror commit](https://git.randommeaninglesscharacters.com/github/dmca/commit/6d56d3f3e5b663982259996d0f043c69569e6171). Exact dates were not verified on the original repo.
- **GitHub's DMCA process** can disable whole repositories, and forks are handled separately ([GitHub DMCA policy](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy)).
- **Licences of list sources:**

  | Source | Licence / status |
  |---|---|
  | neetcode-gh/leetcode (flags for `blind75` and `neetcode150` in `.problemSiteData.json`) | MIT ([repo](https://github.com/neetcode-gh/leetcode)) |
  | NeetCode 250 membership | Only in the neetcode.io site bundle; no licence stated ([neetcode.io/practice](https://neetcode.io/practice)) |
  | yangshun/tech-interview-handbook | MIT, but the Grind 75 page and data are "© 2026 Tech Interview Handbook. All rights reserved" ([repo](https://github.com/yangshun/tech-interview-handbook), [Grind 75](https://www.techinterviewhandbook.org/grind75/changelog)) |
  | seanprashad/leetcode-patterns | Licence reported as NOASSERTION ([repo](https://github.com/seanprashad/leetcode-patterns)) |
  | liquidslr company dataset | No licence ([repo](https://github.com/liquidslr/leetcode-company-wise-problems)) |
  | LeetCode study plans | LeetCode "Content" under the ToS ([leetcode.com/terms](https://leetcode.com/terms/)) |

- **Ideas versus expression:** US copyright protection does not "extend to any idea, procedure, process, system, method of operation … regardless of the form in which it is described" ([17 U.S.C. §102(b)](https://www.law.cornell.edu/uscode/text/17/102)). The underlying algorithmic tasks (for example "find two numbers summing to target") are ideas. The specific statement text, examples and test data are expression.
- **Common practice:** thousands of public repos publish list membership as problem number + title + LeetCode link, without statements (for example [SQL 50 repos](https://github.com/HamzaHassanain/Leetcode_SQL_50_Study_Plan), [neetcode-250 repos](https://github.com/iamBelugax/neetcode-250)). No takedowns of such title-and-link lists were found in this research.

### Inferences
- **For a personal practice platform:**
  - **Low risk:** storing list membership (IDs, slugs, titles, difficulty, topic tags, the list's ordering) and deep-linking to leetcode.com or neetcode.io. Problem titles and numbers are short factual identifiers.
  - **Copying statements, examples, constraints, editorials or test cases:** conflicts with the ToS and may draw a DMCA notice, especially for Premium problems.
  - **Scraping LeetCode** (including the GraphQL calls used for this research) is prohibited under the ToS for ongoing or programmatic use. A platform should not depend on live scraping.
- **Selection and arrangement of a curated list** (for example the exact NC250 ordering) may carry thin compilation copyright. Using MIT-licensed data (the neetcode-gh repo for Blind 75 / NC150) or rebuilding the bank from public knowledge is safer than copying an "All rights reserved" dataset wholesale. For purely personal, non-distributed use the practical risk is minimal. *This is general legal background, not legal advice.*
- **For a self-hosted judge,** write original problem statements and original test cases for the same algorithmic tasks, keeping the LeetCode link as a reference. SQL problems need original schemas and sample data written for the platform.

### Gaps
- **Whether LeetCode has ever acted against title-and-link list sites** (as opposed to premium-content leaks) was not found.
- **The neetcode.io terms of use** for its list data and hosted problem versions were not retrieved.
- **No court decision** specifically on LeetCode-style problem statements was found.
