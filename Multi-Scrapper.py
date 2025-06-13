from playwright.sync_api import sync_playwright
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Config
NUM_WORKERS = 6
URL_CSV = "All_OLX_Links.csv"
OUTPUT_CSV = "olx_property_details_with_rent_Added.csv"

# Extractor Function
def extract_listing_details(url):
    result = {"property_url": url, "Rent": "N/A"}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url, timeout=60000)

            try:
                page.wait_for_selector("div._3B4o-", timeout=10000)
            except:
                result["error"] = "Main content missing"
                browser.close()
                return result

            keys = page.query_selector_all("span._3V4pD")
            values = page.query_selector_all("span.B6X7c")
            for key, value in zip(keys, values):
                k = key.inner_text().strip()
                v = value.inner_text().strip()
                result[k] = v

            try:
                price_el = page.query_selector("div.T8y-z, span.T8y-z")
                if price_el:
                    result["Rent"] = price_el.inner_text().strip()
            except:
                result["Rent"] = "N/A"

            browser.close()
    except Exception as e:
        result["error"] = str(e)

    return result

# Load URLs
df_links = pd.read_csv(URL_CSV)
urls = df_links["property_url"].dropna().unique().tolist()

all_data = []
with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = {executor.submit(extract_listing_details, url): url for url in urls}
    for i, future in enumerate(as_completed(futures)):
        data = future.result()
        all_data.append(data)
        print(f"[{i+1}/{len(urls)}] Done: {data['property_url'][:60]} | Rent: {data.get('Rent', 'N/A')}")

        if (i + 1) % 20 == 0:
            pd.DataFrame(all_data).to_csv(OUTPUT_CSV, index=False)

pd.DataFrame(all_data).to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Scraping completed. Data saved to: {OUTPUT_CSV}")
