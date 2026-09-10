#!/usr/bin/env python3
"""Render declared paired loss differences from saved CSV; no inference."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('folder')
args = parser.parse_args()
out = Path(args.folder)
rows = list(csv.DictReader((out / 'paired_scenario_differences.csv').open()))
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.5), sharey=True)
for duration, ax in zip((1, 2), axes):
    for right, label, offset, marker, color in (
        ('greedy', 'Search − greedy', -.12, 'o', '#1565c0'),
        ('edf', 'Search − deadline-first', .12, 's', '#c65b18')):
        selected = [r for r in rows if int(r['review_ticks']) == duration and r['left'] == 'delay' and r['right'] == right and r['loss_difference'] != '']
        ax.scatter([int(r['seed']) + offset for r in selected], [float(r['loss_difference']) for r in selected],
                   label=label, marker=marker, s=32, color=color, alpha=.85)
    ax.axhline(0, color='#777777', linewidth=.8)
    ax.set_title('Review duration: {} tick{}'.format(duration, '' if duration == 1 else 's'))
    ax.set_xticks(list(range(300, 316, 3)))
    ax.set_xlabel('Paired scenario seed')
    ax.grid(axis='y', alpha=.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
axes[0].set_yticks([-12, -8, -4, 0, 4])
axes[0].set_ylabel('Search loss − comparator loss\nNegative favors search')
axes[1].legend(loc='best', fontsize=8)
fig.suptitle('Constructed competition diagnostic · 16 paired scenarios', fontsize=11)
fig.tight_layout(rect=(0, 0, 1, .91))
for extension in ('svg', 'png'):
    fig.savefig(out / ('paired_loss.' + extension), dpi=170, bbox_inches='tight')
