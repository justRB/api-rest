from flask import Flask
from flask_restx import Api
from apis.vulnerablePasswordAPI import api as vulnerablePassword
from apis.securePasswordGenerationAPI import api as securePasswordGeneration 
from apis.authenticationAPI import api as authentication 
from apis.usersAPI import api as users 
from apis.logsAPI import api as logs
from apis.fakeIdentityAPI import api as fakeIdentity
from apis.ddosAPI import api as ddos
from apis.randomFaceAPI import api as randomFace
from apis.crawlerAPI import api as crawler
from apis.isValidEmailAPI import api as isValidEmail
from apis.easterEggAPI import api as easterEgg
import sqlite3
from datetime import datetime
from services.services import hash_password 

api = Api(
    title="HackR",
    version="1.0",
    description="An api for people who want to harm the population",
    endpoint="/api/v1",
    default_mediatype="application/json",
    ordered=True,
)

api.add_namespace(easterEgg, path="/easterEgg")
api.add_namespace(vulnerablePassword, path="/vulnerablePassword")
api.add_namespace(securePasswordGeneration, path="/securePasswordGeneration")
api.add_namespace(fakeIdentity, path="/fakeIdentity")
api.add_namespace(users, path="/users")
api.add_namespace(logs, path="/logs")
api.add_namespace(authentication, path="/authentication")
api.add_namespace(ddos, path="/ddos")
api.add_namespace(randomFace, path="/randomFace")
api.add_namespace(crawler, path="/crawler")
api.add_namespace(isValidEmail, path="/isValidEmail")

def init_db():
    conn = sqlite3.connect('db.sqlite')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            authority TEXT NOT NULL,
            creation_date DATETIME NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATETIME NOT NULL,
            description TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # cursor.execute('INSERT INTO users (username, password, authority, creation_date) VALUES (?, ?, ?, ?)', 
    #                (
    #                     "kevin_niel", 
    #                     hash_password("supermotdepasse"), 
    #                     "admin",
    #                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #                 )

    conn.commit()
    conn.close()

def create_app():
    app = Flask(__name__)
    api.init_app(app)

    init_db()

    @app.errorhandler(Exception)
    def default_error_handler(error):
        return {'message': str(error)}, getattr(error, 'code', 500)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
