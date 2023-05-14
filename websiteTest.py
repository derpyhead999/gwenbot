from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = (
    "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
)
options.add_experimental_option("detach", True)
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)  # driver is the browser
driver.get("https://danbooru.donmai.us/")

# driver.quit()
