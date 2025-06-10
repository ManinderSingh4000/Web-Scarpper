# from bs4 import BeautifulSoup
# import os
# import pandas as pd

# d= {}
# title =[]
# price = []
# rating = []     
# link = []


# for file in os.listdir("data"):
#     with open(f"data/{file}" , "r" , encoding='utf-8') as f:
#         soup = BeautifulSoup(f.read() , "html.parser")

#         # Extracting the required data
#         title = soup.find("span" , class_="a-size-base-plus a-color-base a-text-normal")
#         price = soup.find("span" , class_="a-price-whole")
#         rating = soup.find("span" , class_="a-icon-alt")
#         link = soup.find("a" , class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

#         if title and price and rating and link:
#             title.append(title.text.strip()),
#             price.append(price.text.strip()),
#             rating.append(rating.text.strip()),
#             link.append(f"https://www.amazon.in{link['href']}")
            
#             d= {
#                 "Title": title,
#                 "Price": price,
#                 "Rating": rating,
#                 "Link": link
#             }

# # Creating a DataFrame from the dictionary
# df = pd.DataFrame.from_dict(d, orient='index')
# print(df)

from bs4 import BeautifulSoup
import os
import pandas as pd

# Lists to store extracted data
titles = []
prices = []
ratings = []     
links = []

# Loop through all HTML files in the "data" folder
for file in os.listdir("data"):
    with open(f"data/{file}", "r", encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), "html.parser")

        # Find all product cards
        containers = soup.find_all("div", class_="puis-card-container")

        for container in containers:
            # title_tag = container.find("span", class_="a-size-base-plus a-color-base a-text-normal")
            price_tag = container.find("span", class_="a-price-whole")
            # print(price_tag.text.strip())
            rating_tag = container.find("span", class_="a-icon-alt")
            # print(rating_tag.text.strip())
            link_tag = container.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
            if link_tag and 'href' in link_tag.attrs:
                print(f"https://www.amazon.in{link_tag['href']}")

            if price_tag  and rating_tag :
                prices.append(price_tag.text.strip())
                ratings.append(rating_tag.text.strip())
               
                
# Creating the dictionary after loop
data = {
    # "Title": titles,
    "Price": prices,
    "Rating": ratings,
}
# Convert to DataFrame
df = pd.DataFrame(data)

# Show the result
print(df)
# Save DataFrame to CSV 

df.to_csv("extracted_data.csv", index=False, encoding='utf-8')