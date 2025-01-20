# StyleSpark: Analyzing and Matching Code to Iconic Programming Styles using GitHub Actions

![GitHub Action Test](https://github.com/actions/hello-world-docker-action/actions/workflows/ci.yml/badge.svg)
![StyleSpark](https://img.shields.io/badge/Author-Author?style=flat&label=StyleSpark&labelColor=%232111a4&color=%23CFD8DC)

## Overview

StyleSpark is a GitHub Action that analyzes code snippets and matches them to the coding styles of iconic programmers. By leveraging machine learning models, StyleSpark provides insights into which famous programmer's style your code most closely resembles.

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

FILE_EXTENSIONS: A comma-separated list of file extensions to analyze. For example, "py,java,js" will analyze Python, Java, and JavaScript files. This variable tells StyleSpark which types of files to include in the analysis.

COMMIT_CHANGES: A boolean value ("true" or "false") that determines whether the changes should be automatically committed to the repository. If set to "true", StyleSpark will update the README file with the badge indicating the matched programming style and commit the changes. If set to "false", the changes will not be committed.

README_PATH: The path to the README file that should be updated with the badge. This variable specifies the location of the README file in your repository. For example, "README.md" indicates that the README file is located in the root directory of the repository.

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

# Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

# License
This project is licensed under the MIT License. See the LICENSE file for details.