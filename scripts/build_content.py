from pathlib import Path
import hashlib
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv"}
PUBLIC_EXCLUDED_GROUPS = {"汇报文件包"}


SOURCE_GROUPS = [
    ("总控导航", ROOT / "reports/总控台导航", ["00_*.md"]),
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
        "11_*.md",
        "12_*.md",
        "13_*.md",
        "14_*.md",
        "99_*.md",
    ]),
    ("模板库", ROOT / "templates", ["*.md"]),
    ("架构与总控", ROOT, ["长发小寨专属Codex蓝图.md"]),
    ("架构与总控", ROOT / "skills/changfa-xiaozhai-codex", ["SKILL.md"]),
    ("架构与总控", ROOT / "skills/changfa-xiaozhai-codex/references", ["*.md"]),
    ("Jessie Skill库", ROOT / "jessie-skills", ["_skill_manifest.md"]),
    ("AI项目执行", ROOT / "projects", ["**/*.md"]),
    ("竞品分析", ROOT / "reports/竞品分析", ["*.md"]),
    ("资料库说明", ROOT / "assets", ["_资料投放说明.md", "*/README.md"]),
    ("电商资料库", ROOT / "assets/ecommerce", ["*/README.md"]),
]


def doc_id_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", rel).strip("-").lower()
    digest = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:8]
    return f"{slug or 'doc'}-{digest}"


def title_for(text: str, path: Path) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else path.stem


def markdown_asset_gallery(readme_path: Path) -> str:
    asset_files = [
        path for path in sorted(readme_path.parent.iterdir())
        if path.is_file() and path.name not in {"README.md", ".DS_Store"}
    ]
    if not asset_files:
        return ""

    lines = ["", "## 已收录素材", ""]
    for path in asset_files:
        rel = path.relative_to(ROOT / "assets").as_posix()
        site_path = f"./assets/{rel}"
        title = path.stem
        suffix = path.suffix.lower()
        if suffix in IMAGE_EXTENSIONS:
            lines.extend([f"### {title}", "", f"![{title}]({site_path})", ""])
        elif suffix in VIDEO_EXTENSIONS:
            lines.extend([f"### {title}", "", f"[打开视频素材]({site_path})", ""])
        elif suffix in DOCUMENT_EXTENSIONS:
            lines.extend([f"- [{path.name}]({site_path})"])
        else:
            lines.extend([f"- [{path.name}]({site_path})"])
    return "\n".join(lines).rstrip() + "\n"


def sync_assets_for_site() -> None:
    source = ROOT / "assets"
    target = DOCS_ROOT / "assets"
    if not source.exists():
        return

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    for path in source.rglob("*"):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        rel = path.relative_to(source)
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def build_docs() -> list[dict[str, str]]:
    entries = []
    seen = set()
    for group, base, patterns in SOURCE_GROUPS:
        if group in PUBLIC_EXCLUDED_GROUPS:
            continue
        for pattern in patterns:
            for path in sorted(base.glob(pattern)):
                if path in seen or not path.exists():
                    continue
                seen.add(path)
                text = path.read_text(encoding="utf-8")
                if path.name == "README.md" and ROOT / "assets" in path.parents:
                    text = text.rstrip() + "\n" + markdown_asset_gallery(path)
                entries.append({
                    "id": doc_id_for(path),
                    "title": title_for(text, path),
                    "group": group,
                    "path": path.relative_to(ROOT).as_posix(),
                    "markdown": text,
                })
    return entries


def main() -> None:
    sync_assets_for_site()
    docs = build_docs()
    for index, doc in enumerate(docs, start=1):
        doc["number"] = f"{index:02d}"
    output = DOCS_ROOT / "content.js"
    output.write_text(
        "window.CHANGFA_DOCS = "
        + json.dumps(docs, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(docs)} docs to {output}")


if __name__ == "__main__":
    main()
