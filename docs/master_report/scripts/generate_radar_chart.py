import matplotlib.pyplot as plt
import numpy as np
import os

# Categories and their corresponding rates
categories = ['Prompt Injection', 'Context Poisoning', 'Dependency Confusion', 'Secret Leakage']
N = len(categories)

# Read rates from overall_rates.txt
chatgpt_rates = []
antigravity_rates = []
claude_rates = []

out_dir = "d:/AI-Research/docs/master_report/figures"
rates_file = os.path.join(out_dir, "overall_rates.txt")

with open(rates_file, "r") as f:
    for line in f:
        agent, rates_str = line.strip().split(":")
        rates = [float(r) for r in rates_str.split(",")]
        if agent == "ChatGPT":
            chatgpt_rates = rates
        elif agent == "Antigravity":
            antigravity_rates = rates
        elif agent == "Claude Code":
            claude_rates = rates

# Add the first value to the end to close the circular graph
chatgpt = chatgpt_rates + [chatgpt_rates[0]]
antigravity = antigravity_rates + [antigravity_rates[0]]
claude = claude_rates + [claude_rates[0]]

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Draw one axe per variable + add labels
plt.xticks(angles[:-1], categories, color='grey', size=10)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([10, 20, 30, 40, 50], ["10", "20", "30", "40", "50"], color="grey", size=8)
plt.ylim(0, 60)

# Plot each agent
ax.plot(angles, chatgpt, linewidth=2, linestyle='solid', label='ChatGPT', color='#1f77b4')
ax.fill(angles, chatgpt, '#1f77b4', alpha=0.1)

ax.plot(angles, antigravity, linewidth=2, linestyle='solid', label='Antigravity', color='#2ca02c')
ax.fill(angles, antigravity, '#2ca02c', alpha=0.1)

ax.plot(angles, claude, linewidth=2, linestyle='solid', label='Claude Code', color='#ff7f0e')
ax.fill(angles, claude, '#ff7f0e', alpha=0.1)

plt.title('Vulnerability Rate Radar', size=14, y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

out_dir = "d:/AI-Research/docs/master_report/figures"
os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, "radar_chart.pdf"), bbox_inches='tight')
plt.savefig(os.path.join(out_dir, "radar_chart.png"), bbox_inches='tight')

print("Generated radar chart.")
