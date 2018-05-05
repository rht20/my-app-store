from flask import Flask, render_template, request, json, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from flask import session
import os, subprocess, time
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import MySQLdb
from aylien_textapi_python.aylienapiclient import textapi
from flask_bootstrap import Bootstrap
import json
import smtplib


#import app_name_finder,image_link_finder,page_link_finder,rating_finder,merge_links


app = Flask(__name__)
Bootstrap(app)

app.secret_key = os.urandom(30)

mysql = MySQL(app)
conn = MySQLdb.connect(host="localhost", user="root", password="rht20", db="bestAPP")
mysql.init_app(app)

######################################### home #########################################


@app.route('/')
def home1():
#     app_name_finder
#     image_link_finder
#     page_link_finder
#     rating_finder
#     merge_links

     i = 0
     j = 0
     file_path = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/merged_file.txt'
     list = []
     list.append([])

     with open(file_path, 'r') as f:
         for line in f:
             list[j].append(line)
             i += 1

             if i == 8:
                 if list.__len__() == 18:
                     break
                 i = 0
                 j += 1
                 list.append([])

     list.pop()
     return render_template("home1.html", list=list)


@app.route('/home2')
def home2():
    i = 0
    j = 0
    file_path = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/text_files/merged_file.txt'
    list = []
    list.append([])

    with open(file_path, 'r') as f:
        for line in f:
            list[j].append(line)
            i += 1

            if i == 8:
                if list.__len__() == 18:
                    break
                i = 0
                j += 1
                list.append([])

    list.pop()

    return render_template("home2.html", list=list)


######################################### search #########################################


@app.route('/SearchPage', methods=['POST'])
def SearchPage():

    keyword = request.form['SearchWord']
    arg = "arg1=" + keyword
    subprocess.call(["php", "/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/ItemSearch2.php", arg])

    # time.sleep(3)
    merge()

    i = 0
    j = 0

    file_path = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/merged_attribute.txt'
    list = []
    list.append([])

    with open(file_path, 'r') as f:
        for line in f:
            list[j].append(line)
            i += 1

            if i == 9:
                if list.__len__() == 18:
                    break
                i = 0
                j += 1
                list.append([])
                print(list)

    list.pop()
    return render_template("SearchPage.html", list=list)


def merge():
    name1 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FTitle.txt'
    name2 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FImage.txt'
    name3 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FASIN.txt'
    name4 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FRating.txt'
    name5 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/merged_attribute.txt'

    list1 = []
    list2 = []
    list3 = []
    list4 = []

    with open(name1, 'r') as f1:
        for line in f1:
            list1.append(line)
            print(line)

    with open(name2, 'r') as f2:
        for line in f2:
            list2.append(line)
            print(line)

    with open(name3, 'r') as f3:
        for line in f3:
            list3.append(line)
            print(line)

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

    for i in range(0, list1.__len__()):

        with open(name5, 'a') as f5:
            f5.write(list1[i])
            f5.write(list2[i])
            f5.write(list3[i])

            for j in list4[i]:
                f5.write(j)

            f5.write("attrId" + str(i) + "\n")


@app.route('/ShowDetails', methods=['POST'])
def ShowPage():
    Title = request.form['Title']
    Image = request.form['Image_src']
    ASIN = request.form['ASIN']

    #print(ASIN)
    #ASIN= ASIN[:-2]
    #ASIN.rstrip()
    #ASIN.rstrip()
    url = ASIN
    #url = "https://www.amazon.com/gp/product/" + ASIN + "/ref=sr_1_1?s=mobile-apps&ie=UTF8&sr=1-1&keywords="+ASIN
    #url = "https://www.amazon.com/gp/product/" + ASIN + "xxxxx" + ASIN+"yyyy"
    url2 = "https://www.amazon.com/gp/product/B009UX2YAC/ref=sr_1_1?s=mobile-apps&ie=UTF8&sr=1-1&keywords=B009UX2YAC"
    # print("------->"+url)
    # print(".......>"+url2)

    url = "start_url=" + url

    print("yyyyyyyyyyy")

    open('/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/reviewspecial.json', 'w').close()
    os.chdir(os.path.abspath('/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2'))
    print(subprocess.check_output(['scrapy', 'crawl', 'reviewspider', '-a', url, '-o', 'reviewspecial.json']))

    # with open("/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/reviewspecial.json") as items_file:
    #    return items_file.read()


    # open('/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/reviewspecial.json', 'w').close()
    # os.chdir(os.path.abspath('/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2'))
    # print(subprocess.check_output(['scrapy', 'crawl', 'reviewspider', '-a', url, '-o', 'reviewspecial.json']))
    #
    #
    # #with open("/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/reviewspecial.json") as items_file:
    # #    return items_file.read()
    #
   # return Title+Image+ASIN
    #

    return app_details(Title, Image, ASIN)



