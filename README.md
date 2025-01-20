# StyleSpark: Analyzing and Matching Code to Iconic Programming Styles using GitHub Actions

![GitHub Action Test](https://github.com/actions/hello-world-docker-action/actions/workflows/ci.yml/badge.svg)
![StyleSpark](https://img.shields.io/badge/Guido%20van%20Rossum%20(Python%20Creator)-Guido%20van%20Rossum%20(Python%20Creator)?style=flat&label=StyleSpark&labelColor=%232111a4&color=%23CFD8DC)

## Overview

StyleSpark is a GitHub Action that analyzes code snippets and matches them to the coding styles of iconic programmers. You'll be able to get a snazzy badge for your repository- an example is above! By leveraging large language models (particuarly Llama 3), StyleSpark provides insights into which famous programmer's style your code most closely resembles. Use this as a fun tool to explore computing's heros, share a bit about your coding style with the community, or motivate yourself to change up how you write your code!

## Features

- **Code Analysis**: Analyzes code snippets to determine their stylistic attributes.
- **Style Matching**: Matches code to the styles of iconic programmers such as Grace Hopper, Ada Lovelace, Linus Torvalds, and more.
- **Badge Generation**: Automatically updates the README with a badge indicating the matched programming style.

## Supported Programming Styles

| No. | Programmer                  | Description                          | Style Characteristics                                                                 |
|-----|-----------------------------|--------------------------------------|---------------------------------------------------------------------------------------|
| 1   | [Grace Hopper](https://en.wikipedia.org/wiki/Grace_Hopper)                | Compiler Pioneer                     | Focus on readability, with extensive comments and descriptive names. Modular and structured for ease of maintenance. Known for COBOL, emphasizing readability and documentation. |
| 2   | [Ada Lovelace](https://en.wikipedia.org/wiki/Ada_Lovelace)                | First Programmer                     | Focus on logical precision, algorithmic clarity, and mathematical elegance. Abstract, rigorous, and concise algorithms. |
| 3   | [Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds)              | Creator of Linux                     | Minimalist, performance-focused code with short, simple functions. Few comments, prioritizing efficiency and pragmatism. |
| 4   | [Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum)            | Python Creator                       | Code should be clear, simple, and easy to understand. Emphasis on readability and explicitness, with functions that do one thing well. |
| 5   | [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth)                | TeX Creator                          | Detailed documentation and mathematical rigor. Pedantic formatting with highly structured, well-documented algorithms. |
| 6   | [Vint Cerf](https://en.wikipedia.org/wiki/Vint_Cerf)                   | Father of the Internet               | Focus on modular, well-structured, and reusable components. Robust documentation and error handling with adherence to standards. |
| 7   | [James Gosling](https://en.wikipedia.org/wiki/James_Gosling)               | Java Creator                         | Object-oriented design with a focus on portability. Verbose syntax and clear separation of concerns. |
| 8   | [Bjarne Stroustrup](https://en.wikipedia.org/wiki/Bjarne_Stroustrup)           | C++ Creator                          | Code prioritizes efficiency and flexibility, with extensive use of object-oriented and generic programming features. |
| 9   | [Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson)                | UNIX Creator                         | Simple, efficient code designed for quick execution. Modular design and focus on system-level efficiency. |
| 10  | [Brian Kernighan](https://en.wikipedia.org/wiki/Brian_Kernighan)             | C Co-author                          | Clear, simple, and minimalistic code. Focus on small programs with precision and clarity. |
| 11  | [Tim Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee)             | Web Creator                          | Clean, simple, and modular code designed for interoperability and following standards for web technologies. |
| 12  | [Margaret Hamilton](https://en.wikipedia.org/wiki/Margaret_Hamilton_(software_engineer))           | Software Engineering Pioneer         | Safety-focused, with extensive error handling and documentation. Prioritizes reliability in high-stakes systems. |


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
| `FILE_EXTENSIONS` | Comma-separated list of file extensions to analyze. StyleSpark will scan all files with these extensions in your repository. | `".py,.java,.js"` | Yes |
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