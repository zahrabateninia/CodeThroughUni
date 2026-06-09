#!/usr/bin/env python3
import matplotlib.pyplot as plt

X = [7, 8, 12, 1, 4, 0, 9, 1, 3, 5]
indices = list(range(len(X)))  # x positions: 0..9

# Create a colorful bar chart
plt.figure(figsize=(10, 6))

bars = plt.bar(
    indices,
    X,
    color=[
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ],
    edgecolor="black",
    linewidth=1.2
)

plt.title("Bar Chart of X Values", fontsize=16, fontweight="bold")
plt.xlabel("Index", fontsize=14)
plt.ylabel("Value", fontsize=14)


for i, v in enumerate(X):
    plt.text(
        i, v + 0.2, str(v),
        ha="center", va="bottom",
        fontsize=11, fontweight="bold"
    )

plt.xticks(indices, [str(i) for i in indices], fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()
