from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from .distill_config import DistillConfig
from .exporter import distill_skill_schema, save_prompt_pack, save_skill_markdown, save_skill_schema
from .quality import quality_check_file
from .search import duckduckgo_search, normalize_search_results


DEFAULT_RESEARCH_DIR = Path("research")
DEFAULT_GENERATED_DIR = Path("generated")


def ensure_dirs() -> None:
    (DEFAULT_RESEARCH_DIR / "raw").mkdir(parents=True, exist_ok=True)
    (DEFAULT_RESEARCH_DIR / "cleaned").mkdir(parents=True, exist_ok=True)
    (DEFAULT_RESEARCH_DIR / "merged").mkdir(parents=True, exist_ok=True)
    (DEFAULT_RESEARCH_DIR / "reports").mkdir(parents=True, exist_ok=True)
    DEFAULT_GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def search_public_sources(query: str) -> List[Dict[str, str]]:
    results = duckduckgo_search(query, max_results=10)
    normalized = normalize_search_results(results)
    return normalized


def fetch_sources_to_research(query: str) -> List[Dict[str, str]]:
    ensure_dirs()
    sources = search_public_sources(query)
    raw_dir = DEFAULT_RESEARCH_DIR / "raw"
    (raw_dir / "sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding="utf-8")
    (raw_dir / "source_links.txt").write_text("\n".join(item["url"] for item in sources) + "\n", encoding="utf-8")
    return sources


def build_seed_materials(query: str, sources: List[Dict[str, str]]) -> List[str]:
    materials: List[str] = []
    for item in sources:
        materials.append(
            f"标题: {item.get('title')}\nURL: {item.get('url')}\n类型: {item.get('type')}\n摘要: {item.get('snippet', '')}\n主题: {query}"
        )
    return materials


def distill_from_query(query: str, config_path: str = "distill_config.yaml") -> Tuple[dict, Path, Path, Path]:
    ensure_dirs()
    sources = fetch_sources_to_research(query)
    materials = build_seed_materials(query, sources)

    config = DistillConfig.load(config_path)
    skill_id = f"pangu.{query.strip().lower().replace(' ', '-')}.001"
    name = f"{query} Skill"
    schema = distill_skill_schema(materials, skill_id=skill_id, name=name, config=config)

    schema_path = DEFAULT_GENERATED_DIR / "distilled_skill.yaml"
    markdown_path = DEFAULT_GENERATED_DIR / "SKILL.md"
    prompt_pack_path = DEFAULT_GENERATED_DIR / "prompt_pack.md"

    save_skill_schema(schema, schema_path)
    save_skill_markdown(schema, markdown_path)
    save_prompt_pack(schema, prompt_pack_path)

    return schema, schema_path, markdown_path, prompt_pack_path


def quality_report_for_schema(schema_path: Path) -> Path:
    ensure_dirs()
    report_path = DEFAULT_RESEARCH_DIR / "reports" / "quality_report.md"
    quality_check_file(schema_path, report_path)
    return report_path
