from flask import Blueprint,request,jsonify
from backend.redis_clients import redis_auth,redis_cach
from backend.models.models import db,ParkingLot,ParkingSpot,ReserveParking,User,Admin
from datetime import *
import re
import json


admin_bp = Blueprint('admin_bp',__name__)


@admin_bp.route("/home")
def admin_home():
    
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached = redis_cach.get("admin:homepage")

    if cached:
        return jsonify(json.loads(cached))

    PL=[]
    lots=ParkingLot.query.all()
    for lot in lots:
        os=ParkingSpot.query.filter_by(lot_id=lot.lot_id,status='O').count()
        PL.append({"id":lot.lot_id,"os":os,"ms":lot.max_spots})
        
    redis_cach.set("admin:homepage", json.dumps(PL), ex=30)
    return jsonify(PL),200

@admin_bp.route("/lot_details/<lotid>",methods=['GET'])
def lot_details(lotid):
    
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached = redis_cach.get(f"admin:lotdetails:{lotid}")

    if cached:
        return jsonify(json.loads(cached))
    
    lot = ParkingLot.query.filter_by(lot_id=lotid).first()
    s=[]
    if not lot:
        return ({"error":"Parking Lot not found"}), 404
    
    spots = ParkingSpot.query.filter_by(lot_id=lotid).all()
    os=ParkingSpot.query.filter_by(lot_id=lot.lot_id,status='O').count()
    for spot in spots:
        sd={
        spot.spot_id:spot.status
        }
        s.append(sd)
        
    result={
        "lot_id": lot.lot_id,
        "prime_location_name": lot.prime_location_name,
        "price": lot.price,
        "address": lot.address,
        "pin_code": lot.pin_code,
        "max_spots": lot.max_spots,
        "occupidespot": os,
        "spots":s
    }
    
    redis_cach.set(f"admin:lotdetails:{lotid}", json.dumps(result), ex=120)
    return jsonify(result), 200    

@admin_bp.route("/edit_parking/<lotid>",methods=['PUT'])
def edit_Parkinglot(lotid):
    
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached = redis_cach.get(f"admin:lotdetails:{lotid}")
    if cached:
        redis_cach.delete(f"admin:lotdetails:{lotid}")
    
    data = request.get_json()
    lot = ParkingLot.query.filter_by(lot_id=lotid).first()
    if not lot:
        return jsonify({"error": "Lot not found"}), 404

    lot.address = data.get('address', lot.address)
    lot.price = data.get('price', lot.price)
    lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
    lot.pin_code = data.get('pin_code', lot.pin_code)

    db.session.commit()
    return jsonify({"message": "Parking lot updated successfully"}), 200

@admin_bp.route('delete_parking/<lotid>', methods=['DELETE'])
def delete_parking(lotid):
    
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached = redis_cach.get("admin:homepage")
    cached2 = redis_cach.get(f"admin:lotdetails:{lotid}")

    if cached:
        redis_cach.delete("admin:homepage")
    if cached2:
        redis_cach.delete(f"admin:lotdetails:{lotid}")
    
    dlso=ParkingSpot.query.filter_by(lot_id=lotid,status='O').first()
    if dlso:
        return jsonify({"message": "There are Reservations in the Parking Spot"}), 404
    else:
        dls=db.session.query(ParkingSpot).filter_by(lot_id=lotid).all()
        for i in dls:
            dres=ReserveParking.query.filter_by(spot_id=i.spot_id).all()
            for j in dres:
                db.session.delete(j)
            db.session.delete(i)
        db.session.commit()
        dl=db.session.query(ParkingLot).filter_by(lot_id=lotid).first()
        db.session.delete(dl)
        db.session.commit()
        return jsonify({"message": f"Parking lot {lotid} deleted successfully"}), 200

