#importing usability, making sure it's set correctly
from flask import Flask
from config import Config
# IMPORT YOUR BLUEPRINTS
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from .models import db as root_db, login_manager, ma

from flask_migrate import Migrate

#flask CORS import - cross origin resource sharing. future proofing for flask api access
from flask_cors import CORS

from .helpers import JSONEncoder

app = Flask(__name__)

#temp route to show how it works, no longer necessary
#@app.route("/") #simple route on the homepage
#def hello_world():
#    return"<p>Hello, world!</p>"

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

#configure config using Config class
app.config.from_object(Config)

#allows connection between app and database
#wrapping app with database
root_db.init_app(app)
migrate = Migrate(app, root_db)

ma.init_app(app)
login_manager.init_app(app)
#makes login required, wont allow unlogged users in certian routes
login_manager.login_view = "auth.signin"

#not instantiating, just telling apps json encoder to use the specified class
app.json.encoder = JSONEncoder

CORS(app)