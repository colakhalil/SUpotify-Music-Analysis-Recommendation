from flask import Flask 
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin 
db = MySQL() 

def create_app(): 
    app = Flask(__name__)
    app.config["SESSION_COOKIE_NAME"] = "spotify_cookie"
    app.secret_key = "sdfsdf943urıjf0"

    # Veritabanı bağlantısı oluşturma
    app.config['MYSQL_HOST'] = 'db'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_PASSWORD'] = 'Atakan2002'
    app.config['MYSQL_DB'] = 'flaskapp'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    CORS(app, resources={
        r"/sign_up": {"origins": "http://localhost:3000"},
        r"/login": {"origins": "http://localhost:3000"},
        r"/sauth": {"origins": "http://localhost:3000"}
    })

    from .auth import auth
    from .main_page import main
    
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    
    db.init_app(app)
    return app
