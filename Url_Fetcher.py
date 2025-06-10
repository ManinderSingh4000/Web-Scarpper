from playwright.sync_api import sync_playwright
import pandas as pd
import time

def fetch_all_olx_links(base_url, total_pages):
    all_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for page_num in range(1, total_pages + 1):
            url = f"{base_url}?page={page_num}"
            print(f"Scraping: {url}")
            page.goto(url)

            try:
                page.wait_for_selector('li._1DNjI', timeout=5000)
            except:
                print(f"No listings found on page {page_num}")
                continue

            link_elements = page.query_selector_all('li._1DNjI a')

            for a in link_elements:
                href = a.get_attribute('href')
                if href:
                    full_url = "https://www.olx.in" + href if href.startswith("/") else href
                    all_links.append(full_url)

            time.sleep(1)  # optional pause between pages

        browser.close()

    df = pd.DataFrame(all_links, columns=["property_url"])
    return df

# Config
base_url = "https://www.olx.in/en-in/mohali_g4296460/pg-guest-houses_c1449"
total_pages_to_scrape = 50  # change as needed

df_links = fetch_all_olx_links(base_url, total_pages_to_scrape)
df_links.to_csv("olx_property_links.csv", index=False)
print(df_links.head())
