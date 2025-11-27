from flask import Flask, jsonify
from flask_cors import CORS
# from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from backend.routes.login import login_bp
from backend.routes.user import user_bp
from backend.routes.admin import admin_bp

from backend.models.models import db, Admin



def create_app():
    app = Flask(__name__)
    CORS(app, 
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        expose_headers=["Authorization"],
        allow_headers=["Content-Type", "Authorization"]
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SECRET_KEY'] = 'supersecret'
    app.config['SECURITY_PASSWORD_SALT'] = 'somesalt'
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False  
    app.config['WTF_CSRF_ENABLED'] = False

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
          
    app.register_blueprint(login_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,port=5000)
