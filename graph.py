import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def build_text_graph(records, scale=50):
    records = sorted(records, key=lambda r: datetime.fromisoformat(r["date"]))
    date_price_map = defaultdict(list)
    for rec in records:
        date_price_map[rec["date"]].append(rec["price"])
    averages = [(date, sum(prices) / len(prices)) for date, prices in sorted(date_price_map.items())]
    max_price = max(price for _, price in averages) or 1
    lines = ["Average price trend:"]
    for date, price in averages:
        bar = "#" * int(price / max_price * scale)
        lines.append(f" {date} | {bar} {price:.3f}")
    return "\n".join(lines)


def build_matplotlib_graph(records):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise SystemExit(
            "matplotlib is required for --mode matplotlib; install it with `pip install matplotlib`."
        )
    date_price_map = defaultdict(list)
    for rec in records:
        date_price_map[datetime.fromisoformat(rec["date"])].append(rec["price"])
    unique_dates = sorted(date_price_map)
    averages = [sum(prices) / len(prices) for prices in (date_price_map[dt] for dt in unique_dates)]
    fig, ax = plt.subplots()
    ax.plot(unique_dates, averages, marker="o")
    ax.set_xticks(unique_dates)
    ax.set_xticklabels([dt.strftime("%Y-%m-%d") for dt in unique_dates], rotation=45, ha="right")
    ax.set_ylabel("Average Price")
    ax.set_title("Average Oil Price Trend")
    fig.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Render oil price history.")
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=Path("price_history.json"),
        help="JSON file containing the price history data.",
    )
    parser.add_argument(
        "--scale",
        "-s",
        type=int,
        default=50,
        help="Maximum width for the text graph bars.",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["txt", "viz"],
        default="txt",
        help="Output mode: text (default) or visual line plot.",
    )
    args = parser.parse_args()
    records = json.loads(args.file.read_text())
    if args.mode == "txt":
        print(build_text_graph(records, scale=args.scale))
    else:
        build_matplotlib_graph(records)


if __name__ == "__main__":
    main()