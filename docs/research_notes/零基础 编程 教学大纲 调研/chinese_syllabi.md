# Chinese zero-background programming syllabi & official curriculum standards (Python + data), as of Nov 2026

Research date: 2026-11-22. Scope: how authoritative Chinese beginner curricula sequence their first units, and in particular whether they start from 数据 / 数据类型 / 数据的表示与特点 before control flow. All chapter and section titles are quoted verbatim from the sources unless marked otherwise.

Source-quality note: two official documents were read in full from the 教育部 (moe.gov.cn) originals: the 普通高中信息技术课程标准（2017年版2020年修订） text and the 义务教育信息科技课程标准（2022年版） PDF (a scanned image PDF, read page by page). The NCRE 2025 outlines came from verbatim PDF reposts on a university site (yznu.edu.cn), not from neea.edu.cn itself. Textbook tables of contents came from dzkbw.com (an e-textbook mirror). Bootcamp outlines came from the official Bilibili uploads (the episode lists).

---

## Q1. NCRE 二级 Python 语言程序设计考试大纲 (latest edition), plus NCRE 数据库-related outlines

### Takeaway
The current outline is the **2025年版**, and no 2026 edition was found. Its order is 基本语法元素 → 基本数据类型 → 程序的控制结构 → 函数和代码复用 → 组合数据类型 → 文件和数据格式化 → 程序设计方法 → 计算生态. So scalar data types, including bool/None, type checking/conversion and comparison/logical operators, come **before** control flow. Composite types (list/set/dict) come **after** functions, and file formats (only CSV is named) come near the end. The 2025 NCRE 二级 MySQL outline starts from database concepts (基本概念与方法), not from SQL syntax.

