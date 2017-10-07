'''
Shannon Lau and Taylor Wong
SoftDev1 Period 7
HW #07: Do I Know You?
2017-10-4
'''

from flask import Flask, render_template, redirect, url_for, session, request
import os

# Create flask app and establish secret_key
app = Flask(__name__)

#encrypts cookie values
app.secret_key = os.urandom(32)

accounts = {'hello':'world'}

# Landing page
@app.route("/")
def hello_world():
    # If not logged out, render welcome page
    # Else, render login page
    if 'uname' in session.keys():
        return render_template('welcome.html', USERNAME = session['uname'])
    else:
        return render_template('login.html', ERROR = "")

# Renders welcome or login page (with error)
@app.route('/welcome')
def welcome():
    form_dict = request.args
    uname = form_dict['uname']
    password = form_dict['password']
    # Check for existing username
    if uname in accounts.keys():
        # Check for valid password
        if (accounts[uname] == password):
            # Add username data to session
            session['uname'] = uname
            return render_template('welcome.html', USERNAME = uname)
        else:
            return render_template('login.html', ERROR = 'Incorrect password.')
    else:
        return render_template('login.html', ERROR = 'Incorrect username.')

# Log out procedure
@app.route('/logout')
def logout():
    # Remove username data from session
    if 'uname' in session:
        session.pop('uname')
    return render_template('login.html', ERROR = "")

if __name__ == "__main__":
    app.debug = True
    app.run()
