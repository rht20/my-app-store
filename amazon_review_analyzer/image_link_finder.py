from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

file_path = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/image_links.txt'
with open(file_path, "w") as f:
    f.write("")

# Find links
url = "https://www.amazon.com/Best-Sellers-Appstore-Android-Game-Apps/zgbs/mobile-apps/2478844011"
html = urlopen(url)
bs = BeautifulSoup(html, "lxml")
links = bs.find("div", {"id": "zg_centerListWrapper"}).findAll("img", src=re.compile("([A-Za-z0-9_?&=:()])+"))

# Write in file
for link in links:
    x = link['src']
    with open(file_path, 'a') as f:
        f.write(x)
        f.write("\n")
    print(x)

# Reference link:
#(https://www.amazon.com/)+
#https://www.youtube.com/watch?v=-E1SC_oz9m4
#https://www.amazon.com/Best-Sellers-Appstore-Android-Productivity-Apps/zgbs/mobile-apps/2478859011#1