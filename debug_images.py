import requests
from bs4 import BeautifulSoup
import json

def debug_ml(query):
    print(f"--- Debugging Mercado Livre ({query}) ---")
    url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'}
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        item = soup.select_one('li.ui-search-layout__item')
        if item:
            print("Found item.")
            img_tag = item.select_one('.poly-component__image') or item.select_one('.poly-card__portada img') or item.select_one('img.ui-search-result-image__element')
            if img_tag:
                print("Image Tag:", img_tag)
                print("src:", img_tag.get('src'))
                print("data-src:", img_tag.get('data-src'))
            else:
                print("No image tag found in item.")
                # Print more of the item html
                print(item.prettify()[:1000])
        else:
            print("No items found.")
    except Exception as e:
        print("Error:", e)

def debug_shopee(query):
    print(f"\n--- Debugging Shopee ({query}) ---")
    url = f"https://shopee.com.br/search?keyword={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    try:
        r = requests.get(url, headers=headers)
        print("Status Code:", r.status_code)
        if r.status_code == 200:
            print("Response length:", len(r.text))
            if "shopee.com.br/api/v4/search/search_items" in r.text:
                print("Found API reference in HTML.")
            # Check for JSON in scripts
            soup = BeautifulSoup(r.text, 'html.parser')
            # Shopee textual results?
            items = soup.select('.shopee-search-item-result__item')
            print(f"Found {len(items)} HTML items.")
        else:
             print("Coult not fetch HTML.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    debug_ml("iphone")
    debug_shopee("iphone")
