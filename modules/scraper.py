# modules/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from modules.utils import  get_content_string

def scrape_news(company_name: str):
    base_url = "https://www.indiatoday.in/search/"
    if " " in company_name:
        company_name = company_name.replace(" ", "-")
    search_url = base_url + company_name
    print(company_name)
    headers = {"User-Agent": "Mozilla/5.0"}
    news_articles = {}  # Dictionary to store scraped data

    # Setup headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    article_links = []

    for article in soup.find_all("article", class_="grid_card_container"):
        a_tag = article.find("a", class_="grid_card_link")
        if a_tag and "href" in a_tag.attrs:
            article_links.append(a_tag["href"])

    driver.quit()

    # Scrape Top 10 Articles
    for link in article_links:
        get_content_string(link, headers, news_articles)
        if len(news_articles) == 10:
            break
    print(f"✅ Scraped {len(news_articles)} articles for {company_name}")
    return news_articles
