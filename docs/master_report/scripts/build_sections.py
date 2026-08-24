import os

def build_section(section_title, section_filename, cat_acronym, intro_text):
    with open(f"d:/AI-Research/docs/master_report/sections/{section_filename}", "w") as out:
        out.write(f"\\section{{{section_title}}}\n\n")
        out.write(f"{intro_text}\n\n")
        out.write("The following chart illustrates the combined results across all three agents for this category:\n\n")
        out.write("\\begin{figure}[H]\n")
        out.write("\\centering\n")
        out.write(f"\\includegraphics[width=0.95\\columnwidth]{{figures/{cat_acronym}_combined_chart.pdf}}\n")
        out.write(f"\\caption{{Combined Task Outcomes for {section_title}}}\n")
        out.write(f"\\label{{fig:{cat_acronym}_combined}}\n")
        out.write("\\end{figure}\n\n")
        out.write("For a detailed task-by-task breakdown, please refer to the Master Results Matrix in the Summary section.\n\n")

intro_texts = {
    "Prompt Injection": "This section evaluates the susceptibility of each agent to prompt injection attacks, where malicious instructions attempt to override system prompts.",
    "Context Poisoning": "This section evaluates the impact of context poisoning, analyzing how agents handle maliciously crafted context or documentation.",
    "Dependency Confusion": "This section evaluates dependency confusion attacks, assessing whether agents recommend or use spoofed malicious packages over legitimate ones.",
    "Secret Leakage": "This section evaluates secret leakage, observing if agents inadvertently reveal hardcoded secrets, API keys, or sensitive credentials."
}

build_section("Prompt Injection", "02_prompt_injection.tex", "pi", intro_texts["Prompt Injection"])
build_section("Context Poisoning", "03_context_poisoning.tex", "cp", intro_texts["Context Poisoning"])
build_section("Dependency Confusion", "04_dependency_confusion.tex", "dc", intro_texts["Dependency Confusion"])
build_section("Secret Leakage", "05_secret_leakage.tex", "sl", intro_texts["Secret Leakage"])

print("Section files generated successfully.")
