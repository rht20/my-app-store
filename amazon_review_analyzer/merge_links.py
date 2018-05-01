# Read a file
name1 = "templates/text_files/app_name.txt"
name2 = "templates/text_files/image_links.txt"
name3 = "templates/text_files/page_links.txt"
name4 = "templates/text_files/app_rating.txt"
name5 = "templates/text_files/merged_file.txt"

list1 = []
list2 = []
list3 = []
list4 = []
list5 = []

"""
with open(name5, 'w') as f5:
    f5.write("")

# Read from 3 files and merge to another file
with open(name1, 'r') as f1:
    c1 = 0
    for line1 in f1:
        c1 += 1
        if line1.__len__() > 19:
            continue
        with open(name2, 'r') as f2:
            c2 = 0
            for line2 in f2:
                c2 += 1
                if c1 == c2:
                    with open(name3, 'r') as f3:
                        c3 = 0
                        for line3 in f3:
                            c3 += 1
                            if c2 == c3:
                                with open(name4, 'r') as f4:
                                    c4 = 0
                                    for line4 in f4:
                                        c4 += 1
                                        x = int(c3)*5
                                        if x == c4:
                                            list = []
                                            tc = 0
                                            for tl in f4:
                                                tc += 1
                                                if tc == c4:
                                                    
                                            with open(name4, 'a') as f4:
                                                f4.write(line1)
                                                f4.write(line2)
                                                f4.write(line3)

                                                print(line1)
                                                print(line2)
                                                print(line3)
"""

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
