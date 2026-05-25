from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List
from urllib.parse import quote_plus
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""
    source: str = "duckduckgo"


RESULT_RE = re.compile(
    r'<a rel="nofollow" class="result__a" href="(.*?)".*?>(.*?)</a>.*?result__snippet">(.*?)</a>',
    re.S,
)


def _strip_html(text: str) -> str:
    return re.sub(r"<.*?>", "", text)


def _fallback_results(query: str, max_results: int) -> List[SearchResult]:
    return [
        SearchResult(
            title=f"{query} 公开资料示例 {idx + 1}",
            url=f"https://example.com/{quote_plus(query)}/{idx + 1}",
            snippet=f"用于在网络不可用时保持流水线可运行的占位结果 {idx + 1}",
            source="fallback",
        )
        for idx in range(max_results)
    ]


def duckduckgo_search(query: str, max_results: int = 10) -> List[SearchResult]:
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except (URLError, TimeoutError, OSError):
        return _fallback_results(query, max_results)

    results: List[SearchResult] = []
    for href, title_html, snippet_html in RESULT_RE.findall(html)[:max_results]:
        results.append(
            SearchResult(
                title=_strip_html(title_html).strip(),
                url=href.strip(),
                snippet=_strip_html(snippet_html).strip(),
            )
        )

    if not results:
        fallback = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)".*?>(.*?)</a>', html, re.S)
        for href, title_html in fallback[:max_results]:
            results.append(
                SearchResult(
                    title=_strip_html(title_html).strip(),
                    url=href.strip(),
                )
            )

    if not results:
        return _fallback_results(query, max_results)

    return results


def normalize_search_results(results: List[SearchResult]) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for item in results:
        normalized.append(
            {
                "title": item.title,
                "url": item.url,
                "snippet": item.snippet,
                "type": "web",
                "source": item.source,
            }
        )
    return normalized
