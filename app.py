from flask import Flask, render_template, session, url_for, redirect, request
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def root():
    # check if logged in
    if not 'loggedin?' in session:
        session["loggedin?"] = False

    if session['loggedin?']:
        return redirect("/welcome")

    # need user data
    return render_template('form.html', text = 'Please enter your login')

# get here through form.html
@app.route("/login", methods = ["POST", "GET"])
def login():
    # check credentials
    usercheck = False
    passcheck = False
    session["user"] = request.form.get("username")
    if request.form.get("username") == "brown":
            usercheck = True
    if request.form.get("password") == "13":
            passcheck = True

    if (usercheck and passcheck):
        session['loggedin?'] = True
        return redirect("/welcome")
    elif(usercheck and not passcheck):
        return render_template('form.html', text = "wrong password")
    elif(not usercheck and passcheck):
        return render_template('form.html', text = "wrong username")
    return render_template('form.html', text = "wrong username and password")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html", username = session['user'])

@app.route("/signout")
def signout():
    session.pop("user")
    session.pop("loggedin?")
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
