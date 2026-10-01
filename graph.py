import argparse
import json
from datetime import datetime
from pathlib import Path


def latest_price_per_day(records):
    """Map each date to the last price recorded that day (history is append-only)."""
    return {rec["date"]: rec["price"] for rec in records}


def build_text_graph(records, scale=50):
    daily = sorted(latest_price_per_day(records).items())
    max_price = max(price for _, price in daily) or 1
    lines = ["Lowest price trend:"]
    for date, price in daily:
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
    daily = latest_price_per_day(records)
    unique_dates = sorted(datetime.fromisoformat(d) for d in daily)
    prices = [daily[dt.date().isoformat()] for dt in unique_dates]
    fig, ax = plt.subplots()
    ax.plot(unique_dates, prices, marker="o")
    ax.set_xticks(unique_dates)
    ax.set_xticklabels([dt.strftime("%Y-%m-%d") for dt in unique_dates], rotation=45, ha="right")
    ax.set_ylabel("Lowest Price")
    ax.set_title("Lowest Oil Price Trend")
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