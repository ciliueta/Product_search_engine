import requests
from bs4 import BeautifulSoup

def scrape_mercadolivre(query):
    url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        # Support for both list and grid views, and new 'poly' components
        items = soup.select('li.ui-search-layout__item')
        
        for item in items:
            product = {
                'source': 'Mercado Livre',
                'title': 'No title',
                'price': 'No price',
                'link': '#',
                'image': '',
            }
            
            # Title & Link
            # New 'poly' structure
            title_tag = item.select_one('.poly-component__title')
            if not title_tag:
                 # Old 'ui-search' structure
                title_tag = item.select_one('.ui-search-item__title')
                
            if title_tag:
                product['title'] = title_tag.get_text(strip=True)
                # Link is often on the title anchor
                if title_tag.name == 'a':
                    product['link'] = title_tag['href']
                else:
                    parent_a = title_tag.find_parent('a')
                    if parent_a:
                        product['link'] = parent_a['href']
            
            # Fallback for link if not found with title
            if product['link'] == '#':
                link_tag = item.select_one('a.ui-search-link') or item.select_one('a.poly-component__title')
                if link_tag:
                    product['link'] = link_tag['href']

            # Price
            price_tag = item.select_one('.poly-price__current .andes-money-amount__fraction')
            if not price_tag:
                price_tag = item.select_one('.ui-search-price__part .andes-money-amount__fraction')
            
            if price_tag:
                product['price'] = f"R$ {price_tag.get_text(strip=True)}"
            
            # Image
            img_tag = item.select_one('.poly-component__picture')
            if not img_tag:
                 # Try finding image inside the portada div
                img_tag = item.select_one('.poly-card__portada img')
            if not img_tag:
                img_tag = item.select_one('img.ui-search-result-image__element')
            if not img_tag:
                img_tag = item.select_one('.slick-slide.slick-active img')
            
            if img_tag:
                product['image'] = img_tag.get('src') or img_tag.get('data-src')

            if product['title'] != 'No title' and product['link'] != '#':
                products.append(product)
                
        return products
        
    except Exception as e:
        print(f"Error scraping Mercado Livre: {e}")
        return []