@admin_bp.route('/add_parkinglot',methods=['POST'])
def add_parkinglot():
    from backend.utils.emailer import send_email
    
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached = redis_cach.get("admin:homepage")

    if cached:
        redis_cach.delete("admin:homepage")
    
    data = request.get_json()
    
    lotid = data.get('lot_id')
    address = data.get('address')
    price = data.get('price')
    pl = data.get('pl')
    pc = data.get('pin_code')
    ms = data.get('max_spots')
    
    plot=ParkingLot.query.filter_by(lot_id=lotid).first()
    if plot:
        return jsonify({"error": f"Parking lot with ID {lotid} already exists"}), 400

    new_lot=ParkingLot(
        lot_id=lotid,
        address=address,
        price=price,
        prime_location_name=pl,
        pin_code=pc,
        max_spots=ms
    )
    db.session.add(new_lot)
    db.session.commit()

    for i in range(0,ms):
        sid=f"{lotid}{i+1}"
        new_spot=ParkingSpot(
            spot_id=sid,
            lot_id=lotid,
            status="A"
        )
        db.session.add(new_spot)
    db.session.commit()
    
    from backend.tasks import notify_users_new_lot
    notify_users_new_lot.delay(new_lot.lot_id,new_lot.address,new_lot.prime_location_name)
    
    return jsonify({"message": "Parking lot added successfully", "lot_id": lotid}), 201

@admin_bp.route('/spot_details/<spotid>', methods=["GET"])
def admin_spotsDetails(spotid):
    
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    spot=ParkingSpot.query.filter_by(spot_id=spotid).first()
    res=ReserveParking.query.filter_by(spot_id=spotid).filter(ReserveParking.out_time.is_(None)).first()
    data={
        "spotid":spot.spot_id,
        "lotid":spot.lot_id,
        "status":spot.status,
        "res_id":res.res_id,
        "userid":res.user_id,
        "vehicle_no":res.vehicle_no,
        "entry_date":res.in_date,
        "entry_time":res.in_time.strftime("%H:%M:%S") if res.in_time else 'N/A',
        "cost":res.cost_unit_time,
    }
    return jsonify(data), 200

@admin_bp.route('/users', methods=["GET"])
def admin_user():
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached=redis_cach.get("admin:users")
    if cached:
        return jsonify(json.loads(cached))
    
    users=User.query.all()
    ud=[]
    for user in users:
        res=ReserveParking.query.filter_by(user_id=user.userid).count()
        ud.append({"user_id":user.userid,
           "fname":user.fullname,
           "email":user.email,
           "address":user.address,
           "pincode":user.pincode,
           "res_count":res
           })
        
    redis_cach.set("admin:users", json.dumps(ud), ex=120)
    return jsonify(ud), 200

@admin_bp.route('/user/<userid>',methods=["GET"])
def admin_userRes(userid):
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    
    user=User.query.filter_by(userid=userid).first()
    res=ReserveParking.query.filter_by(user_id=userid).all()
    reservation=[]
    for r in res:
        spot=ParkingSpot.query.filter_by(spot_id=r.spot_id).first()
        lot=ParkingLot.query.filter_by(lot_id=spot.lot_id).first()
        reservation.append({
            "res_id":r.res_id,
            "address":lot.address,
            "spot_id":spot.spot_id,
            "vehicle_no":r.vehicle_no,
            "entry_date":r.in_date,
            "entry_time":r.in_time.strftime("%H:%M:%S") if r.in_time else 'N/A',
            "exit_time":r.out_time.strftime("%H:%M:%S") if r.out_time else 'N/A',
            "exit_date":r.out_date,
            "cost":r.cost_unit_time,
        })
    us={
        "userid":user.userid,
        "email":user.email,
        "reservations":reservation
    }
    return jsonify(us), 200

