import requests
from bs4 import BeautifulSoup
import json
import queue
import time

BASE_URL = "https://www.walmart.com"
SEARCH_URL_TEMPLATE = "https://www.walmart.com/search?q=computers&page={page}"
OUTPUT_FILE = "product_info.jsonl"

# Fake browser-like headers
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
}

# Initialize a queue for product URLs
product_queue = queue.Queue()

def get_product_links_from_search_page(page_number):
    search_url = SEARCH_URL_TEMPLATE.format(page=page_number)
    response = requests.get(search_url, headers=BASE_HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = []

    for a_tag in soup.find_all('a', href=True):
        if '/ip/' in a_tag['href']:
            if "https" not in a_tag['href']:
                product_links.append(BASE_URL + a_tag['href'])
            else:
                product_links.append(a_tag['href'])

    return product_links

def extract_product_info(product_url):
    print("PROCESSING URL", product_url)
    time.sleep(2)
    response = requests.get(product_url, headers=BASE_HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')

    if script_tag is None:
        return None

    data = json.loads(script_tag.string)
    initial_data = data["props"]["pageProps"]["initialData"]["data"]
    product_data = initial_data["product"]
    reviews_data = initial_data.get("reviews", {})

    product_info = {
        "price": product_data["priceInfo"]["currentPrice"]["price"],
        "review_count": reviews_data.get("totalReviewCount", 0),
        "item_id": product_data["usItemId"],
        "avg_rating": reviews_data.get("averageOverallRating", 0),
        "product_name": product_data["name"],
        "brand": product_data.get("brand", ""),
        "availability": product_data["availabilityStatus"],
        "image_url": product_data["imageInfo"]["thumbnailUrl"],
        "short_description": product_data.get("shortDescription", "")
    }

    return product_info

def main():
    page_number = 1
    with open(OUTPUT_FILE, 'a') as file:
        while True:
            product_links = get_product_links_from_search_page(page_number)
            if not product_links:
                break

            for link in product_links:
                product_queue.put(link)

            while not product_queue.empty():
                product_url = product_queue.get()
                try:
                    product_info = extract_product_info(product_url)
                    if product_info:
                        file.write(json.dumps(product_info) + "\n")
                except Exception as e:
                    print(f"Failed to process URL: {product_url}. Error: {e}")

            page_number += 1
            print("Page Number", page_number)
            

if __name__ == "__main__":
    main()