### Cited Findings
**Edition status**
- The document is titled 「全国计算机等级考试（NCRE）二级Python语言程序设计考试大纲(2025年版）」. — [NCRE Python 2025 outline (repost, yznu.edu.cn)](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf)
- A 深圳市教育局 attachment lists the NCRE 考试大纲（2025年版） system, including 二级Python语言程序设计考试大纲（2025年版）, and notes that the outlines can be downloaded from 中国教育考试网. This comes from the search-result summary; the docx itself was not opened. — [szeb.sz.gov.cn attachment](https://szeb.sz.gov.cn/attachment/1/1724/1724604/12855469.docx)
- A non-official page says the 2026 NCRE still uses the 2025 version. I could not verify this. — [bendibao](https://m.bendibao.com/show978736.html). A CSDN post says the "2023年版" is current. It reads as stale ("截至2024年") and conflicts with the 2025 PDFs. — [CSDN](https://bbs.csdn.net/topics/620514837)

**基本要求 (2025)**, verbatim and in order:
1. 掌握Python语言的基本语法规则。
2. 掌握不少于3个基本的Python标准库。
3. 掌握不少于3个Python第三方库，掌握获取并安装第三方库的方法。
4. 能够阅读和分析Python程序。
5. 熟练使用IDLE开发环境，能够将脚本程序转变为可执行程序。
6. 了解Python计算生态在以下方面（不限于）的主要第三方库名称：网络爬虫、数据分析、数据可视化、机器学习、Web开发等。

Source: [NCRE Python 2025 outline](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf)

**考试内容 (2025)**, verbatim and in order. Source for everything below: [NCRE Python 2025 outline](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf)
- **一、Python语言基本语法元素**
  1. 程序的基本语法元素：程序的格式框架、缩进、注释、变量、命名、保留字、连接符、数据类型、赋值语句、引用。
  2. 基本输入输出函数：input()、eval()、print()。
  3. 源程序的书写风格。
  4. Python语言的特点。
- **二、基本数据类型**
  1. 数字类型：整数类型、浮点数类型和复数类型。
  2. 数字类型的运算：数字运算操作符、数字运算函数。
  3. 真假无：True、False、None。
  4. 字符串类型及格式化：索引、切片、基本的format()格式化方法。
  5. 字符串类型的操作：字符串操作符、操作函数和操作方法。
  6. 类型判断和类型间转换。
  7. 逻辑运算和比较运算。
- **三、程序的控制结构**
  1. 程序的三种控制结构。
  2. 程序的分支结构：单分支结构、二分支结构、多分支结构。
  3. 程序的循环结构：遍历循环、条件循环。
  4. 程序的循环控制：break、continue。
  5. 程序的异常处理：try-except及异常处理类型。
- **四、函数和代码复用**
  1. 函数的定义和使用。
  2. 函数的参数传递：可选参数传递、参数名称传递、函数的返回值。
  3. 变量的作用域：局部变量和全局变量。
  4. 函数递归的定义和使用。
- **五、组合数据类型**
  1. 组合数据类型的基本概念。
  2. 列表类型：创建、索引、切片。
  3. 列表类型的操作：操作符、操作函数和操作方法。
  4. 集合类型：创建。
  5. 集合类型的操作：操作符、操作函数和操作方法。
  6. 字典类型：创建、索引。
  7. 字典类型的操作：操作符、操作函数和操作方法。
- **六、文件和数据格式化**
  1. 文件的使用: 文件打开、读写和关闭。
  2. 数据组织的维度：一维数据和二维数据。
  3. 一维数据的处理：表示、存储和处理。
  4. 二维数据的处理：表示、存储和处理。
  5. 采用CSV格式对一二维数据文件的读写。
- **七、Python程序设计方法**: 1. 过程式编程方法。2. 函数式编程方法。3. 生态式编程方法。4. 蒙特卡洛计算方法。5. 递归计算方法。
- **八、Python计算生态**
  1. 标准库的使用：turtle库、random库、time库。
  2. 基本的Python内置函数。
  3. 利用pip工具的第三方库安装方法。
  4. 第三方库的使用：jieba库、PyInstaller库、基本NumPy库。
  5. 更广泛的Python计算生态，只要求了解第三方库的名称，不限于以下领域：网络爬虫、数据分析、文本处理、数据可视化、用户图形界面、机器学习、Web开发、游戏开发等。

**考试方式 (2025)**: 上机考试，120分钟，满分100分。单项选择题40分（含公共基础知识部分10分）; 操作题60分（基本编程题和综合编程题）。考试环境：「Windows 7操作系统，建议Python 3.5.3至Python 3.9.10，IDLE开发」。 — [NCRE Python 2025 outline](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf)

**NCRE 二级 MySQL数据库程序设计 考试大纲（2025年版）**. Source for this block: [NCRE MySQL 2025 outline (repost)](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/93fbb5d7-5fad-4868-a11d-a0b253751745.pdf)
- 基本要求: 掌握数据库的基本概念和方法; 熟练掌握MySQL的安装与配置; 熟练掌握MySQL平台下使用SQL语言实现数据库的交互操作; 熟练掌握MySQL的数据库编程; 熟悉PHP应用开发语言…; 掌握MySQL数据库的管理与维护技术。
- 考试内容, in order:
  - **一、基本概念与方法**: 1. 数据库基础知识（数据库相关的基本概念; 数据库系统的特点与结构; 数据模型）2. 关系数据库、关系模型 3. 数据库设计基础（数据库设计的步骤; 关系数据库设计的方法）4. MySQL概述（系统特性与工作方式; MySQL编程基础：结构化查询语言SQL、MySQL语言结构）
  - **二、MySQL平台下的SQL交互操作**: 1. 数据库 2. 数据表（表结构、表数据的基本概念; 创建/更新/重命名/复制/删除/查看数据表; 插入/删除/更新; 「简单查询、聚合查询、连接查询、条件查询、嵌套查询、联合查询」; 数据完整性约束）3. 索引 4. 视图
  - **三、MySQL的数据库编程**: 触发器; 事件; 存储过程和存储函数
  - **四、MySQL的管理与维护**: 服务器使用与管理; 用户账号管理; 账户权限管理; 备份与恢复（含二进制日志）
  - **五、MySQL的应用编程**: PHP语言的基本使用方法; 基于B/S结构的PHP简单应用程序
- 考试方式: 120分钟; 单选40分（含公共基础知识10分）; 操作题60分（基本操作题、简单应用题及综合应用题）; 环境「WAMP 5.0及以上；数据库管理系统：MySQL 5.5；编程语言：PHP」。
- A 2025 二级MySQL 样题及参考答案 is also published. — [MySQL sample (repost)](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/74147847-d5fe-432e-ac21-7914e64049bc.pdf)
- NCRE also has 2025 outlines for **二级openGauss数据库程序设计**, which has the same 一、基本概念与方法 opening and adds 模式(Schema)的操作 and 「openGauss 数据库支持的数据类型」 under 数据表 ([openGauss 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/9cd6869d-e0b0-4ed8-8dbe-78db23c56c1a.pdf)), and for **二级Access数据库程序设计** ([Access 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/ce6858d4-344f-42e8-898d-d974d59d4c8a.pdf)).

### Inferences
- NCRE files 「数据类型」 under the first unit, 基本语法元素, and then gives it a full unit of its own (二、基本数据类型) **before** 三、控制结构. Bool/None (「真假无」), 类型判断和类型间转换 and 比较/逻辑运算 all sit in the data-type unit. This supports a "data first" opening stage: a learner can be taught what True/False/None are and how to compare values before ever writing `if`.
- 「数据组织的维度：一维数据和二维数据」 and CSV are explicitly a *data-format* topic, but NCRE places it 6th, after functions and composite types. It names no JSON.
- The exam environment caps at Python 3.9.10, so `match` (3.10+) is outside NCRE scope even though some newer tutorials teach it (see Q4).
- The database outlines all start from 「数据库基础知识 / 数据模型 / 关系模型」. That is concept-first, a precedent for introducing "table-shaped data" conceptually before syntax.

### Gaps
- I could not fetch the official PDF from ncre.neea.edu.cn. The verbatim text above is from a university repost whose title page reads 2025年版 (the PDF metadata creation date is 2024-12-27).
- I found no official neea.edu.cn notice confirming whether a 2026 edition exists or whether the 2025 edition continues into 2026.
- I could not obtain the 2023年版 text, so I cannot list the 2023→2025 changes (e.g. whether 「真假无」 and 「基本NumPy库」 are new in 2025).
- The 公共基础知识 (10 points) outline was not retrieved.

---

## Q2. 嵩天等《Python语言程序设计》（北京理工大学，中国大学MOOC）: week order, first weeks, data-type treatment

### Takeaway
The MOOC has 9 teaching weeks in 3 parts (2 + 5 + 2). Week 1 is 程序设计基本方法 + 环境 + a 温度转换 example + 语法元素分析. Week 2 is turtle drawing. **Week 3 is 基本数据类型** (数字类型 and 字符串), then 控制结构 → 函数 → 组合数据类型 → **文件和数据格式化 (一维/二维数据, CSV)**. NCRE's outline mirrors this order, apart from the extra turtle week (NCRE lists turtle under 计算生态).

### Cited Findings
- The icourse163 page (course BIT-268001) has three parts. 「第一部分（2周）Python快速入门，"初识Python语言"」 covers basic programming methods and Python's syntax elements. 「第二部分（5周）Python基础语法，"深入Python语言"」 covers the full basic syntax. 「第三部分（2周）Python编程思维，"运用Python语言"」 covers the computing ecosystem and programming methodology. There are 16 classic cases, 50+ programming problems and 100+ single-choice questions. — [icourse163 BIT-268001](https://www.icourse163.org/course/BIT-268001)
- The current offering is the **第32次开课**, with >559万 cumulative learners. The page targets 「Python零基础学习者」, requires only that learners can use a computer, and explicitly lists 「全国计算机等级考试二级Python科目考生」 as an audience. The reference textbook is 《Python语言程序设计基础（第3版）》 by 嵩天、黄天羽、杨雅婷. — [icourse163 BIT-268001](https://www.icourse163.org/course/BIT-268001)
- Lecture order (Bilibili mirror of the BIT course, 56 lectures; numbering = chapter.lecture; chapter 1 is the course intro, so chapter N ≈ MOOC week N−1). Source for this list: [Bilibili BV1JL4y1x7xC](https://www.bilibili.com/video/BV1JL4y1x7xC/)
  - 2（Week 1）: 2.2 程序设计基本方法 · 2.3 Python开发环境配置 · 2.4 "温度转换" · 2.5 Python程序语法元素分析
  - 3（Week 2）: 3.2 深入理解Python语言 · 3.3 Python蟒蛇绘制 · 3.4 turtle库的使用 · 3.5 turtle程序语法元素分析
  - **4（Week 3）: 4.2 数字类型与操作 · 4.3 天天向上的力量 · 4.4 字符串类型与操作 · 4.5 time库的使用 · 4.6 文本进度**
  - 5（Week 4）: 5.2 程序的控制结构 · 5.3 身体质量指数BMI · 5.4 程序的循环结构 · 5.5 random库的使用 · 5.6 圆周率的计算
  - 6（Week 5）: 6.2 函数的定义和使用 · 6.3 七段数码管绘制 · 6.4 代码复用与函数递归 · 6.5 PyInstaller库 · 6.6 科赫雪花小包裹
  - 7（Week 6）: 7.2 集合类型与操作 · 7.3 序列类型及操作 · 7.4 基本统计值计算 · 7.5 字典类型及操作 · 7.6 jieba库及使用 · 7.7 文本词频统计
  - **8（Week 7）: 8.2 文件的使用 · 8.3 自动轨迹绘制 · 8.4 一维数据的格式化与处理 · 8.5 二维数据的格式化与处理 · 8.6 wordcloud库 · 8.7 政府工作报告词云**
  - 9（Week 8）: 9.2 体育竞技分析 · 9.3 Python程序设计思维 · 9.4 第三方库的安装 · 9.5 os库 · 9.6 第三方库安装脚本
  - 10（Week 9）: 10.2 Python库之数据处理到人工智能 · 10.3 霍兰德人格分析雷达图 · 10.4 从web解析到网络空间 · 10.5 从人机交互到艺术设计 · 10.6 玫瑰花绘制
  - 11.1 全课程总结

### Inferences
- 嵩天's "data" teaching runs in two layers. Scalar types (数字/字符串) come in week 3, right after hello-world-style programs and turtle. "Data organization" (一维/二维数据, i.e. lists and tables as files, CSV) comes in week 7, framed as 「数据的格式化与处理」. The week 7 framing (dimensions of data → representation → storage → processing) is a ready-made vocabulary for a 「认识不同的数据格式和特点」 stage, but 嵩天 teaches it late.
- Every unit pairs concept → 实例 → 库 → 实例. Week 3's pairing is 天天向上的力量 (numeric growth) and 文本进度条 (string formatting), which shows data types taught through small computations.

### Gaps
- I did not obtain the official week-by-week syllabus text from icourse163; the page only shows the 3-part summary, and the 2026 schedule is an image. Lecture titles come from a Bilibili mirror (rehosted, consolidated from 256 short lectures into 56).
- The 《Python语言程序设计基础（第3版）》 (高等教育出版社) table of contents was not found. So it is **unverified** whether the textbook or MOOC covers JSON / 高维数据. NCRE 2025 names only CSV.

---

## Q3. 普通高中信息技术课程标准（2017年版2020年修订）必修1《数据与计算》 and 义务教育信息科技课程标准（2022年版）: how data/encoding/data structures are introduced and ordered; textbook chapter order

### Takeaway
Both official standards are explicitly **data-first**. High-school 必修1 orders its content requirements 数据与信息（特征、编码）→ 数据处理与应用 → 算法与程序实现 → 人工智能. The compulsory-education standard puts 「数据与编码」 in grades 3–4, before 「身边的算法」 / 「过程与控制」 in grades 5–6. Both major 必修1 textbooks open with a data/encoding chapter before any programming. The 人教中图版 programming section opens with 「2.3.1 数据类型」 before variables, statements and control structures.

### Cited Findings
**High school standard (普通高中信息技术课程标准 2017年版2020年修订, 教育部制定)**. Source for this block unless noted: [MOE notice + official zip](http://www.moe.gov.cn/srcsite/A26/s8001/202006/t20200603_462199.html) (zip: [W020200603315372317586.zip](http://www.moe.gov.cn/srcsite/A26/s8001/202006/W020200603315372317586.zip), file 11)
- The compulsory courses are 「数据与计算」 and 「信息系统与社会」. 必修1 「本模块包括"数据与信息""数据处理与应用""算法与程序实现"三部分内容」, and 「本模块是信息技术课程后续学习的基础」.
- 【内容要求】 for 必修1, verbatim and in order:
  - 1.1 在具体感知数据与信息的基础上，描述数据与信息的特征，知道数据编码的基本方式。
  - 1.2 在运用数字化工具的学习活动中，理解数据、信息与知识的相互关系，认识数据对人们日常生活的影响。
  - 1.3 针对具体学习任务，体验数字化学习过程，感受利用数字化工具和资源的优势。
  - 1.4 通过典型的应用实例，了解数据采集、分析和可视化表达的基本方法。
  - 1.5 根据任务需求，选用恰当的软件工具或平台处理数据，完成分析报告，理解对数据进行保护的意义。
  - 1.6 从生活实例出发，概述算法的概念与特征，运用恰当的描述方法和控制结构表示简单算法。
  - 1.7 掌握一种程序设计语言的基本知识，使用程序设计语言实现简单算法。通过解决实际问题，体验程序设计的基本流程，感受算法的效率，掌握程序调试与运行的方法。
  - 1.8 通过人工智能典型案例的剖析，了解智能信息处理的巨大进步和应用潜力，认识人工智能在信息社会中的重要作用。
- 教学提示 (3) suggests organizing students to 「探究顺序结构、选择结构和循环结构的特点」, with examples 「百钱买百鸡」 (枚举), 「选课系统」 and 「趣味小游戏」. 教学提示 (2) uses 「网络购书」 to explore 「网站获取用户数据的基本类型」 and simple analysis methods (对比分析法、平均分析法).
- 【学业要求】 opens with 「学生能够描述数据与信息的特征，知道数据编码的基本方式」, then 「能够利用软件工具或平台对数据进行整理、组织、计算与呈现」, then 「掌握一种程序设计语言的基本知识，利用程序设计语言实现简单算法」. The standard names no language; Python is the textbooks' choice.
- 选择性必修1 「数据与数据结构」 content requirements start with 「1.1 通过列举实例，分析数据与社会各领域的关系，理解数字、数值和数据的基本含义」, then the concept of 数据结构, 数组/链表, 「包括字符串、队列、栈在内的线性表」, 抽象数据类型/二叉树, and 排序/查找 (迭代、递归).
- The revision team framed the subject's 大概念 as 「数据、算法、信息系统和信息社会」, with data listed first. — [高中信息技术课程标准修订说明, 中国电化教育 2016.12](https://aic-fe.bnu.edu.cn/docs/20181017153017714873.pdf)

**Compulsory education standard (义务教育信息科技课程标准 2022年版)**. Source for this block: [MOE notice page](http://www.moe.gov.cn/srcsite/A26/s8001/202204/t20220420_619921.html); official PDF [W020220420582361024968.pdf](http://www.moe.gov.cn/srcsite/A26/s8001/202204/W020220420582361024968.pdf), pp.12–13, 23–24, 29
- The content is organized around 「数据、算法、网络、信息处理、信息安全、人工智能六条逻辑主线」, 「体现循序渐进和螺旋式发展」. The **data strand** is 「数据来源的可靠性—数据的组织与呈现—数据对现代社会的重要意义」. The 信息处理 strand includes 「使用编码建立数据间内在联系的原则与方法」.
- Modules by 学段:
  - 第一学段（1–2年级）: 信息交流与分享 / 信息隐私与安全 / 跨学科主题 数字设备体验
  - **第二学段（3–4年级）: 在线学习与生活 / 数据与编码 / 跨学科主题 数据编码探秘**
  - 第三学段（5–6年级）: 身边的算法 / 过程与控制 / 小型系统模拟
  - 第四学段（7–9年级）: 互联网应用与创新 / 物联网实践与探索 / 人工智能与智慧社会 / 互联智能设计
  - 「3～8年级单独开设课程」.
- The 「数据与编码」 module 「包括"数字与编码""数据与数据安全""数据的组织与呈现"三部分内容」 and 「本模块是信息科技课程后续学习的基础」. 「在本模块中，编码的目的是作为唯一标识，之后的模块中还会介绍用于其他目的的编码」.
- 数据与编码 内容要求, verbatim excerpts:
  - (1) 「感受身边无所不在的数据，可以使用数字、字母或文字编码表示信息」
  - (3) 「知道如何使用编码建立数据间的内在联系，以便计算机识别和管理，了解编码长度与所包含信息量之间的关系」
  - (4) 「了解数字化表示信息的优势，体验信息存储和传输过程中所必需的编码和解码步骤，初步理解数据校验的目的和意义」
  - (6) 「使用数字化工具组织并呈现收集的数据，借助可视化方式表示数据之间的关系以支撑自己的观点」
  - (7) 「能用数据记录并描述规律性发生的事件」
  - Its 学业要求 asks students to 「判断数据的合理性和可靠性」.
- The cross-disciplinary topic 「数据编码探秘」 includes 「用编码描述秩序」「用数据讲故事」「自我管理小管家」「在线学习小能手」.
- 身边的算法（5–6年级）学业要求: 「能用符号和编码表示问题求解所关心的对象，采用自然语言、流程图等方式，运用三种基本控制结构及其组合，正确进行问题求解的算法描述」. Its 教学提示: 「本模块要求学生体验计算机程序…不要求每个算法问题都由学生编程实现，阅读理解、修改运行等也都是有意义的体验」.

**Textbooks for 必修1《数据与计算》 (2019 editions, 普通高中教科书)**
- **人教中图版**. Source: [dzkbw.com 人教中图版 必修1 目录](http://www.dzkbw.com/books/rjb/xinxijishu/gzbx1/)
  - 第1章 认识数据与大数据（主题学习项目：体质数据促健康）
    - 1.1 数据、信息与知识（1.1.1 感知数据 · 1.1.2 认识信息 · 1.1.3 理解知识）
    - **1.2 数字化与编码（1.2.1 数字化及其作用 · 1.2.2 二进制与数制转换 · 1.2.3 数据编码 · 1.2.4 数据压缩）**
    - 1.3 数据科学与大数据（1.3.1 数据科学的兴起 · 1.3.2 大数据及其应用）
  - 第2章 算法与程序实现（主题学习项目：编程控灯利出行）
    - 2.1 解决问题的一般过程和用计算机解决问题
    - 2.2 算法的概念及描述（认识算法 · 描述算法）
    - **2.3 程序设计基本知识（2.3.1 数据类型 · 2.3.2 常量、变量及表达式 · 2.3.3 程序语句 · 2.3.4 程序结构）**
    - 2.4 常见算法的程序实现（解析算法 · 枚举算法 · 算法效率 · 程序的调试方法）
  - 第3章 数据处理与应用（主题学习项目：用水分析助决策）: 3.1 数据处理的一般过程（数据采集 · 数据整理 · 数据分析 · 数据呈现）· 3.2 数据采集与整理（含 数据安全）· 3.3 数据分析与可视化 · 3.4 数据分析报告与应用
  - 第4章 走进智能时代: 4.1 认识人工智能 · 4.2 利用智能工具解决问题（含 4.2.2 编程调用平台中的智能工具）· 4.3 人工智能的应用与影响
- **浙教版**. Source: [dzkbw.com 浙教版 必修1 目录](http://www.dzkbw.com/books/zjb/xinxijishu/gzbx1/002.htm)
  - 第一章 数据与信息: 1.1 感知数据 · 1.2 数据、信息与知识 · **1.3 数据采集与编码** · 1.4 数据管理与安全 · 1.5 数据与大数据
  - 第二章 算法与问题解决: 2.1 算法的概念及描述 · 2.2 算法的控制结构 · 2.3 用算法解决问题的过程
  - 第三章 算法的程序实现: 3.1 用计算机编程解决问题的一般过程 · **3.2 Python语言程序设计** · 3.3 简单算法及其程序实现
  - 第四章 数据处理与应用: 4.1 常用表格数据的处理 · 4.2 大数据处理 · 4.3 大数据典型应用
  - 第五章 人工智能及应用: 5.1 人工智能的产生与发展 · 5.2 人工智能的应用 · 5.3 人工智能对社会的影响
- 浙教版 3.2 sub-lessons, from teaching-resource listings (not the textbook itself): one listing names 「3.2.1 python 数据类型与表达式」 ([zxxk](https://www.zxxk.com/soft/49369545.html)). Another, per search summary, lists 「3.2.1 Python基本语法知识、3.2.2 顺序结构的程序实现」 ([21cnjy](https://mip.21cnjy.com/mulu/8/178759-1.html)). Both indicate data types/expressions open the Python section. A teacher's code repository for the 浙教 book notes the textbook's IDLE screenshots show Python 3.7.0 (search-result summary). — [cnblogs BobHuang](https://cnblogs.com/BobHuang/p/15621121.html)
- **教科版 (2019) 必修1**: per a search summary, its 「第2单元 编程计算」 covers 计算机解决问题的过程、分支、循环和可复用代码. I could not open the page (HTTP 403). — [51jiaoxi 教科版目录](https://www.51jiaoxi.com/xx/tb_b3000065/)

### Inferences
- This is the strongest authoritative precedent for a "start from data" first stage. The national standards (both 学段) and both textbooks checked put 「数据的特征 / 编码 / 数字化（二进制）」 **before** algorithms and programming. They frame data as 「后续学习的基础」.
- In 人教中图版 the in-programming order is **数据类型 → 常量、变量及表达式 → 程序语句 → 程序结构**: types first, then variables/expressions, then control structures. This matches a 「认识不同的数据格式和特点」 → variables → control-flow progression.
- The standards treat "data format" at two levels: encoding/representation (数字、字母、文字编码; 二进制; 编码长度与信息量; 压缩/校验) and organization/presentation (数据的组织与呈现; 表格数据; 可视化). A beginner platform could map these onto (a) Python literal types (int/float/str/bool/None) and (b) structured formats (table/CSV, key-value/JSON).
- The 2022 standard's note that reading, modifying and running programs counts as meaningful experience supports "read/modify-first" exercise types in an early stage.

### Gaps
- The textbook tables of contents come from a third-party e-textbook mirror (dzkbw.com), not from the publishers (人民教育出版社/中国地图出版社, 浙江教育出版社). The sub-lessons of 浙教 3.2 are not verified from the textbook itself.
- I did not retrieve tables of contents for 粤教版, 沪教版, 华东师大版, 教科版 or 北师大版 必修1, or for any 选择性必修1《数据与数据结构》 textbook.
- The 2022 compulsory standard does not name a programming language. I found no official statement on which grade first uses a text-based language.

---

## Q4. Popular free tutorials & bootcamps: first ~10 sections in order

### Takeaway
Every popular resource checked follows the same pattern: environment/hello-world → (comments/print) → **variables + basic data types (int/float/str/bool, type conversion)** → operators → input → if → loops. Data types always come before control flow. Composite types (list/dict) come either right after the scalar types (廖雪峰) or after loops/functions (黑马, NCRE-style). None of them starts from data *formats* (CSV/JSON); file and data-format topics are mid-to-late.

### Cited Findings
**廖雪峰 Python 教程**. Source for this block: [liaoxuefeng.com 简介/目录](https://liaoxuefeng.com/books/python/introduction/index.html)
- Top level: 1 简介 · 2 Python历史 · 3 安装Python（3.1 Python解释器）· 4 第一个Python程序（4.1 使用文本编辑器 · 4.2 输入和输出）· **5 Python基础** · 6 函数 · 7 高级特性 · 8 函数式编程 · 9 模块 · 10 面向对象编程 · … · 13 IO编程 · … · 21 访问数据库 · …
- 「Python基础」 sub-sections in order: **5.1 数据类型和变量 · 5.2 字符串和编码** · 5.3 使用list和tuple · 5.4 条件判断 · 5.5 模式匹配 · 5.6 循环 · 5.7 使用dict和set.
- Self-description: 「小白的Python新手教程」, 「零起点」, 「基于最新的Python 3版本」.
- The 「数据类型和变量」 page lists 整数 · 浮点数 · 字符串 · 布尔值 · 空值, then 变量 and 常量. — [liaoxuefeng 数据类型和变量](https://liaoxuefeng.com/books/python/basic/data-types/index.html)

**菜鸟教程 Python3 (runoob.com)**
- The runoob pages for 「Python3 基础语法」 and 「Python3 基本数据类型」 exist as separate early pages. The data-type page teaches that variables need no declaration and are created on assignment. — [runoob 基本数据类型](https://www.runoob.com/python3/python3-data-type.html), [runoob 基础语法](https://www.runoob.com/python3/python3-basic-syntax.html) (via search summary; the site returned Cloudflare 521 throughout this session)

**黑马程序员** 「黑马程序员python零基础全套教程，8天python从入门到精通」 (Bilibili, uploaded 2022-08-08). Source for this block: [Bilibili BV1qW4y1a7fU](https://www.bilibili.com/video/BV1qW4y1a7fU/)
- 第一章: 初识Python · 什么是编程语言 · Python环境安装 · 第一个Python程序-HelloWorld · 练习讲解 · 「第一个Python程序-常见问题解答」 · Python解释器 · PyCharm…
- **第二章 (Python基础语法), in order: 01 字面量 · 02 注释 · 03 变量 · 04 数据类型 · 05 数据类型转换 · 06 标识符 · 07 运算符 · 08 字符串的三种定义方式 · 09 字符串的拼接 · 10 字符串格式化 · 11 字符串格式化的精度控制 · 12 字符串格式化的方式2 · 13 对表达式进行格式化 · 14 字符串格式化练习题讲解 · 15 数据输入(input语句)**
- 第三章: 01 布尔类型和比较运算符 · 02 if语句的基本格式 · … · if else · if_elif_else · 判断语句的嵌套
- 第四章: while循环 · … · for循环的基础语法 · range语句 · for循环临时变量作用域 · … · continue和break

**尚硅谷** 「尚硅谷Python视频教程，0基础入门学习python，轻松掌握python」 (Bilibili, 2024-03-19, 139 episodes). Source for this block: [Bilibili av1151955951](https://www.bilibili.com/video/av1151955951/)
- 001 课程简介 · 002–005 初识python（介绍/安装）· 006 第1个程序-新建项目 · 007 注释 · 008 打印变量 · 009 一行打印多个内容 · 010 格式化输出 · 011 input · **012 初识python-流程图** · 013–014 总结/练习
- **015 变量的创建 · 016 变量的修改 · 017 变量的命名 · 018 变量的类型 · 019 数据类型-整数 · 020 浮点数 · 021 布尔型 · 022 字符串 · 023 字符串索引 · 024 类型转换 · 025 小整数地址** · 026–027 总结/练习
- 028–036 运算符（算数、赋值、比较、逻辑、位、成员、优先级）
- 037–044 条件判断（单分支、双分支、多分支、嵌套选择、**match**、闰年判断）· 045 循环-while…

**千锋教育** 「千锋教育Python全套视频教程800集（完整版）」 (Bilibili, 2019-09-27). Source for this block: [Bilibili av69060979](https://www.bilibili.com/video/av69060979)
- 00 学前必看 · 01 python简介 · 02 python特点 · 03 安装与配置 · 04 pip包管理命令 · 05 安装问题总结 · 06 第一个python小程序 · 07 介绍命名规则 · **08 变量 · 09 变量命名规则** · 10 回顾 · 11 print使用 · 12 转义字符 · **13 字符串和常量** · 14 格式化输出 · 15 格式化使用%s,%d和%f · 16 format格式化方式 · **17 input输入之捕鱼达人** · 18 练习英雄联盟 · 19 赋值运算符及内存分析 · 20 算术运算符 · 22 关系运算符 · 23 逻辑运算符 · **24 二进制+八进制+十进制** · 25–26 位运算 · 27 三目与运算符优先级 · 28 if语句 · … · 31 循环for · … · 36 while循环

### Inferences
- Consensus first-10 ordering for Chinese beginner material: 环境/HelloWorld → 注释/print → 变量 → 数据类型（int/float/bool/str）→ 类型转换 → 运算符 → 字符串格式化 → input → 布尔/比较 → if → loops.
- 廖雪峰 is unusual in putting 「字符串和编码」 (ASCII/Unicode/UTF-8) as the 2nd lesson and list/tuple before `if`. It is the closest mainstream tutorial to a "representation first" stage. 千锋 includes number bases (二进制/八进制/十进制) early, which matches the 课标's 「二进制与数制转换」.
- 黑马 starts the syntax chapter with 「字面量」 (literals, i.e. "what kinds of values exist") before variables. That is a concrete precedent for a "认识数据" opening: show values of different types before naming them.
- 尚硅谷 inserts 「流程图」 before variables, and its 2024 course teaches `match`, which differs from NCRE's ≤3.9 environment.

### Gaps
- **菜鸟教程 sidebar order was not verified.** runoob.com returned HTTP 521 on every attempt, and web.archive.org could not be fetched. From prior knowledge, *unverified this session*, the order is roughly: 简介 → 环境搭建 → 基础语法 → 基本数据类型 → 数据类型转换 → 解释器 → 注释 → 运算符 → 数字(Number) → 字符串 → 列表 → 元组 → 字典 → 集合 → 条件控制 → 循环语句 → 编程第一步 → … Treat this as a hypothesis to recheck.
- Bootcamp outlines come from public Bilibili episode lists, not from paid-course syllabus pages. 黑马's and 千锋's current (2025–2026) paid bootcamp syllabi were not checked. The 千锋 list is a 2019 upload.
- 千锋 and 黑马 have newer "2024/2025版" uploads (a 648-episode and a 370-episode series appeared in search results); their episode lists were not verified.

---

## Q5. Common Chinese beginner pain points noted by these sources

### Takeaway
The recurring pain points are:
- `input()` always returns a string, so 字符串 vs 数字 confusion causes TypeError/ValueError and needs int()/float()
- `/` vs `//` vs `%` (整除、取余, and `/` always giving a float)
- `=` as assignment rather than mathematical equality
- None ≠ 0
- float rounding error
- 缩进 (IndentationError)
- full-width Chinese punctuation (`：`, `（）`) causing `SyntaxError: invalid character`

The curricula build in type conversion explicitly: NCRE's 「类型判断和类型间转换」, 黑马's 「数据类型转换」 lesson right before 「数据输入(input语句)」, and 尚硅谷's 「类型转换」.

### Cited Findings
- **input returns str**: runoob's input() page states that whatever is entered, the return value is always a string, and numeric use needs explicit conversion (int()/float()). It also notes that `int("1.5")` raises ValueError and needs float(). — [runoob input()](https://www.runoob.com/python3/python3-func-input.html) (via search summary; site unreachable for direct fetch). English corroboration: TypeError when doing `//` or `%` on an un-converted input string — [BU CS111 common errors](https://www.cs.bu.edu/courses/cs111/problem_sets/errors.shtml)
- NCRE puts `eval()` alongside `input()` as a core I/O function (「基本输入输出函数：input()、eval()、print()」), the classic `eval(input())` pattern for getting numbers. It also lists 「类型判断和类型间转换」 as a data-type exam point. — [NCRE Python 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf)
- **Division**: 「`/`除法计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数」 (`9 / 3` → `3.0`). 「`//`，称为地板除」 (`10 // 3` → `3`). The remainder is `%` (`10 % 3` → `1`). — [廖雪峰 数据类型和变量](https://liaoxuefeng.com/books/python/basic/data-types/index.html)
- **Assignment vs equality**: 「请不要把赋值语句的等号等同于数学的等号。」 — [廖雪峰](https://liaoxuefeng.com/books/python/basic/data-types/index.html)
- **Other 廖雪峰 points**: None is not 0 (0 is a meaningful value). Quotes are not part of the string (「`''`或`""`本身只是一种表示方式，不是字符串的一部分」). Float arithmetic 「可能会有四舍五入的误差」. Constants are a naming convention only. — [廖雪峰](https://liaoxuefeng.com/books/python/basic/data-types/index.html)
- **Hello-world troubleshooting** is a whole lesson: 黑马 has a dedicated episode 「第一个Python程序-常见问题解答」. 千锋 has 「安装问题总结」. — [黑马 BV1qW4y1a7fU](https://www.bilibili.com/video/BV1qW4y1a7fU/), [千锋 av69060979](https://www.bilibili.com/video/av69060979)
- **Indentation**: NCRE lists 「缩进」 as the second item among basic syntax elements. — [NCRE Python 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf). "expected an indented block" / "unexpected indent" are the typical errors — [BU CS111](https://www.cs.bu.edu/courses/cs111/problem_sets/errors.shtml)
- **Full-width punctuation**: a Chinese Q&A attributes `SyntaxError: invalid character` to using a Chinese colon (or comma) instead of the English one; the fix is to retype it with an English input method. — [CSDN 文库](https://wenku.csdn.net/answer/2os29aknjz) (low-authority source); corroborated by [DEV Community](https://dev.to/lavary/how-to-fix-syntaxerror-invalid-character-in-python-28ie)

### Inferences
- For a Chinese-UI platform, the full-width-punctuation problem is specific to Chinese-IME users and deserves first-class handling: detect `：（），“”` in code and give a friendly hint.
- A "认识数据" first stage that makes 字符串 vs 数字 visible (e.g. `"5"` vs `5`, `type()`, what `input()` gives back, `/` vs `//`) directly targets the most-cited pain points before control flow adds complexity. This matches NCRE's placement of type conversion and comparisons inside 基本数据类型.

### Gaps
- I found no authoritative Chinese study (e.g. a 教研 paper with data) ranking beginner errors. The points above come from tutorial authors and a low-authority Q&A site, not from empirical research.
- runoob's 「Python3 注释/运算符」 pages and their beginner warnings were not readable directly (site down).

---

## Q6 (synthesis of the objective). Do authoritative Chinese curricula start from data before control flow?

### Takeaway
Yes, at two different granularities. (1) The **national IT standards and textbooks** start with *data as a concept*: 数据与信息的特征, 编码, 二进制/数字化, 数据的组织与呈现. Programming comes after, and the 人教中图 programming section itself opens with 数据类型. (2) **Programming syllabi** (NCRE, 嵩天, 廖雪峰, 黑马, 尚硅谷, 千锋) start with *data types* (int/float/str/bool, conversion, operators) before control flow. Structured *data formats* (一维/二维数据, CSV, JSON) are consistently late. No authoritative source opens with file formats.

### Cited Findings
- 必修1 order is 数据与信息（1.1 特征与编码）→ 数据处理与应用（1.4–1.5）→ 算法与程序实现（1.6–1.7）. — [MOE 高中课标 2017/2020](http://www.moe.gov.cn/srcsite/A26/s8001/202006/t20200603_462199.html)
- 义务教育: 「数据与编码」 (3–4年级) comes before 「身边的算法」「过程与控制」 (5–6年级). — [MOE 义务教育信息科技课标 2022 PDF](http://www.moe.gov.cn/srcsite/A26/s8001/202204/W020220420582361024968.pdf)
- 人教中图版: 第1章 认识数据与大数据（含 数字化与编码）before 第2章 算法与程序实现, whose 2.3 starts 「2.3.1 数据类型」. — [dzkbw 人教中图版](http://www.dzkbw.com/books/rjb/xinxijishu/gzbx1/)
- 浙教版: 第一章 数据与信息（含 数据采集与编码）before 第二章 算法 and 第三章 Python. — [dzkbw 浙教版](http://www.dzkbw.com/books/zjb/xinxijishu/gzbx1/002.htm)
- NCRE: 二、基本数据类型 before 三、程序的控制结构; 六、文件和数据格式化 (一维/二维数据, CSV) comes 6th. — [NCRE Python 2025](https://jxjy.yznu.edu.cn/_upload/article/files/ba/d9/7ef53e5f49a6a178b0032e40f6b9/5809d0d3-3b83-4bf5-8017-e09cc366138a.pdf)
- 嵩天 MOOC: 基本数据类型 in week 3, 文件和数据格式化 in week 7. — [Bilibili BV1JL4y1x7xC](https://www.bilibili.com/video/BV1JL4y1x7xC/)

### Inferences
- A first stage titled 「认识不同的数据格式和特点」 has solid official backing if it is framed at the 课标 level: what data is, how it is encoded and represented (numbers vs text vs true/false vs "nothing"), and how data is organized (single value → list → table). That is 数据的组织与呈现 / 一维·二维数据. The platform can borrow official vocabulary: 「数据与信息的特征」「数据编码」「数据的组织与呈现」「一维数据、二维数据」「类型判断和类型间转换」.
- Introducing CSV/JSON-like formats *as things to look at and recognize* (not parse with file I/O) in stage 1 departs from every programming syllabus checked, but it is consistent with the standards' 「感知数据」 and 「数据的组织与呈现」 framing. The 2022 standard explicitly values reading and modifying given programs over writing from scratch, which fits a "recognize/compare formats" activity style.
- Suggested concrete alignment, an inference rather than a sourced claim: Stage 1 = 字面量与数据类型 (黑马-style 「字面量」 → int/float/str/bool/None, type(), conversion, input() returns str) + 数据的组织 (one value vs a list of values vs a table/CSV row-column vs key-value/JSON object). Then variables/expressions (人教中图 2.3.2) → control structures.

### Gaps
- No Chinese authoritative curriculum was found that teaches JSON at the beginner level. Whether 嵩天's textbook (第3版) covers JSON is unverified.
- No official source was found that sequences "data formats (CSV/JSON)" before variables or control flow. That ordering would be the platform's own design choice.
