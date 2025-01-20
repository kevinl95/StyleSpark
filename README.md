# StyleSpark: Analyzing and Matching Code to Iconic Programming Styles using GitHub Actions

![GitHub Action Test](https://github.com/actions/hello-world-docker-action/actions/workflows/ci.yml/badge.svg)
![StyleSpark](https://img.shields.io/badge/Guido%20van%20Rossum-Guido%20van%20Rossum?style=flat&label=StyleSpark&labelColor=%232111a4&color=%23CFD8DC)

## Overview

StyleSpark is a GitHub Action that analyzes code snippets and matches them to the coding styles of iconic programmers. You'll be able to get a snazzy badge for your repository- an example is above! By leveraging large language models (particuarly Llama 3), StyleSpark provides insights into which famous programmer's style your code most closely resembles. Use this as a fun tool to explore computing's heros, share a bit about your coding style with the community, or motivate yourself to change up how you write your code!

## Features

- **Code Analysis**: Analyzes code snippets to determine their stylistic attributes.
- **Style Matching**: Matches code to the styles of iconic programmers such as Grace Hopper, Ada Lovelace, Linus Torvalds, and more.
- **Badge Generation**: Automatically updates the README with a badge indicating the matched programming style.

## Supported Programming Styles

1. Grace Hopper – Compiler Pioneer
2. Ada Lovelace – First Programmer
3. Linus Torvalds – Creator of Linux
4. Guido van Rossum – Python Creator
5. Donald Knuth – TeX Creator
6. Vint Cerf – Father of the Internet
7. James Gosling – Java Creator
8. Bjarne Stroustrup – C++ Creator
9. Ken Thompson – UNIX Creator
10. Brian Kernighan – C Co-author
11. Tim Berners-Lee – Web Creator
12. Margaret Hamilton – Software Engineering Pioneer

## Usage

To use StyleSpark in your GitHub repository, follow these steps:

**Create a Workflow File**: Add a new workflow file in your repository's `.github/workflows` directory.

```yaml
name: StyleSpark Analysis

on:
  push:
    branches:
      - main

jobs:
  analyze-code:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run StyleSpark
        uses: kevinl95/StyleSpark@main
        with:
          FILE_EXTENSIONS: "py,java,js"
          COMMIT_CHANGES: "true"
          README_PATH: "README.md"
```

## Configuration Variables

| Configuration | Description | Example | Required |
|--------------|-------------|---------|----------|
| `FILE_EXTENSIONS` | Comma-separated list of file extensions to analyze. StyleSpark will scan all files with these extensions in your repository. | `"py,java,js"` | Yes |
| `COMMIT_CHANGES` | Boolean value that determines whether StyleSpark should automatically commit changes to your README. If `true`, a badge will be added or updated in your README showing your matched programming style. | `"true"` or `"false"` | No (defaults to `"false"`) |
| `README_PATH` | Path to your README file relative to the repository root. This is where StyleSpark will add or update the style badge. | `"README.md"` or `"docs/README.md"` | No (defaults to `'README.md'`) |

# Development

To develop and test StyleSpark locally, follow these steps:

## Clone the Repository:

```bash
git clone https://github.com/kevinl95/StyleSpark.git
cd StyleSpark
```

## Build the Docker Image:

```bash
docker build -t stylespark .
```

## Run the Docker Container:

```bash
docker run --rm -v $(pwd):/repo stylespark
```

# Example Output
```
Author: Guido van Rossum
Explanation: Code emphasizes readability with clear function names and docstrings...
```
# Troubleshooting
**Badge not appearing**: Ensure COMMIT_CHANGES is set to "true"

**No style match**: Check that FILE_EXTENSIONS includes your primary code files

**Permission errors**: Verify workflow has write permissions enabled

# Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

# License
This project is licensed under the MIT License. See the LICENSE file for details.