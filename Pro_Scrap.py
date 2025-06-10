import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service   
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome()

query ="Laptop"
file_no =0 
for i in range(1, 20):
    driver.get(f"https://www.amazon.in/s?k={query}&page{i}crid=E371BRJ2GEU0&sprefix=laptop%2Caps%2C230&ref=nb_sb_noss_2")
    
    elems = driver.find_elements(By.CLASS_NAME , "puis-card-container")
    print(f"{len(elems) }Items Found")

    for elem in elems:

        d = elem.get_attribute("outerHTML")
        with open(f"{query}_{file_no}.html" ,"w" , encoding='utf-8') as f:
            f.write(d)
            file_no +=1

        # print(elem.text)
    
    time.sleep(3)

driver.close()