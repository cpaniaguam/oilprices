# Heating Oil Price Finder

This Python service fetches the main table from the [New England Oil website](https://www.newenglandoil.com/rhodeisland/zone4.asp?x=0) and identifies the heating oil supplier with the lowest price greater than zero in Zone 4 of Rhode Island.

## Features
- Scrapes the heating oil supplier table from the specified webpage.
- Extracts the "Company Name" and "Price" columns.
- Identifies the company with the lowest price greater than zero.

## Requirements
- Python 3.10+
- Required Python packages:
  - `requests`
  - `beautifulsoup4`

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd oilprices
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script to fetch the company with the lowest heating oil price greater than zero:
```bash
python3 lowest_price_service.py
```

## Output
The script will output the name of the company with the lowest price and the corresponding price. For example:
```
The company with the lowest price greater than zero is ABC Oil with a price of $2.45
```

## License
This project is licensed under the MIT License.