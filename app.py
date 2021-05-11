from flask import Flask, flash, request, render_template, redirect, url_for, session, g
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import seed
import schema
import os


# Flask application is created
app = Flask(__name__)

# Application secret key
app.secret_key = "Don't tell anyone"


# EMAIL SMTP DETAILS
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "legendbest123@gmail.com"
app.config['MAIL_PASSWORD'] = "gcpvxzooaxjqabdb"
app.config['MAIL_DEFAULT_SENDER'] = "legendbest123@gmail.com"
app.config['MAIL_ASCII_ATTACHMENTS'] = False
# These are our application smtp settings so we can send to relevent professor

mail = Mail(app)
# Created Main() for sending mail


# Route: Login
# Description: Login Features are set in this route
# Status : Completed
@app.route('/', methods=['GET', 'POST'])
def index():

    if 'email' in session:               # if Email is already in session
        g.email = session['email']        # Then store it in g
        # And redirect it to contact_info route
        return redirect(url_for('contact_info'))

    elif request.method == 'POST':      # When a post request is send to the login page
        # It will check the action if the action is login
        if (request.form['action'] == 'login'):
            # Email will be requested from the form and stored in email variable
            email = request.form['email']
            # Password is requested and stored in password field
            password = request.form['password']
            # send it to checkRecord method where our backend will check whether our login information is valid or invalid if valid it will send True else False
            resp = seed.CheckRecord(email, password)
            if (resp):        # if resp is True
                session['email'] = email  # Store the email in session

                # And Redirect it to contact_info route
                return redirect(url_for('contact_info'))
            else:     # Else
                # Show message that Email or password is invalid
                flash("Email or Password is invalid", "danger")
                # And redirect to login again
                return redirect(url_for('index'))
    else:  # Else
        return render_template("index.html")    # render login page


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Sign up Route
# Description: Add and display sign up form
# Status : Completed


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if 'email' in session:
        g.email = session['email']
        return redirect(url_for('contact_info'))

    elif request.method == 'POST':

        if (request.form['action'] == 'signup'):

            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            if (password == confirmPassword):
                password = generate_password_hash(password)
                email = request.form['email']

                resp = seed.InsertRecord(email, password)
                if (resp):
                    flash("Account Created Successfully", "success")
                    return redirect(url_for('signup'))
                else:
                    flash("Use another email", "danger")
                    return redirect(url_for('signup'))
            else:
                flash("Password doesn't matched", "danger")
                return redirect(url_for('signup'))

    else:
        return render_template("signup.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Syllabus Process
# Description: Add and Update Details
# Status : Completed


@app.route('/contact-info', methods=['GET', 'POST'])
def contact_info():
    if 'email' in session:
        g.email = session['email']
        if request.method == 'POST':
            if (request.form['action'] == 'contact-info'):

                email = request.form['email']
                firstName = request.form['firstName']
                lastName = request.form['lastName']
                phoneNumber = request.form['phoneNumber']
                street = request.form['street']
                city = request.form['city']

                state = request.form['state']

                zipCode = request.form['zipCode']
                timeDetails = request.form['timeDetails']

                natureOfTime = request.form['natureOfTime']

                resp = seed.UpdateRecord(
                    email, firstName, lastName, phoneNumber, street, city, state, zipCode, timeDetails, natureOfTime)
                if (resp):

                    flash("Details Updated", "success")
                    return redirect(url_for('contact_info'))
                else:
                    flash("Try a new Email Address!", "danger")
                    return redirect(url_for('contact_info'))
            elif(request.form['action'] == 'Submit-Form'):
                email = session['email']
                firstName = session['firstName']
                lastName = session['lastName']
                phoneNumber = session['phoneNumber']
                street = session['street']
                city = session['city']

                state = session['state']

                zipCode = session['zipCode']
                timeDetails = session['timeDetails']

                natureOfTime = session['natureOfTime']
                msg = Message('Contact Info !',
                              sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])

                # for storing data into Database

                OfficeH = seed.FetchOfficeHours(session['email'])

                textMessage = ""
                for office in OfficeH:
                    textMessage = textMessage + "Day: " + \
                        office[1] + "\tBegin Time: " + office[2] + \
                        "\tEnd Time: " + office[3]+"\n"
                msg.body = "Thank you for submitting your information.\nYour Account Information is: \nFirst Name: " + firstName + "\nLast Name: " + lastName + "\nPhone Number: " + phoneNumber + "\nStreet: " + \
                    street + "\nCity: " + city + "\nState: " + state + "\nZip Code: " + zipCode + "\nTime Details: " + \
                    timeDetails + "\nNature Of Time: " + natureOfTime + \
                    "\n\nYour Office Hours are: \n\n" + textMessage
                mail.send(msg)

                flash("Details Sent", "success")
                return redirect(url_for('contact_info'))
            else:
                flash("You are trying to access the page without permission", "danger")
                return redirect(url_for('contact_info'))

        else:

            return render_template('contact-info.html')
    else:
        flash("Session Ended", "warning")
        return redirect(url_for('index'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Office Hour
# Description: Fetch Data when table is updated
# Status : Completed


@app.route('/office_hour', methods=['GET', 'POST'])
def office_hour():
    if 'email' in session:
        g.email = session['email']
        officeHours = seed.FetchOfficeHours(session['email'])
        return render_template('office_hour.html', officeHours=officeHours)
    else:
        flash("Session Ended", "warning")
        return redirect(url_for('index'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Office Hour  Action
# Description: Add Edit and delete Office Hour
# Status : Completed


@app.route("/action", methods=['GET', 'POST'])
def OfficeAction():
    if 'email' in session:
        g.email = session['email']

        if request.method == "POST":
            if request.form['action'] == 'submit':
                # storing size of form values like days
                rows = int((len(request.form) - 1) / 3)

                for i in range(0, rows):

                    days = request.form["days{}".format(i)]
                    beginTime = request.form["beginTime{}".format(i)]
                    endTime = request.form["endTime{}".format(i)]

                    seed.InsertOffice(
                        days, beginTime, endTime, session['email'])

                flash("Office Hours Added", "success")
                return redirect(url_for("office_hour"))
            elif request.form['action'] == 'edit':
                days = request.form['days']
                beginTime = request.form['beginTime']
                endTime = request.form['endTime']
                sno = request.form['sno']
                resp = seed.EditOffice(days, beginTime, endTime, sno)
                if (resp):

                    flash("Updated Successfully", "success")
                    return redirect(url_for("office_hour"))
                else:
                    flash("Not Updated", "warning")
                    return redirect(url_for("office_hour"))
            elif request.form['action'] == 'delete':
                sno = request.form['sno']
                resp = seed.DeleteOffice(sno)
                if (resp):

                    flash("Deleted Successfully", "success")
                    return redirect(url_for("office_hour"))
                else:
                    flash("Not Deleted", "warning")
                    return redirect(url_for("office_hour"))
            else:
                return redirect(url_for("office_hour"))
        else:
            flash("Session Ended", "warning")
            return redirect(url_for('index'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Syllabus Route
# Description: Syllabus route with fetch syllabus to update table
# Status : Completed


@app.route('/syllabus', methods=['GET', 'POST'])
def syllabus():
    if 'email' in session:
        g.email = session['email']
        Syllabus = seed.FetchSyllabus(g.email)
        return render_template('syllabus.html', Syllabus=Syllabus)
    else:
        flash("Session Ended", "warning")
        return redirect(url_for('index'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Syllabus Process
# Description: Add Download and delete syllabus
# Status : Completed


@app.route("/process", methods=['GET', 'POST'])
def SyllabusAction():
    if 'email' in session:
        g.email = session['email']

        if request.method == "POST":
            if request.form['action'] == 'submit':

                UPLOAD_FOLDER = 'static/users/' + session['email']+"/syllabus"

                if not os.path.exists('static/users/'+session['email']):
                    os.makedirs('static/users/'+session['email'])
                    os.makedirs('static/users/' +
                                session['email']+"/syllabus")

                app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

                app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

                # storing size of form values like days
                rows = int((len(request.form) - 1) / 2)

                for i in range(0, rows):

                    course = request.form["course{}".format(i)]
                    section = request.form["section{}".format(i)]
                    file = request.files["FileSyllabus{}".format(i)]
                    filename = secure_filename(file.filename)

                    if filename != '':

                        file.save(os.path.join(
                            app.config['UPLOAD_PATH'], filename))
                        path = app.config['UPLOAD_PATH']+'/'+filename
                        courseFile = path

                        resp = seed.InsertSyllabus(
                            course, section, courseFile, session['email'])
                        if resp:
                            pass
                        else:
                            flash("File Name Error", "danger")
                            return redirect(url_for("syllabus"))

                    else:
                        flash("File Name Error", "danger")
                        return redirect(url_for("syllabus"))
                flash("Course Successfully Added", "success")
                return redirect(url_for("syllabus"))
            elif request.form['action'] == 'download':

                sno = request.form['sno']
                resp = seed.DownloadFile(sno)
                if (resp):

                    flash("Download Successfully Started", "success")
                    return redirect(url_for("syllabus"))
                else:
                    flash("Not Downloaded", "warning")
                    return redirect(url_for("syllabus"))
            elif request.form['action'] == 'delete':
                sno = request.form['sno']
                resp = seed.DeleteSyllabus(sno)
                if (resp):
                    flash("Deleted Successfully", "success")
                    return redirect(url_for("syllabus"))
                else:
                    flash("Not Deleted", "warning")
                    return redirect(url_for("syllabus"))
            else:
                return redirect(url_for("syllabus"))
        else:
            flash("Session Ended", "warning")
            return redirect(url_for('index'))


@ app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# Route: Logout
# Description: Logout the account
# Status : Completed
@ app.route("/logout")
def logout():
    if 'email' in session:
        session.pop('email', None)
        flash("Account Logged Out", "success")
        return redirect(url_for('index'))
    else:
        flash("Session Ended", "danger")
        return redirect(url_for('index'))


@ app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


app.debug = True


if __name__ == '__main__':
    app.run(port=3000, debug=True)