@admin_bp.route("/summary")
def AdminSummary():
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:
        return jsonify({"error": "Unauthorized"}), 403
    
    res = ReserveParking.query.filter(ReserveParking.out_time.isnot(None)).all()

    lotDetails = {}
    total_rev = 0

    # FIXED: Properly initialize dictionary without overwriting it
    lots = ParkingLot.query.all()
    for lot in lots:
        lotDetails[lot.lot_id] = {
            'lot_label': f"Lot {lot.lot_id}",
            'ava_count': 0,
            'occ_count': 0,
            'rev': 0
        }

    spots = ParkingSpot.query.all()

    # Count available & occupied spots
    for spot in spots:
        if spot.lot_id in lotDetails:   # safety check
            if spot.status == 'A':
                lotDetails[spot.lot_id]['ava_count'] += 1
            else:
                lotDetails[spot.lot_id]['occ_count'] += 1

    # Calculate revenue for each lot
    for r in res:
        in_datetime = datetime.combine(r.in_date, r.in_time)
        out_datetime = datetime.combine(r.out_date, r.out_time)
        hours = (out_datetime - in_datetime).total_seconds() / 3600
        revenue = round(r.cost_unit_time * hours, 2)

        s = ParkingSpot.query.get(r.spot_id)
        if s and s.lot_id in lotDetails:   # safety check
            lotDetails[s.lot_id]['rev'] += revenue

        total_rev += revenue

    # Final JSON response
    return jsonify({
        'total_rev': round(total_rev, 2),
        'lots': lotDetails
    })

    

