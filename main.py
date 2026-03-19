from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from deep_translator import GoogleTranslator
import requests
import os
import time
import re
from collections import Counter

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://elpais.com/opinion/")

time.sleep(5)

# accept cookie popup
try:
    cookie_button = driver.find_element(By.XPATH, "//button[contains(.,'Aceptar')]")
    cookie_button.click()
    time.sleep(2)
except:
    pass

# collect first 5 article links
article_elements = driver.find_elements(By.CSS_SELECTOR, "article h2 a")[:5]

titles = []
links = []

for el in article_elements:
    titles.append(el.text)
    links.append(el.get_attribute("href"))

print("\n--- SPANISH TITLES ---")
for t in titles:
    print(t)

os.makedirs("images", exist_ok=True)

# visit each article
for i, link in enumerate(links):

    driver.get(link)

    time.sleep(4)

    paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")

    content = " ".join([p.text for p in paragraphs[:5]])

    print("\nCONTENT PREVIEW:")
    print(content[:300])

    # download article image
    try:
        img = driver.find_element(By.CSS_SELECTOR, "figure img").get_attribute("src")
        img_data = requests.get(img).content

        with open(f"images/article_{i}.jpg", "wb") as f:
            f.write(img_data)
    except:
        pass

driver.quit()

# translate titles
print("\n----- TRANSLATED TITLES -----")

translated_titles = []

for t in titles:
    translated = GoogleTranslator(source="es", target="en").translate(t)
    translated_titles.append(translated)
    print(translated)

# analyze repeated words
words = []

for header in translated_titles:
    words.extend(re.findall(r'\b\w+\b', header.lower()))

counts = Counter(words)

print("\n----- WORDS REPEATED MORE THAN TWICE -----")

for word, count in counts.items():
    if count > 2:
        print(word, count)