# Heating Oil Price Finder

This Python service fetches the main table from the [New England Oil website](https://www.newenglandoil.com/rhodeisland/zone4.asp?x=0) and identifies the heating oil supplier with the lowest price in Zone 4 of Rhode Island.

## Features
- Scrapes the heating oil supplier table from the specified webpage.
- Extracts the "Company Name" and "Price" columns.
- Identifies the company with the lowest price greater than zero.

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd oilprices
   ```
2. Install the required dependencies:
   ```bash
   uv sync
   ```

## Usage
Run the script to fetch the company with the lowest heating oil price greater than zero:
```bash
uv run lowest_price_service.py
```

## Output
The script will output the name of the company with the lowest price and the corresponding price. For example:
```

The company with the lowest price is XYZ OIL with a price of $4.25
```

## Graph CLI
Render the historical price data as a simple text graph or a visual plot using `graph.py`.

- **Purpose:** Show average price trend over time from `price_history.json`.
- **Flags:**
   - `--file, -f`: Path to the JSON price history file (default: `price_history.json`).
   - `--scale, -s`: Maximum width for the text graph bars (default: `50`).
   - `--mode, -m`: Output mode — `txt` for a terminal text graph (default) or `viz` to open a matplotlib plot.

- **Examples:**

```bash
# text graph using the default file
uv run graph.py

# text graph with a larger bar scale
uv run graph.py --mode txt --scale 80

# show a visual plot
uv run graph.py --mode viz
```

## License
This project is licensed under the MIT License.