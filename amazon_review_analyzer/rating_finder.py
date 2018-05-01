from lxml import html
import requests

page = requests.get('https://www.amazon.com/Best-Sellers-Appstore-Android-Game-Apps/zgbs/mobile-apps/2478844011')
tree = html.fromstring(page.content)

rating = tree.xpath('//span[@class="a-icon-alt"]/text()')

file_path = 'templates/text_files/app_rating.txt'
with open(file_path, "w") as f:
    f.write("")

for i in rating:
    x = (i)
    x = x.split(" ")[0]
    x = round(float(x)+0.1)

    for j in range(0,5):
        with open(file_path, 'a') as f:
            if x > 0:
                f.write(" selected")
            else:
                f.write("")
            f.write("\n")
            x -= 1


with open(file_path,'r') as f:
    for i in f:
        print(i)
