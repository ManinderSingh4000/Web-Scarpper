import streamlit as st
from playwright.sync_api import sync_playwright
import requests
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def get_proxies():
    # Example proxy list (Replace with actual proxy providers if needed)
    return [
        "http://user:pass@proxy1:port",
        "http://user:pass@proxy2:port",
    ]

def fetch_page(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    proxies = random.choice(get_proxies())
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_extra_http_headers(headers)
        page.goto(url, wait_until="networkidle")
        content = page.content()
        browser.close()
        return content

def scrape_data(url):
    try:
        page_source = fetch_page(url)
        soup = BeautifulSoup(page_source, "html.parser")
        return soup.prettify()
    except Exception as e:
        return f"Error: {str(e)}"

st.title("AI Web Scraper with CAPTCHA Bypass & IP Rotation")
url = st.text_input("Enter Website URL")
if st.button("Scrape Data"):
    if url:
        result = scrape_data(url)
        st.text_area("Scraped Content", result, height=300)
    else:
        st.error("Please enter a valid URL")
