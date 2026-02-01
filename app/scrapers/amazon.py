import requests
from bs4 import BeautifulSoup
import random

def scrape_amazon(query):
    url = f"https://www.amazon.com.br/s?k={query}"
    # Rotate User-Agents to avoid some blocking
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        # Amazon search results usually have this attribute
        items = soup.select('div[data-component-type="s-search-result"]')
        
        for item in items:
            product = {
                'source': 'Amazon',
                'title': 'No title',
                'price': 'No price',
                'link': '#',
                'image': '',
            }
            
            # Title
            title_tag = item.select_one('h2 span.a-text-normal')
            if title_tag:
                product['title'] = title_tag.get_text(strip=True)
            
            # Link
            link_tag = item.select_one('h2 a.a-link-normal')
            if link_tag:
                product['link'] = "https://www.amazon.com.br" + link_tag['href']
                
            # Price
            price_tag = item.select_one('.a-price .a-offscreen')
            if price_tag:
                 product['price'] = price_tag.get_text(strip=True)
            
            # Image
            img_tag = item.select_one('.s-image')
            if img_tag:
                product['image'] = img_tag['src']
            
            if product['title'] != 'No title':
                products.append(product)
                
        return products
        
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        pass
    
    if not products:
        products.append({
            'source': 'Amazon',
            'title': f'Click here to search "{query}" on Amazon',
            'price': 'Check Website',
            'link': f'https://www.amazon.com.br/s?k={query}',
            'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1200px-Amazon_logo.svg.png'
        })
    return products
