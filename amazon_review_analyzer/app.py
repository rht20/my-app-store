from flask import Flask, render_template, request, json, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from flask import session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import MySQLdb
import os
#import app_name_finder,image_link_finder,page_link_finder,rating_finder,merge_links


app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = os.urandom(30)

conn = MySQLdb.connect(host="localhost",user="root",password="rht20",db="bestAPP")

# init MYSQL
mysql.init_app(app)


######################################### home #########################################

@app.route('/')
def home1():
#    app_name_finder
#    image_link_finder
#    page_link_finder
#    rating_finder
#    merge_links

    i = 0
    j = 0
    file_path = 'templates/text_files/merged_file.txt'
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

    return render_template("home1.html", list=list)

@app.route('/home2')
def home2():

    i = 0
    j = 0
    file_path = 'templates/text_files/merged_file.txt'
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

    return render_template("home2.html", list=list)


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
            return render_template("home2.html")

        else:
            return render_template("registration_error.html")


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
            with open(file_path,'r') as f:
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


if __name__ == '__main__':
    app.run(debug=True)