######################################### registration #########################################

@app.route('/registration_form')
def registration_form():
    return render_template("registration_form.html")


@app.route('/registration_form_error')
def registration_form_error():
    return render_template("registration_error.html")


@app.route('/registration_form_response', methods=['POST'])
def registration_form_response():
    u_name = request.form['InputName']
    u_email = request.form['InputEmail']
    u_password = request.form['InputPassword']

    if request.method == 'POST':

        # Create cursor
        cur = conn.cursor()
        cur.execute("SELECT email FROM Profile WHERE email = (%s)", (u_email,))
        data = cur.fetchall()

        if not data:
            cur.execute("INSERT INTO Profile(name, email, password) VALUES(%s, %s, %s)",
                        (u_name, u_email, u_password))

            # Commit to DB
            conn.commit()

            # Close connection
            cur.close()

            send_mail(u_email)

            return render_template("home2.html")

        else:
            return render_template("registration_error.html")


def send_mail(u_email):
    mail_to = u_email
    mail_from = "amazonreviewextractor@gmail.com"
    password = "amazon-review"
    subject = "Welcome"
    text = "Congratulations, successfully new account created!"

    body = '\r\n'.join((['To: %s' % mail_to, 'From: %s' % mail_from, 'Subject: %s' %subject, '', text]))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(mail_from, password)
    server.sendmail(mail_from, mail_to, body)
    server.quit()


######################################### login #########################################

@app.route('/login_form')
def login_form():
    return render_template("login_form.html")


@app.route('/login_form_error')
def login_form_error():
    return render_template("login_error.html")


@app.route('/login_form_response', methods=['POST'])
def login_form_response():
    u_email = request.form['InputEmail']
    u_password = request.form['InputPassword']

    if request.method == 'POST':

        if u_email == "" or u_password == "":
            return render_template("login_error.html")
        # Create cursor
        cur = conn.cursor()
        cur.execute("SELECT password FROM Profile WHERE email = (%s)", (u_email,))
        data = cur.fetchall()

        if not data:
            return render_template("login_error.html")

        pword = data[0][0]

        if str(u_password) == str(pword):
            cur = conn.cursor()
            cur.execute("SELECT * FROM Profile WHERE email = (%s)", (u_email,))
            data = cur.fetchall()

            session['name'] = data[0][0]
            session['email'] = data[0][1]

            i = 0
            j = 0
            file_path = 'templates/text_files/merged_file.txt'
            list = []
            list.append([])
            with open(file_path, 'r') as f:
                for line in f:
                    if i < 2:
                        list[j].append(line)
                    i += 1

                    if i == 3:
                        if list.__len__() == 18:
                            break
                        i = 0
                        j += 1
                        list.append([])

            return render_template("home2.html", list=list)

        else:
            return render_template("login_error.html")


@app.route('/forget_password')
def forget_password():
    return render_template("login_form.html")


######################################### profile #########################################

