from flask import Flask,render_template,url_for
from aylien_textapi_python.aylienapiclient import textapi
from flask_bootstrap import Bootstrap
import os
import json
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
Bootstrap(app)


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
    return render_template(
        'graphicsreview.html',
        graphicsarraylist=graphics_arraylist

    )


@app.route("/control")
def controlpath():
    return render_template(
        'controlreview.html',
        controlarraylist=control_arraylist

    )


@app.route("/powerconsume")
def powerconsumepath():
    return render_template(
        'powerconsumereview.html',
        powerconsumearralist=power_consume_arraylist

    )


@app.route("/userfriendly")
def userfriendlypath():
    return render_template(
        'userfriedlyreviewshow.html',
        userfriendlyarraylist=userfriendly_arraylist

    )


@app.route("/advertisement")
def advertisementpath():
    return render_template(
        'advertisereview.html',
        advertisementarraylist=advertisement_arraylist

    )

@app.route("/crash")
def crashpath():
    return render_template(
        'crashreview.html',
        crasharraylist=crash_arraylist

    )

@app.route('/')
def hello_world(title ,imagelink ,installlink ):
    del graphics_arraylist[:]
    del control_arraylist[:]
    del crash_arraylist[:]
    del userfriendly_arraylist[:]
    del power_consume_arraylist[:]
    del advertisement_arraylist[:]
    del features[:]
    data = json.load(open('/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/amazonreview2/reviewspecial.json'))
    # file_string =str(open("templates/zaoad_text_file/appdetails.txt"))
    file_string = ""
    for i in data[0]["review_body"]:
        file_string += i
    for i in data[0]["desc"]:
        s = i[5:-5]
        features.append(s)
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

    full_filename = "https://images-na.ssl-images-amazon.com/images/I/71b3zeOIPbL.png"

    s = "{0:.2f}".format(average_positive_sentiment)
    average_positive_sentiment = float(s)

    return render_template(
        'app_details.html', positive_senti=average_positive_sentiment, negative_senti=average_negative_sentiment,
        graphicsupvote=graphics_upvote, graphicsdownvote=graphics_downvote,
        controlupvote=control_upvote, controldownvote=control_downvote,
        powerconsumeupvote=power_consume_upvote, powerconsumedownvote=power_consume_downvote, crashupvote=crash_upvote,
        crashdownvote=crash_downvote, userfriendlyupvote=userfriendly_upvote,
        userfriendlydownvote=userfriendly_downvote, advertiseupvote=advertise_upvote,
        advertisedownvote=advertise_downvote,
        featureslist=features,title=title,imagelink=imagelink,installlink=installlink
    )
if __name__ == '__main__':

    app.run()
