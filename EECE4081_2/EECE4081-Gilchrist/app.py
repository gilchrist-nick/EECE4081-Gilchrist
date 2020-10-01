# Name: Nicholas Gilchrist
# Assignment 1
# Due:  9/8/2020

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
 
database = "sqlite:///brokenlaptop.db"

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

#Using CRUD Functions to create,read,update, and delete entries for laptops

@app.route('/create', methods=['GET','POST'])
def create(): 
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(brokenlaptop)
        db.session.commit()
        
    dispLaptop = BrokenLaptop.query.all()
    return render_template("create.html",dispLaptop = dispLaptop)

@app.route('/')
def read():
    brokenlaptop = BrokenLaptop.query.all()
    return render_template("index.html",brokenlaptop=brokenlaptop)

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
    
    if request.form:
           
        lap.brand = request.form.get("brand")
        lap.price = request.form.get("price")
        
        db.session.commit()
        
    return render_template("update.html", brokenlaptop = lap)

class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    
if __name__ == '__main__':
    app.run(debug=True)
