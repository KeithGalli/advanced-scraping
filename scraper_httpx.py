import httpx
import json
from parsel import Selector

# fake browser like headers
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}
response = httpx.get("https://www.walmart.com/ip/Bose-SoundLink-Revolve-Wireless-Portable-Bluetooth-Speaker-Series-II-Black/711426711", headers=BASE_HEADERS)
sel = Selector(text=response.text)
data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
data = json.loads(data)
print("DATA", data.keys())

product = data["props"]["pageProps"]["initialData"]["data"]["product"]["priceInfo"]["currentPrice"]["price"]
print(product)