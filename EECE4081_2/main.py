# Name: Nicholas Gilchrist
# Assignment 1
# Due:  9/8/2020

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import os

from flask_sqlalchemy import SQLAlchemy

 
#database = "sqlite:///brokenlaptop.db"
database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )



app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database

db = SQLAlchemy(app)

##################################################
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
# if you do not do this step, the database file will not be created and you will receive an error message saying "table does not exist".
###################################################
#https://github.com/ahmed217/BrokenLaptop.git
#Using CRUD Functions to create,read,update, and delete entries for laptops




@app.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all() 
    return 'DB Initialized'


@app.route('/test')
def test():
    return 'App is running'

@app.route('/create', methods=['GET','POST'])
def create(): 
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(brokenlaptop)
        db.session.commit()
        
    dispLaptop = BrokenLaptop.query.all()
    return render_template("create.html",dispLaptop = dispLaptop,title = "Create Broken Laptop")


@app.route('/')
def read():
    brokenlaptop = BrokenLaptop.query.all()
    return render_template("index.html",brokenlaptop=brokenlaptop, title = 'Inventory of Broken Laptops' )

@app.route('/delete/<laptop_id>') # add id
def delete(laptop_id):
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    db.session.delete(brokenlaptop)
    # add a line of code to commit the delete operation 
    db.session.commit()
    return redirect("/")
 
@app.route('/update/<laptop_id>', methods=['GET','POST']) # add id 
def update(laptop_id):
    
    lap = BrokenLaptop.query.get(laptop_id)
    idString = str(lap)
    
    if request.form:
           
        lap.brand = request.form.get("brand")
        lap.price = request.form.get("price")
        
        db.session.commit()
        
    return render_template("update.html", brokenlaptop = lap, title = 'Update ID: ' + idString)
    

class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    
if __name__ == '__main__':
    app.run(debug=True)
