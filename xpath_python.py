from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# Setup Selenium WebDriver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the webpage
driver.get("https://www.walmart.com/ip/Bose-SoundLink-Revolve-Wireless-Portable-Bluetooth-Speaker-Series-II-Black/711426711?athcpid=711426711&athpgid=AthenaItempage&athcgid=null&athznid=cc&athieid=v0&athstid=CS020&athguid=9DxSutFhNfeiaaq-_yMiWwIfzW5a5GudUnTB&athancid=239819927&athena=true&athbdg=L1103")


# Locate element by XPath
element = driver.find_element(By.XPATH, '//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[2]/div/div/section[3]')

# Print the text of the element
print(element.text)

# Close the driver
driver.quit()
