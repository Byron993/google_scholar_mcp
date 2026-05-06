"""Core functions for Google Scholar search"""

import random
import textwrap
import time

import requests
from bs4 import BeautifulSoup, Tag
from googletrans import Translator


def is_chinese(text: str) -> bool:
    """检查文本是否包含中文"""
    return any("一" <= char <= "鿿" for char in text)


async def translate_to_english(text: str) -> str:
    """将中文翻译为英文"""
    translator = Translator()
    translated = await translator.translate(text, src="zh-cn", dest="en")
    return translated.text


def get_paper_abstract(paper_url: str) -> str:
    """从论文页面获取摘要"""
    try:
        headers_candidate = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        ]
        headers = {
            "User-Agent": random.choice(headers_candidate),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/webp,image/apng,*/*;q=0.8"
            ),
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        response = requests.get(paper_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            abstract_rules = [
                ("meta", {"property": "og:description"}, "content"),
                ("meta", {"name": "citation_abstract"}, "content"),
                ("div", {"class": "abstract"}, None),
                ("div", {"class": "abstract-text"}, None),
                ("section", {"id": "abstract"}, None),
                ("section", {"class": "article-information abstract"}, None),
                ("p", {"class": "abstract-text"}, None),
            ]

            abstract_candidates = []

            for tag, attrs, content_attr in abstract_rules:
                try:
                    element = soup.find(tag, attrs)
                    if isinstance(element, Tag):
                        if content_attr:
                            val = element.attrs.get(content_attr, "")
                            abstract_candidates.append(str(val).strip())
                        else:
                            abstract_candidates.append(element.get_text().strip())
                except Exception:
                    continue

            if abstract_candidates:
                max_abstract = max(abstract_candidates, key=len)
                if len(max_abstract) > 0:
                    return max_abstract

        return "无法获取摘要"
    except Exception as e:
        return f"获取摘要时出错: {str(e)}"


def format_paper(paper: dict, index: int) -> str:
    """格式化单篇论文信息"""
    text = f"=== 论文 {index} ===\n"
    text += f"标题: {paper['title']}\n"
    authors = paper["authors"]
    if isinstance(authors, list):
        text += f"作者: {', '.join(authors)}\n"
    else:
        text += f"作者: {authors}\n"
    text += f"期刊: {paper['journal']}\n"
    text += f"发表年份: {paper['year']}\n"
    text += f"URL: {paper['url']}\n"
    text += f"引用次数: {paper['num_citations']}\n"
    text += "摘要:\n"

    abstract = paper["abstract"]
    if abstract and abstract not in ("无摘要信息", "无法获取摘要"):
        abstract_lines = textwrap.wrap(abstract, width=80)
        for line in abstract_lines:
            text += f"  {line}\n"
    else:
        text += f"  {abstract}\n"

    return text


async def search_scholar(query: str, num_results: int = 5) -> str:
    """搜索 Google Scholar 并返回论文信息"""
    from scholarly import scholarly

    if is_chinese(query):
        query = await translate_to_english(query)

    search_query = scholarly.search_pubs(query)

    results = []
    count = 0

    for _ in range(num_results * 2):
        try:
            paper = next(search_query)

            paper_info = {
                "title": paper.get("bib", {}).get("title", "无题目"),
                "authors": paper.get("bib", {}).get("author", "无作者信息"),
                "journal": paper.get("bib", {}).get("venue", "无期刊信息"),
                "year": paper.get("bib", {}).get("pub_year", "无发表年份"),
                "url": paper.get("pub_url", "无URL"),
                "num_citations": paper.get("num_citations", "无引用"),
            }

            has_abstract = False
            if "pub_url" in paper and paper["pub_url"]:
                paper_info["abstract"] = get_paper_abstract(paper["pub_url"])
                has_abstract = paper_info["abstract"] not in (
                    "无法获取摘要",
                    "获取摘要时出错",
                )
            else:
                paper_info["abstract"] = "无法获取摘要"

            if has_abstract:
                results.append(paper_info)
                count += 1

            if count >= num_results:
                break

            time.sleep(2 + random.gauss(0, 0.5))

        except StopIteration:
            break
        except Exception:
            continue

    if not results:
        return "未找到相关论文"

    return "\n\n".join(format_paper(p, i) for i, p in enumerate(results, 1))
