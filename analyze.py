import os
import re
from gpt4all import GPT4All

code_len = 250

# Initialize the GPT-4 All model
def load_model():
    # Initialize the GPT-4 model. It will automatically download the model if it's not already present.
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    return model

# Step 2: Prompt the model and get a response
def get_model_response(model, prompt):
    # Run the model to generate a response for the given prompt
    response = model.generate(prompt)
    return response

def read_code_files(repo_path, file_extensions, max_tokens=code_len):
    """Read all code files and return the code content, stopping when enough code is collected."""
    code = ""
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                with open(os.path.join(root, file), "r") as f:
                    code += f.read() + "\n"
                    # Check the length of the current code
                    if len(code) > max_tokens:
                        return code[:max_tokens]
    return code[:max_tokens]

def truncate_code(code, max_tokens):
    """Truncate code to fit within the max token length."""
    if len(code) > max_tokens:
        print(f"Truncating code to fit within {max_tokens} characters.")
        return code[:max_tokens]
    return code

def generate_badge_url(author_name):
    base_url = "https://img.shields.io/badge/Author-Author?style=flat&label=StyleSpark&labelColor=%232111a4&color=%23CFD8DC"
    formatted_author_name = author_name.replace(" ", "%20")  # Encode spaces for URL
    return base_url.replace("Author", formatted_author_name)


def update_readme_with_badge(readme_path, badge_url):
    badge_markdown = f"![StyleSpark]({badge_url})"

    try:
        with open(readme_path, "r") as file:
            content = file.read()

        # Check if a badge already exists
        if "![StyleSpark]" in content:
            # Replace the existing badge
            content = re.sub(r"!\[StyleSpark\]\(.*?\)", badge_markdown, content)
        else:
            # Append the badge to the top of the README
            content = badge_markdown + "\n\n" + content

        # Write back the updated README
        with open(readme_path, "w") as file:
            file.write(content)

        print(f"Updated {readme_path} with badge.")
    except FileNotFoundError:
        print(f"{readme_path} not found.")
        with open(readme_path, "w") as file:
            file.write(content)

        print(f"Updated {readme_path} with badge.")
    except FileNotFoundError:
        print(f"{readme_path} not found.")


def analyze_code_style(code):
    """
    Analyze the style of given code and match it to predefined styles.

    Parameters:
        code (str): The user's code snippet to analyze.

    Returns:
        tuple: The style author and the explanation that most closely matches the code.
    """
    # Initialize model
    model = load_model()
    # Create the prompt with style descriptions and code
    prompt = f"""
        Given the following list of programming styles, determine which one best matches the provided code snippet. Respond in the format:

        Author: <Author's Name>
        Explanation: <Detailed explanation of why this style matches>

        List of Styles:
        1. Grace Hopper – Compiler Pioneer
        Focus on readability, with extensive comments and descriptive names. Code is modular, structured for ease of maintenance.
        Known for COBOL, a language emphasizing readability and documentation.
        2. Ada Lovelace – First Programmer
        Focus on logical precision, algorithmic clarity, and mathematical elegance. Her algorithms were abstract, rigorous, and concise.
        3. Linus Torvalds – Creator of Linux
        Minimalist, performance-focused code with short, simple functions. Few comments, prioritizing efficiency and pragmatism.
        4. Guido van Rossum – Python Creator
        Code should be clear, simple, and easy to understand. Emphasis on readability and explicitness, with functions that do one thing well.
        5. Donald Knuth – TeX Creator
        Detailed documentation and mathematical rigor. Pedantic formatting with highly structured, well-documented algorithms.        7. Tim Berners-Lee – Web Creator
            Clean, simple, and modular code designed for interoperability and following standards for web technologies.
        6. Margaret Hamilton – Software Engineering Pioneer
            Safety-focused, with extensive error handling and documentation. Prioritizes reliability in high-stakes systems.

        Here is the code snippet:\n\n
        {code}\n\n
        Please provide the answer in the specified format:
    """
    # Get the response from the model
    result = get_model_response(model, prompt)
    print(result)
    # Split the result into author and explanation
    if ":" in result:
        author, explanation = result.split(":", 1)
        author = author.strip()
        explanation = explanation.strip()
    else:
        author = "Unknown"
        explanation = "The model did not provide a clear author and explanation."

    return author, explanation


if __name__ == "__main__":
    repo_path = "repo"
    # Get the user's selected file extension types
    file_extensions = os.getenv("FILE_EXTENSIONS").split(",")
    # Determine if the user wants their README updated
    update_readme = os.getenv("COMMIT_CHANGES", "false").lower() in ("true", "1", "yes")
    # Get the README path
    readme_path = os.path.join(repo_path, os.getenv("README_PATH"))
    # Read all code files in the project directory
    code = read_code_files(repo_path, file_extensions)

    # Truncate the code if it exceeds the maximum token length
    code = truncate_code(code, max_tokens=code_len)

    # Analyze the code style
    author_name, style_analysis = analyze_code_style(code)
    # Commit changes, if requested
    if update_readme:
        badge_url = generate_badge_url(author_name)
        update_readme_with_badge(readme_path, badge_url)
    print(author_name)
    print(style_analysis)
