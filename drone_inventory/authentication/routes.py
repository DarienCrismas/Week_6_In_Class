from flask import Blueprint, render_template, request, redirect, url_for, flash
from drone_inventory.forms import UserLoginForm
from drone_inventory.models import User, db, check_password_hash

from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods=["GET", "POST"])

def signup():
    userform = UserLoginForm()

    try:
        if request.method == "POST" and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data
            print(email, password)

            user = User(email, username, password)

            #add to database
            db.session.add(user)
            db.session.commit()

             #add to html later. category user-created
            flash(f"You have successfully created a user account {email}.", "user-created")

            #will redirect to home if form built correctly
            return redirect(url_for("auth.signin"))
    except:
        raise Exception("Invalid form data. Please check your submissions.")
    
    #returns form instantiated here
    return render_template("signup.html", form=userform)

@auth.route("/signin", methods = ["GET", "POST"])
def signin():
    userform = UserLoginForm()

    try:
        if request.method == "POST" and userform.validate_on_submit():
            email = userform.email.data
            #username technically not being used to validate and not actually necessary
            username = userform.username.data
            password = userform.password.data
            print(email, password)

            #find email on user model that == email on userform
            logged_user = User.query.filter(User.email == email).first()
            #checking hashed password against password passed in
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You were successfully logged in.")
                return redirect(url_for("site.profile")) 
            else:
                flash("Your email or password is incorrect", "auth-failed")
                return redirect("auth.signin")
    except:
        raise Exception("Invalid Form Data: please check your form")

    #associate form so it knows what form we're actually referring to
    return render_template("signin.html", form=userform)

#defaults to get with no methods
@auth.route("/logout")
#can't log out if not logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.home"))

