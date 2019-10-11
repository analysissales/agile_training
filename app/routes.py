from app import app,db
from flask import render_template,redirect, request, flash, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user,logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import os
import pandas as pd,collections,matplotlib.pyplot as plt


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(company_name=form.company_name.data, email=form.email.data, address=form.address.data, contact=form.contact.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(company_name=form.company_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)
   


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# df=pd.read_csv("sample_data.csv")
# Products=df['Product Name'].unique()
# quantity=df['Quantity'] 
# dc=collections.Counter(df['Product Name'])
# dic= dict.fromkeys(Products, 0)
# list1=df['Product Name']
# list2=df['Quantity']
# for i in range(len(list1)):
#     dic[list1[i]]+=list2[i]
# Quantity=list(dic.values())
# indexOfMax=Quantity.index(max(Quantity))
# colors = ["#1f77b4", "#ff9f0e", "#2ca02c", "#d62728", "#8c564b", "#8c587f"]
# explode = [0, 0, 0, 0, 0, 0]
# fig=plt.figure()
# explode[indexOfMax]=0.1
# plt.pie(Quantity, labels=Products, explode=explode, colors=colors,
# autopct='%1.1f%%', shadow=True, startangle=140)
# date=df['Date'].unique()
# plt.title("Quantities sold of each product on Date: "+str(date))
#         # plt.show()
# fig.savefig('app/static/people_photo/abc.png')

# Code for generating pie chart in static/people_photo
df=pd.read_csv("sample_data.csv")
Products=df['Product Name'].unique()
quantity=df['Quantity'] 
dc=collections.Counter(df['Product Name'])
dic= dict.fromkeys(Products, 0)
list1=df['Product Name']
list2=df['Quantity']
for i in range(len(list1)):
    dic[list1[i]]+=list2[i]
Quantity=list(dic.values())
indexOfMax=Quantity.index(max(Quantity))
colors = ["#1f77b4", "#ff9f0e", "#2ca02c", "#d62728", "#8c564b", "#8c587f"]
explode = [0, 0, 0, 0, 0, 0]
fig_pie=plt.figure()
explode[indexOfMax]=0.1
plt.pie(Quantity, labels=Products, explode=explode, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
date=df['Date'].unique()
plt.title("Quantities sold of each product on Date: "+str(date))
# plt.show()
fig_pie.savefig('app/static/people_photo/pie_chart.png')

# Code for generating bar graph in static/people_photo
fig_bar=plt.figure()
Payments=collections.Counter(df['Payment method'])
payment_method=Payments.keys()
Usage=list(Payments.values())
plt.bar(payment_method, Usage, color=(0.4, 0.6, 0.8, 1.0), edgecolor='blue')
plt.xlabel("Payment  Method")
plt.ylabel("Number of bills out of "+str(sum(Usage)))
plt.title("Statistics for payment methods used:")
# plt.show()
fig_bar.savefig('app/static/people_photo/bar_graph.png')


PEOPLE_FOLDER = os.path.join('static','people_photo')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/piechart')
def show_piechart():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pie_chart.png')
    return render_template("piechart.html", user_image = full_filename)


@app.route('/bargraph')
def show_bargraph():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bar_graph.png')
    return render_template("bargraph.html", user_image = full_filename)