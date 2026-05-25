from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Wikipedia pages for skill distillation")
    parser.add_argument("--query", required=True, help="Wikipedia page title or search term")
    parser.add_argument("--lang", default="en", help="Wikipedia language, e.g. en, zh")
    parser.add_argument("--output-dir", default="research/raw/wiki", help="Output directory")
    parser.add_argument("--output-name", default=None, help="Optional base filename override")
    return parser.parse_args()


def fetch_url(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def strip_tags(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if not m:
        return "Wikipedia Page"
    return re.sub(r"\s*-\s*Wikipedia.*$", "", m.group(1).strip(), flags=re.I)


def fetch_wikipedia_page(query: str, lang: str) -> dict:
    page_url = f"https://{lang}.wikipedia.org/wiki/{quote(query.replace(' ', '_'))}"
    html = fetch_url(page_url)
    title = extract_title(html)
    text = strip_tags(html)

    return {
        "title": title,
        "url": page_url,
        "lang": lang,
        "content": text,
    }


def save_result(result: dict, output_dir: str, output_name: str | None = None) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    base_name = output_name or result["title"]
    safe_name = re.sub(r"[^a-zA-Z0-9_\-\u4e00-\u9fff]+", "_", base_name).strip("_") or "wikipedia_page"

    json_path = out / f"{safe_name}.json"
    txt_path = out / f"{safe_name}.txt"

    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    txt_path.write_text(
        f"Title: {result['title']}\nURL: {result['url']}\nLanguage: {result['lang']}\n\n{result['content']}\n",
        encoding="utf-8",
    )

    index_path = out / "index.txt"
    with index_path.open("a", encoding="utf-8") as f:
        f.write(f"{result['title']} | {result['url']}\n")


def main() -> int:
    args = parse_args()

    try:
        result = fetch_wikipedia_page(args.query, args.lang)
    except Exception as exc:
        print(f"Failed to fetch Wikipedia page: {exc}")
        return 1

    save_result(result, args.output_dir, args.output_name)
    print(f"Fetched Wikipedia page: {result['title']}")
    print(f"Saved to: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
