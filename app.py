from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt
import random
import smtplib  # For sending emails

app = Flask(__name__)
app.secret_key = 'nishita'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger'
app.config['MYSQL_DB'] = 'blood_bank'

mysql = MySQL(app)

# Utility functions for password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Function to send MFA code via email
def send_mfa_code(email, code):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Example using Gmail
        server.starttls()
        server.login('your_email@gmail.com', 'your_email_password')  # Your email credentials
        message = f"Your MFA code is: {code}"
        server.sendmail('your_email@gmail.com', email, message)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def home():
    return render_template('join.html')  # Points to the Join Us page

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    mobile = request.form['mobile']
    email = request.form['email']
    blood_group = request.form['blood_group']
    password = request.form['password']
    state = request.form['state']
    address = request.form['address']
    
    hashed_password = hash_password(password)

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO users (first_name, last_name, age, gender, mobile, email, blood_group, password,state,district,address ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                   (first_name, last_name, age, gender, mobile, email, blood_group, hashed_password, state,password,address))
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for('login'))  # Redirect to login after registration

@app.route('/login')
def login():
    return render_template('login.html')  # Show the login form

@app.route('/do_login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password(password, user[7]):  # Assuming user[7] is the hashed password
        # Generate a one-time code
        mfa_code = random.randint(100000, 999999)
        
        # Send the MFA code via email
        send_mfa_code(email, mfa_code)
        
        # Store the code in the session for later verification
        session['mfa_code'] = mfa_code
        session['user_id'] = user[0]  # Store user ID
        
        return render_template('mfa.html')  # Show MFA input form

    return 'Login failed', 401




@app.route('/verify-mfa', methods=['POST'])
def verify_mfa():
    entered_code = request.form['mfa_code']
    
    if 'mfa_code' in session and str(session['mfa_code']) == entered_code:
        # MFA successful, grant access
        return redirect(url_for('profile'))
    
    return 'Invalid MFA code', 401

@app.route('/profile')
def profile():
    return 'Welcome to your profile!'

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')



if __name__ == '__main__':
    app.run(debug=True)