@app.route('/profile')
def profile():
    list = []
    list.append(session['name'])
    list.append(session['email'])
    return render_template("profile.html", list=list)


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    u_name = request.form['InputName']
    u_email = session['email']
    u_cpassword = request.form['InputCPassword']
    u_password = request.form['InputPassword']

    if request.method == 'POST':

        # Create cursor
        cur = conn.cursor()
        cur.execute("SELECT password FROM Profile WHERE email = (%s)", (u_email,))
        data = cur.fetchall()

        cpword = data[0][0]

        if cpword != u_cpassword:
            list = []
            list.append(session['name'])
            list.append(session['email'])
            return render_template("edit_profile_error.html", list=list)

        if u_password != "":
            u_cpassword = u_password

        # Remove old entry from database
        cur = conn.cursor()
        cur.execute("DELETE FROM Profile WHERE email = (%s)", (u_email,))

        cur.execute("INSERT INTO Profile(name, email, password) VALUES(%s, %s, %s)",
                    (u_name, u_email, u_cpassword))

        # Commit to DB
        conn.commit()

        # Close connection
        cur.close()

        # Remove old session and create new session
        session.pop('name', None)
        session.pop('email', None)
        session['name'] = u_name
        session['email'] = u_email

        list = []
        list.append(session['name']);
        list.append(session['email'])

        return render_template("profile.html", list=list)


######################################### analysis #########################################

def grahicsreview(review_string):
    if "graphics" in review_string:
        return 1
    return 0


def controlreview(review_string):
    if review_string.find("battery") != -1:
        return 1
    return 0


def powerreview(review_string):
    if review_string.find("power") != -1:
        return 1
    return 0


def userfriendly(review_string):
    if review_string.find("user friendly") != -1:
        return 1
    return 0


def crashreview(review_string):
    if review_string.find("crash") != -1:
        return 1
    return 0


def adsreview(review_string):
    if review_string.find("ads") != -1:
        return 1
    if review_string.find("add") != -1:
        return 1
    return 0

def advertisedreview(review_string):
    if review_string.find("advertise") != -1:
        return 1
    return 0


graphics_arraylist=[]
control_arraylist=[]
power_consume_arraylist = []
userfriendly_arraylist = []
advertisement_arraylist = []
crash_arraylist = []
average_positive_sentiment=0
average_negative_sentiment=0
features=[]


@app.route("/graphics")
def graphicspath():
    return render_template('graphicsreview.html', graphicsarraylist=graphics_arraylist)


@app.route("/control")
def controlpath():
    return render_template('controlreview.html', controlarraylist=control_arraylist)


@app.route("/powerconsume")
def powerconsumepath():
    return render_template('powerconsumereview.html', powerconsumearralist=power_consume_arraylist)


@app.route("/userfriendly")
def userfriendlypath():
    return render_template('userfriedlyreviewshow.html', userfriendlyarraylist=userfriendly_arraylist)


@app.route("/advertisement")
def advertisementpath():
    return render_template('advertisereview.html', advertisementarraylist=advertisement_arraylist)


@app.route("/crash")
def crashpath():
    return render_template('crashreview.html', crasharraylist=crash_arraylist)


