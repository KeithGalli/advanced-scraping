import requests
from bs4 import BeautifulSoup
import csv
import time

# Fake browser-like headers
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}


# Initialize the queue with the starting URL(s)
queue = ["https://www.walmart.com/ip/Bose-SoundLink-Flex-Wireless-Waterproof-Portable-Bluetooth-Speaker-Stone-Blue/239819927?athcpid=239819927&athpgid=AthenaContentPage_8375901&athcgid=null&athznid=ItemCarousel_8d6e53ca-39df-4a3e-b287-66252caf893c_items&athieid=v0&athstid=CS020&athguid=y7X9gmfjLc3RDDf0wZqcWn6vChKRpK2VAwVP&athancid=null&athena=true"]
scraped_urls = set()
csv_file = 'products.csv'

# Function to write product data to CSV
def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to scrape the product information from a URL
def scrape_product_info(url):
    response = requests.get(url, headers=BASE_HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    print("SOUP", soup)
    
    # Extract product information with robust checks
    product_name = soup.find('h1', {'id': 'main-title'})
    product_price = soup.find('span', {'itemprop': 'price'})
    product_rating = soup.find('span', {'itemprop': 'ratingValue'})
    product_reviews = soup.find('a', {'data-testid': 'item-review-section-link'})
    
    # Get the text if the element is found, else set to 'N/A'
    product_name_text = product_name.text.strip() if product_name else 'N/A'
    product_price_text = product_price.text.strip() if product_price else 'N/A'
    product_rating_text = product_rating.text.strip() if product_rating else 'N/A'
    product_reviews_text = product_reviews.text.strip() if product_reviews else 'N/A'
    
    # Write product data to CSV
    write_to_csv([product_name_text, product_price_text, product_rating_text, product_reviews_text])

# Function to extract links from a webpage
def extract_links(url):
    response = requests.get(url, headers=BASE_HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/ip/' in href:
            full_url = requests.compat.urljoin("https://www.walmart.com/", href)
            print("FULL URL", full_url)
            if full_url not in scraped_urls and full_url not in queue:
                links.append(full_url)
    return links

# Initialize CSV file with headers
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Rating', 'Number of Reviews'])

# Main loop
while queue:
    current_url = queue.pop(0)
    
    if current_url not in scraped_urls:
        try:
            scrape_product_info(current_url)
            scraped_urls.add(current_url)
            new_links = extract_links(current_url)
            print
            queue.extend(new_links)
        except Exception as e:
            print(f"Error scraping {current_url}: {e}")
    
    time.sleep(1)  # Wait for 1 second to avoid overloading the server

print("Scraping complete.")
