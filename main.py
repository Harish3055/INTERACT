# -*- coding: utf-8 -*-
"""
@author: Harish M
@Title : Interact 
"""
#packages required
import string
from flask import Flask, render_template
import pickle
import numpy as np
from flask import *
from flask_mail import *
from random import *
import random
from Check import cosine_sim
import mysql.connector
from datetime import datetime

#QUESTIONS TO ASK
initial = [
    "Short description about you", "Can I know your gender",
    "Can I know about your educational qualification?", "Loan amount required",
    "Repayment period in years", "May I know your profile?",
    "Are you salaried? or Doing your business?"
]
salaried = [
    "If salaried, pl share your monthly take home salary", "Are you married? "
]
marital = [
    "if yes, what is your wife?", "How many children you have?",
    "Your residence is rented or own house?"
]
business = [
    "If you are a business man: Can you breifly explain about your business?",
    "Are you a tax assessee?"
]
tax = [
    "Whether your firm name is GST registered? ",
    "Which product you are dealing with?", "Are you an Entrepreneur?",
    "Are you a whole sale trader or a retailer?",
    "What is your annual turnover?",
    "Have you taken loan to run your business?", "Overdraft or Term loan"
]
loan = [
    "what is the monthly EMI you are paying?",
    "How many instalments are still due for payment?"
]
area = [
    "Do you have any real asset?",
    "If yes where do you have urban or semi-urban or rural?"
]
overdraft = ["If Overdraft, what is the drawing power?"]

#CHECK CONSTRAINTS
m1 = "Are you salaried? or Doing your business?"
m2 = "Are you married? "
m3 = "Are you a tax assessee?"
m4 = "Overdraft or Term loan"
m5 = "Have you taken any loan?"
e = [
    "I am doing my business", "Yes I am married", "Yes I am", "overdraft",
    "yes"
]

#initialising the variable
i = 0
answer = 0
quest = ""
ls = []
p = {
    'Date': "",
    'Email': "",
    'ph_no': "",
    'Gender': int(0),
    'Married': int(0),
    'Education': int(0),
    'Self_Employed': int(0),
    'ApplicantIncome': int(0),
    'CoapplicantIncome': int(0),
    'LoanAmount': int(0),
    'Loan_Amount_Term': int(0),
    'Credit_History': int(0),
    'Property_Area': int(0),
    'LoanAmount_log': int(0)
}
p['Date'] = str(datetime.today().strftime('%d-%m-%y'))
query = "INSERT INTO customer_details (Date_,Email,ph_no,Gender,Married,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,LoanAmount_log,Loan_eligibility) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

#opening the ml saved model using pickle
f = open('model_2_RFC.pickle', 'rb')
model = pickle.load(f)
f.close()

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="Harish@3055",
                               database="interact")
conn = mydb.cursor()
app = Flask(__name__)
mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'EMAIL-TD'
app.config['MAIL_PASSWORD'] = 'PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)


@app.route('/')
def index():
    return render_template("otp.html")


@app.route('/verify', methods=["POST"])
def verify():
    email = request.form["email"]
    ph_no = request.form['ph_no']
    p['Email'] = str(email)
    p['Email'] = ''.join(random.choices(string.ascii_letters,
                                        k=10)) + "@gmail.com"
    p['ph_no'] = str(ph_no)
    p['ph_no'] = "".join([random.choice(string.digits) for i in range(10)])
    msg = Message('Interact',
                  sender='techspeaks@gmail.com',
                  recipients=[email])
    msg.body = 'One time password ->' + str(otp)
    mail.send(msg)

    return render_template('verify.html')


