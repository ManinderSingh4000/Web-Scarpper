import pandas as pd
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service   
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome(service=Service(), options=Options())

File_No = 1
for i in range(1, File_No + 1):
    with open(f"data/Laptop.html", "r", encoding="utf-8") as file:
        content = file.read()
    
    soup = BeautifulSoup(content, "html.parser")
    elem = soup.find_all("div", class_="puis-card-container")

    description = soup.find_all("h2" , class_="a-size-medium ")
    for desc in description:
        print(desc.string())

    img_src = soup.find("img" , class_="s-image")
    for src in img_src:
        print(src.text)

    # price = soup.find_all("span", class_="a-price-whole")
    # for p in price:
    #     print(p.text)

    # for e in elem:
    #     print("------------")
    #     print(e.text)

        # Uncomment the next line to write to a file
#         with open(f"data/Laptop.html", "a", encoding="utf-8") as file:
#             file.write(d)
# # query ="Laptop"
# driver.get(f"https://www.amazon.in/s?k={query}&crid=E371BRJ2GEU0&sprefix=laptop%2Caps%2C230&ref=nb_sb_noss_2")

# elem = driver.find_elements(By.CLASS_NAME ,"puis-card-container" )

# for e in elem:
#     print("------------")
#     d = e.get_attribute("outerHTML")
#     with open(f"data/{query}.html", "a", encoding="utf-8") as file:
#         file.write(d)


# for ele in elem:
#     print(ele.text)
#     print("--------------------------------------------------")

driver.close()

