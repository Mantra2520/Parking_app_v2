from flask import Blueprint, request, jsonify
from models.models import db, User, Role, Admin
from werkzeug.security import check_password_hash,generate_password_hash
import secrets

login_bp = Blueprint('login_bp', __name__)

# For now use an in-memory token dict (later move to Redis)
active_admin_tokens = {}
active_user_tokens = {}

@login_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    uid = data.get('userid')
    password = data.get('password')

    admin = Admin.query.filter_by(admin=uid).first()
    user = User.query.filter_by(userid=uid).first()
    
    # if not admin:
    #     if not user:
    #         return jsonify({"error": "userid not found Please Singup"}), 404
    if admin:
        if check_password_hash(admin.password, password):
            token = secrets.token_hex(16)
            active_admin_tokens[token] = admin.id
            return jsonify({"token": token, "admin_id": admin.id,"role":"admin"})
        else:
            return jsonify({"error": "Wrong password, Please try again."})
        
    elif user:
        if check_password_hash(user.password, password):
            token = secrets.token_hex(16)
            active_user_tokens[token] = user.userid
            return jsonify({
                "token": token,
                "userid": user.userid,
                "role":"user"
            }), 200
        else:
            return jsonify({"error": "Wrong password, Please try again."})
            
    else:
        return jsonify({"error": "userid not found Please Singup"}), 404



@login_bp.route('/singup', methods=['POST'])
def user_singup():
    data = request.get_json()
    
    uid=data.get('userid')
    fulln=data.get('fullname')
    em=data.get('email')
    pas=data.get('password')
    ad=data.get('address')
    pc=data.get('pincode')
    
    if User.query.filter_by(userid=uid).first():
        return jsonify({"error": "User ID already exists"}), 400

    if User.query.filter_by(email=em).first():
        return jsonify({"error": "Email already registered"}), 400
    
    hasspass= generate_password_hash(pas)
    
    new_user = User(
        userid=uid,
        fullname=fulln,
        email=em,
        password=hasspass,
        address=ad,
        pincode=pc
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"messsage":"User registered sucessfully"}), 201


