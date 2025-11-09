from flask import Flask, jsonify
from flask_cors import CORS
# from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from routes.login import*
from routes.admin_home import *

from models.models import db, User, Role, Admin


def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SECRET_KEY'] = 'supersecret'
    app.config['SECURITY_PASSWORD_SALT'] = 'somesalt'
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False  
    app.config['WTF_CSRF_ENABLED'] = False  
    CORS(app)  

    db.init_app(app)

    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()

        if not Admin.query.filter_by(admin='admin').first():
            hashed_pw = generate_password_hash('admin123') 
            new_admin = Admin(admin='admin', password=hashed_pw)
            db.session.add(new_admin)
            db.session.commit()
        if not User.query.filter_by(userid='mantra').first():
            hashed_pw1 = generate_password_hash("mantra123")
            new_user = User(userid="mantra", fullname="Mantra Patel", email="mantra@example.com", password=hashed_pw1,address="hi",pincode=123456)
            db.session.add(new_user)
            db.session.commit()
            
    app.register_blueprint(login_bp, url_prefix="/")
    app.register_blueprint(admin_home_bp, url_prefix="/admin")



    @app.route("/main")
    def main():
        data = [
            {'name': "Mantra", 'age': 20},
            {'name': "Om", 'age': 26}
        ]
        return jsonify(data)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
