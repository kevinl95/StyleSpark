import os
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer

code_len = 563  # 1024 - 461 tokens for the style descriptions

style_descriptions = """
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
   Detailed documentation and mathematical rigor. Pedantic formatting with highly structured, well-documented algorithms.
6. Vint Cerf – Father of the Internet
   Focus on modular, well-structured, and reusable components. Robust documentation and error handling with adherence to standards.
7. James Gosling – Java Creator
   Object-oriented design with a focus on portability. Verbose syntax and clear separation of concerns.
8. Bjarne Stroustrup – C++ Creator
   Code prioritizes efficiency and flexibility, with extensive use of object-oriented and generic programming features.
9. Ken Thompson – UNIX Creator
   Simple, efficient code designed for quick execution. Modular design and focus on system-level efficiency.
10. Brian Kernighan – C Co-author
    Clear, simple, and minimalistic code. Focus on small programs with precision and clarity.
11. Tim Berners-Lee – Web Creator
    Clean, simple, and modular code designed for interoperability and following standards for web technologies.
12. Margaret Hamilton – Software Engineering Pioneer
    Safety-focused, with extensive error handling and documentation. Prioritizes reliability in high-stakes systems.
"""

def analyze_code_style(code, style_descriptions):
    """
    Analyze the style of given code and match it to predefined styles.

    Parameters:
        code (str): The user's code snippet to analyze.
        style_descriptions (str): Descriptions of programming styles to match against.

    Returns:
        tuple: The style author and the explanation that most closely matches the code.
    """
    # Load GPT-2 model and tokenizer
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Set the pad token to eos token
    tokenizer.pad_token = tokenizer.eos_token

    # Create the prompt with style descriptions and code
    prompt = (
        f"{style_descriptions}\n\n"
        f"Code:\n{code}\n\n"
        f"Question: Which style does this code most closely match? Provide the author followed by a colon (:) and explanation."
    )
    print(prompt)
    # Encode the prompt to count tokens
    inputs = tokenizer.encode_plus(
        prompt,
        return_tensors="pt",
        max_length=1024-50,
        truncation=True,  # Ensure the input is within the model's limits
        padding="max_length"  # Pad to the maximum length
    )

    # Check the number of tokens to ensure we're within the limit
    num_tokens = inputs["input_ids"].shape[-1]
    print(num_tokens)
    # If the prompt exceeds the token limit, truncate it accordingly
    if num_tokens > 1024 - 50:
        print(
            f"Warning: Prompt exceeds token limit with {num_tokens} tokens. Truncating..."
        )
        truncated_tokens = inputs["input_ids"][0][:1024-50]
        prompt = tokenizer.decode(truncated_tokens, skip_special_tokens=True)
        inputs = tokenizer.encode_plus(
            prompt, return_tensors="pt", truncation=True, padding="max_length"
        )

    # Generate the response
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=50,  # Generate up to 50 new tokens
        num_return_sequences=1,
    )

    # Decode and process the response
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-process result to extract a meaningful answer
    result = result.replace(prompt, "").strip()
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


def read_code_files(repo_path, file_extensions, max_tokens=code_len):
    """Read all code files and return the code content, stopping when enough code is collected."""
    code = ""
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                with open(os.path.join(root, file), "r") as f:
                    code += f.read() + "\n"
                    # Tokenize the current code and check the token count
                    encoded_code = tokenizer.encode(code, return_tensors="pt")
                    num_tokens = encoded_code.shape[-1]

                    # If the code exceeds the max_tokens, stop reading files
                    if num_tokens > max_tokens:
                        return code
    return code


def truncate_code(code, max_tokens):
    """Truncate code to fit within the max token length."""
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    encoded_code = tokenizer.encode(code, return_tensors="pt")

    if encoded_code.shape[-1] > max_tokens:
        print(f"Truncating code to fit within {max_tokens} tokens.")
        return tokenizer.decode(encoded_code[0][:max_tokens], skip_special_tokens=True)

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
    author_name, style_analysis = analyze_code_style(code, style_descriptions)
    # Commit changes, if requested
    if update_readme:
        badge_url = generate_badge_url(author_name)
        update_readme_with_badge(readme_path, badge_url)
    print(author_name)
    print(style_analysis)