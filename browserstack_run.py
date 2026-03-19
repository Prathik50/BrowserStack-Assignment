import os
import threading
import time
import re
import requests
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

URL = "https://hub-cloud.browserstack.com/wd/hub"

browsers = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "Chrome Test"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Firefox Test"
    },
    {
        "browserName": "Edge",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "Edge Test"
    },
    {
        "deviceName": "iPhone 14",
        "realMobile": "true",
        "osVersion": "16",
        "sessionName": "iPhone Test"
    },
    {
        "deviceName": "Samsung Galaxy S23",
        "realMobile": "true",
        "osVersion": "13",
        "sessionName": "Samsung Test"
    }
]


def run_test(cap):

    options = webdriver.ChromeOptions()

    # add capabilities
    for key, value in cap.items():
        options.set_capability(key, value)

    # ✅ BrowserStack authentication
    options.set_capability("bstack:options", {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY
    })

    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )

    driver.get("https://elpais.com/opinion/")
    time.sleep(5)

    # accept cookies
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[contains(.,'Aceptar')]")
        cookie_button.click()
        time.sleep(2)
    except:
        pass

    # get first 5 articles
    article_elements = driver.find_elements(By.CSS_SELECTOR, "article h2 a")[:5]

    titles = []
    links = []

    for el in article_elements:
        titles.append(el.text)
        links.append(el.get_attribute("href"))

    print(f"\n[{cap.get('sessionName')}] SPANISH TITLES:")
    for t in titles:
        print(t)

    os.makedirs("images", exist_ok=True)

    # visit each article
    for i, link in enumerate(links):

        driver.get(link)
        time.sleep(4)

        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        content = " ".join([p.text for p in paragraphs[:5]])

        print(f"\n[{cap.get('sessionName')}] CONTENT PREVIEW:")
        print(content[:200])

        # download image
        try:
            img = driver.find_element(By.CSS_SELECTOR, "figure img").get_attribute("src")
            img_data = requests.get(img).content

            with open(f"images/{cap.get('sessionName')}_article_{i}.jpg", "wb") as f:
                f.write(img_data)
        except:
            pass

    driver.quit()

    # translate titles
    translated_titles = []
    for t in titles:
        translated = GoogleTranslator(source="es", target="en").translate(t)
        translated_titles.append(translated)

    print(f"\n[{cap.get('sessionName')}] TRANSLATED TITLES:")
    for t in translated_titles:
        print(t)

    # word analysis
    words = []
    for header in translated_titles:
        words.extend(re.findall(r'\b\w+\b', header.lower()))

    counts = Counter(words)

    print(f"\n[{cap.get('sessionName')}] WORDS > 2 TIMES:")
    for word, count in counts.items():
        if count > 2:
            print(word, count)


# run threads
threads = []

for cap in browsers:
    t = threading.Thread(target=run_test, args=(cap,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("All BrowserStack tests completed.")