@admin_bp.route("/search", methods=['POST'])
def smart_search():
    token = request.headers.get("Authorization")

    id = redis_auth.get(f"token:{token}")
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if Admin.query.filter_by(admin=id).first() is None:

        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    query = data.get("query", "").strip().upper()
    spot_pattern = re.compile(r"^[A-Z][0-9]+$")         # A12, B1, C44
    lot_pattern = re.compile(r"^[A-Z]$")                # A, B, C
    vehicle_pattern = re.compile(r"^[A-Z]{2}[0-9A-Z]{2,8}$")  # loose but safe

    if not query:
        return jsonify({"error": "Empty search input"}), 400

    # -------------------------
    # 1. RESERVATION ID SEARCH
    # -------------------------
    if query.isdigit():
        res = ReserveParking.query.filter_by(res_id=int(query)).first()
        if not res:
            return jsonify({"type": "none", "message": "No reservation found"})
        user = User.query.filter_by(userid=res.user_id).first()
        spot = ParkingSpot.query.filter_by(spot_id=res.spot_id).first()
        lot = ParkingLot.query.filter_by(lot_id=spot.lot_id).first()

        
        reservation_data = {
            "res_id": res.res_id,
            "spot_id": res.spot_id,
            "user_id": res.user_id,
            "vehicle_no": res.vehicle_no,
            "in_date": res.in_date.isoformat() if res.in_date else 'N/A',
            "out_date": res.out_date.isoformat() if res.out_date else 'N/A',
            "in_time": res.in_time.strftime("%H:%M:%S") if res.in_time else 'N/A',
            "out_time": res.out_time.strftime("%H:%M:%S") if res.out_time else 'N/A',
            "cost_unit_time": res.cost_unit_time
        }
        
        if user:
            user_data = {
                "userid": user.userid,
                "fullname": user.fullname,
                "email": user.email,
                "address": user.address,
                "pincode": user.pincode,
            }
        else:
            user_data= None

        if spot:
            spot_data = {
                "spot_id": spot.spot_id,
                "lot_id": spot.lot_id,
                "status": spot.status
            }
        else:
            spot_data= None
            
        if lot:
            lot_data = {
                "lot_id": lot.lot_id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "max_spots": lot.max_spots
            }

        else:
            lot_data= None
            
        return jsonify({
            "type": "reservation",
            "reservation": reservation_data,
            "user": user_data,
            "spot": spot_data,
            "lot": lot_data
        })

    # -------------------------
    # 2. SPOT ID SEARCH (A12)
    # -------------------------
    if spot_pattern.match(query):
        spot = ParkingSpot.query.filter_by(spot_id=query).first()
        if not spot:
            return jsonify({"type": "none", "message": "Spot not found"})

        lot = ParkingLot.query.filter_by(lot_id=spot.lot_id).first()
        res = ReserveParking.query.filter_by(spot_id=query).order_by(
            ReserveParking.res_id.desc()
        ).first()
        
        if spot:
            spot_data = {
                "spot_id": spot.spot_id,
                "lot_id": spot.lot_id,
                "status": spot.status
            }
        else:
            spot_data= None
            
        if lot:
            lot_data = {
                "lot_id": lot.lot_id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "max_spots": lot.max_spots
            }

        else:
            lot_data= None
            
        if res:
            reservation_data = {
                "res_id": res.res_id,
                "spot_id": res.spot_id,
                "user_id": res.user_id,
                "vehicle_no": res.vehicle_no,
                "in_date": res.in_date.isoformat() if res.in_date else 'N/A',
                "out_date": res.out_date.isoformat() if res.out_date else 'N/A',
                "in_time": res.in_time.strftime("%H:%M:%S") if res.in_time else 'N/A',
                "out_time": res.out_time.strftime("%H:%M:%S") if res.out_time else 'N/A',
                "cost_unit_time": res.cost_unit_time
            }

        else:
            reservation_data= None
        

        return jsonify({
            "type": "spot",
            "spot": spot_data,
            "lot": lot_data,
            "current_reservation": reservation_data
        })

    # -------------------------
    # 3. LOT ID SEARCH (A)
    # -------------------------
    if lot_pattern.match(query):
        lot = ParkingLot.query.filter_by(lot_id=query).first()
        if not lot:
            return jsonify({"type": "none", "message": "Lot not found"})
        
        if lot:
            lot_data = {
                "lot_id": lot.lot_id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "max_spots": lot.max_spots
            }

        else:
            lot_data= None

        return jsonify({
            "type": "lot",
            "lot": lot_data,
        })

    # -------------------------
    # 4. VEHICLE NUMBER SEARCH
    # -------------------------
    if any(c.isdigit() for c in query) and vehicle_pattern.match(query):
        ress = ReserveParking.query.filter(
            ReserveParking.vehicle_no.ilike(f"%{query}%")
        ).all()

        if not ress:
            return jsonify({"type": "none", "message": "No reservation with vehicle"})

        reservation_data=[]
        
        for res in ress:
            reservation_data.append({
                "res_id": res.res_id,
                "spot_id": res.spot_id,
                "user_id": res.user_id,
                "vehicle_no": res.vehicle_no,
                "in_date": res.in_date.isoformat() if res.in_date else 'N/A',
                "out_date": res.out_date.isoformat() if res.out_date else 'N/A',
                "in_time": res.in_time.strftime("%H:%M:%S") if res.in_time else 'N/A',
                "out_time": res.out_time.strftime("%H:%M:%S") if res.out_time else 'N/A',
                "cost_unit_time": res.cost_unit_time
            })

        return jsonify({
            "type": "vehicle",
            "reservations": reservation_data
        })

    # -------------------------
    # 5. USER SEARCH (default)
    # -------------------------
    user = User.query.filter((User.userid.ilike(f"%{query}%")) | (User.fullname.ilike(f"%{query}%"))).first()

    if user:
        ress = ReserveParking.query.filter_by(user_id=user.userid).all()
        
        user_data = {
            "userid": user.userid,
            "fullname": user.fullname,
            "email": user.email,
            "address": user.address,
            "pincode": user.pincode,
        }
        
        reservation_data=[]
        
        for res in ress:
            reservation_data.append({
                "res_id": res.res_id,
                "spot_id": res.spot_id,
                "user_id": res.user_id,
                "vehicle_no": res.vehicle_no,
                "in_date": res.in_date.isoformat() if res.in_date else 'N/A',
                "out_date": res.out_date.isoformat() if res.out_date else 'N/A',
                "in_time": res.in_time.strftime("%H:%M:%S") if res.in_time else 'N/A',
                "out_time": res.out_time.strftime("%H:%M:%S") if res.out_time else 'N/A',
                "cost_unit_time": res.cost_unit_time
            })

        return jsonify({
            "type": "user",
            "user": user_data,
            "reservations": reservation_data
        })

    # -------------------------
    # 6. PRIME LOCATION SEARCH (last fallback)
    # -------------------------
    lots = ParkingLot.query.filter(
        ParkingLot.prime_location_name.ilike(f"%{query}%")
    ).all()

    if lots:
        
        lot_data =[]
        
        for lot in lots:
            lot_data.append({
                "lot_id": lot.lot_id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "max_spots": lot.max_spots
            })
        
        return jsonify({
            "type": "location",
            "lots": lot_data
        })

    # -------------------------
    # 7. NOTHING FOUND
    # -------------------------
    return jsonify({"type": "none", "message": "No match found"})
