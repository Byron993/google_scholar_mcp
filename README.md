# Google Scholar MCP Server

MCP server for Google Scholar academic paper search.

## Features

- Search academic papers via Google Scholar
- Automatically retrieve paper abstracts
- Support Chinese keyword search with auto-translation
- Return paper metadata (title, authors, journal, year, citations, URL)

## Usage

### uvx (recommended)

```bash
uvx --from google-scholar-mcp google-scholar-mcp
```

Or from source:

```bash
uvx --from . google-scholar-mcp
```

### Cherry Studio Configuration

```json
{
  "mcpServers": {
    "google_scholar": {
      "command": "uvx",
      "args": ["--from", "google-scholar-mcp", "google-scholar-mcp"]
    }
  }
}
```

## Development

```bash
# Run tests
uv run pytest -v

# Run server locally
uv run google-scholar-mcp
```

## Notes

- VPN required to access Google Scholar
- Chinese queries are auto-translated to English
- Abstract retrieval depends on paper page structure

## License

MIT