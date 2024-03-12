from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
# from collections import defaultdict

import time
import random
import os

from util.cookies import accept_cookies
from util.domain import get_domain
from util.to_utf8 import to_utf8
from util.Link import Link

from keywords import keywords

LOADING_PROGRESS_UNIT = 100 / (len(keywords))

MIN_SLEEP = int(os.getenv('MIN_SLEEP'))
MAX_SLEEP = int(os.getenv('MAX_SLEEP'))


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def get_overall(uni_url):
  loading_progress = 0

  link = Link()
  
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

  for field, keyword_types in keywords.items():
    found_link = False
    field_query = keyword_types["query"]
    query = f"{uni_url} {field_query}"
    url = link.build(query)

    driver.get(url)
    
    accept_cookies(driver)    

    soup = BeautifulSoup(driver.page_source, "html.parser")
    anchors = soup.find_all("a")

    for anchor in anchors:
      result_url = anchor.get("href")

      result_domain = get_domain(result_url)
      uni_domain = get_domain(uni_url)

      # Ensure both domains are of the same type and anchor is part of main results before processing
      if uni_domain not in result_domain or not anchor.has_attr("aria-label"):
        continue

      if any(substring in result_url for substring in keyword_types["url"]):
        found_link = True
        time.sleep(random.uniform(MIN_SLEEP, MAX_SLEEP))
        loading_progress += LOADING_PROGRESS_UNIT
        yield to_utf8({
          "data": {
            "label": field_query,
            "url": result_url,
          },
          "progress": loading_progress
        })

        print(f"Found {field_query} link: {result_url}")
        break

    if found_link == False:
      loading_progress += LOADING_PROGRESS_UNIT
      yield to_utf8({
        "progress": loading_progress
      })
  driver.quit()