import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import os
import requests


def InsertRecord(email, password):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(email,password) VALUES (?,?)", (email, password))
        connection.commit()
        message = True
    except:
        message = False

    cursor.close()
    connection.close()
    return message


def CheckRecord(email, password):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT password,firstName,lastName,phone,street,city,state,zipCode,timeDetails,natureOfTime FROM users WHERE email=?", (email,))
        result = cursor.fetchone()

        if (check_password_hash(result[0], password)):
            print("Matched")
            connection.commit()
            message = True
            if result[1] == None:
                session['firstName'] = ""
            else:
                session['firstName'] = result[1]
            if result[2] == None:
                session['lastName'] = ""
            else:
                session['lastName'] = result[2]
            if result[3] == None:
                session['phoneNumber'] = ""
            else:
                session['phoneNumber'] = result[3]
            if result[4] == None:
                session['street'] = ""
            else:
                session['street'] = result[4]
            if result[5] == None:
                session['city'] = ""
            else:
                session['city'] = result[5]
            if result[6] == None:
                session['state'] = ""
            else:
                session['state'] = result[6]
            if result[7] == None:
                session['zipCode'] = ""
            else:
                session['zipCode'] = result[7]
            if result[8] == None:
                session['timeDetails'] = ""
            else:
                session['timeDetails'] = result[8]
            if result[9] == None:
                session['natureOfTime'] = ""
            else:
                session['natureOfTime'] = result[9]
        else:
            print("Password issue")
            message = False
        connection.commit()

    except:
        print("Query issue")
        message = False

    cursor.close()
    connection.close()
    return message


def SessionUpdate(email):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT firstName,lastName,phone,street,city,state,zipCode,timeDetails,natureOfTime,email FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        if result[0] == None:
            session['firstName'] = ""
        else:
            session['firstName'] = result[0]
        if result[1] == None:
            session['lastName'] = ""
        else:
            session['lastName'] = result[1]
        if result[2] == None:
            session['phoneNumber'] = ""
        else:
            session['phoneNumber'] = result[2]
        if result[3] == None:
            session['street'] = ""
        else:
            session['street'] = result[3]
        if result[4] == None:
            session['city'] = ""
        else:
            session['city'] = result[4]
        if result[5] == None:
            session['state'] = ""
        else:
            session['state'] = result[5]
        if result[6] == None:
            session['zipCode'] = ""
        else:
            session['zipCode'] = result[6]
        if result[7] == None:
            session['timeDetails'] = ""
        else:
            session['timeDetails'] = result[7]
        if result[8] == None:
            session['natureOfTime'] = ""
        else:
            session['natureOfTime'] = result[8]
        session['email'] = result[9]
        message = True
        connection.commit()
    except:
        message = False
        print("Query issue")

    cursor.close()
    connection.close()
    return message


def UpdateRecord(email, firstName, lastName, phone, street, city, state, zipCode, timeDetails, natureOfTime):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE users SET firstName=?,lastName=?,phone=?,street=?,city=?,state=?,zipCode=?,timeDetails=?,natureOfTime=?,email=? WHERE email=?", (firstName, lastName, phone, street, city, state, zipCode, timeDetails, natureOfTime, email, session['email'],))

        connection.commit()
        message = SessionUpdate(email)

    except:
        print("Query issue")
        message = False

    cursor.close()
    connection.close()
    return message


def InsertOffice(days, beginTime, endTime, email):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO office(days,beginTime,endTime,email) VALUES (?,?,?,?)", (days, beginTime, endTime, email))
        connection.commit()
        message = True
    except:
        message = False

    cursor.close()
    connection.close()
    return message


def FetchOfficeHours(email):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    officeHours = []
    try:
        cursor.execute(
            "SELECT sno,days,beginTime,endTime from office where email = ?", (email,))
        result = cursor.fetchall()
        for work in result:
            officeHours.append(work)
        connection.commit()

    except:
        pass

    cursor.close()
    connection.close()
    return officeHours


def EditOffice(days, beginTime, endTime, sno):
    message = False
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    officeHours = []
    try:
        cursor.execute(
            "UPDATE office SET days=?,beginTime=?,endTime=? where sno=? and email = ?", (days, beginTime, endTime, sno, session['email'],))
        message = True
        connection.commit()

    except:
        message = False

    cursor.close()
    connection.close()
    return message


def DeleteOffice(sno):
    message = False
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    officeHours = []
    try:
        cursor.execute(
            "DELETE from office where sno=? and email = ?", (sno, session['email'],))
        message = True
        connection.commit()

    except:
        message = False

    cursor.close()
    connection.close()
    return message


def InsertSyllabus(course, section, courseFile, email):

    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO syllabus(course,section,courseFile,email) VALUES (?,?,?,?)",
                       (course, section, courseFile, email,))

        connection.commit()
        message = True

    except:
        message = False

    cursor.close()
    connection.close()
    return message


def FetchSyllabus(email):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    Syll = []

    cursor.execute(
        "SELECT sno,course,section,courseFile FROM syllabus WHERE email = ?", (email,),)
    result = cursor.fetchall()

    for work in result:

        Syll.append(work)
    connection.commit()

    cursor.close()
    connection.close()

    return Syll


def DeleteSyllabus(sno):
    message = False
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()
    officeHours = []
    try:
        cursor.execute(
            "SELECT courseFile from syllabus where sno=? and email = ?", (sno, session['email'],))
        result = cursor.fetchone()
        os.remove(result[0])

        cursor.execute(
            "DELETE from syllabus where sno=? and email = ?", (sno, session['email'],))
        message = True
        connection.commit()

    except:
        message = False

    cursor.close()
    connection.close()
    return message


def DownloadFile(sno):
    connection = sqlite3.connect('qa_app.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT courseFile FROM syllabus WHERE sno = ? and email = ?", (sno, session['email'],),)
    result = cursor.fetchone()

    filePath = result[0].split("/")
    filePath = filePath[len(filePath)-1]
    url = "http://localhost:3000/"+result[0]
    downloaded_obj = requests.get(url)

    with open(filePath, "wb") as file:
        file.write(downloaded_obj.content)

    connection.commit()

    cursor.close()
    connection.close()

    return True
