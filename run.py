from flask import Flask, render_template, request, jsonify
from app.scrapers.mercadolivre import scrape_mercadolivre
from app.scrapers.amazon import scrape_amazon
from app.scrapers.shopee import scrape_shopee
import concurrent.futures

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return render_template('index.html', error='Please enter a search term')

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(scrape_mercadolivre, query),
            executor.submit(scrape_amazon, query),
            executor.submit(scrape_shopee, query)
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Scraper error: {e}")

    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
