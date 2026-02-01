from app.scrapers.mercadolivre import scrape_mercadolivre
import sys

# Ensure the parent directory is in python path to import app module
sys.path.append('.')

def test():
    query = "iphone"
    print(f"Testing Mercado Livre Scraper with query: {query}")
    results = scrape_mercadolivre(query)
    print(f"Found {len(results)} results.")
    if results:
        print("First result:")
        print(results[0])
    else:
        print("No results found.")

if __name__ == "__main__":
    test()
