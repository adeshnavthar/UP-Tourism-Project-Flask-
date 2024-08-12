from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
import datetime
from flask_mail import Mail,Message
from main import mail


def homepage():
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    sql = "select * from tour"
    cursor = con.cursor()
    cursor.execute(sql)
    tours = cursor.fetchall()
    sql = "select * from category;"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("homepage.html",tours = tours,cats = cats)

def AboutUs():
    return render_template("AboutUs.html")

def showTours(cid):
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    sql = "select * from tour where cat_id=%s;"
    val = (cid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    tours = cursor.fetchall()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("homepage.html",tours = tours,cats = cats)


def addToCart():
    if "uname" in session:
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        
        uname = session["uname"]
        tour_id = request.form["tour_id"]
        qty = request.form["qty"]
        price=request.form["price"]
        subtotal=int(qty)*int(price)
        #Check for duplicate
        sql = "select count(*) from mycart where username=%s and tour_id=%s"
        val = (uname,tour_id)
        cursor.execute(sql,val)
        result = cursor.fetchone()[0]
        if(int(result) >= 1):
            return "Item already in cart"
        else:
            sql = "insert into mycart (username,tour_id,qty,subtotal) values (%s,%s,%s,%s)"
            val = (uname,tour_id,qty,subtotal)
            cursor.execute(sql,val)
            con.commit()
        con.close()  
        return redirect("/")        
    else:
        return redirect("/login")


def ViewDetails(tour):
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    sql = "select * from tour where tour_id=%s"
    val = (tour,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    tour = cursor.fetchone()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("ViewDetails.html",tour = tour,cats=cats)

def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = "select count(*) from user_info where username = %s and password=%s and role='user'"
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()        
        if (int(result[0]) == 1):
            session["uname"] = uname
            return redirect("/")
        else:
            messege="Please enter valid Username and Password!"
            return render_template("login.html",messege=messege)

def signup():
    if request.method == "GET":
        return render_template("sign up.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        email = request.form["email"]
        result = checkDuplicate(uname)
        if(result==True):
            return render_template("sign up.html", message1="Please use different username!!")
        else:
            sql = "insert into user_info values (%s,%s,%s,'user')"
            con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
            val = (uname,pwd,email)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
            con.close()
            message="User registered successfully! Go to Login"
            return render_template ("sign up.html",message=message)

        
def checkDuplicate(uname):
    sql = "select count(*) from user_info where username = %s and role='user'"
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    val = (uname,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    result = cursor.fetchone()
    con.close()
    if (int(result[0]) == 1):
        return True
    else:
        return False

def logout():
    session.clear()
    return redirect("/")


def addToCart():
    if "uname" in session:
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        
        uname = session["uname"]
        tour_id = request.form["tour_id"]
        tour_name = request.form["tour_name"]
        duration = request.form["duration"]
        price=request.form["price"]
        image=request.form["Image"]
        img_spl=image[8:]
        qty = request.form["qty"]
        subtotal=int(price)*int(qty)

        sql = "select count(*) from mycart where username=%s and tour_id=%s"
        val = (uname,tour_id)
        cursor.execute(sql,val)
        result = cursor.fetchone()[0]
        if(int(result) >= 1):
            return redirect("/showCart")
        else:
            sql = "insert into mycart (tour_id,username,tour_name,duration,price,image,qty,subtotal) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (tour_id,uname,tour_name,duration,price,img_spl,qty,subtotal)
            cursor.execute(sql,val)
            con.commit()
        con.close()  
        return redirect("/showCart")        
    else:
        return redirect("/login")
    
def ShowCart():
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    cursor = con.cursor()
    uname=session["uname"]
    sql="select count(*) from mycart where username=%s"
    val=(uname,)
    cursor.execute(sql,val)
    cart_count = cursor.fetchone()
    con.close()


    if cart_count[0]==0:
        return render_template("None_in_cart.html")
    else:
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        if request.method == "GET":        
            sql = "select * from mycart where username=%s"
            val = (session["uname"],)        
            cursor.execute(sql,val)
            result = cursor.fetchall()
            sql = "select sum(subtotal) from mycart_vw where username=%s"
            val = (session["uname"],)
            cursor.execute(sql,val)
            sum = cursor.fetchone()[0]
            session["total"] = sum
            sql = "select * from category"
            cursor = con.cursor()
            cursor.execute(sql)
            cats = cursor.fetchall()
            return render_template("showCart.html",tours=result,sum = sum,cats=cats)
        else:        
            action = request.form["action"]
            tour_id = request.form["tour_id"]
            uname = session["uname"]
            if (action == "delete"):           
                sql = "delete from mycart where tour_id=%s"
                val = (tour_id,)
                cursor.execute(sql,val)   
                con.commit()
                con.close()
                return redirect(url_for("ShowCart"))
            
def MakePayment():
    if request.method =="GET":
        return render_template("MakePayment.html") 
    
    elif request.method =="POST":
        uname = session["uname"]
        date_tour = request.form["date_tour"]
        date_payment=datetime.date.today()
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        total=session["total"]
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        sql = "insert into mypayment values (%s,%s,%s,%s,%s,%s)"
        val = (uname,cardno,cvv,expiry,total,date_payment)
        cursor.execute(sql,val)
        con.commit()
        owner = "insert into balance values (%s,%s)"
        val2 = (session["total"],date_payment)
        cursor.execute(owner,val2)
        con.commit()
        updateorderMaster(date_payment,date_tour)

        sql = "select email from user_info where username=%s"
        val= (uname,)
        cursor.execute(sql,val)
        email = str(cursor.fetchone()[0])
        con.close()
        con.close()

        return render_template("orderConfirm.html",email=email)

        
    
def updateorderMaster(a,b):
    uname = session["uname"]
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    cursor = con.cursor()
    sql = "select tour_name,duration,price,qty,subtotal from mycart where username=%s"
    val = (uname,)
    cursor.execute(sql,val)
    result = cursor.fetchall()
    data = []
    for tour in result:
        data.append(tour)
    for data in data:
        uname=session["uname"]
        tour_name=data[0]
        duration=data[1]
        price=data[2]
        qty=data[3]
        subtotal=data[4]
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        sql = "insert into ordermaster (username,tour_name,price,qty,subtotal,duration) values (%s,%s,%s,%s,%s,%s)"
        val = (uname,tour_name,price,qty,subtotal,duration)
        cursor.execute(sql,val)
        con.commit()
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    cursor = con.cursor()
    sql = "update ordermaster set data_of_booking=%s where username=%s"
    val=(a,uname)
    cursor.execute(sql,val)
    con.commit()
    sql = "update ordermaster set date_of_tour=%s where username=%s"
    val=(b,uname)
    cursor.execute(sql,val)
    con.commit()

    sql = "delete from mycart where username=%s"
    val = (session["uname"],)
    cursor.execute(sql,val)
    con.commit()

#email
    send_message()



def send_message():

    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    cursor = con.cursor()

    uname = session["uname"]

    sql = "select * from ordermaster where username=%s"
    val= (uname,)
    cursor.execute(sql,val)
    mail_body = (cursor.fetchall())

    sql = "select email from user_info where username=%s"
    val= (uname,)
    cursor.execute(sql,val)
    email = str(cursor.fetchone()[0])

    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    cursor = con.cursor()
    sql="select sum(subtotal) from ordermaster where username=%s"
    val=(uname,)
    cursor.execute(sql,val)
    sum1=cursor.fetchone()
    total=sum1[0]
    con.close()

    from datetime import datetime

    date_of_tour = str(mail_body[0][6])
    date_obj1 = datetime.strptime(date_of_tour, "%Y-%m-%d")
    date_of_tour = date_obj1.strftime("%d-%m-%Y")

    date_of_booking= str(mail_body[0][5])
    date_obj2 = datetime.strptime(date_of_booking, "%Y-%m-%d")
    date_of_booking = date_obj2.strftime("%d-%m-%Y")

    subject = "UP Tours- Bookings"

    html_content = render_template('email_template.html',mail = mail_body,total=total,date_of_tour=date_of_tour,date_of_booking=date_of_booking)

    
    message = Message(subject=subject,sender="Adesh Navthar",
                    recipients=[email],
                    html=html_content)

    mail.send(message)



def orderConfirm():
    return render_template("orderConfirm.html")



def bookings():
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    cursor = con.cursor()
    uname=session["uname"]
    sql="select count(*) from ordermaster where username=%s"
    val=(uname,)
    cursor.execute(sql,val)
    booking_count = cursor.fetchone()
    con.close()

    if booking_count[0]==0:
        return render_template("None_in_booking.html")
    else:
        uname=session["uname"]
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        sql="select * from ordermaster where username=%s"
        val=(uname,)
        cursor.execute(sql,val)
        result=cursor.fetchall()
        con.close()
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cursor = con.cursor()
        sql="select sum(subtotal) from ordermaster where username=%s"
        val=(uname,)
        cursor.execute(sql,val)
        sum1=cursor.fetchone()
        sum=sum1[0]
        con.close()
        return render_template("my_bookings.html",tours=result,sum=sum)

