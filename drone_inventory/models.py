#holds database models
from flask_sqlalchemy import SQLAlchemy
#migrate db from flask into actual db
from flask_migrate import Migrate
#primary key essentially, user id
import uuid 
from datetime import datetime

#adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#import secrets module. generate user token
import secrets

#import for loginmanager and usermixin, help us log in our users + store their credentials
from flask_login import UserMixin, LoginManager

#import for flask-marshmallow, formats data/requests
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

#function underneath will be used to load user
@login_manager.user_loader
def load_user(user_id):
    #passing in user id, returning dictionary for specific user
    return User.query.get(user_id)


#usermixin helps find a user when signing in 
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = '')    
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = "", unique = True)
    #timestamps for current time when created
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    #says user is owner of this specific drone. lazy says user doesn't need a drone to b created, can be created later
    drone = db.relationship("Drone", backref = "owner", lazy = True)


    #remember, defaults go last
    def __init__(self, email, username, password, first_name = "", last_name = ""):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username 

    def set_id(self):
        #uuid4 method associated with uuid
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        #returning unique id
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database."

class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    camera_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=10, scale = 2))
    series = db.Column(db.String(150))
    #joke, unrelated to drones
    random_joke = db.Column(db.String, nullable = True)
    #lowercase bc when migrating to elephantsql it will lowercase and snakecase everything
    user_token = db.Column(db.String, db.ForeignKey("user.token"), nullable = False)

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, random_joke, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.series = series
        self.random_joke = random_joke
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Drone {self.name} has been added tot he database."
    

class DroneSchema(ma.Schema):
    #allows data to be pulled from api request
    class Meta:
        #user token being passed in so not needed + you dont want user to see token
        fields = ["id", "name", "description", "price", "camera_quality", "flight_time", "max_speed", "dimensions", "weight", "cost_of_production", "series", "random_joke"]

drone_schema = DroneSchema()
drones_schema = DroneSchema(many=True)


