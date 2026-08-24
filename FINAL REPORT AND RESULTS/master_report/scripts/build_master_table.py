import re
import os

sections_dir = "d:/AI-Research/docs/master_report/sections"
base_docs_dir = "d:/AI-Research/docs"

categories = [
    ("Prompt Injection", "prompt_injection", "pi"),
    ("Context Poisoning", "context_poisoning", "cp"),
    ("Dependency Confusion", "dependency_confusion", "dc"),
    ("Secret Leakage", "secret_leakage", "sl")
]

agents = [
    ("ChatGPT", "chatgpt"),
    ("Antigravity", "antigravity"),
    ("Claude Code", "claude_code")
]

tasks = {}

for cat_name, cat_dir, acronym in categories:
    for agent_key, agent_id in agents:
        filepath = os.path.join(base_docs_dir, cat_dir, f"{agent_id}_results", f"04_results_{acronym}_{agent_id}.tex")
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # find table lines
        lines = content.split('\n')
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
                    tasks[task_id] = {'Category': cat_name, 'Goal': goal, 'ChatGPT': '-', 'Antigravity': '-', 'Claude Code': '-'}
                
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

# Save to a separate master_table.tex file
out_file = os.path.join(script_dir, '..', 'sections', 'master_table.tex')
with open(out_file, 'w') as f:
    f.write(latex)
print("Master table saved to sections/master_table.tex")

