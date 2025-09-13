[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/byron993-google-scholar-mcp-badge.png)](https://mseep.ai/app/byron993-google-scholar-mcp)

# Google Scholar MCP Server (Optimized for Cherry Studio)

An MCP-based Google Scholar search service optimized for Cherry Studio, providing academic paper search, abstract retrieval, and supporting both Chinese and English queries.

## Features

- Search academic papers via Google Scholar (not limited to arXiv)
- Automatically retrieve and filter paper abstracts (only keeping complete abstracts)
- Support Chinese keyword search with auto-translation to English
- Return comprehensive paper metadata (title, authors, journal, year, citations, URL, etc.)
- Optimized for Cherry Studio integration via MCP protocol

## Installation

`google_scholar_mcp` can be installed using `uv`. Below are two approaches: a quick start for immediate use and a detailed setup for development.

### Quick Start

For users who want to quickly run the server:

1. **Install Package**:
   ```bash
   uv add google_scholar_mcp
   ```

2. **Configure Cherry Studio**:
   Add this configuration to your Cherry Studio configuration file:
   ```json
   {
     "mcpServers": {
       "google_scholar_server": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/your/google_scholar_mcp",
           "run",
           "gsd_mcp.py"
         ]
       }
     }
   }
   ```
   > Note: Replace `/path/to/your/google_scholar_mcp` with your actual installation path.

## Usage

### Response Example

```text
=== Paper 1 ===
Title: Deep Learning
Authors: Yann LeCun, Yoshua Bengio, Geoffrey Hinton  
Journal: Nature
Year: 2015
URL: https://www.nature.com/articles/nature14539
Citations: 95183
Abstract:
  Deep learning allows computational models composed of multiple processing layers to learn representations of data with multiple levels of abstraction...
```

## Notes

1. Abstract retrieval depends on paper page structure and may not always succeed
2. VPN connection is required throughout usage to access Google Scholar
3. Please set reasonable request frequency to avoid being blocked by Google Scholar
4. Chinese queries are automatically translated to English for searching

## Dependencies

- googletrans>=4.0.2
- httpx>=0.28.1
- mcp[cli]>=1.7.0
- scholarly>=1.7.11

## License

MIT License
