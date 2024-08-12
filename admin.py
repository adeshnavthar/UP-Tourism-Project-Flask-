from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector


def adminlogin():
    if request.method == "GET":
        return render_template("adminlogin.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = "select count(*) from user_info where username = %s and password=%s and role='Admin'"
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()
        if (int(result[0]) == 1):
            session["uname"] = uname
            return redirect("/AdminPage")
        else:
            message="Please enter valid Username and Password!"
            return render_template("adminlogin.html",msg=message)
        

def adminLogout():
    session.clear()
    return redirect(url_for("adminlogin"))
    

def adminPage():
    if "uname" in session:
        return render_template("adminpage.html")
    else:
        return redirect(url_for("adminlogin"))