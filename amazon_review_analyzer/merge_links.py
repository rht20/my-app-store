# Read a file
name1 = "/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/app_name.txt"
name2 = "/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/image_links.txt"
name3 = "/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/page_links.txt"
name4 = "/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/app_rating.txt"
name5 = "/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/merged_file.txt"

list1 = []
list2 = []
list3 = []
list4 = []
list5 = []

with open(name1, 'r') as f1:
    for line in f1:
        list1.append(line)

with open(name2, 'r') as f2:
    for line in f2:
        list2.append(line)

with open(name3, 'r') as f3:
    for line in f3:
        list3.append(line)

i = 5
j = -1
with open(name4, 'r') as f4:
    for line in f4:
        if i == 5:
            i = 0
            j += 1
            list4.append([])

        list4[j].append(line)
        i += 1


with open(name5, 'w') as f5:
    f5.write("")

for i in range(0,list1.__len__()):
    if list1[i].__len__() > 19:
        continue

    with open(name5, 'a') as f5:
        f5.write(list1[i])
        f5.write(list2[i])
        f5.write(list3[i])

        for j in list4[i]:
            f5.write(j)
