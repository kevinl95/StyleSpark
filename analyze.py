from transformers import pipeline
import os

style_descriptions = """
1. Grace Hopper – Pioneering Compiler Development
    Focus on Readability: Code should be highly readable, often with extensive comments explaining complex concepts.
    Descriptive Naming: Emphasis on clear, descriptive names for variables and functions.
    Modularization: Code tends to be structured in a way that supports ease of maintenance and understanding, with functions and subroutines well-defined.
    Language Use: Primarily known for her work on COBOL, a language designed to be readable by non-programmers.
    Comments and Documentation: Extensive comments to make the code easy to follow for both programmers and non-programmers.
    Citation: Hopper was instrumental in the creation of the COBOL programming language, which emphasizes readability and documentation.
2. Ada Lovelace – First Computer Programmer
    Mathematical Precision: Ada’s style would likely focus on logical precision and mathematical elegance.
    Algorithmic Clarity: Expect algorithm descriptions that are rigorous and abstract, suitable for the analytical nature of her work on Charles Babbage’s Analytical Engine.
    Language: Her contributions were theoretical, so imagine concise, yet deeply analytical expressions of algorithms.
    Citation: Lovelace is known for creating the first algorithm intended for a machine, emphasizing logical structure over verbosity.
3. Linus Torvalds – Creator of Linux Kernel
    Minimalism: Code is efficient, direct, and focused on performance. No unnecessary abstractions.
    Clean and Concise: Short functions with a preference for simplicity and pragmatism.
    Lack of Excessive Comments: Comments are kept to a minimum, often only when the code needs clarification.
    Straightforward Code: Torvalds values code that works without much decoration.
    Citation: Torvalds has frequently emphasized simplicity and performance in his work on the Linux kernel.
4. Guido van Rossum – Creator of Python
    Readability and Clarity: Code should be clear and readable, with an emphasis on simplicity and ease of understanding.
    Whitespace: Python’s use of indentation and spaces (no braces) reflects Guido's belief in code that reads like English.
    Explicit is Better than Implicit: The guiding principle of Python’s design.
    Function Definitions: Guido’s style favors simple, easy-to-follow functions that do one thing well.
    Citation: Guido van Rossum is the creator of Python and has consistently advocated for readability and simplicity in programming.
5. Donald Knuth – Creator of TeX and Algorithm Analysis
    Detailed Documentation: Knuth’s code is highly documented, with each function and algorithm explained in depth.
    Mathematical Rigor: Expect very detailed explanations of algorithmic steps, especially in terms of efficiency.
    Pedantic Formatting: Code is structured to fit the highest standards of correctness and readability.
    Citation: Knuth is the author of The Art of Computer Programming and creator of TeX, which emphasizes well-documented, mathematically sound algorithms.
6. Vint Cerf – Father of the Internet
    Networking Focus: Code tends to prioritize networking and distributed systems with clear modular boundaries.
    Efficiency: Code needs to be efficient in how it handles networking protocols.
    Low-Level Detail: While not necessarily focused on high-level design, his code would handle networking problems at a low level with precision.
    Clear Separation of Concerns: Networking and application layers are distinctly separated.
    Citation: Vint Cerf is a key figure behind the development of TCP/IP, ensuring that code works efficiently across networks.
7. James Gosling – Creator of Java
    Object-Oriented Design: Code is modular, object-oriented, and highly reusable.
    Cross-Platform: The design emphasizes portability and the "write once, run anywhere" philosophy.
    Verbose Syntax: Java is known for its verbose syntax, and Gosling’s coding style is no different—clear and explicit, with clear separation of concerns.
    Citation: Gosling's Java programming language emphasizes object-oriented principles and cross-platform compatibility.
8. Bjarne Stroustrup – Creator of C++
    Performance and Control: Code prioritizes efficiency and control over abstraction.
    Flexibility: C++ allows low-level memory manipulation, which Stroustrup leverages for performance.
    Object-Oriented and Generic Programming: Stroustrup advocates for strong support for both paradigms.
    C++-specific Constructs: Extensive use of templates and multiple inheritance.
    Citation: Stroustrup designed C++ to combine high performance with flexibility, enabling both low- and high-level programming.
9. Ken Thompson – Creator of UNIX
    Simplicity and Efficiency: Code is minimalistic, designed to do just enough to get the job done.
    Modular Design: UNIX and its tools follow a modular design philosophy—code should do one thing and do it well.
    Focus on Speed: Code is designed for quick execution, often with a focus on system-level efficiency.
    Citation: Thompson was integral in the development of UNIX, which is known for its simplicity and modularity.
10. Brian Kernighan – Co-author of UNIX and C Programming Language
    Clarity and Precision: Code should be clear and easy to understand, following the principle that simple is better.
    Minimalism: Avoid unnecessary complexity in code, especially in terms of system design.
    Small Programs: Strong emphasis on creating small programs that perform well with minimal overhead.
    Citation: Kernighan co-authored the book The C Programming Language with Dennis Ritchie, which focuses on writing clear and simple code.
11. John Carmack – Game Developer, Programmer
    Optimized and Efficient: Carmack is known for writing highly optimized code, particularly for graphics programming and game engines.
    Innovative Algorithms: Expect cutting-edge algorithms designed to maximize performance in games.
    Low-Level and High-Level Balance: Carmack blends low-level optimization with high-level design principles in game development.
    Citation: Carmack is known for his work on Doom and Quake, where he pushed the limits of game engine performance.
12. Tim Berners-Lee – Creator of the World Wide Web
    Clean and Simple: Code that serves its purpose without unnecessary complexity.
    Modular Design: Focus on flexibility and interoperability of different web technologies (HTML, CSS, HTTP).
    Standardization: Code follows standards to ensure compatibility across different systems.
    Citation: Berners-Lee designed the first web browser and web server, focusing on simplicity and interoperability.
13. Margaret Hamilton – Software Engineering Pioneer
    Safety and Reliability: Hamilton’s code focuses on safety and robustness, especially for mission-critical systems (e.g., Apollo Guidance Computer).
    Error Handling: Extensive error detection and recovery mechanisms.
    Detailed Documentation: Every step of the process is documented to ensure reliability in high-stakes environments.
    Citation: Hamilton was responsible for the software that took humans to the moon, prioritizing safety and reliability.
14. Jeff Dean – Google Engineer
    Scale and Efficiency: Code is designed for massive scale, especially for distributed systems.
    Optimized Algorithms: Focus on algorithms that maximize performance at scale.
    Concurrency: Expect a heavy use of concurrent processing techniques and multi-threaded execution.
    Citation: Jeff Dean worked on Google’s infrastructure and algorithms, focusing on scaling systems efficiently.
15. Edsger Dijkstra – Algorithm and Software Engineering Pioneer
    Elegance: Dijkstra's code is known for its elegance and mathematical beauty.
    Clear Structure: Code is highly structured and easy to follow, with an emphasis on correctness.
    Formal Methods: Use of formal verification methods and mathematical proofs in the design of algorithms.
    Citation: Dijkstra contributed to the development of algorithm design and formal methods in software engineering.
16. Scott Fahlman – Creator of the Emoticon and AI Researcher
    Logical and Structured: Code is designed with clarity and logic, avoiding unnecessary complexity.
    Clear Function Design: Functions and subroutines are defined with specific, clear purposes.
    Concise Comments: Comments are concise but provide enough context to understand the reasoning behind design decisions.
    Citation: Fahlman is known for his work on AI and the creation of the first emoticon (the smiley face).
17. Sheryl Sandberg – Technology Executive and Advocate
    Empathy and Communication: Code is designed with a focus on user experience, particularly in social and collaborative platforms.
    Clarity and Simplicity: Sandberg’s approach involves simplifying interactions, avoiding unnecessary complexity.
    Collaboration: Strong emphasis on team-based development and iterative feedback.
    Citation: Sandberg has been a key figure in Facebook’s growth, focusing on product simplicity and user engagement.
18. Marissa Mayer – Former Google Executive
    User-Centered Design: Mayer’s focus is on code that enhances user experience, often integrating feedback loops.
    Efficiency: Code should be efficient not just in execution, but also in user interaction and interface design.
    Productivity-Focused: Mayer's approach to code is centered around productivity, making systems faster and easier for users.
    Citation: Mayer played a major role in the development of Google’s user-centric products.
19. Richard Stallman – Free Software Movement Founder
    Freedom and Openness: Code should be free and open, allowing modification, redistribution, and collaboration.
    Simplicity and Functionality: Avoiding unnecessary complexity, with a focus on practical functionality.
    License-Driven: Emphasis on the use of open-source licenses (GPL) for code to ensure its freedom.
    Citation: Stallman is the founder of the Free Software Foundation and creator of the GNU Project, advocating for software freedom.
20. Vint Cerf - Father of the Internet
    Clarity and Modularity: Cerf's work on foundational internet protocols like TCP/IP reflects a style that prioritizes clean, modular design. His code would likely use logical decomposition and well-structured functions to make components reusable and maintainable.
    Robust Documentation: Cerf’s background suggests a focus on comprehensive comments and clear documentation to ensure that complex systems can be understood and extended by others. Expect a style that includes extensive inline comments, headers, and design rationales.
    Error Handling: Given the distributed nature of his work, Cerf’s style would likely emphasize rigorous error handling and fail-safes to ensure system resilience.
    Standards-Oriented: His style would adhere to established standards and best practices, reflecting his contributions to protocols that serve as the backbone of modern communication.
    Readable Naming: Expect meaningful variable and function names, reflecting the clarity and universality necessary in protocols designed for global use.
"""


def analyze_code_style(code):
    # Load a pre-trained model for text classification
    classifier = pipeline(
        "text-classification", model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    # Create the prompt with style descriptions and code
    prompt = f"{style_descriptions}\n\nCode:\n{code}\n\nWhich style does this code most closely match?"

    # Analyze the code style
    result = classifier(prompt)
    return result


if __name__ == "__main__":
    # Read all code files in the project directory
    code = ""
    for root, dirs, files in os.walk("/path/to/repository"):
        for file in files:
            if file.endswith(
                (".py", ".js", ".java", ".cpp", ".c", ".h", ".html", ".css", ".sh")
            ):
                with open(os.path.join(root, file), "r") as f:
                    code += f.read() + "\n"

    style_analysis = analyze_code_style(code)
    print(style_analysis)
