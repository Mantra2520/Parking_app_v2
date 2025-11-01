from flask import Flask, jsonify  # ✅ added jsonify
from flask_cors import CORS
from models.models import db, User, Admin, ParkingLot, ParkingSpot, ReserveParking


def create_app():
    app = Flask(__name__)
    
    CORS(app,origins="*")
    
    return app

app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'

db.init_app(app)

with app.app_context():
    db.create_all()

    if not Admin.query.filter_by(admin='admin').first():
        new_admin = Admin(admin='admin', password = 'admin123')
        db.session.add(new_admin)
        db.session.commit()

p = [
    {'name': "Mantra", 'age': 20},
    {'name': "Om", 'age': 26}
]

@app.route("/main")
def main():
    return jsonify(p)  # ✅ returns JSON response

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