@app.route('/validate', methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        return redirect(url_for('home'))
    return render_template('verify.html', error="Incorrect OTP :)")


@app.route('/home')
def home():
    global i
    i = 0
    return render_template(
        'index2.html',
        qn=
        "Hello sir, I am your virtual marketing agent, you can answer the series of question ahead.Say 'NEXT' to proceed further",
        url='next_qn')


@app.route('/getdata/<answer1>', methods=['GET', 'POST'])
def data_get(answer1):
    global answer
    global quest
    global p
    print(answer1)
    if quest == initial[1]:
        if answer1 in ['mail', 'male']:
            p['Gender'] = int(1)
    if quest == initial[2]:
        if answer1 == 'no':
            p['Education'] = int(0)
        else:
            p['Education'] = int(1)
    if quest == initial[3]:
        str1 = answer1.replace(',', '')
        p['LoanAmount'] = int(str1)
        p['LoanAmount_log'] = float(np.log(int(str1)))
    if quest == initial[4]:
        str1 = answer1.replace(',', '')
        p['Loan_Amount_Term'] = int(int(str1) * 360)
    if quest == salaried[0]:
        str1 = answer1.replace(',', '')
        p['ApplicantIncome'] = int(str1)
    if quest == area[1]:
        if answer1 == 'urban':
            p['Property_Area'] = int(1)
        elif answer1 == 'rural':
            p['Property_Area'] = int(2)
        else:
            p['Property_Area'] = int(3)

    if quest == m1:
        if cosine_sim(answer1, e[0]) > 0.2:
            p['Self_Employed'] = int(1)
            answer = '0'
        else:
            p['Self_Employed'] = int(0)
            answer = '1'
    elif quest == area[0]:
        if cosine_sim(answer1, e[4]) > 0.2:
            answer = '0001'
        else:
            answer = 'break'
    elif quest == m2:
        if cosine_sim(answer1, e[1]) > 0.2:
            p['Married'] = int(1)
            answer = '11'
        else:
            answer = '101'

    elif quest == marital[len(marital) - 1]:
        answer = '101'
    elif quest == m5:
        if cosine_sim(answer1, "yes i have loan") > 0.2:
            p['Credit_History'] = int(1)
            answer = '111'
        else:
            answer = 'NULL'
    elif quest == m3:
        if cosine_sim(answer1, e[2]) > 0.2:
            answer = '01'
        else:
            answer = 'NULL'
    elif quest == m4:
        if cosine_sim(answer1, e[3]) > 0.2:
            answer = '011'
        else:
            answer = '010'
    elif answer == '010' or answer == '011' and quest == loan[
            len(loan) - 1] or quest == overdraft[0]:
        answer = 'NULL'
    return 't_in = %s ; result: %s ;' % (answer, answer)


@app.route('/next_qn')
def next_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(initial):
        quest = initial[index]
        return render_template('index2.html',
                               qn=initial[index],
                               url='/next_qn')
    else:
        print(answer)
        i = 1
        if answer == '1':
            quest = salaried[0]
            return render_template('index2.html',
                                   qn=salaried[0],
                                   url='/next_qn/salaried_qn')
        else:
            quest = business[0]
            return render_template('index2.html',
                                   qn=business[0],
                                   url='/next_qn/business_qn')


@app.route('/next_qn/salaried_qn')
def salaried_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(salaried):
        quest = salaried[index]
        return render_template('index2.html',
                               qn=salaried[index],
                               url='/next_qn/salaried_qn')
    else:
        print(answer)
        i = 1
        if answer == '11':
            quest = marital[0]
            return render_template('index2.html',
                                   qn=marital[0],
                                   url='/next_qn/salaried_qn/marital_qn')
        else:
            quest = m5
            return render_template('index2.html', qn=m5, url='/next_qn/check')


@app.route('/next_qn/salaried_qn/marital_qn')
def marital_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(marital):
        quest = marital[index]
        return render_template('index2.html',
                               qn=marital[index],
                               url='/next_qn/salaried_qn/marital_qn')
    else:
        i = 1
        quest = m5
        return render_template('index2.html', qn=m5, url='/next_qn/check')


@app.route('/next_qn/salaried_qn/area_qn')
def area_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(area) and answer != "break":
        quest = area[index]
        return render_template('index2.html',
                               qn=area[index],
                               url='/next_qn/salaried_qn/area_qn')
    else:
        i = 1
        return render_template('index2.html',
                               qn='Thank you for choosing our service',
                               url='/next_qn/last_qn')


@app.route('/next_qn/check')
def check_qn():
    global answer
    global i
    global quest
    if answer == '111':

        return render_template('index2.html',
                               qn=loan[0],
                               url='/next_qn/salaried_qn/loan_qn')
    else:
        i = 1
        quest = area[0]
        return render_template('index2.html',
                               qn=area[0],
                               url='/next_qn/salaried_qn/area_qn')


@app.route('/next_qn/salaried_qn/loan_qn')
def loan_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(loan):
        quest = loan[index]
        return render_template('index2.html',
                               qn=loan[index],
                               url='/next_qn/salaried_qn/loan_qn')
    else:
        i = 1
        quest = area[0]
        return render_template('index2.html',
                               qn=area[0],
                               url='/next_qn/salaried_qn/area_qn')


@app.route('/next_qn/business_qn')
def business_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(business):
        quest = business[index]
        return render_template('index2.html',
                               qn=business[index],
                               url='/next_qn/business_qn')
    else:
        print(answer)
        i = 1
        if answer == '01':
            quest = tax[0]
            return render_template('index2.html',
                                   qn=tax[0],
                                   url='/next_qn/business_qn/tax_qn')
        else:
            return render_template('index2.html',
                                   qn='Thank you for choosing our service',
                                   url='/next_qn/last_qn')


@app.route('/next_qn/business_qn/tax_qn')
def tax_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(tax):
        quest = tax[index]
        return render_template('index2.html',
                               qn=tax[index],
                               url='/next_qn/business_qn/tax_qn')
    else:
        print(answer)
        i = 1
        if answer == '010':
            return render_template('index2.html',
                                   qn=loan[0],
                                   url='/next_qn/business_qn/tax_qn/loan_qnb')
        else:
            i = 1
            quest = overdraft[0]
            return render_template('index2.html',
                                   qn=overdraft[0],
                                   url='/next_qn/business_qn/tax_qn/over_qn')


@app.route('/next_qn/business_qn/tax_qn/loan_qnb')
def loan_qnb():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(loan):
        quest = loan[index]
        return render_template('index2.html',
                               qn=loan[index],
                               url='/next_qn/business_qn/tax_qn/loan_qnb')
    else:
        i = 1
        quest = area[0]
        return render_template('index2.html',
                               qn=area[0],
                               url='/next_qn/salaried_qn/area_qn')


@app.route('/next_qn/business_qn/tax_qn/over_qn')
def over_qn():
    global i
    global answer
    global quest
    index = i
    i = i + 1
    if index < len(overdraft):
        quest = overdraft[index]
        return render_template('index2.html',
                               qn=overdraft[index],
                               url='/next_qn/business_qn/tax_qn/over_qn')
    else:
        i = 1
        quest = area[0]
        return render_template('index2.html',
                               qn=area[0],
                               url='/next_qn/salaried_qn/area_qn')


@app.route('/next_qn/last_qn')
def last_qn():
    global i
    global query
    i = 0
    add_db = list(p.values())
    test = add_db[3:]
    test = np.array(test).reshape(1, -1)
    pred = model.predict(test)
    add_db.append(int(pred[0]))
    print(add_db)
    val = tuple(add_db)
    conn.execute(query, val)
    mydb.commit()
    mydb.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
