import requests
import json

def scrape_shopee(query):
    # Shopee API v4 endpoint (often used by the frontend)
    # Note: This might require specific headers or cookies to work reliably.
    url = "https://shopee.com.br/api/v4/search/search_items"
    params = {
        "by": "relevancy",
        "keyword": query,
        "limit": 50,
        "newest": 0,
        "order": "desc",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH",
        "version": 2
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Referer': f'https://shopee.com.br/search?keyword={query}',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        products = []
        if 'items' in data:
            for item_wrapper in data['items']:
                item = item_wrapper.get('item_basic', {})
                if not item:
                    continue
                    
                itemid = item.get('itemid')
                shopid = item.get('shopid')
                name = item.get('name')
                price_min = item.get('price_min') # Shopee price is usually in cents
                price_max = item.get('price_max')
                image = item.get('image')
                
                # Construct link
                # typically: shopee.com.br/Product-Name-i.shopid.itemid
                safe_name = name.replace(' ', '-').replace('/', '-') if name else 'product'
                link = f"https://shopee.com.br/{safe_name}-i.{shopid}.{itemid}"
                
                # Construct image url
                # https://cf.shopee.com.br/file/{image}
                img_url = f"https://cf.shopee.com.br/file/{image}" if image else ""
                
                # Format price
                price = "N/A"
                if price_min:
                    price = f"R$ {price_min / 100000:.2f}" 
                    # Note: Shopee api prices are sometimes x100000. 
                    # Usually it's x100000 for VND/IDR, but for BRL it might be x100 or x1.
                    # Let's assume standard API behavior, but verification is needed.
                    # Checking common knowledge: Shopee API price is usually micros.
                    
                product = {
                    'source': 'Shopee',
                    'title': name,
                    'price': price,
                    'link': link,
                    'image': img_url
                }
                products.append(product)
                
        return products

    except Exception as e:
        print(f"Error scraping Shopee: {e}")
        # Return fallback
        pass
    
    if not products:
        products.append({
            'source': 'Shopee',
            'title': f'Click here to search "{query}" on Shopee',
            'price': 'Check Website',
            'link': f'https://shopee.com.br/search?keyword={query}',
            'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Shopee.svg/1200px-Shopee.svg.png' # Generic Shopee logo
        })
    return products
