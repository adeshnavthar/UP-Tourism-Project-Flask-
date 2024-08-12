import os
from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
from werkzeug.utils import secure_filename

def showAllTours():
    con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
    sql = "select t.cat_id,t.tour_id, t.tour_name,t.duration,t.price,t.image,t.description from tour t inner join category c on c.cid = t.cat_id;"
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    return render_template("showAllTours.html",tours = result)

def addTour():
    if request.method == "GET":
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        con.close()
        return render_template("addNewTour.html",cats=result)
    else:
        cname = request.form["cname"]
        price = request.form["price"]
        desc = request.form["desc"]
        duration = request.form["duration"]
        cid = request.form["cat"]
        f = request.files['image'] 
        filename = secure_filename(f.filename)
        filename = "static/Images/"+f.filename
        #This will save the file to the specified location
        f.save(filename)   
        filename = "Images/"+f.filename
        
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        sql = "insert into tour (cat_id,tour_name,duration,price,image,description) values (%s,%s,%s,%s,%s,%s)"
        val = (cid,cname,duration,price,filename,desc)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()        
        return redirect(url_for('showAllTours'))
        
        
def editCategory(cid):
    if request.method == "GET":
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        sql = "select * from category where cid=%s"
        val = (cid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()
        return render_template("editCategory.html",cat=result)
    else:
        cname = request.form["cname"]
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        sql = "update Category set cname=%s where cid=%s"
        val = (cname,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()        
        return redirect("/ShowAllCategories")


def deleteCategory(cid):
    if request.method == "GET":
        return render_template("deleteConfirm.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
            sql = "delete from category where cid=%s"
            val = (cid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/ShowAllCategories")




#=====================================================================================================
        
def editTour(tour_id):
    if request.method == "GET":  
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cate_tour="select cid, cname from category"
        cursor = con.cursor()
        cursor.execute(cate_tour)
        result1 = cursor.fetchall()

        sql = "select * from tour where tour_id=%s"
        val = (tour_id,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()

        return render_template("editTour.html",cat=result,category=result1)
    else:
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        cat_id="select cat_id from tour where tour_id=%s"
        var=(tour_id,)
        cursor = con.cursor()
        cursor.execute(cat_id,var)
        result1 = cursor.fetchone()
        con.close()
        cat_id=int(result1[0])
        tour_id = request.form["tour_id"]
        tour_name = request.form["tour_name"]
        price = request.form["price"]
        description = request.form["desc"]
        duration = request.form["duration"]
        f = request.files['file'] 
        filename = secure_filename(f.filename)
        filename = "static/Images/"+f.filename
        #This will save the file to the specified location
        f.save(filename)   
        filename = "Images/"+f.filename
        print(filename)
        con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
        sql = "update tour set tour_name=%s,duration=%s,price=%s,image=%s,description=%s where tour_id=%s"
        val = (tour_name,duration,price,filename,description,tour_id)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()        
        return redirect("/ShowAllTours")

def deleteTour(tour_id):
    
    if request.method == "GET":
        return render_template("deleteConfirm.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con = mysql.connector.connect(host="localhost",user="root",password="8023",database="tourdb")
            image_url="select image from tour where tour_id =%s"
            val_i=(tour_id,)
            cursor = con.cursor()
            cursor.execute(image_url,val_i)
            url=cursor.fetchone()

            sql = "delete from tour where tour_id=%s"
            val = (tour_id,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
            delete_png_file(url)
            return redirect("/ShowAllTours",)
        
        else:
            return redirect("/ShowAllTours")
        


def delete_png_file(url):
    file_path = "static/"+url[0]
    os.remove(file_path)
    
    
