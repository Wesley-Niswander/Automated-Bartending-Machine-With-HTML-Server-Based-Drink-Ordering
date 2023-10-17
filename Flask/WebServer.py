#To run this from the terminal navigate to the folder and do this (after creating virtual folder (.venv))
#. .venv/bin/activate
#export FLASK_APP=test.py
#export FLASK_ENV=developement
#flask run
#also can do flask run --host=0.0.0.0 to make visible to other networked devices. (Since this is a developemnt server this 
#gives users the ability to run any arbitrary Python code on your machine so use caution)
# also flask run --debugger goes into debugging mode and allows the app to continually refresh as code changes

#bootstrap and codepen for html css examples

#Liverserver extension allows you to open and test raw html. right click open html file and open in live server

#aref for hyperlink

from flask import Flask, jsonify, render_template, redirect, url_for, make_response, request
import sys
import time
import json
import subprocess
import mysql.connector as db
from mysql.connector import Error
# import pandas as pd
#from flask.ext.images import resized_img_src

app = Flask(__name__)
#app.secret_key= 'monkey'
#images = Images(app)

@app.route('/MainMenu')
def mainMenu():
    return render_template('mainMenu.html')

@app.route('/Vodka')
def vodka():
    return render_template('vodkaMenu.html')

@app.route('/Tequila')
def tequila():
    return render_template('tequilaMenu.html')

@app.route('/Gin')
def gin():
    return render_template('ginMenu.html')

@app.route('/Rum')
def rum():
    return render_template('rumMenu.html')

@app.route('/Setup') #not accessible through main menu
def setup():
    return render_template('setup.html')

@app.route('/order')  
@app.route('/order/<drink>')
@app.route('/order/<drink>/<name>')
def order(drink=None,name=None):
    #Write order to sql database
    dbconnection = db.connect(
            host ='localhost',
            user = 'root',
            password ='1234',
            database = 'drinkz')
    try:
        cursor = dbconnection.cursor()

        try:
            cursor.execute("SELECT * FROM orders WHERE order_number = (SELECT MAX(order_number) FROM orders);")
            orderMax = cursor.fetchone()
            orderNumber = orderMax[2]+1
            #find row with maximum order number, pull out values. Next order number is max order number + 1

            cursor.fetchall()
            #Discard extra data in case there are multiple entries

            cursor.execute("INSERT INTO orders (drink,name,order_number) VALUES ('"+drink+"' , '"+name[1:]+"' , '"+str(orderNumber) +"');")
            dbconnection.commit()
            #insert in the new drink with drink, name ([1:] because first character is "-" which is added in
            # html code to make url valid in the 'no entry' case), and order number

        except:
            cursor.execute("INSERT INTO orders (drink,name,order_number) VALUES ('"+drink+"' , '"+name[1:]+"' , '0');")
            dbconnection.commit()
            #insert in the new drink. The new order number is zero since no other orders found
            
            orderNumber = 0
            #Start fresh at order number 0

        cursor.execute("SELECT * FROM orders;")
        for drink in cursor:
            print(drink)
        #Print the orders in the table (for diagnostic purposes)
        
    except db.Error as error:
        print(error)
    dbconnection.close()
    return redirect(url_for('mainMenu'))

@app.route('/getNextOrder')
def getorder():
    #Pull FIFO order from database, then delete it and return the data
    dbconnection = db.connect(
            host ='localhost',
            user = 'root',
            password ='1234',
            database = 'drinkz')
    try:
        cursor = dbconnection.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_number = (SELECT MIN(order_number) FROM orders);")
        order = cursor.fetchone()
        #Pull out the order with the minimum order number (oldest order FIFO)

        cursor.fetchall()
        #Run in case there are duplicates. There should only be one, 
        #but sql will throw error if the cursor is not emptied before next querey

        cursor.execute("DELETE FROM orders WHERE order_number = "+str(order[2])+";")
        dbconnection.commit()
        #Delete the order from the database

        cursor.execute("SELECT * FROM orders;")
        for drink in cursor:
            print(drink)
        #Print table for reference/diagnostics
    except db.Error as error:
        print(error)
    dbconnection.close()
    return jsonify({"drink" : order[0],"name" : order[1],"order number" : order[2]})

@app.route('/flushOrders')
def flushOrders():
    #This allows for clearing of the table... Not a url an end user would/should use... Maybe I should keep this one a secret
    dbconnection = db.connect(
        host ='localhost',
        user = 'root',
        password ='1234',
        database = 'drinkz')
    try:
        cursor = dbconnection.cursor()
        cursor.execute("DELETE FROM orders;")
        dbconnection.commit()
        #Nuke the table
    except:
        print("Failed to clear table")
    dbconnection.close()
    return "done"

#Database entry
# sudo systemctl start mariadb
# sudo mysql
    # subprocess.run("sudo systemctl start mariadb")
    # subprocess.run("sudo mysql")
    # subprocess.run("USE drinkz;")
    # subprocess.run("INSERT INTO orders (drink)")
    # subprocess.run("VALUES ('" + name + "');")
    # subprocess.run("EXIT;")
