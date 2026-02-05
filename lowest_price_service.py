import requests
from bs4 import BeautifulSoup

def fetch_lowest_price_provider():
    url = "https://www.newenglandoil.com/rhodeisland/zone4.asp?x=0"
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

if __name__ == "__main__":
    try:
        company, price = fetch_lowest_price_provider()
        print(f"The company with the lowest price greater than zero is {company} with a price of ${price:.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")