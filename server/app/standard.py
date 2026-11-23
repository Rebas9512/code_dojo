"""正式通过后供学习者对照的标准写法。"""

import re

from pydantic import BaseModel

from .problems import Problem


class StandardAnswer(BaseModel):
    code: str
    language: str
    notes_md: str = ""
    advanced_md: str = ""
    has_notes: bool = False


# 跳过围栏里的内容，Python 注释也可能以二级标题的形式开头。
MARKDOWN_PART = re.compile(
    r"^```(?P<language>[^\n`]*)\n(?P<code>[\s\S]*?)^```[ \t]*$|^## (?P<title>[^\n]+)$", re.MULTILINE,
)


def note_sections(markdown: str) -> list[tuple[str, str]]:
    headings = [match for match in MARKDOWN_PART.finditer(markdown) if match["title"]]
    ends = [heading.start() for heading in headings[1:]] + [len(markdown)]
    return [(heading["title"].strip(), markdown[heading.end():end].strip()) for heading, end in zip(headings, ends)]


def standard_answer(problem: Problem) -> StandardAnswer:
    language = problem.track.language
    suffix = "sql" if language == "sql" else "py"
    code = problem.read(f"standard.{suffix}")
    if code is None:
        solution = problem.file(f"solution.{suffix}").read_text(encoding="utf-8")
        return StandardAnswer(code=solution, language=language)

    notes = []
    advanced = ""
    for title, body in note_sections(problem.read("standard.md") or ""):
        section = f"## {title}\n\n{body}"
        if title == "进阶写法":
            advanced = section
        else:
            notes.append(section)
    return StandardAnswer(code=code, language=language, notes_md="\n\n".join(notes), advanced_md=advanced, has_notes=bool(notes))
