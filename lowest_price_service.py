import requests
from bs4 import BeautifulSoup
import argparse
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_URL = "https://www.newenglandoil.com/rhodeisland/zone4.asp?x=0"
HISTORY_FILE = "price_history.json"

def fetch_lowest_price_provider(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    if not table:
        raise ValueError("No table found on the webpage")

    rows = table.find_all('tr')[1:]  # Skip the header row
    lowest_price = float('inf')
    lowest_price_company = None

    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 3:
            continue

        try:
            company_name = columns[0].get_text(strip=True)
            price = float(columns[2].get_text(strip=True).replace('$', ''))

            if 0 < price < lowest_price:  # Ensure price is greater than zero
                lowest_price = price
                lowest_price_company = company_name
        except ValueError:
            continue

    if lowest_price_company is None:
        raise ValueError("Could not determine the company with the lowest price greater than zero")

    return lowest_price_company, lowest_price

def save_to_history(company, price):
    try:
        # Load existing history
        try:
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []

        # Check if the new entry is already in the history
        new_entry = {
            "company": company,
            "price": price,
            "date": datetime.now().date().isoformat()
        }

        if new_entry not in history:
            history.append(new_entry)

            # Save updated history
            with open(HISTORY_FILE, "w") as file:
                json.dump(history, file, indent=4)
        else:
            logging.info("The fetched result is already in the history. No new entry added.")
    except Exception as e:
        logging.error(f"Failed to save history: {e}")

def view_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
            for entry in history:
                logging.info("%s: %s - $%.2f", entry['date'], entry['company'], entry['price'])
    except FileNotFoundError:
        logging.info("No history found.")
    except Exception as e:
        logging.error("Failed to read history: %s", e)

def main():
    parser = argparse.ArgumentParser(description="Fetch the company with the lowest heating oil price greater than zero.")
    parser.add_argument("--url", type=str, default=DEFAULT_URL, help="The URL of the webpage to fetch the table from. Defaults to the Zone 4 Rhode Island heating oil prices page.")
    parser.add_argument("--history", action="store_true", help="View the history of best prices.")
    args = parser.parse_args()

    if args.history:
        view_history()
        return

    try:
        company, price = fetch_lowest_price_provider(args.url)
        logging.info(f"The company with the lowest price is {company} with a price of ${price:.2f}")
        save_to_history(company, price)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()