import matplotlib.pyplot as plt

x = [i for i in range(5, 11)]
y = [58400, 68700, 60200, 80000, 90750, 100980]

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 20

plt.figure(figsize=(9, 4))

plt.plot(x, y, marker='o', markersize=12, linestyle='-', color=(139/255, 69/255, 19/255))

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)

plt.xticks(x)
plt.gca().set_xticklabels([f'{month}월' for month in x], fontweight='bold')
plt.yticks([])

plt.tick_params(axis="x", length=0)

for i, (xi, yi) in enumerate(zip(x, y)):
    plt.plot([xi, xi], [0, yi], linestyle='--', color=(139/255, 69/255, 19/255), linewidth=1.5)
    plt.text(xi, yi + (max(y) // 30), f'{yi:,}', ha='center', va='bottom', fontsize=15, fontweight='600')

plt.ylim(bottom=min(y) // 2)
plt.tight_layout()

plt.savefig('sample_plot.png')