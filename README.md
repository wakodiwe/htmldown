> [!CAUTION]
> Very early stage! 

# htmldown

Fetch HTML from URL and convert to readable Markdown.

## Installation

```bash
pip install htmldown
```

Or for development:

```bash
pip install -e .
```

## Usage

```bash
htmldown https://example.com              # Save as example.md
htmldown https://example.com -p           # Print to stdout
htmldown https://example.com -o file.md   # Custom output path
htmldown https://example.com -d /tmp      # Output directory
```

## Features

- Extracts main body content using readability
- Converts HTML to clean Markdown
- Strips anchor links from URLs (e.g., `url#section` → `url`)
- Handles various encodings automatically

## As Python Module

```python
from htmldown import fetch_and_convert

markdown = fetch_and_convert("https://example.com")
print(markdown)
```

## Dependencies

- html2text
- beautifulsoup4
- readability-lxml
- chardet
