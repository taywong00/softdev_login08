from flask import Flask, render_template, session, url_for, redirect, request
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

# root route
@app.route("/")
def root():
    # Go to welcome if properly logged in
    if 'loggedin?' in session and session['loggedin?'] == True:
        return redirect("/welcome")

    #else go to /login
    return redirect('/login')

# get here through form.html
@app.route("/login", methods = ["POST", "GET"])
def login():
    # Go to welcome if properly logged in (for people who are messing around with URL)
    if 'loggedin?' in session and session['loggedin?'] == True:
        return redirect("/welcome")

    # set log in status to false if it's not there and show login w/o rude wrong credentials message
    # should only appear once per login
    if not 'loggedin?' in session:
        session['loggedin?'] = False
        return render_template('form.html', text = 'Please enter your login')

    # check credentials against built in value
    usercheck = False
    passcheck = False
    session["user"] = request.form.get("username")
    if request.form.get("username") == "brown":
            usercheck = True
    if request.form.get("password") == "13":
            passcheck = True

    # process the credentials + says whats wrong with your credentials
    if (usercheck and passcheck):
        session['loggedin?'] = True
        return redirect("/welcome")
    elif(usercheck and not passcheck):
        return render_template('form.html', text = "wrong password")
    elif(not usercheck and passcheck):
        return render_template('form.html', text = "wrong username")
    return render_template('form.html', text = "wrong username and password")


# get here through valid login check
@app.route("/welcome")
def welcome():
    # are you supposed to be here?
    if not 'loggedin?' in session or session['loggedin?'] == False:
        return redirect("/login")

    return render_template("welcome.html", username = session['user'])


# get here through welcome.html
@app.route("/signout")
def signout():
    # should remove logged in status if possibke
    if 'loggedin?' in session and session['loggedin?']:
        session.pop("user")
        session.pop("loggedin?")

    # go back to root
    return redirect("/")

def debug():
    print "\n\n\n"
    print "session:"
    print session
    print "app:"
    print app
    print "\nrequest.headers:"
    print request.headers
    print "\nrequest.method:"
    print request.method
    print "\nrequest.args:"
    print request.args
    print "\nrequest.form:"
    print request.form

if __name__ == "__main__":
    app.debug = True
    app.run()
