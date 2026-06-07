from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .core import connect, ensure_dir, ensure_project, fetch_one, next_id, read_json, rel, root_path, utc_now, write_human_text, write_json
from .p0b import create_run, create_tool_setup_item, write_decision

P1_LIVE_SCOUTS = ["search", "bilibili", "youtube", "wiki_official"]
P1_CAPABILITY_PROBES = ["douyin", "xiaohongshu"]
P1_SCORE_WEIGHTS = {
    "heat": 0.18,
    "growth": 0.20,
    "freshness": 0.12,
    "repetition_signal": 0.12,
    "comment_sentiment": 0.12,
    "transferability": 0.10,
    "asset_readiness": 0.07,
    "tool_readiness": 0.06,
    "source_confidence": 0.08,
    "fatigue_penalty": -0.15,
}
LIVE_ALLOWED_STATES = {"allow", "allow_with_limits"}
P1_SCOUT_MODES = {"fixture", "auto", "live"}
YOUTUBE_SEARCH_MAX_RESULTS = 5


def _run_dir(root: Path, run_id: str, *parts: str) -> Path:
    return root / "runs" / run_id / "p1_research" / Path(*parts)


def _policy_for_guess(source_type: str) -> tuple[str, str]:
    if source_type == "official":
        return "direct_use", "not_required"
    if source_type in {"wiki", "search_result"}:
        return "reference_only", "not_required"
    return "analysis_only", "pending"


def _permission_value(root: Path, capability: str, default: str = "ask") -> str:
    try:
        return str(read_json(root / "config" / "permissions.json").get("permissions", {}).get(capability, default))
    except FileNotFoundError:
        return default


def _secrets(root: Path) -> dict[str, Any]:
    path = root / "config" / "secrets.local.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _youtube_api_key(root: Path) -> str | None:
    env_key = os.environ.get("YOUTUBE_API_KEY")
    if env_key:
        return env_key
    youtube = _secrets(root).get("youtube", {})
    if isinstance(youtube, dict):
        key = youtube.get("api_key")
        if isinstance(key, str) and key.strip():
            return key.strip()
    return None


def _live_search_allowed(root: Path, scout_mode: str) -> tuple[bool, list[str]]:
    if scout_mode == "fixture":
        return False, ["scout_mode is fixture"]
    web_search = _permission_value(root, "research.web_search")
    metadata = _permission_value(root, "research.collect_metadata")
    missing: list[str] = []
    if scout_mode == "auto" and web_search not in LIVE_ALLOWED_STATES:
        missing.append(f"research.web_search is {web_search}")
    if metadata not in LIVE_ALLOWED_STATES:
        missing.append(f"research.collect_metadata is {metadata}")
    return not missing, missing


def _query_items(query_plan: dict[str, Any], platform: str) -> list[dict[str, str]]:
    return [query for item in query_plan.get("rounds", []) for query in item.get("queries", []) if query.get("platform") == platform]


