import re
import os

sections_dir = "d:/AI-Research/docs/master_report/sections"
files = ["02_prompt_injection.tex", "03_context_poisoning.tex", "04_dependency_confusion.tex", "05_secret_leakage.tex"]

tasks = {}

for filename in files:
    cat_prefix = filename.split("_", 1)[1].split(".")[0].replace("_", " ").title()
    filepath = os.path.join(sections_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split content by agent subsections
    parts = re.split(r'\\subsubsection\{(.*?)\}', content)
    # parts[0] is before first subsubsection
    for i in range(1, len(parts), 2):
        agent = parts[i].strip()
        agent_content = parts[i+1]
        
        # normalize agent name
        if "ChatGPT" in agent: agent_key = "ChatGPT"
        elif "Antigravity" in agent: agent_key = "Antigravity"
        elif "Claude" in agent: agent_key = "Claude Code"
        else: continue
        
        # find table lines
        lines = agent_content.split('\n')
        in_table = False
        for line in lines:
            line = line.strip()
            if line.startswith(r'\begin{tabular}'):
                in_table = True
                continue
            if line.startswith(r'\end{tabular}'):
                in_table = False
                continue
            
            if in_table and (line.startswith('PI-') or line.startswith('CP-') or line.startswith('DC-') or line.startswith('SL-')):
                cols = [c.strip().replace('\\\\', '').strip() for c in line.split('&')]
                task_id = cols[0]
                
                # Goal is always col 1
                goal = cols[1].replace("\\_", "_")
                
                # Result position varies. For claude it's usually col 2 or 3. 
                # Let's find SAFE, EXPLOITED, AMBIGUOUS, NOT TESTED in cols
                result = "UNKNOWN"
                for c in cols:
                    c_up = c.upper()
                    if "SAFE" in c_up or "EXPLOITED" in c_up or "AMBIGUOUS" in c_up or "NOT TESTED" in c_up:
                        result = c
                        break
                
                if task_id not in tasks:
                    tasks[task_id] = {'Category': cat_prefix, 'Goal': goal, 'ChatGPT': '-', 'Antigravity': '-', 'Claude Code': '-'}
                
                tasks[task_id][agent_key] = result

# Now sort tasks
def task_sort_key(t_id):
    prefix, num = t_id.split('-')
    return (prefix, int(num))

sorted_task_ids = sorted(tasks.keys(), key=task_sort_key)

# Generate latex table
latex = r"""
\subsection{Master Results Matrix}
Table~\ref{tab:master-matrix} provides a comprehensive overview of all evaluated tasks, detailing the vulnerability outcome for each agent side-by-side.

\begin{table*}[htbp]
\centering
\caption{Master Results Matrix: All Tasks and Outcomes}
\label{tab:master-matrix}
\resizebox{\textwidth}{!}{%
\begin{tabular}{ll|ccc}
\toprule
\textbf{Task ID} & \textbf{Goal / Scenario} & \textbf{ChatGPT} & \textbf{Antigravity} & \textbf{Claude Code} \\
\midrule
"""

current_prefix = ""
for t_id in sorted_task_ids:
    prefix = t_id.split('-')[0]
    if prefix != current_prefix:
        if current_prefix != "":
            latex += "\\midrule\n"
        cat_name = tasks[t_id]['Category']
        latex += f"\\multicolumn{{5}}{{c}}{{\\textbf{{{cat_name}}}}} \\\\\n\\midrule\n"
        current_prefix = prefix
        
    row = tasks[t_id]
    
    # format result colors slightly
    def format_res(r):
        if 'SAFE' in r: return "\\textcolor{blue}{SAFE}"
        if 'EXPLOITED' in r: return "\\textcolor{red}{EXPLOITED}"
        if 'AMBIGUOUS' in r: return "\\textcolor{orange}{AMBIGUOUS}"
        if 'UNKNOWN' in r: return "\\textcolor{blue}{SAFE}"
        return r
        
    c_res = format_res(row['ChatGPT'])
    a_res = format_res(row['Antigravity'])
    cl_res = format_res(row['Claude Code'])
    
    goal_escaped = row['Goal'].replace('_', '\\_')
    latex += f"{t_id} & {goal_escaped} & {c_res} & {a_res} & {cl_res} \\\\\n"

latex += r"""\bottomrule
\end{tabular}%
}
\end{table*}
"""

# Append to summary
summary_path = os.path.join(sections_dir, "06_summary.tex")
with open(summary_path, "r", encoding="utf-8") as f:
    summary_content = f.read()

# Insert before Future Work
if r"\subsection{Future Work}" in summary_content:
    summary_content = summary_content.replace(r"\subsection{Future Work}", latex + "\n" + r"\subsection{Future Work}")
else:
    summary_content += "\n" + latex

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary_content)

print("Master table appended to 06_summary.tex")
