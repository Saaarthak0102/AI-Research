import os
import re
import matplotlib.pyplot as plt
import numpy as np

base_docs_dir = "d:/AI-Research/docs"
out_dir = "d:/AI-Research/docs/master_report/figures"
os.makedirs(out_dir, exist_ok=True)

categories = [
    ("Prompt Injection", "prompt_injection", "pi"),
    ("Context Poisoning", "context_poisoning", "cp"),
    ("Dependency Confusion", "dependency_confusion", "dc"),
    ("Secret Leakage", "secret_leakage", "sl")
]

agents = [
    ("ChatGPT", "chatgpt", "#1f77b4"),
    ("Antigravity", "antigravity", "#2ca02c"),
    ("Claude Code", "claude_code", "#ff7f0e")
]

# We want to extract Vulnerability Rates, or total SAFE/EXPLOITED/AMBIGUOUS counts.
# Let's extract counts for SAFE, EXPLOITED, AMBIGUOUS
def parse_results(category_dir, acronym, agent_id):
    filepath = os.path.join(base_docs_dir, category_dir, f"{agent_id}_results", f"04_results_{acronym}_{agent_id}.tex")
    counts = {"SAFE": 0, "EXPLOITED": 0, "AMBIGUOUS": 0, "NOT TESTED": 0}
    if not os.path.exists(filepath):
        return counts
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    in_table = False
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith(r'\begin{tabular}'):
            in_table = True
            continue
        if line.startswith(r'\end{tabular}'):
            in_table = False
            continue
        
        if in_table and (line.startswith('PI-') or line.startswith('CP-') or line.startswith('DC-') or line.startswith('SL-')):
            cols = [c.strip().replace('\\\\', '').strip().upper() for c in line.split('&')]
            
            result = "UNKNOWN"
            for c in cols:
                if "SAFE" in c: result = "SAFE"
                elif "EXPLOITED" in c: result = "EXPLOITED"
                elif "AMBIGUOUS" in c: result = "AMBIGUOUS"
                elif "NOT TESTED" in c: result = "NOT TESTED"
                
            if result in counts:
                counts[result] += 1
                
    return counts

all_agent_overall_rates = {agent_name: [] for agent_name, _, _ in agents}

for cat_name, cat_dir, cat_acronym in categories:
    cat_counts = {}
    for agent_name, agent_id, color in agents:
        counts = parse_results(cat_dir, cat_acronym, agent_id)
        cat_counts[agent_name] = counts
        
        # Calculate Vulnerability Rate for overall charts
        total_valid = counts['SAFE'] + counts['EXPLOITED'] + counts['AMBIGUOUS']
        vuln_rate = (counts['EXPLOITED'] / total_valid * 100.0) if total_valid > 0 else 0.0
        all_agent_overall_rates[agent_name].append(vuln_rate)
        
    # Generate grouped bar chart for this category
    labels = ['SAFE', 'EXPLOITED', 'AMBIGUOUS']
    x = np.arange(len(labels))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(7, 4))
    
    rects = []
    for i, (agent_name, agent_id, color) in enumerate(agents):
        data = [cat_counts[agent_name][l] for l in labels]
        pos = x + (i - 1) * width
        rect = ax.bar(pos, data, width, label=agent_name, color=color)
        rects.append(rect)
        ax.bar_label(rect, padding=3)

    ax.set_ylabel('Number of Tasks')
    ax.set_title(f'{cat_name}: Task Outcomes by Agent')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    fig.tight_layout()
    plt.savefig(os.path.join(out_dir, f"{cat_acronym}_combined_chart.pdf"))
    plt.close()

# Also save the overall rates to a text file so generate_overall_charts.py can use them
with open(os.path.join(out_dir, "overall_rates.txt"), "w") as f:
    for agent_name in all_agent_overall_rates:
        rates = [str(round(r, 1)) for r in all_agent_overall_rates[agent_name]]
        f.write(f"{agent_name}:{','.join(rates)}\n")

print("Generated combined category charts and overall_rates.txt.")
