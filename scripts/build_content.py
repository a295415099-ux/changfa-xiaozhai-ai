from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]


SOURCE_GROUPS = [
    ("汇报文件包", ROOT / "reports/品牌设计部AI汇报文件包", [
        "00_*.md",
        "01_*.md",
        "02_*.md",
        "03_*.md",
        "04_*.md",
        "05_*.md",
        "06_*.md",
        "07_*.md",
        "08_*.md",
        "09_*.md",
        "10_*.md",
        "99_*.md",
    ]),
    ("模板库", ROOT / "templates", ["*.md"]),
    ("架构与总控", ROOT, ["长发小寨专属Codex蓝图.md"]),
    ("架构与总控", ROOT / "skills/changfa-xiaozhai-codex", ["SKILL.md"]),
    ("架构与总控", ROOT / "skills/changfa-xiaozhai-codex/references", ["*.md"]),
    ("Jessie Skill库", ROOT / "jessie-skills", ["_skill_manifest.md"]),
    ("资料库说明", ROOT / "assets", ["_资料投放说明.md", "*/README.md"]),
]


def doc_id_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return re.sub(r"[^a-zA-Z0-9]+", "-", rel).strip("-").lower()


def title_for(text: str, path: Path) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else path.stem


def build_docs() -> list[dict[str, str]]:
    entries = []
    seen = set()
    for group, base, patterns in SOURCE_GROUPS:
        for pattern in patterns:
            for path in sorted(base.glob(pattern)):
                if path in seen or not path.exists():
                    continue
                seen.add(path)
                text = path.read_text(encoding="utf-8")
                entries.append({
                    "id": doc_id_for(path),
                    "title": title_for(text, path),
                    "group": group,
                    "path": path.relative_to(ROOT).as_posix(),
                    "markdown": text,
                })
    return entries


def main() -> None:
    docs = build_docs()
    output = ROOT / "docs/content.js"
    output.write_text(
        "window.CHANGFA_DOCS = "
        + json.dumps(docs, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(docs)} docs to {output}")


if __name__ == "__main__":
    main()
