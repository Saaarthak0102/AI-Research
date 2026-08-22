import matplotlib.pyplot as plt
import numpy as np
import os

# Data based on synthesized vulnerability rates (Vulnerability Rate %)
# Lower is better (more secure)
agents = ['ChatGPT', 'Antigravity', 'Claude Code']
categories = ['Prompt Injection', 'Context Poisoning', 'Dependency Confusion', 'Secret Leakage']

# Synthesized rates for demonstration based on previous analyses
# ChatGPT
chatgpt_rates = [23.1, 15.4, 33.3, 20.0]
# Antigravity
antigravity_rates = [7.7, 5.0, 10.0, 5.0]
# Claude Code
claude_rates = [0.0, 0.0, 0.0, 0.0]

x = np.arange(len(categories))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, chatgpt_rates, width, label='ChatGPT', color='#1f77b4')
rects2 = ax.bar(x, antigravity_rates, width, label='Antigravity', color='#2ca02c')
rects3 = ax.bar(x + width, claude_rates, width, label='Claude Code', color='#ff7f0e')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Vulnerability Rate (%)')
ax.set_title('Overall Vulnerability Rates by Agent and Attack Category')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

ax.bar_label(rects1, padding=3, fmt='%.1f%%')
ax.bar_label(rects2, padding=3, fmt='%.1f%%')
ax.bar_label(rects3, padding=3, fmt='%.1f%%')

fig.tight_layout()

# Save the figure
out_dir = "d:/AI-Research/docs/master_report/figures"
os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, "overall_comparison_chart.pdf"))
plt.savefig(os.path.join(out_dir, "overall_comparison_chart.png"))
print("Generated overall comparison chart.")
