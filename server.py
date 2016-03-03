from flask import Flask, render_template, request, redirect, session, flash 
from mysqlconnection import MySQLConnector

import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


app= Flask(__name__)
app.secret_key = "ThisisSecret"
mysql = MySQLConnector('users')

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():

	return render_template('index.html')

@app.route('/registarion', methods=["Post"])
def registarion():



	check= True

	#First Name
	if len(request.form['firstname']) <1:
		flash("Enter First name")
		check = False

	elif request.form['firstname'].isalpha() == False:
		flash("Error: Num in Name")
		check = False
	else:
		firstname = request.form['firstname']

	
	#Last Name

	if len(request.form['lastname']) <1:
		flash("Enter First name")
		check = False

	elif request.form['lastname'].isalpha() == False:
		flash("Error: Num in Name")
		check = False

	else:
		lastname = request.form['lastname']

	#EMAIL

	if not EMAIL_REGEX.match(request.form['email']):
		flash("Error: Invalid Email")
		check = False

	else:
		email = request.form['email']

	#password
	if len(request.form['password']) <1 or len(request.form['password']) < 8:
		flash("Error: Enter password or password must be 8 characters long")
		check = False
	
	if len(request.form['cpassword']) <1:
		flash("Error: confirm Password")
		check = False
	
	elif request.form['password'] != request.form['cpassword']:
		flash("Error: passwords do not match")
		check = False
	
	else:
		password =  request.form['password']

		pw_hash = bcrypt.generate_password_hash(password)
		
 		print pw_hash

	if check == True:
		flash("Thanks for submitting your information.")
		
		
		query = "INSERT INTO users(first_name, last_name, password, email, ceated_at) VALUES ( '{}', '{}', '{}', '{}', NOW() )".format(firstname, lastname, pw_hash, email )
		mysql.run_mysql_query(query)
		
		return redirect('/login')
	else: 
		
		return redirect('/')



#user to login 
@app.route('/login')
def login():


	return render_template('index3.html')

@app.route('/validation', methods= ['POST'])
def validation():
	


	email = request.form['email']
	password = request.form['password']
	query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(email)
	user = mysql.fetch(query)
	if len(user) < 1:

		flash("Error")
		return redirect('/login')
	
	session['id'] = user[0]['id']



	if bcrypt.check_password_hash(user[0]['password'], password):
		return redirect('/success')

	else:
		flash("Error:Email or password dont match")
		return redirect('/')


@app.route('/success')
def success():
 
	
	return render_template('index2.html')
app.run(debug=True)
