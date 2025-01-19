from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

code_len = 564  # 1024 - 460 tokens for the style descriptions

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
        str: The style that most closely matches the code.
    """
    # Load DistilGPT2 model and tokenizer
    model_name = "distilgpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Create the prompt with style descriptions and code
    prompt = (
        f"{style_descriptions}\n\n"
        f"Code:\n{code}\n\n"
        f"Question: Which style does this code most closely match?"
    )

    # Encode the prompt to count tokens
    inputs = tokenizer.encode(
        prompt,
        return_tensors="pt",
        max_length=code_len,
        truncation=True,  # Ensure the input is within the model's limits
    )

    # Check the number of tokens to ensure we're within the limit
    num_tokens = inputs.shape[-1]

    # If the prompt exceeds the token limit, truncate it accordingly
    if num_tokens > code_len:
        print(
            f"Warning: Prompt exceeds token limit with {num_tokens} tokens. Truncating..."
        )
        prompt = tokenizer.decode(inputs[0][:code_len], skip_special_tokens=True)
        inputs = tokenizer.encode(
            prompt, return_tensors="pt", max_length=code_len, truncation=True
        )

    # Generate the response
    outputs = model.generate(
        inputs,
        max_length=128,  # Limit output length for concise results
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
    )

    # Decode and process the response
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-process result to extract a meaningful answer
    result = result.replace(prompt, "").strip()

    return result


def read_code_files(repo_path, file_extensions, max_tokens=code_len):
    """Read all code files and return the code content, stopping when enough code is collected."""
    code = ""
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")

    for root, dirs, files in os.walk(repo_path):
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
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
    encoded_code = tokenizer.encode(code, return_tensors="pt")

    if encoded_code.shape[-1] > max_tokens:
        print(f"Truncating code to fit within {max_tokens} tokens.")
        return tokenizer.decode(encoded_code[0][:max_tokens], skip_special_tokens=True)

    return code


if __name__ == "__main__":
    # Get the path to the checked-out repository
    repo_path = os.getenv("GITHUB_WORKSPACE")
    # Get the user's selected file extension types
    file_extensions = os.getenv("FILE_EXTENSIONS").split(",")

    # Read all code files in the project directory
    code = read_code_files(repo_path, file_extensions)

    # Truncate the code if it exceeds the maximum token length
    code = truncate_code(code, max_tokens=code_len)

    # Analyze the code style
    style_analysis = analyze_code_style(code, style_descriptions)
    print(style_analysis)
