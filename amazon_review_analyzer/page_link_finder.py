from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

file_path = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/page_links.txt'
with open(file_path, "w") as f:
    f.write("")

# Find links:
url = "https://www.amazon.com/Best-Sellers-Appstore-Android-Game-Apps/zgbs/mobile-apps/2478844011"
html = urlopen(url)
bs = BeautifulSoup(html, "lxml")
links = bs.find("div", {"id": "zg_centerListWrapper"}).findAll("a", href=re.compile("([A-Za-z0-9_?&=:()])+"))

# Write in file:
c = 0
for link in links:
    if c%4 == 0:
        x = "https://www.amazon.com/" + link['href']
        with open(file_path, 'a') as f:
            f.write(x)
            f.write("\n")
        print(x)
    c += 1

# Reference link:
#https://www.youtube.com/watch?v=-E1SC_oz9m4