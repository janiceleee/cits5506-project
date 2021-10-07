from flask import Flask, render_template
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime 
#from server import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///parking.db'
db = SQLAlchemy(app) #sets up the db 
migrate = Migrate(app, db)

class Bay(db.Model):   
    #__tablename__ = "Bay"
    
    #create db columns
    id = db.Column(db.Integer, primary_key = True) #this column is automatically computed, we don't need to input it in the table
    bay_id = db.Column(db.Integer) #Bay number
    bay_type = db.Column(db.String(64)) #car, motorbike etc
    bay_user_group = db.Column(db.String(128)) #staff, students, handicapped
    bay_status = db.Column(db.String(128)) #vacant, occupied
    bay_restrictions = db.Column(db.Integer) #3 hours etc

    def __repr__(self):
        return '<Bay {}>'.format(self.bay_id)

db.create_all() #creates the table 

"""
#create some mock bays
bay1 = Bay(bay_id = '1', bay_type = 'Car',  bay_user_group = "student", bay_status = 'vacant', bay_restrictions = 3) 
bay2 = Bay(bay_id = '2', bay_type = 'Motorbike',  bay_user_group = "student", bay_status = 'occupied', bay_restrictions = 4) 
bay3 = Bay(bay_id = '3', bay_type = 'Car',  bay_user_group = "student", bay_status = 'occupied', bay_restrictions = 3) 
bay4 = Bay(bay_id = '4', bay_type = 'Motorbike',  bay_user_group = "student", bay_status = 'vacant', bay_restrictions = 4) 
bay5 = Bay(bay_id = '5', bay_type = 'Car',  bay_user_group = "student", bay_status = 'occupied', bay_restrictions = 3)
bay6 = Bay(bay_id = '6', bay_type = 'Car',  bay_user_group = "student", bay_status = 'occupied', bay_restrictions = 3)
bay7 = Bay(bay_id = '7', bay_type = 'Car',  bay_user_group = "staff", bay_status = 'occupied', bay_restrictions = 3)
bay8 = Bay(bay_id = '8', bay_type = 'Car',  bay_user_group = "staff", bay_status = 'occupied', bay_restrictions = 3)
bay9 = Bay(bay_id = '9', bay_type = 'Car',  bay_user_group = "staff", bay_status = 'vacant', bay_restrictions = 3)

#add them to the table
db.session.add(bay1) 
db.session.add(bay2) 
db.session.add(bay3) 
db.session.add(bay4) 
db.session.add(bay5) 
db.session.add(bay6) 
db.session.add(bay7) 
db.session.add(bay8) 
db.session.add(bay9) 
db.session.commit() #commit change """

#insert code here to get sensor reading + change car bay 1 bay_status depending on our sensor reading
#server()
#print(server.bay_status)

#num_available_bays = Bay.query.filter_by(bay_status = 'vacant').count() #get number of available car spots

@app.route('/') #landing page
def index(): 
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M") 
    num_available_bays = Bay.query.filter_by(bay_status = 'vacant').count()
    templateData = {
      'num_available_bays' : num_available_bays,
      'time': timeString
      }
    one = db.session.query(Bay).get(1)
    count = db.session.query(Bay).count()
    print(one.bay_status)
    print(count)
    #finds the index.html inside the templates folder and the templateData variables are dynamically inserted into the index.html rendered
    return render_template('index.html', **templateData) 


