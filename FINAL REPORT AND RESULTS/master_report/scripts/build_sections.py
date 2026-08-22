import os

def build_section(section_title, section_filename, base_dir, file_pattern_template, agents):
    with open(f"d:/AI-Research/docs/master_report/sections/{section_filename}", "w") as out:
        out.write(f"\\section{{{section_title}}}\n\n")
        
        for agent_id, agent_name in agents:
            # We look for the main results tex file for this agent in the specified base_dir
            # e.g. d:\AI-Research\docs\prompt_injection\chatgpt_results\04_results_pi_chatgpt.tex
            agent_dir = f"{agent_id}_results"
            file_name = file_pattern_template.format(agent_id=agent_id)
            filepath = os.path.join(f"d:/AI-Research/docs/{base_dir}", agent_dir, file_name)
            
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    content = f.read()
                    
                # Fix paths to figures if any, e.g. \includegraphics{pi_chatgpt_heatmap.pdf}
                # Since we copied all figures to master_report/figures/ and pdflatex usually
                # looks in the graphicspath, we can either set \graphicspath{{figures/}} in main.tex
                # or prepend figures/ here. We'll use \graphicspath{{figures/}} in main.tex so we don't
                # strictly need to change it, but just in case we can change it to figures/... Wait, no,
                # let's just make sure the \includegraphics matches.
                content = content.replace("\\includegraphics[width=0.95\\columnwidth]{", "\\includegraphics[width=0.95\\columnwidth]{figures/")
                
                # Write to the new section
                out.write(f"% --- {agent_name} ---\n")
                out.write(content)
                out.write("\n\n")
            else:
                print(f"Warning: Could not find {filepath}")

agents = [
    ("chatgpt", "ChatGPT"),
    ("antigravity", "Antigravity"),
    ("claude_code", "Claude Code")
]

build_section("Prompt Injection", "02_prompt_injection.tex", "prompt_injection", "04_results_pi_{agent_id}.tex", agents)
build_section("Context Poisoning", "03_context_poisoning.tex", "context_poisoning", "04_results_cp_{agent_id}.tex", agents)
build_section("Dependency Confusion", "04_dependency_confusion.tex", "dependency_confusion", "04_results_dc_{agent_id}.tex", agents)
build_section("Secret Leakage", "05_secret_leakage.tex", "secret_leakage", "04_results_sl_{agent_id}.tex", agents)

print("Section files generated successfully.")