def app_details(title, imagelink, installlink):

    del graphics_arraylist[:]
    del control_arraylist[:]
    del crash_arraylist[:]
    del userfriendly_arraylist[:]
    del power_consume_arraylist[:]
    del advertisement_arraylist[:]
    del features[:]

    data = json.load(open('/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/reviewspecial.json'))
    file_string = ""

    for i in data[0]["review_body"]:
        file_string += i

    for i in data[0]["desc"]:
        s = i[5:-5]
        features.append(s)

    file = open("/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/tag.txt", "r")
    for line in file:
        file_string += line

    main_str = file_string


    # client = textapi.Client("bd0e6efe", "e2cae699e4c44c35ccd6bd3b587b03c8")
    # client = textapi.Client("402c4f5d", "c4ce28551be5a50a9299d5badb825287")
    client = textapi.Client("45413792", "f768215f4375e4941ef8d0e8287e4832")
    file_string = file_string.split('.')

    positive_sentiment = 0.0
    negative_sentiment = 0.0
    positive_review_number = 0
    negative_review_number = 0
    graphics_upvote = 0
    graphics_downvote = 0
    control_upvote = 0
    control_downvote = 0
    power_consume_upvote = 0
    power_consume_downvote = 0
    userfriendly_upvote = 0
    userfriendly_downvote = 0
    advertise_upvote = 0
    advertise_downvote = 0
    crash_upvote = 0
    crash_downvote = 0

    i = 0
    while i < len(file_string):
        reviewstring = file_string[i]
        sentiment = client.Sentiment({'text': file_string[i]})
        positive = 0
        negative = 0

        if (str(sentiment['polarity']) == 'negative'):
            negative = 1
            print(str(sentiment['text']) + ' is ' + 'negative')
            negative_sentiment += float(str(sentiment['polarity_confidence']))
            s = "{0:.2f}".format(negative_sentiment)
            negative_sentiment = float(s)
            negative_review_number += 1

        elif (str(sentiment['polarity']) == 'positive'):
            positive = 1
            print(str(sentiment['text']) + ' is ' + 'positive')
            positive_sentiment += float(str(sentiment['polarity_confidence']))
            s = "{0:.2f}".format(positive_sentiment)
            positive_sentiment = float(s)
            positive_review_number += 1

        if (grahicsreview(reviewstring)):
            graphics_arraylist.append(reviewstring)
            if (positive == 1):
                graphics_upvote += 1
            elif (negative == 1):
                graphics_downvote += 1

        if (controlreview(reviewstring)):
            control_arraylist.append(reviewstring)
            if (positive == 1):
                control_upvote += 1
            elif (negative == 1):
                control_downvote += 1

        if (powerreview(reviewstring)):
            power_consume_arraylist.append(reviewstring)
            if (positive == 1):
                power_consume_downvote += 1

            elif (negative == 1):
                power_consume_upvote += 1

        if (crashreview(reviewstring)):
            crash_arraylist.append(reviewstring)
            if (positive == 1):
                crash_downvote += 1
            elif (negative == 1):
                crash_upvote += 1

        if (userfriendly(reviewstring)):
            userfriendly_arraylist(reviewstring)
            if (positive == 1):
                userfriendly_upvote += 1
            if (negative == 1):
                userfriendly_downvote += 1

        if (adsreview(reviewstring)):
            advertisement_arraylist.append(reviewstring)
            if (positive == 1):
                advertise_downvote += 1
            elif (negative == 1):
                advertise_upvote += 1
        i = i + 1
    if (negative_review_number == 0):
        negative_review_number = 1
    if (positive_review_number == 0):
        positive_review_number = 1
    total = positive_review_number + negative_review_number
    average_negative_sentiment = negative_sentiment / negative_review_number
    average_positive_sentiment = positive_sentiment / positive_review_number
    average_positive_sentiment = average_positive_sentiment * positive_review_number / total
    average_negative_sentiment = average_negative_sentiment * negative_review_number / total
    # return 'positive review : '+str(average_positive_sentiment)+'\n'+'negative review : '+str(average_negative_sentiment)

    s = "{0:.2f}".format(average_positive_sentiment)
    average_positive_sentiment = float(s)
    average_positive_sentiment=average_positive_sentiment*100
    average_positive_sentiment_percentage=int(average_positive_sentiment)
    s = "{0:.2f}".format(average_negative_sentiment)
    average_negative_sentiment = float(s)
    average_negative_sentiment = average_negative_sentiment * 100
    average_negative_sentiment_percentage = int(average_negative_sentiment)

    return render_template(
        'app_details.html',
        positive_senti=average_positive_sentiment_percentage, negative_senti=average_negative_sentiment_percentage,
        graphicsupvote=graphics_upvote, graphicsdownvote=graphics_downvote,
        controlupvote=control_upvote, controldownvote=control_downvote,
        powerconsumeupvote=power_consume_upvote, powerconsumedownvote=power_consume_downvote,
        crashupvote=crash_upvote, crashdownvote=crash_downvote,
        userfriendlyupvote=userfriendly_upvote,userfriendlydownvote=userfriendly_downvote,
        advertiseupvote=advertise_upvote,advertisedownvote=advertise_downvote,
        featureslist=features, title=title, imagelink=imagelink, installlink=installlink)


if __name__ == '__main__':
    app.run(debug=True)
