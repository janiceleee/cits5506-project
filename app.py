from flask import Flask, render_template
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime 

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


@app.route('/') #landing page
def index(): 
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M") 

		#get number of available car spots
    num_available_bays = Bay.query.filter_by(bay_status = 'vacant').count() 

		#get information about bay in database
    bay = db.session.query(Bay)
    
    templateData = {
      'num_available_bays' : num_available_bays,
      'time': timeString,
			'bay1': bay.get(1).bay_status,
			'bay2': bay.get(2).bay_status,
			'bay3': bay.get(3).bay_status,
			'bay4': bay.get(4).bay_status,
			'bay5': bay.get(5).bay_status,
			'bay6': bay.get(6).bay_status,
			'bay7': bay.get(7).bay_status,
			'bay8': bay.get(8).bay_status,
			'bay9': bay.get(9).bay_status,
    }

		#debugging - check if database is updated
    one = db.session.query(Bay).get(1)
    count = db.session.query(Bay).count()
    print(one.bay_status)
    print(count)

    #finds the index.html inside the templates folder and the templateData variables are dynamically inserted into the index.html rendered
    return render_template('index.html', **templateData) 


