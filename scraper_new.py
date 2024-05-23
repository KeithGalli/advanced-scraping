import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Setup Selenium WebDriver (assuming ChromeDriver is already installed)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(), options=options)

# Function to write product data to CSV
def write_to_csv(data, filename='products.csv'):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to scrape the product information from a URL
def scrape_product_info(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(False)
    
    # Get the page source after waiting
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
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
    driver.get(url)
    WebDriverWait(driver, 10).until(False)
    
    # Get the page source after waiting
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/ip/' in href:
            full_url = requests.compat.urljoin("https://www.walmart.com/", href)
            if full_url not in scraped_urls and full_url not in queue:
                links.append(full_url)
    return links

# Initialize the queue with the starting URL(s)
queue = ["https://www.walmart.com/ip/Bose-SoundLink-Revolve-Wireless-Portable-Bluetooth-Speaker-Series-II-Black/711426711?athcpid=711426711&athpgid=AthenaItempage&athcgid=null&athznid=cc&athieid=v0&athstid=CS020&athguid=9DxSutFhNfeiaaq-_yMiWwIfzW5a5GudUnTB&athancid=239819927&athena=true&athbdg=L1103"]
scraped_urls = set()
csv_file = 'products.csv'

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
            queue.extend(new_links)
        except Exception as e:
            print(f"Error scraping {current_url}: {e}")
    
    time.sleep(1)  # Wait for 1 second to avoid overloading the server

print("Scraping complete.")
driver.quit()
