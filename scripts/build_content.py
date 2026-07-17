from pathlib import Path
import csv
import hashlib
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".m4v"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv"}
PUBLIC_EXCLUDED_GROUPS = {"汇报文件包"}
VISUAL_INDEX_PATH = ROOT / "assets/ecommerce/视觉资产索引.json"
VISUAL_ROOTS = {
    "hero": ROOT / "assets/ecommerce/首图",
    "detail": ROOT / "assets/ecommerce/商详页",
    "home": ROOT / "assets/ecommerce/首页",
}


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


def visual_asset_id(*parts: str) -> str:
    source = "/".join(parts)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", source).strip("-").lower()
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:8]
    return f"{slug or 'visual'}-{digest}"


def site_asset_path(path: str) -> str:
    clean = path.removeprefix("./assets/").removeprefix("assets/")
    return f"./assets/{clean}"


def normalize_visual_collection(collection: dict) -> dict:
    normalized = dict(collection)
    normalized.setdefault("id", visual_asset_id(
        normalized.get("type", "visual"),
        normalized.get("product", "待归档"),
        normalized.get("platform", "未标平台"),
        normalized.get("version", "未标版本"),
    ))
    normalized.setdefault("project", "待关联项目")
    normalized.setdefault("product", "待归档")
    normalized.setdefault("platform", "未标平台")
    normalized.setdefault("version", "未标版本")
    normalized.setdefault("date", "")
    normalized.setdefault("status", "待整理")
    normalized.setdefault("note", "")
    normalized.setdefault("metrics", [])

    media = []
    for item in normalized.get("media", []):
        if isinstance(item, str):
            item = {"path": item, "title": Path(item).stem}
        entry = dict(item)
        path = entry.pop("path", entry.get("src", ""))
        if not path:
            continue
        entry["src"] = site_asset_path(path)
        entry.setdefault("title", Path(path).stem)
        entry.setdefault("kind", "video" if Path(path).suffix.lower() in VIDEO_EXTENSIONS else "image")
        media.append(entry)
    normalized["media"] = media
    return normalized


def read_visual_metrics(version_dir: Path) -> list[dict[str, str]]:
    data_path = version_dir / "_数据.csv"
    if not data_path.exists():
        return []
    with data_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def scan_visual_folders() -> list[dict]:
    collections = []
    for visual_type, base in VISUAL_ROOTS.items():
        if not base.exists():
            continue
        grouped: dict[tuple[str, str, str], list[Path]] = {}
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
                continue
            rel = path.relative_to(base)
            folders = rel.parts[:-1]
            product = folders[0] if len(folders) >= 1 else "待归档"
            platform = folders[1] if len(folders) >= 2 else "未标平台"
            version = folders[2] if len(folders) >= 3 else path.stem
            grouped.setdefault((product, platform, version), []).append(path)

        for (product, platform, version), media_paths in grouped.items():
            version_dir = base / product / platform / version
            meta_path = version_dir / "_版本说明.json"
            metadata = {}
            if meta_path.exists():
                metadata = json.loads(meta_path.read_text(encoding="utf-8"))
            collection = {
                "id": visual_asset_id(visual_type, product, platform, version),
                "type": visual_type,
                "project": metadata.get("project", "待关联项目"),
                "product": metadata.get("product", product),
                "platform": metadata.get("platform", platform),
                "version": metadata.get("version", version),
                "date": metadata.get("date", ""),
                "status": metadata.get("status", "待整理"),
                "note": metadata.get("note", ""),
                "metrics": metadata.get("metrics", read_visual_metrics(version_dir)),
                "media": [
                    {
                        "path": path.relative_to(ROOT / "assets").as_posix(),
                        "title": path.stem,
                    }
                    for path in media_paths
                ],
            }
            collections.append(normalize_visual_collection(collection))
    return collections


def build_visual_assets() -> list[dict]:
    manual = []
    if VISUAL_INDEX_PATH.exists():
        payload = json.loads(VISUAL_INDEX_PATH.read_text(encoding="utf-8"))
        manual = [normalize_visual_collection(item) for item in payload.get("collections", [])]

    combined = {collection["id"]: collection for collection in scan_visual_folders()}
    combined.update({collection["id"]: collection for collection in manual})
    return sorted(
        combined.values(),
        key=lambda item: (item.get("type", ""), item.get("date", ""), item.get("version", "")),
        reverse=True,
    )


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
    visual_assets = build_visual_assets()
    visual_output = DOCS_ROOT / "visual-assets.js"
    visual_output.write_text(
        "window.CHANGFA_VISUAL_ASSETS = "
        + json.dumps(visual_assets, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(docs)} docs to {output}")
    print(f"Wrote {len(visual_assets)} visual collections to {visual_output}")


if __name__ == "__main__":
    main()
