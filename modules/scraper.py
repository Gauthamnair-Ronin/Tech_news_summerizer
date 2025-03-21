from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import json 
# =============================
# Configuration
# =============================
company_name = "tesla"
base_url = "https://www.indiatoday.in/search/"
search_url = base_url + company_name
headers = {"User-Agent": "Mozilla/5.0"}
news_articles = {}  # Dictionary to store the news articles

# =============================
# Set up Selenium WebDriver
# =============================
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# =============================
# Load Search Page & Extract Links
# =============================
driver.get(search_url)
time.sleep(3)  # Wait for JS content to load

soup = BeautifulSoup(driver.page_source, "html.parser")
article_links = []

for article in soup.find_all("article", class_="grid_card_container"):
    a_tag = article.find("a", class_="grid_card_link")
    if a_tag and "href" in a_tag.attrs:
        article_links.append(a_tag["href"])

driver.quit()

# =============================
# Helper Function: Clean Article Text
# =============================
def clean_article_content(content):
    keyword = "advertisement"
    lowered = content.lower()
    index = lowered.find(keyword)
    if index != -1:
        return content[:index].strip()
    return content.strip()

# =============================
# Helper Function: Scrape Content from Article Page
# =============================
def get_content_string(link):
    try:
        page = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract title
        title = soup.find("title").text.strip()
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()

        # Extract content
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.text for p in paragraphs])
        article_text = clean_article_content(article_text)

        # Add to dictionary if title is valid
        if "advertisement" not in title.lower():
            news_articles[title] = article_text
    except Exception as e:
        print(f"❌ Failed to scrape {link}: {e}")

# =============================
# Scrape Top 10 Articles
# =============================
for link in article_links:
    get_content_string(link)
    if len(news_articles) == 10:
        break

# =============================
# Save to json for better key value pair visualization
# =============================
with open("news_articles.json", "w", encoding="utf-8") as f:
    json.dump(news_articles, f, ensure_ascii=False, indent=4)

"""# =============================
# Print Summary
# =============================
for title, content in news_articles.items():
    print("Title :", title)
    print("Content :", content)
    print("\n" + "="*80 + "\n")"""
