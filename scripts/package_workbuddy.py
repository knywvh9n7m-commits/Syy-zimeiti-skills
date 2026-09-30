"""Package the shared Skill body with WorkBuddy-compatible frontmatter."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "syy-zimeiti-skills"
FRONTMATTER = """---
name: syy-zimeiti-skills
display_name: Syy-zimeiti-skills
description: 研究指定社交平台的趋势、对标账号、评论需求和选题机会，默认使用公开网页，不调用付费数据接口。
description_zh: 使用公开网页研究社媒趋势、对标、评论需求和选题；默认不调用付费数据接口。
description_en: Research public social content, creators, audience questions, and content ideas without paid data APIs by default.
version: 0.2.0
author: Syy
license: MIT
---
"""


def package(output: Path) -> None:
    source = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n.*?\r?\n---\r?\n", source, re.S)
    if not match:
        raise ValueError("SKILL.md frontmatter is missing")
    body = source[match.end() :]
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as bundle:
        for path in sorted(SKILL_DIR.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            relative = Path("syy-zimeiti-skills") / path.relative_to(SKILL_DIR)
            if path.name == "SKILL.md" and path.parent == SKILL_DIR:
                bundle.writestr(relative.as_posix(), FRONTMATTER + body)
            else:
                bundle.write(path, relative.as_posix())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    package(parser.parse_args().out)
