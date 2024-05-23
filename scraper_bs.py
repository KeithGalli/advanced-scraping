import requests
from bs4 import BeautifulSoup
import json

# Fake browser-like headers
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
}

walmart_url = "https://www.walmart.com/ip/Bose-SoundLink-Revolve-Wireless-Portable-Bluetooth-Speaker-Series-II-Black/711426711"
response = requests.get(walmart_url, headers=BASE_HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the script tag with id "__NEXT_DATA__"
script_tag = soup.find('script', id='__NEXT_DATA__')
data = json.loads(script_tag.string)
product = data["props"]["pageProps"]["initialData"]["data"]["product"]

# Intermediate variables to simplify access
initial_data = data["props"]["pageProps"]["initialData"]["data"]
product_data = initial_data["product"]
reviews_data = initial_data["reviews"]

# Simplified variables using intermediate variables
price = product_data["priceInfo"]["currentPrice"]["price"]
review_count = reviews_data["totalReviewCount"]
item_id = product_data["usItemId"]
avg_rating = reviews_data["averageOverallRating"]
product_name = product_data["name"]
brand = product_data["brand"]
availability = product_data["availabilityStatus"]
image_url = product_data["imageInfo"]["thumbnailUrl"]
short_description = product_data["shortDescription"]

# Printing the simplified variables for verification
print("Price:", price)
print("Review Count:", review_count)
print("Item ID:", item_id)
print("Average Rating:", avg_rating)
print("Product Name:", product_name)
print("Brand:", brand)
print("Availability:", availability)
print("Image URL:", image_url)
print("Short Description:", short_description)


