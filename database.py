#create database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import *



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
db.session.commit() #commit change