def _source_type_from_url(url: str, platform: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    if platform == "wiki_official" or "wikipedia.org" in host or "wiki" in host:
        return "wiki"
    if any(marker in url.lower() for marker in ("official", "mihoyo.com", "hoyoverse.com", "bilibili.com/bangumi")):
        return "official"
    if platform in {"bilibili", "youtube"}:
        return "platform_user"
    if platform == "search":
        return "search_result"
    return "unknown"


def _clean_goal_for_search(goal: str) -> str:
    cleaned = re.sub(r"^\s*(find|discover|research|look for|search for)\s+", "", goal, flags=re.I)
    return re.sub(r"\s+", " ", cleaned).strip() or goal


def _make_candidate(
    *,
    run_id: str,
    platform: str,
    url: str | None,
    title: str,
    query_used: str,
    evidence_mode: str,
    metadata_source: str,
    live_results_claimed: bool,
    author: str | None = None,
    content_type: str = "unknown",
    source_type_guess: str | None = None,
    observed_metrics: dict[str, Any] | None = None,
    published_at: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
    cover_url: str | None = None,
    platform_item_id: str | None = None,
    confidence: float = 0.4,
    capability_gaps: list[str] | None = None,
    requires_review: bool = True,
    notes: str = "",
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "platform": platform,
        "url": url,
        "title": title.strip() or "Untitled source candidate",
        "author": author,
        "account": author,
        "content_type": content_type,
        "source_type_guess": source_type_guess or _source_type_from_url(url or "", platform),
        "observed_metrics": observed_metrics or {"views": None, "likes": None, "comments": None, "shares": None, "favorites": None},
        "published_at": published_at,
        "description": description,
        "tags": tags or [],
        "cover_url": cover_url,
        "platform_item_id": platform_item_id,
        "collected_at": utc_now(),
        "query_used": query_used,
        "evidence_mode": evidence_mode,
        "metadata_source": metadata_source,
        "live_results_claimed": live_results_claimed,
        "confidence": confidence,
        "capability_gaps": capability_gaps or [],
        "requires_review": requires_review,
        "notes": notes,
        "discovery_reason": [evidence_mode, "query", query_used],
    }


def _fetch_text(url: str, timeout: float = 8.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Kairove-P1-Scout/0.1 (+metadata-only; no downloads)"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read(700_000).decode(charset, errors="replace")


def _fetch_text_with_ephemeral_cookies(url: str, bootstrap_url: str, referer: str, timeout: float = 8.0) -> str:
    import http.cookiejar

    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    headers = {"User-Agent": "Mozilla/5.0 Kairove-P1-Scout (+metadata-only; no login)", "Referer": referer}
    opener.open(urllib.request.Request(bootstrap_url, headers=headers), timeout=timeout).read(2048)
    with opener.open(urllib.request.Request(url, headers=headers), timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read(900_000).decode(charset, errors="replace")


def _clean_html_text(value: str) -> str:
    return re.sub(r"\s+", " ", urllib.parse.unquote(re.sub(r"<[^>]+>", " ", value))).strip()


def _clean_bilibili_title(value: str) -> str:
    return _clean_html_text(value.replace("\\u003C", "<").replace("\\u003E", ">").replace("\\/", "/"))


def _search_duckduckgo_lite(query: str, max_results: int = 5) -> tuple[list[dict[str, str]], list[str]]:
    gaps: list[str] = []
    try:
        html = _fetch_text("https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query}))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        html = ""
        gaps.append(f"duckduckgo request failed: {exc}")
    results: list[dict[str, str]] = []
    pattern = r'<a[^>]+class=["\'][^"\']*result__a[^"\']*["\'][^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
    for match in re.finditer(pattern, html, re.I | re.S):
        href = match.group(1)
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        if "uddg" in qs:
            href = qs["uddg"][0]
        if href.startswith("//"):
            href = "https:" + href
        if href.startswith("http"):
            results.append({"url": href, "title": _clean_html_text(match.group(2)), "metadata_source": "duckduckgo_lite"})
        if len(results) >= max_results:
            break
    if results:
        return results, gaps
    gaps.append("duckduckgo page returned no parseable result links")
    bing_results, bing_gaps = _search_bing(query, max_results=max_results)
    return bing_results, gaps + bing_gaps


def _search_bing(query: str, max_results: int = 5) -> tuple[list[dict[str, str]], list[str]]:
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
    try:
        html = _fetch_text(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return [], [f"bing request failed: {exc}"]
    results: list[dict[str, str]] = []
    block_pattern = r'<li[^>]+class=["\'][^"\']*b_algo[^"\']*["\'][^>]*>(.*?)</li>'
    link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
    for block in re.findall(block_pattern, html, re.I | re.S):
        match = re.search(link_pattern, block, re.I | re.S)
        if not match:
            continue
        href = match.group(1)
        title = _clean_html_text(match.group(2))
        href = _decode_bing_redirect(href)
        if href.startswith("http") and title:
            results.append({"url": href, "title": title, "metadata_source": "bing_search_html"})
        if len(results) >= max_results:
            break
    return (results, []) if results else ([], ["bing page returned no parseable result links"])


def _decode_bing_redirect(url: str) -> str:
    parsed = urllib.parse.urlparse(url.replace("&amp;", "&"))
    query = urllib.parse.parse_qs(parsed.query)
    encoded = query.get("u", [None])[0]
    if encoded:
        try:
            import base64

            if encoded.startswith("a1"):
                decoded = base64.urlsafe_b64decode(encoded[2:] + "===")
                return decoded.decode("utf-8", errors="replace")
        except (ValueError, OSError):
            return url
    return url


def _result_is_relevant(result: dict[str, str], platform: str) -> bool:
    text = f"{result.get('title', '')} {result.get('url', '')}".lower()
    if any(noise in text for noise in ("find my iphone", "find-your-phone", "/icloud/find", "learn-find-hub")):
        return False
    if platform == "bilibili":
        return "bilibili.com" in text
    if platform == "youtube":
        return "youtube.com" in text or "youtu.be" in text
    if platform == "wiki_official":
        return "wiki" in text or "official" in text
    relevance_terms = ("ai", "video", "short", "shorts", "trend", "format", "tiktok", "youtube", "bilibili", "douyin", "xiaohongshu")
    return sum(1 for term in relevance_terms if term in text) >= 2


def _wiki_official_results(query: str, max_results: int = 5) -> tuple[list[dict[str, str]], list[str]]:
    params = urllib.parse.urlencode({"action": "opensearch", "search": query, "limit": max_results, "namespace": 0, "format": "json"})
    try:
        data = json.loads(_fetch_text(f"https://en.wikipedia.org/w/api.php?{params}"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return [], [f"wiki opensearch failed: {exc}"]
    return [{"title": title, "url": url} for title, url in zip(data[1] if len(data) > 1 else [], data[3] if len(data) > 3 else [])], []


def _platform_search_query(query: str, platform: str) -> str:
    if platform == "youtube":
        return f"site:youtube.com/shorts OR site:youtube.com/watch {query}"
    if platform == "bilibili":
        return f"site:bilibili.com/video {query}"
    return query


def _bilibili_public_web_results(query: str, max_results: int = 5) -> tuple[list[dict[str, Any]], list[str]]:
    params = urllib.parse.urlencode({"search_type": "video", "keyword": query, "page": 1})
    url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
    try:
        data = json.loads(_fetch_text_with_ephemeral_cookies(url, "https://www.bilibili.com/", "https://www.bilibili.com/"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return [], [f"bilibili public web search failed: {exc}"]
    if data.get("code") != 0:
        return [], [f"bilibili public web search returned code {data.get('code')}"]
    results: list[dict[str, Any]] = []
    for item in data.get("data", {}).get("result", []):
        bvid = item.get("bvid")
        if not bvid:
            continue
        title = _clean_bilibili_title(str(item.get("title") or f"Bilibili video {bvid}"))
        pic = item.get("pic")
        if isinstance(pic, str) and pic.startswith("//"):
            pic = "https:" + pic
        results.append({
            "url": f"https://www.bilibili.com/video/{bvid}",
            "title": title,
            "author": item.get("author"),
            "published_at": str(item.get("pubdate")) if item.get("pubdate") else None,
            "description": _clean_html_text(str(item.get("description") or "")) or None,
            "tags": [tag.strip() for tag in str(item.get("tag") or "").split(",") if tag.strip()],
            "cover_url": pic,
            "platform_item_id": bvid,
            "metadata_source": "bilibili_public_web_search_api",
            "observed_metrics": {
                "views": item.get("play"),
                "likes": None,
                "comments": None,
                "shares": None,
                "favorites": item.get("favorites"),
                "danmaku": item.get("video_review"),
            },
        })
        if len(results) >= max_results:
            break
    return (results, []) if results else ([], ["bilibili public web search returned no video candidates"])


def _youtube_html_results(query: str, max_results: int = 5) -> tuple[list[dict[str, str]], list[str]]:
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": query})
    try:
        html = _fetch_text(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return [], [f"youtube html search failed: {exc}"]
    results: list[dict[str, str]] = []
    seen: set[str] = set()
    for video_id in re.findall(r'"videoId":"([^"]+)"', html):
        if video_id in seen:
            continue
        seen.add(video_id)
        is_shorts = f'"WEB_PAGE_TYPE_SHORTS"' in html[max(0, html.find(video_id) - 300): html.find(video_id) + 500]
        url_path = f"shorts/{video_id}" if is_shorts else f"watch?v={video_id}"
        results.append({
            "url": f"https://www.youtube.com/{url_path}",
            "title": f"YouTube {'Shorts' if is_shorts else 'video'} candidate for {query}",
            "platform_item_id": video_id,
            "metadata_source": "youtube_search_html",
        })
        if len(results) >= max_results:
            break
    return (results, []) if results else ([], ["youtube html page returned no parseable video ids"])


def _youtube_api_results(root: Path, query: str, max_results: int = YOUTUBE_SEARCH_MAX_RESULTS) -> tuple[list[dict[str, str]], list[str]]:
    api_key = _youtube_api_key(root)
    if not api_key:
        return [], ["youtube api key not configured"]
    params = urllib.parse.urlencode({
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
    })
    url = f"https://www.googleapis.com/youtube/v3/search?{params}"
    try:
        data = json.loads(_fetch_text(url))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return [], [f"youtube data api search failed: {exc}"]
    results: list[dict[str, str]] = []
    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})
        if not video_id:
            continue
        results.append({
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "title": snippet.get("title") or f"YouTube video candidate for {query}",
            "author": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "description": snippet.get("description"),
            "cover_url": max((thumb.get("url") for thumb in snippet.get("thumbnails", {}).values() if thumb.get("url")), default=None),
            "platform_item_id": video_id,
            "metadata_source": "youtube_data_api_v3_search",
        })
    return (results, []) if results else ([], ["youtube data api returned no video items"])


def _hard_platform_public_web_probe(platform: str, query: str) -> dict[str, Any]:
    if platform == "douyin":
        url = "https://www.douyin.com/search/" + urllib.parse.quote(query)
    elif platform == "xiaohongshu":
        url = "https://www.xiaohongshu.com/search_result?keyword=" + urllib.parse.quote(query)
    else:
        return {"public_web_probe": "unsupported_platform"}
    try:
        html = _fetch_text(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"public_web_probe": "failed", "probe_url": url, "gap": f"public page request failed: {exc}"}
    visible_hint = bool(re.search(r"(搜索|视频|笔记|note|douyin|xiaohongshu|抖音|小红书)", html, re.I))
    return {
        "public_web_probe": "reachable",
        "probe_url": url,
        "visible_metadata": "unknown_or_requires_browser_runtime" if not visible_hint else "page_shell_reachable",
        "candidate_extraction": "not_attempted_without_browser_session",
    }


def create_query_plan(root: str | Path, run_id: str, goal: str) -> dict[str, Any]:
    base = root_path(root)
    search_goal = _clean_goal_for_search(goal)
    with connect(base) as conn:
        query_plan_id = next_id(conn, "queryplan")
        conn.commit()
    query_plan = {
        "query_plan_id": query_plan_id,
        "run_id": run_id,
        "goal": goal,
        "implementation_mode": "p1_real_source_scouts_with_fixture_fallback",
        "rounds": [
            {"round": 1, "purpose": "broad discovery", "queries": [
                {"platform": "search", "query": f"{search_goal} AI short video trend format", "purpose": "broad web discovery"},
                {"platform": "bilibili", "query": f"{search_goal} AI short video hot format", "purpose": "Chinese platform video discovery"},
                {"platform": "youtube", "query": f"{search_goal} AI shorts trend", "purpose": "global AI video trend clues"},
            ]},
            {"round": 2, "purpose": "official/wiki reference check", "queries": [
                {"platform": "wiki_official", "query": f"{search_goal} official wiki reference", "purpose": "official/wiki source discovery"},
            ]},
            {"round": 3, "purpose": "hard-platform capability probes", "queries": [
                {"platform": "douyin", "query": search_goal, "purpose": "capability probe only"},
                {"platform": "xiaohongshu", "query": search_goal, "purpose": "capability probe only"},
            ]},
        ],
        "limits": {"max_candidates_total": 300, "max_harvested_sources_total": 60, "max_format_observations": 20, "max_sources_per_format_observation": 12},
        "created_at": utc_now(),
    }
    write_json(_run_dir(base, run_id, "query_plans", f"{query_plan_id}.json"), query_plan)
    write_decision(base, run_id, None, "p1_query_plan", "create_query_plan", "Created autonomous P1 query plan.", {"query_plan_id": query_plan_id})
    return query_plan


def _fixture_candidates(goal: str, run_id: str, query_plan_id: str) -> list[dict[str, Any]]:
    common = {"run_id": run_id, "query_used": f"fixture query plan {query_plan_id}", "evidence_mode": "fixture", "metadata_source": "fixture_library", "live_results_claimed": False}
    return [
        _make_candidate(**common, platform="fixture_search", url="fixture://p1/search/abstract-ai-short-format", title=f"{goal} - repeated abstract AI short format discussion", author="fixture_library", content_type="topic_page", source_type_guess="search_result", confidence=0.55, requires_review=False, notes="Fixture-backed broad web candidate shape; not live data."),
        _make_candidate(**common, platform="fixture_bilibili", url="fixture://p1/bilibili/role-substitution-short", title=f"{goal} - role substitution short video example", author="fixture_library", content_type="video", source_type_guess="platform_user", observed_metrics={"views": 120000, "likes": 8500, "comments": 560, "shares": None, "favorites": 2100}, confidence=0.62, notes="Fixture-backed Bilibili candidate shape; not live data."),
        _make_candidate(**common, platform="fixture_youtube", url="fixture://p1/youtube/ai-shorts-payoff", title=f"{goal} - AI Shorts payoff/reversal example", author="fixture_library", content_type="video", source_type_guess="platform_user", observed_metrics={"views": 98000, "likes": 6400, "comments": 430, "shares": None, "favorites": None}, confidence=0.58, notes="Fixture-backed YouTube candidate shape; not live data."),
        _make_candidate(**common, platform="fixture_wiki_official", url="fixture://p1/wiki/official-reference", title=f"{goal} - official/wiki reference candidate", author="fixture_library", content_type="wiki_page", source_type_guess="wiki", confidence=0.6, requires_review=False, notes="Fixture-backed wiki/official candidate shape; not live data."),
    ]


def _live_candidates_for_platform(root: Path, run_id: str, query_plan: dict[str, Any], platform: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    gaps: list[str] = []
    for query in _query_items(query_plan, platform):
        query_text = query["query"]
        if platform == "wiki_official":
            results, result_gaps = _wiki_official_results(query_text)
            content_type, metadata_source = "wiki_page", "wikipedia_opensearch"
        elif platform == "bilibili":
            results, result_gaps = _bilibili_public_web_results(query_text)
            content_type, metadata_source = "video", "bilibili_public_web_search_api"
        elif platform == "youtube":
            results, result_gaps = _youtube_api_results(root, query_text)
            if not results:
                html_results, html_gaps = _youtube_html_results(query_text)
                results = html_results
                result_gaps = result_gaps + html_gaps
            content_type, metadata_source = "video", "youtube_data_api_or_html"
        else:
            results, result_gaps = _search_duckduckgo_lite(_platform_search_query(query_text, platform))
            content_type, metadata_source = ("video" if platform in {"bilibili", "youtube"} else "topic_page"), "duckduckgo_lite"
        gaps.extend(result_gaps)
        rejected = 0
        for result in results:
            if not _result_is_relevant(result, platform):
                rejected += 1
                continue
            source = result.get("metadata_source", metadata_source)
            confidence = 0.66 if source == "youtube_data_api_v3_search" else 0.6 if source == "bilibili_public_web_search_api" else 0.58 if platform == "wiki_official" else 0.5
            candidates.append(_make_candidate(run_id=run_id, platform=platform, url=result.get("url"), title=result.get("title") or query_text, author=result.get("author"), content_type=content_type, source_type_guess=_source_type_from_url(result.get("url", ""), platform), observed_metrics=result.get("observed_metrics"), published_at=result.get("published_at"), description=result.get("description"), tags=result.get("tags"), cover_url=result.get("cover_url"), platform_item_id=result.get("platform_item_id"), query_used=query_text, evidence_mode="live_metadata", metadata_source=source, live_results_claimed=True, confidence=confidence, requires_review=platform != "wiki_official", notes="Metadata-only live scout result. No comments, downloads, screenshots, or platform API data claimed."))
        if rejected:
            gaps.append(f"rejected {rejected} low-relevance search results")
    return candidates, {"platform": platform, "status": "live_results_found" if candidates else "live_attempt_no_candidates", "live_results_claimed": bool(candidates), "candidate_count": len(candidates), "capability_gaps": gaps}


def _insert_candidates(root: Path, run_id: str, items: list[dict[str, Any]], status: str) -> list[str]:
    candidate_ids: list[str] = []
    with connect(root) as conn:
        for item in items:
            candidate_source_id = next_id(conn, "sourcecand")
            item["candidate_source_id"] = candidate_source_id
            conn.execute("INSERT INTO source_candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (candidate_source_id, run_id, item["platform"], item["url"], item["title"], item.get("author"), item["content_type"], json.dumps(item["observed_metrics"], ensure_ascii=False), json.dumps(item["discovery_reason"], ensure_ascii=False), status, item["collected_at"]))
            candidate_ids.append(candidate_source_id)
            write_json(_run_dir(root, run_id, "source_candidates", f"{candidate_source_id}.json"), item)
        conn.commit()
    return candidate_ids


def run_scouts(root: str | Path, run_id: str, query_plan: dict[str, Any], scout_mode: str = "auto") -> list[str]:
    if scout_mode not in P1_SCOUT_MODES:
        raise ValueError(f"unknown P1 scout mode: {scout_mode}")
    base = root_path(root)
    candidate_ids: list[str] = []
    scout_results: list[dict[str, Any]] = []
    live_allowed, live_missing = _live_search_allowed(base, scout_mode)
    if live_allowed:
        for platform in P1_LIVE_SCOUTS:
            live_items, scout_result = _live_candidates_for_platform(base, run_id, query_plan, platform)
            if live_items:
                candidate_ids.extend(_insert_candidates(base, run_id, live_items, "accepted_live_metadata"))
            else:
                scout_result["tool_setup_item"] = create_tool_setup_item(base, f"{platform}_scout", scout_result.get("capability_gaps") or ["no parseable live metadata results"], f"P1 {platform} scout attempted live metadata search but produced no usable candidates.", priority="medium")
            scout_results.append(scout_result)
    else:
        for platform in P1_LIVE_SCOUTS:
            setup_id = create_tool_setup_item(base, f"{platform}_scout", live_missing or ["live scout disabled"], f"P1 records {platform} search as a capability gap and can use fixture evidence for offline acceptance.", priority="medium")
            scout_results.append({"platform": platform, "status": "capability_gap_recorded", "live_results_claimed": False, "tool_setup_item": setup_id, "capability_gaps": live_missing, "notes": "No fake external data was produced."})
    for platform in P1_CAPABILITY_PROBES:
        probe_queries = _query_items(query_plan, platform)
        public_probe = _hard_platform_public_web_probe(platform, probe_queries[0]["query"] if probe_queries else query_plan["goal"])
        setup_id = create_tool_setup_item(base, f"{platform}_capability_probe", ["login/session", "official API or browser automation", "stable metadata access"], f"{platform} is a P1 capability probe only until setup is configured.", priority="high")
        scout_results.append({"platform": platform, "status": "probe_only", "live_results_claimed": False, "capabilities": {"search": "requires_browser_or_api", "metadata": "partial_or_unknown", "comments": "requires_auth_or_browser", "download_video": "blocked_or_limited"}, "public_web_probe": public_probe, "tool_setup_item": setup_id, "notes": "Probe only. No login, cookie, browser automation, comments, or downloads were attempted."})
    fixture_ids: list[str] = []
    if scout_mode == "fixture" or not candidate_ids:
        fixture_ids = _insert_candidates(base, run_id, _fixture_candidates(query_plan["goal"], run_id, query_plan["query_plan_id"]), "accepted_fixture_evidence")
        candidate_ids.extend(fixture_ids)
    scout_report = {"run_id": run_id, "query_plan_id": query_plan["query_plan_id"], "status": "p1_scout_completed_with_honest_fallbacks", "scout_mode": scout_mode, "live_results_claimed": any(item.get("live_results_claimed") for item in scout_results), "live_candidate_count": len(candidate_ids) - len(fixture_ids), "fixture_candidate_count": len(fixture_ids), "candidate_count": len(candidate_ids), "candidate_ids": candidate_ids, "scout_results": scout_results, "created_at": utc_now()}
    write_json(_run_dir(base, run_id, "scout_results", "scout_report.json"), scout_report)
    write_decision(base, run_id, None, "p1_scout", "run_p1_scouts", "Ran P1 scouts with live metadata attempts only when permitted and fixture fallback when needed.", {"candidate_count": len(candidate_ids), "scout_mode": scout_mode})
    return candidate_ids


def dedupe_and_rank_candidates(root: str | Path, run_id: str, candidate_ids: list[str]) -> list[str]:
    base = root_path(root)
    seen_urls: set[str] = set()
    ranked: list[tuple[float, str]] = []
    for candidate_id in candidate_ids:
        path = _run_dir(base, run_id, "source_candidates", f"{candidate_id}.json")
        item = read_json(path)
        if item["url"] in seen_urls:
            continue
        seen_urls.add(item["url"])
        metrics = item.get("observed_metrics", {})
        score = float(item.get("confidence", 0.0))
        if metrics.get("views"):
            score += min(float(metrics["views"]) / 1_000_000.0, 0.25)
        if metrics.get("comments"):
            score += min(float(metrics["comments"]) / 10_000.0, 0.1)
        if item.get("evidence_mode") == "live_metadata":
            score += 0.08
        item["harvest_priority"] = round(score, 3)
        item["harvest_reason"] = ["relevant_to_query", f"evidence_mode:{item.get('evidence_mode')}"]
        write_json(path, item)
        ranked.append((score, candidate_id))
    ranked.sort(reverse=True)
    ranked_ids = [candidate_id for _, candidate_id in ranked]
    write_json(_run_dir(base, run_id, "source_candidates", "dedupe_rank_report.json"), {"ranked_candidate_ids": ranked_ids, "deduped_count": len(ranked_ids), "created_at": utc_now()})
    return ranked_ids


def harvest_sources(root: str | Path, run_id: str, candidate_ids: list[str], max_sources: int = 12) -> list[str]:
    base = root_path(root)
    source_ids: list[str] = []
    now = utc_now()
    live_evidence_upgrade_needed = False
    with connect(base) as conn:
        for candidate_id in candidate_ids[:max_sources]:
            candidate = fetch_one(conn, "source_candidates", "candidate_source_id", candidate_id)
            candidate_file = read_json(_run_dir(base, run_id, "source_candidates", f"{candidate_id}.json"))
            source_type = candidate_file.get("source_type_guess", "unknown")
            usage_policy, review_status = _policy_for_guess(source_type)
            source_id = next_id(conn, "source")
            manifest_path = base / "research_assets" / "manifests" / "sources" / f"{source_id}.json"
            evidence_mode = candidate_file.get("evidence_mode", "unknown")
            harvest_status = "metadata_only_live" if evidence_mode == "live_metadata" else "metadata_only_fixture" if evidence_mode == "fixture" else "metadata_only_manual"
            files_available = {"metadata": True, "page_snapshot": False, "raw_video": False, "cover": False, "screenshots": False, "comments": False, "transcript": False, "audio_ref": False}
            manifest = {
                "source_id": source_id,
                "candidate_source_id": candidate_id,
                "run_id": run_id,
                "platform": candidate["platform"],
                "url": candidate["url"],
                "title": candidate["title"],
                "author": candidate["author"],
                "account": candidate_file.get("account") or candidate["author"],
                "source_type": source_type,
                "content_type": candidate["content_type"],
                "usage_policy": usage_policy,
                "review_status": review_status,
                "harvest_status": harvest_status,
                "source_mode": evidence_mode,
                "live_results_claimed": bool(candidate_file.get("live_results_claimed")),
                "manual_entry": evidence_mode == "manual_seed",
                "fixture": evidence_mode == "fixture",
                "requires_review": bool(candidate_file.get("requires_review", review_status == "pending")),
                "files_available": files_available,
                "files": {"metadata": rel(base, _run_dir(base, run_id, "source_candidates", f"{candidate_id}.json")), "page_snapshot": None, "raw_video": None, "cover": None, "screenshots": [], "comments": None, "transcript": None, "audio_ref": None},
                "unavailable_evidence": [name for name, available in files_available.items() if not available],
                "tool_setup_items_needed": ["snapshot_or_browser_tool", "comment_or_transcript_access", "download_permission"] if evidence_mode == "live_metadata" else [],
                "provenance": {"source_url": candidate["url"], "platform": candidate["platform"], "collected_at": now, "query_used": candidate_file.get("query_used"), "metadata_source": candidate_file.get("metadata_source"), "used_by_run": run_id, "what_was_saved": ["structured_metadata"], "why_saved": "P1 source intelligence metadata harvest."},
                "notes": candidate_file.get("notes") or "Metadata-only harvest. No unavailable evidence is claimed.",
                "created_at": now,
            }
            write_json(manifest_path, manifest)
            if evidence_mode == "live_metadata":
                live_evidence_upgrade_needed = True
            conn.execute("INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (source_id, candidate_id, run_id, candidate["platform"], candidate["url"], source_type, candidate["content_type"], usage_policy, review_status, harvest_status, rel(base, manifest_path), None, now, now))
            source_ids.append(source_id)
        conn.commit()
    if live_evidence_upgrade_needed:
        create_tool_setup_item(base, "p1_harvester_evidence_upgrade", ["page snapshot/screenshot/comment/transcript tooling not configured"], "P1 harvested live metadata but richer evidence remains unavailable.", priority="low")
    write_json(_run_dir(base, run_id, "harvested_sources", "harvest_report.json"), {"source_ids": source_ids, "harvest_status": "metadata_only", "created_at": now})
    write_decision(base, run_id, None, "p1_harvest", "harvest_metadata_sources", "Harvested metadata-only sources with provenance and explicit unavailable evidence fields.", {"source_count": len(source_ids)})
    return source_ids


def build_evidence_observations(root: str | Path, run_id: str, source_ids: list[str]) -> list[str]:
    base = root_path(root)
    observation_ids: list[str] = []
    with connect(base) as conn:
        for source_id in source_ids:
            source = fetch_one(conn, "sources", "source_id", source_id)
            candidate_file = read_json(_run_dir(base, run_id, "source_candidates", f"{source['candidate_source_id']}.json"))
            evidence_id = next_id(conn, "evidenceobs")
            available_inputs = ["url", "title", "platform", "metadata_source"]
            for field in ("author", "published_at", "description", "cover_url", "observed_metrics", "tags"):
                value = candidate_file.get(field)
                if value:
                    available_inputs.append(field)
            missing_inputs = ["page_screenshot", "video_frames", "transcript", "comments", "audio_metadata", "full_video_content"]
            if not candidate_file.get("cover_url"):
                missing_inputs.append("cover_image_url")
            observation = {
                "evidence_observation_id": evidence_id,
                "run_id": run_id,
                "source_id": source_id,
                "candidate_source_id": source["candidate_source_id"],
                "platform": source["platform"],
                "url": source["url"],
                "evidence_mode": candidate_file.get("evidence_mode"),
                "metadata_source": candidate_file.get("metadata_source"),
                "live_results_claimed": bool(candidate_file.get("live_results_claimed")),
                "available_inputs": available_inputs,
                "missing_inputs": missing_inputs,
                "observed_text": {
                    "title": candidate_file.get("title"),
                    "description": candidate_file.get("description"),
                    "tags": candidate_file.get("tags", []),
                    "author": candidate_file.get("author"),
                    "published_at": candidate_file.get("published_at"),
                },
                "observed_visual": {
                    "cover_url": candidate_file.get("cover_url"),
                    "page_screenshot": None,
                    "frame_samples": [],
                },
                "observed_metrics": candidate_file.get("observed_metrics", {}),
                "platform_item_id": candidate_file.get("platform_item_id"),
                "content_visibility": "metadata_and_cover_url_only" if candidate_file.get("cover_url") else "metadata_only",
                "understanding_limits": [
                    "No full video viewing is claimed.",
                    "No comments, danmaku, transcript, audio, screenshot, or downloaded media are claimed.",
                    "Format inference must remain weak until richer evidence exists.",
                ],
                "next_evidence_needed": ["page screenshot", "cover/image inspection", "transcript/captions if available", "short manual/browser viewing note"],
                "requires_review": bool(candidate_file.get("requires_review", True)),
                "created_at": utc_now(),
            }
            write_json(_run_dir(base, run_id, "evidence_observations", f"{evidence_id}.json"), observation)
            observation_ids.append(evidence_id)
        conn.commit()
    write_decision(base, run_id, None, "p1_evidence_observation", "build_evidence_observations", "Created evidence observations before source understanding.", {"evidence_observation_count": len(observation_ids)})
    return observation_ids


def build_understanding_reports(root: str | Path, run_id: str, source_ids: list[str], evidence_observation_ids: list[str]) -> list[str]:
    base = root_path(root)
    report_ids: list[str] = []
    with connect(base) as conn:
        for source_id, evidence_id in zip(source_ids, evidence_observation_ids):
            source = fetch_one(conn, "sources", "source_id", source_id)
            report_id = next_id(conn, "understanding")
            evidence = read_json(_run_dir(base, run_id, "evidence_observations", f"{evidence_id}.json"))
            observed_text = evidence.get("observed_text", {})
            title = observed_text.get("title") or str(source["url"])
            description = observed_text.get("description") or ""
            title_terms = [term for term in re.split(r"[\s/_#|:：,，。！!]+", title) if term]
            description_terms = [term for term in re.split(r"[\s/_#|:：,，。！!]+", description) if term][:20]
            has_richer_metadata = bool(description or evidence.get("observed_visual", {}).get("cover_url"))
            report = {
                "understanding_report_id": report_id,
                "source_id": source_id,
                "evidence_observation_id": evidence_id,
                "summary": f"Evidence-limited understanding for {source['platform']} source: {title}",
                "content_type_guess": ["ordinary_ai_video_format_candidate", source["content_type"]],
                "text_signals": {"title_keywords": title_terms, "description_keywords": description_terms, "visible_text": [title] + ([description] if description else []), "transcript_summary": None},
                "visual_signals": {"style_guess": "unknown_until_cover_or_frames_are_inspected", "subject_guess": "unknown_until_cover_or_frames_are_inspected", "subtitle_style_guess": "unknown_until_screenshot_or_frames", "ai_generated_likelihood": None, "cover_url": evidence.get("observed_visual", {}).get("cover_url")},
                "audio_signals": {"has_music": None, "music_or_sound_role": "unknown_from_metadata_only", "beat_or_hook_notes": []},
                "story_or_format_clues": {"roles": ["unknown_from_metadata_only"], "beats": [], "hook": "title/description may suggest a topic hook; video structure is not viewed yet", "punchline": None, "repeatable_parts": ["topic angle only"] if has_richer_metadata else []},
                "confidence": 0.52 if source["harvest_status"] == "metadata_only_live" and has_richer_metadata else 0.46 if source["harvest_status"] == "metadata_only_live" else 0.38,
                "missing_inputs": evidence.get("missing_inputs", []),
                "understanding_limits": evidence.get("understanding_limits", []),
                "created_at": utc_now(),
            }
            write_json(_run_dir(base, run_id, "understanding_reports", f"{report_id}.json"), report)
            report_ids.append(report_id)
        conn.commit()
    write_decision(base, run_id, None, "p1_understanding", "build_understanding_reports", "Built metadata-only P1 understanding reports without hallucinating missing inputs.", {"report_count": len(report_ids)})
    return report_ids


def build_format_observations(root: str | Path, run_id: str, source_ids: list[str], understanding_ids: list[str], evidence_observation_ids: list[str]) -> tuple[list[str], list[str]]:
    base = root_path(root)
    with connect(base) as conn:
        observation_id = next_id(conn, "fmtobs")
        opportunity_id = next_id(conn, "opp")
        conn.commit()
    confidence_label = "weak_observation"
    observation = {"observation_id": observation_id, "run_id": run_id, "candidate_format_name": "ordinary_ai_short_format_transfer_watchlist", "evidence_sources": source_ids, "evidence_observation_ids": evidence_observation_ids, "understanding_report_ids": understanding_ids, "shared_signals": ["metadata-visible short-video topic", "format function still needs page/cover/frame viewing", "evidence observation exists before understanding"], "possible_routes": ["ordinary_ai_format_video", "script_council_later", "character_reenactment_later"], "confidence_label": confidence_label, "confidence": 0.42, "needs_more_sources": True, "created_at": utc_now()}
    scores = {"heat": 0.45, "growth": 0.45, "freshness": 0.5, "repetition_signal": min(0.3 + 0.1 * len(source_ids), 0.65), "comment_sentiment": 0.4, "transferability": 0.6, "asset_readiness": 0.35, "tool_readiness": 0.5, "source_confidence": 0.4, "fatigue_penalty": 0.15}
    opportunity = {"opportunity_id": opportunity_id, "run_id": run_id, "title": "Ordinary AI short-video format transfer watchlist", "opportunity_type": "ai_video_style", "confidence_label": confidence_label, "score_total": round(sum(scores[key] * P1_SCORE_WEIGHTS[key] for key in scores), 4), "score_profile_id": "p1_opportunity_default_v1", "score_weights": P1_SCORE_WEIGHTS, "score_components": scores, "evidence_sources": source_ids, "evidence_observation_ids": evidence_observation_ids, "representative_examples": source_ids[:3], "format_observation_id": observation_id, "understanding_report_ids": understanding_ids, "why_it_matters": "This observation proves the P1 handoff shape for a repeated ordinary AI short-video format.", "why_it_may_be_stale": "Trend, comments, growth, and richer viewing evidence are incomplete.", "comment_sentiment_summary": "unknown_without_comments", "asset_and_reference_notes": ["page/cover/frame evidence should be enriched before P2 decisions"], "tool_or_ai_method_guess": [{"method": "unknown_ai_video_method", "confidence": 0.2, "evidence": ["metadata and evidence observation only"], "suggested_action": "collect_page_or_cover_evidence"}], "p0b_handoff_readiness": "needs_more_evidence", "recommended_p0b_start_mode": "opportunity_packet", "review_items": [], "created_at": utc_now()}
    write_json(_run_dir(base, run_id, "format_observations", f"{observation_id}.json"), observation)
    write_json(_run_dir(base, run_id, "opportunity_packets", f"{opportunity_id}.json"), opportunity)
    write_decision(base, run_id, None, "p1_format_observation", "create_weak_format_observation", "Created early P1 format observation and opportunity packet.", {"observation_id": observation_id, "opportunity_id": opportunity_id})
    return [observation_id], [opportunity_id]


def write_research_review_report(root: str | Path, run_id: str, query_plan: dict[str, Any], candidate_ids: list[str], source_ids: list[str], evidence_observation_ids: list[str], observation_ids: list[str], opportunity_ids: list[str]) -> dict[str, str]:
    base = root_path(root)
    report_dir = _run_dir(base, run_id, "reports")
    ensure_dir(report_dir)
    scout_report = read_json(_run_dir(base, run_id, "scout_results", "scout_report.json"))
    live_count = scout_report.get("live_candidate_count", 0)
    fixture_count = scout_report.get("fixture_candidate_count", 0)
    report_json = {"run_id": run_id, "goal": query_plan["goal"], "query_plan_id": query_plan["query_plan_id"], "candidate_count": len(candidate_ids), "source_count": len(source_ids), "evidence_observation_count": len(evidence_observation_ids), "evidence_observation_ids": evidence_observation_ids, "format_observation_ids": observation_ids, "opportunity_ids": opportunity_ids, "live_results_claimed": bool(scout_report.get("live_results_claimed")), "live_candidate_count": live_count, "fixture_candidate_count": fixture_count, "mode": scout_report.get("scout_mode"), "created_at": utc_now()}
    live_note = "本次存在 live metadata candidates；它们只代表真实页面搜索/metadata 级发现，不代表已抓取标题细节、评论、截图、下载或趋势验证。" if live_count else "本次没有 live candidate，说明真实搜索未获准、网络不可用、页面不可解析，或平台能力仍缺失；系统已记录 ToolSetupItem，而不是伪造结果。"
    md = f"""# P1 研究复盘报告 / Research Review Report

Run: `{run_id}`
研究目标: {query_plan['goal']}

## 这次运行做了什么

- 生成自主 query plan。
- 运行 P1 scout mode: `{scout_report.get('scout_mode')}`。
- Broad web / Wiki / YouTube / Bilibili 只采集 metadata/search-result/API metadata 级候选；不会声称评论、下载、截图或未标明来源的结果。
- Douyin / Xiaohongshu 只做 capability probe 和 ToolSetupItem，不假装全自动抓取。
- Harvester 生成 metadata-only source manifest，并明确记录 fixture / live / manual 模式。
- 生成 Understanding Reports、weak Format Observation 和 TrendOpportunityPacket。

## 数量

- Source candidates: {len(candidate_ids)}
- Live metadata candidates: {live_count}
- Fixture candidates: {fixture_count}
- Harvested sources: {len(source_ids)}
- Evidence observations: {len(evidence_observation_ids)}
- Format observations: {len(observation_ids)}
- Opportunity packets: {len(opportunity_ids)}

## 重要诚实说明

`live_results_claimed` = `{bool(scout_report.get('live_results_claimed'))}`。

{live_note}

当前 opportunity 仍标为 `weak_observation`，不能当作完整热点判断或 P1 全量验收通过。

## 建议下一步

1. 如果要真实 broad web search，把 `research.web_search` 设为 `allow_with_limits`，或用 `--scout-mode live` 明确尝试。
2. 给 YouTube/Bilibili 配置稳定 metadata/API/浏览器路径后重跑。
3. Douyin/Xiaohongshu 需要登录/API/cookie/浏览器自动化前，仍只允许 probe 或手动入口。
4. 只有当真实证据足够强，才把 opportunity 交给 P0-B 开生产 job。
"""
    write_json(report_dir / "research_review.json", report_json)
    write_human_text(report_dir / "research_review.md", md)
    write_json(base / "reports" / "phase_reports" / "phase1_research_review_index.json", report_json)
    write_human_text(base / "reports" / "phase_reports" / "phase1_research_review.md", md)
    return {"json": rel(base, report_dir / "research_review.json"), "markdown": rel(base, report_dir / "research_review.md")}


def run_p1_self_check(root: str | Path, run_id: str) -> dict[str, Any]:
    base = root_path(root)
    run_root = _run_dir(base, run_id)
    required = {"query_plan": run_root / "query_plans", "scout_report": run_root / "scout_results" / "scout_report.json", "source_candidates": run_root / "source_candidates", "harvest_report": run_root / "harvested_sources" / "harvest_report.json", "evidence_observations": run_root / "evidence_observations", "understanding_reports": run_root / "understanding_reports", "format_observations": run_root / "format_observations", "opportunity_packets": run_root / "opportunity_packets", "research_review": run_root / "reports" / "research_review.md"}
    checks = []
    for name, path in required.items():
        exists = path.exists() and (not path.is_dir() or any(path.iterdir()))
        checks.append({"name": name, "path": rel(base, path), "ok": exists, "message": "exists" if exists else "missing"})
    scout_report_path = run_root / "scout_results" / "scout_report.json"
    if scout_report_path.exists():
        scout_report = read_json(scout_report_path)
        live_count = int(scout_report.get("live_candidate_count", 0))
        checks.append({"name": "live_claim_matches_candidates", "ok": bool(scout_report.get("live_results_claimed")) == (live_count > 0), "message": "live_results_claimed must only be true when live candidates exist"})
        checks.append({"name": "live_capability_status", "ok": live_count > 0 or int(scout_report.get("fixture_candidate_count", 0)) > 0, "message": "P1 must either produce live candidates or honest fixture fallback candidates"})
        for platform in P1_CAPABILITY_PROBES:
            probe = next((item for item in scout_report.get("scout_results", []) if item.get("platform") == platform), None)
            checks.append({"name": f"{platform}_probe_only", "ok": bool(probe and probe.get("status") == "probe_only" and probe.get("live_results_claimed") is False), "message": f"{platform} must remain probe-only without login/API/browser setup"})
    for candidate_path in (run_root / "source_candidates").glob("sourcecand_*.json"):
        item = read_json(candidate_path)
        required_fields = ["candidate_source_id", "platform", "url", "title", "author", "published_at", "description", "tags", "cover_url", "platform_item_id", "collected_at", "query_used", "evidence_mode", "metadata_source", "live_results_claimed", "confidence", "capability_gaps", "requires_review", "notes"]
        missing = [field for field in required_fields if field not in item]
        checks.append({"name": f"candidate_schema_{candidate_path.stem}", "ok": not missing, "message": "missing fields: " + ", ".join(missing) if missing else "schema ok"})
        if item.get("evidence_mode") == "fixture":
            checks.append({"name": f"fixture_not_live_{candidate_path.stem}", "ok": item.get("live_results_claimed") is False, "message": "fixture candidates must not claim live results"})
    for evidence_path in (run_root / "evidence_observations").glob("evidenceobs_*.json"):
        item = read_json(evidence_path)
        required_fields = ["evidence_observation_id", "source_id", "candidate_source_id", "available_inputs", "missing_inputs", "observed_text", "observed_visual", "understanding_limits", "next_evidence_needed"]
        missing = [field for field in required_fields if field not in item]
        checks.append({"name": f"evidence_schema_{evidence_path.stem}", "ok": not missing, "message": "missing fields: " + ", ".join(missing) if missing else "schema ok"})
        checks.append({"name": f"evidence_no_full_video_claim_{evidence_path.stem}", "ok": "full_video_content" in item.get("missing_inputs", []), "message": "P1 evidence observation must not imply full video content was viewed"})
    failed = [item for item in checks if not item["ok"]]
    report = {"run_id": run_id, "status": "pass" if not failed else "fail", "failed_count": len(failed), "checks": checks, "checked_at": utc_now()}
    write_json(run_root / "reports" / "p1_self_check_report.json", report)
    failed_lines = "\n".join(f"- `{item['name']}`: {item['message']}" for item in failed) or "- None"
    write_human_text(run_root / "reports" / "p1_self_check_report.md", f"""# P1 自检报告 / Self-Check Report

Run: `{run_id}`
Status: `{report['status']}`
Failed checks: `{len(failed)}`

## Failed Checks

{failed_lines}

## Meaning

这个 self-check 验证 P1 research pipeline 的结构完整性、候选 schema、fixture/live 诚实性，以及 Douyin/XHS 仍为 probe-only。通过不代表完整 P1 验收完成。
""")
    return report


def run_p1_demo(root: str | Path, goal: str, manual_url: str | None = None, scout_mode: str = "auto") -> dict[str, Any]:
    base = ensure_project(root)
    run_id = create_run(base, goal, run_type="research", trigger_type="manual")
    query_plan = create_query_plan(base, run_id, goal)
    candidate_ids = run_scouts(base, run_id, query_plan, scout_mode=scout_mode)
    if manual_url:
        item = _make_candidate(run_id=run_id, platform="manual_seed", url=manual_url, title="Manual seed source", author="user", content_type="unknown", source_type_guess="unknown", query_used="manual_url", evidence_mode="manual_seed", metadata_source="user_input", live_results_claimed=False, confidence=0.4, requires_review=True, notes="Auxiliary manual seed. Not an autonomous scout result.")
        candidate_ids.extend(_insert_candidates(base, run_id, [item], "accepted_manual_seed"))
    ranked_ids = dedupe_and_rank_candidates(base, run_id, candidate_ids)
    source_ids = harvest_sources(base, run_id, ranked_ids)
    evidence_observation_ids = build_evidence_observations(base, run_id, source_ids)
    understanding_ids = build_understanding_reports(base, run_id, source_ids, evidence_observation_ids)
    observation_ids, opportunity_ids = build_format_observations(base, run_id, source_ids, understanding_ids, evidence_observation_ids)
    review_report = write_research_review_report(base, run_id, query_plan, ranked_ids, source_ids, evidence_observation_ids, observation_ids, opportunity_ids)
    self_check = run_p1_self_check(base, run_id)
    with connect(base) as conn:
        conn.execute("UPDATE runs SET status = ?, completed_at = ? WHERE run_id = ?", ("completed_p1", utc_now(), run_id))
        conn.commit()
    write_decision(base, run_id, None, "p1_report", "complete_p1_demo", "P1 research run completed with honest live/fixture status.", {"self_check_status": self_check["status"], "scout_mode": scout_mode})
    return {"root": str(base), "run_id": run_id, "query_plan_id": query_plan["query_plan_id"], "candidate_ids": ranked_ids, "source_ids": source_ids, "evidence_observation_ids": evidence_observation_ids, "understanding_report_ids": understanding_ids, "format_observation_ids": observation_ids, "opportunity_ids": opportunity_ids, "research_review": review_report, "self_check_status": self_check["status"], "scout_mode": scout_mode}
