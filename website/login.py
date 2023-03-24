from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
import MySQLdb.cursors
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
import base64
from io import BytesIO
import json
from flask_mysqldb import MySQL
import bcrypt

from website import mysql

login = Blueprint('login', __name__)

salt = bcrypt.gensalt()


@login.route('/', methods=['post', 'get'])
def start():
    if request.method == 'POST':
        user_option = request.form.get('survey')
        session['user_option'] = user_option
        if user_option is not None:
            if user_option == 'clinical':
                return redirect(url_for('login.log_in'))
            if user_option == 'research':
                return redirect(url_for('login.research'))
    return render_template('start.html')


@login.route('/research', methods=['post', 'get'])
def research():
    if request.method == 'POST':
        if request.form['result'] == 'back':
            return redirect(url_for('login.start'))
        else:
            return redirect(url_for('research_views.dashboard'))
    return render_template('research.html')


@login.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'POST':
        if request.form['result'] == 'back':
            return redirect(url_for('login.research'))
        else:
            if request.form.get('firstname') is not None and request.form.get('lastname') is not None and \
                    request.form.get('email') is not None and request.form.get('password') is not None:
                firstname = request.form.get('firstname')
                lastname = request.form.get('lastname')
                email = request.form.get('email')
                if bcrypt.hashpw(request.form.get('password').encode('utf-8'), salt) == \
                        bcrypt.hashpw(request.form.get('password2').encode('utf-8'), salt):
                    password_hash = bcrypt.hashpw(request.form.get('password').encode('utf-8'), salt)
                    print("test:", password_hash)
                    return redirect(url_for('login.research'))
            else:
                print('Not filled out')
    return render_template('register.html')


@login.route('/log_in', methods=['post', 'get'])
def log_in():
    error = None
    mesg = None
    cont = "Continue as Guest"

    if request.method == 'POST':
        session["checkbox"] = request.form.get("checkbox")
        if request.form['result'] == 'login':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = str(request.form.get('email'))

            if firstname != "" and lastname != "" and email != "":
                print(firstname, lastname, email)
                session['user'] = str(firstname)
                print(session['user'])
                email = str(request.form.get('email'))
                cursor = mysql.connection.cursor()

                cursor.execute('SELECT id FROM login WHERE email = %s', (email,))
                row = cursor.fetchone()
                print("row", row)

                if row:
                    print(row[0])
                    session['user_id'] = row[0]
                else:
                    cursor.execute('INSERT INTO login (firstname, lastname, email) VALUES ( %s, %s, %s)',
                                   (firstname, lastname, email))
                    session['user_id'] = cursor.lastrowid
                mysql.connection.commit()

                mesg = "Successfully logged in. Please continue."
                session['logged_in'] = True
                return redirect(url_for('login.consent'))
            else:
                error = "Please fill out all login information or click Continue as Guest"
                session['user'] = "guest"
        if request.form['result'] == "guest":
            session.clear()
            session["checkbox"] = request.form.get("checkbox")
            session['user'] = 'guest'
            session.pop('logged_in', None)
            session['logged_in'] = False
            return redirect(url_for('screener_views.home'))
    return render_template('login.html', error=error, mesg=mesg, cont=cont)


@login.route('/consent', methods=['post', 'get'])
def consent():
    consent_check = request.form.get('consent_check')
    if request.method == 'POST':
        if consent_check == 'data':
            return redirect(url_for('screener_views.home'))
        else:
            return redirect(url_for('login.log_in'))
    return render_template('consent.html')
