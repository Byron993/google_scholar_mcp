"""Tests for google_scholar_mcp"""

from google_scholar_mcp.core import format_paper, is_chinese


def test_is_chinese():
    assert is_chinese("深度学习") is True
    assert is_chinese("deep learning") is False
    assert is_chinese("深度 learning") is True
    assert is_chinese("") is False


def test_format_paper():
    paper = {
        "title": "Test Paper",
        "authors": ["Author A", "Author B"],
        "journal": "Test Journal",
        "year": "2024",
        "url": "https://example.com/paper",
        "num_citations": 100,
        "abstract": "This is a test abstract for the paper.",
    }
    result = format_paper(paper, 1)

    assert "=== 论文 1 ===" in result
    assert "标题: Test Paper" in result
    assert "作者: Author A, Author B" in result
    assert "期刊: Test Journal" in result
    assert "发表年份: 2024" in result
    assert "引用次数: 100" in result


def test_format_paper_single_author():
    paper = {
        "title": "Single Author Paper",
        "authors": "Solo Author",
        "journal": "Journal",
        "year": "2023",
        "url": "https://example.com",
        "num_citations": 50,
        "abstract": "无法获取摘要",
    }
    result = format_paper(paper, 2)

    assert "作者: Solo Author" in result
    assert "无法获取摘要" in result
