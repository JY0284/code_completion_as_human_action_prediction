"""Replot all 24 accuracy values reported in Table 5 of the paper draft.

Run from any directory with Python and Matplotlib installed.
Source: docs/data/reported-results.json, transcribed from the repository PDF.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def main():
    folder = Path(__file__).resolve().parent
    data = json.loads((folder.parent / "data" / "reported-results.json").read_text(encoding="utf-8"))
    table = data["table_5"]
    rows = table["rows"]
    x = [row["max_context_length"] for row in rows]
    assert x == list(range(8))
    assert table["window_order"] == [4, 6, 8]
    assert all(len(row["accuracy_percent"]) == 3 for row in rows)

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "text.color": "#243247", "axes.labelcolor": "#243247",
        "xtick.color": "#445166", "ytick.color": "#445166",
        "svg.fonttype": "none", "svg.hashsalt": "internetware2022-table5",
    })
    fig, axes = plt.subplots(1, 3, figsize=(12, 5.9), sharey=True)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.34, top=0.77, wspace=0.15)
    fig.suptitle("Reported context ablation (Internetware 2022)", x=0.07, y=0.97,
                 ha="left", fontsize=17, fontweight="bold")
    fig.text(0.07, 0.89, "Source: repository paper draft, Table 5 (PDF page 9); all 24 reported values.", fontsize=11)

    for column, (axis, window) in enumerate(zip(axes, table["window_order"])):
        y = [float(row["accuracy_percent"][column]) for row in rows]
        assert all(0 <= value <= 100 for value in y)
        axis.plot(x, y, color="#2367A4", linewidth=1.8, marker="o", markersize=5)
        axis.set_ylim(0, 100)
        axis.set_xlim(-0.35, 7.35)
        axis.set_xticks(x)
        axis.set_yticks(range(0, 101, 20))
        axis.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        axis.grid(axis="y", color="#DDE2E8", linewidth=0.7)
        axis.set_axisbelow(True)
        for side in ["top", "right"]:
            axis.spines[side].set_visible(False)
        for side in ["left", "bottom"]:
            axis.spines[side].set_color("#BCC5D0")
        axis.set_title("Window: {} actions".format(window), fontsize=12, pad=13)
        axis.set_xlabel("max_context_length", labelpad=9)
        axis.annotate("{:.2f}%".format(y[0]), (x[0], y[0]), xytext=(0, -19),
                      textcoords="offset points", ha="left", fontsize=10)
        axis.annotate("{:.2f}%".format(y[-1]), (x[-1], y[-1]), xytext=(0, 12),
                      textcoords="offset points", ha="right", fontsize=10)
        count = data["table_3"]["test_methods_by_window"][str(window)]
        axis.text(0.5, -0.32, "{:,} eligible test methods".format(count),
                  transform=axis.transAxes, ha="center", fontsize=10)
    axes[0].set_ylabel("Reported Top-5 accuracy (%)", labelpad=12)
    fig.text(0.07, 0.07,
             "30,000 selected test sequences per experiment; test-method sets differ by window.\n"
             "No confidence intervals reported. Context limit is a paper parameter, not BPE-token count.",
             fontsize=10, linespacing=1.6)
    svg_path = folder / "context-ablation.svg"
    fig.savefig(svg_path, facecolor="white", metadata={"Date": None})
    # Keep generated text consistent across operating systems.
    svg_lines = svg_path.read_bytes().splitlines()
    svg_path.write_bytes(b"\n".join(line.rstrip() for line in svg_lines) + b"\n")
    fig.savefig(folder / "context-ablation.png", facecolor="white", dpi=160)
    plt.close(fig)
    print("Rendered context-ablation.svg and context-ablation.png from 24 reported values.")


if __name__ == "__main__":
    main()
