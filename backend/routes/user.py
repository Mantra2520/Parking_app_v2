from flask import Blueprint,request,jsonify,send_file
from backend.models.models import db,ParkingLot,ParkingSpot,ReserveParking,User,Admin
from datetime import datetime, timedelta
from backend.redis_clients import redis_auth,redis_cach
import json
import os



user_bp=Blueprint('user_bp',__name__)


@user_bp.route("/export/csv/<userid>", methods=["POST"])
def export_csv(userid):
    from backend.tasks import export_bookings_csv

    task = export_bookings_csv.delay(userid)

    return jsonify({
        "message": "Export started",
        "task_id": task.id
    }), 202

@user_bp.route("/export/csv/status/<task_id>", methods=["GET"])
def csv_export_status(task_id):
    from backend.celery_app import celery_app
    result = celery_app.AsyncResult(task_id)

    if result.state == "PENDING":
        return jsonify({"state": "PENDING"}), 202

    if result.state == "SUCCESS":
        file_path = result.result["file_path"].replace("\\", "/")

        return jsonify({
            "state": "SUCCESS",
            "file_url": f"http://127.0.0.1:5000/user/export/download?path={file_path}"
        }), 200

    return jsonify({
        "state": result.state,
        "error": str(result.result)
    }), 500

import os
from flask import send_file, jsonify, request

@user_bp.route("/export/download", methods=["GET"])
def download_csv():
    file_path = request.args.get("path")

    if not file_path:
        return jsonify({"error": "Missing file path"}), 400
    
    LEVEL_1 = os.path.dirname(os.path.abspath(__file__))
    LEVEL_2 = os.path.dirname(LEVEL_1)
    BASE_DIR = os.path.dirname(LEVEL_2)

    EXPORT_DIR = os.path.join(BASE_DIR, "exports")


    filename = os.path.basename(file_path)
    safe_path = os.path.join(EXPORT_DIR, filename)


    if not os.path.exists(safe_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(
        safe_path,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )



@user_bp.route('/home/<userid>',methods=['GET'])
def user_home(userid):
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if  userid != id:
        return jsonify({"error": "Unauthorized"}), 403
    
    cached=redis_cach.get(f"user:home:{userid}")
    if cached:
        return jsonify(json.loads(cached))
    
    pov=ReserveParking.query.filter_by(user_id=userid).filter(ReserveParking.out_time.is_(None)).all()
    parkedV=[]
    for res in pov:
        spot=ParkingSpot.query.get(res.spot_id)
        lot=ParkingLot.query.get(spot.lot_id)
        parkedV.append({
            "res_id":res.res_id,
            "address":lot.address,
            "spot_id":spot.spot_id,
            "vehicle_no":res.vehicle_no,
            "entry_date": res.in_date.isoformat() if res.in_date else None,
            "exit_date": res.out_date.isoformat() if res.out_date else None,
            "entry_time":res.in_time.strftime("%H:%M:%S") if res.in_time else None,
            "exit_time":res.out_time.strftime("%H:%M:%S") if res.out_time else None,
        })
    
    lpv=ReserveParking.query.filter(ReserveParking.user_id == userid, ReserveParking.out_time.isnot(None)).order_by(ReserveParking.res_id.desc()).first()

    lastParkedV=None
    if lpv:
        spot=ParkingSpot.query.get(lpv.spot_id)
        lot=ParkingLot.query.get(spot.lot_id)
        lastParkedV={
            "res_id":lpv.res_id,
            "address":lot.address,
            "spot_id":spot.spot_id,
            "vehicle_no":lpv.vehicle_no,
            "entry_date":lpv.in_date.isoformat() if lpv.in_date else None,
            "exit_date":lpv.out_date.isoformat() if lpv.out_date else None,
            "entry_time":lpv.in_time.strftime("%H:%M:%S") if lpv.in_time else None,
            "exit_time":lpv.out_time.strftime("%H:%M:%S") if lpv.out_time else None,
        }
        
    result={
        "userid": userid,
        "active_reservations": parkedV,
        "last_reservation": lastParkedV
    }
    redis_cach.set(f"user:home:{userid}", json.dumps(result), ex=30)
    return jsonify(result), 200
    
    
@user_bp.route('/home/search',methods=['POST'])
def userHomeSearch():
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json() or {}
    search_term = data.get("s", "").strip()

    ps = ParkingLot.query.filter(ParkingLot.pin_code.like(f"%{search_term}%")).all()
    ls = ParkingLot.query.filter(ParkingLot.prime_location_name.like(f"%{search_term}%")).all()

    lots = ps if ps else ls if ls else []
    search_results = []
    for l in lots:
        spot = ParkingSpot.query.filter_by(lot_id=l.lot_id, status="A").first()
        search_results.append({
            "lot_id": l.lot_id,
            "prime_location_name": l.prime_location_name,
            "address": l.address,
            "pin_code": l.pin_code,
            "price": l.price,
            "max_spots": l.max_spots,
            "available": bool(spot),
            "spot_id": spot.spot_id if spot else None
        })
        
    return jsonify({
        "search_results": search_results,
    }), 200
    
@user_bp.route('/summary/<userid>',methods=["GET"])
def user_summary(userid):
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if  userid != id:
        return jsonify({"error": "Unauthorized"}), 403
    
    active_reservations = ReserveParking.query.filter_by(user_id=userid).filter(
        ReserveParking.out_time.is_(None)
    ).order_by(ReserveParking.res_id.desc()).all()

    active_data = []
    for res in active_reservations:
        spot = ParkingSpot.query.get(res.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        active_data.append({
            "res_id": res.res_id,
            "spot_id": res.spot_id,
            "lot_id": spot.lot_id,
            "address": lot.address,
            "vno":res.vehicle_no,
            "prime_location_name": lot.prime_location_name,
            "entry_date": res.in_date.isoformat() if res.in_date else None,
            "entry_time": res.in_time.strftime("%H:%M:%S") if res.in_time else None
        })

    past_reservations = ReserveParking.query.filter(
        ReserveParking.user_id == userid,
        ReserveParking.out_time.isnot(None)
    ).order_by(ReserveParking.res_id.desc()).all()

    past_data = []
    total_minutes = 0
    total_money = 0
    lot_names = []

    for res in past_reservations:
        spot = ParkingSpot.query.get(res.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        lot_names.append(lot.prime_location_name)

        # Find available spot (if any)
        free_spot = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status="A").first()

        # Duration + cost
        in_dt = datetime.combine(res.in_date, res.in_time)
        out_dt = datetime.combine(res.out_date, res.out_time)

        duration = out_dt - in_dt
        minutes = duration.total_seconds() / 60
        total_minutes += minutes

        time_units = minutes / 60
        cost = time_units * res.cost_unit_time
        total_money += cost

        past_data.append({
            "res_id": res.res_id,
            "lot_id": lot.lot_id,
            "address": lot.address,
            "prime_location_name": lot.prime_location_name,
            "in_date":res.in_date.isoformat() if res.in_date else None,
            "in_time": res.in_time.strftime("%H:%M:%S") if res.in_time else None,
            "out_date":  res.out_date.isoformat() if res.out_date else None,
            "out_time": res.out_time.strftime("%H:%M:%S") if res.in_time else None,
            "vno": res.vehicle_no,
            "duration_minutes": int(minutes),
            "cost": round(cost, 2),
            "available_spots":free_spot.spot_id if free_spot else "0"
        })

    total_hours = int(total_minutes / 60)
    most_used_lot = max(set(lot_names), key=lot_names.count) if lot_names else None

    result={"userid": userid,
        "active_reservations": active_data,
        "past_reservations": past_data,
        "stats": {
            "total_completed": len(past_reservations),
            "total_hours": total_hours,
            "total_money": round(total_money, 2),
            "most_used_lot": most_used_lot
        }}
    
    return jsonify(result), 200


@user_bp.route('/profile/<userid>', methods=["GET", "PUT"])
def user_profile(userid):
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if  userid != id:
        return jsonify({"error": "Unauthorized"}), 403

    if request.method == "GET":
        userData = {
            "userid": user.userid,
            "fullname": user.fullname,
            "email": user.email,
            "address": user.address,
            "pincode": user.pincode
        }
        return jsonify(userData)

    if request.method == "PUT":
        data = request.get_json()

        user.fullname = data.get('fullname', user.fullname)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)
        user.pincode = data.get('pincode', user.pincode)

        db.session.commit()

        return jsonify({"message": "User profile updated successfully"})

@user_bp.route('/booking/<userid>/<lotid>',methods=['GET','POST'])
def userBooking(userid,lotid):
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if  userid != id:
        return jsonify({"error": "Unauthorized"}), 403
    
    redis_cach.delete(f"user:home:{userid}")
    redis_cach.delete("admin_homepage")
    redis_cach.delete(f"admin_lotdetails:{lotid}")
    redis_cach.delete("admin_users")
    
    if request.method == 'GET':
        lot = ParkingLot.query.filter_by(lot_id=lotid).first()
        spot = ParkingSpot.query.filter_by(lot_id=lotid, status="A").first()

        if not spot:
            return jsonify({"error": "No available spots"}), 404

        return jsonify({
            "lotid": lotid,
            "spotid": spot.spot_id,
            "userid": userid,
            "location": lot.address,
            "price": lot.price
        })
    elif request.method == 'POST':
        data=request.get_json()
        
        vno=data.get("vno").strip()
        atime=data.get("intime").strip()
        adate=data.get("indate").strip()
        spotid=data.get("spotid").strip()
        format_string = "%Y-%m-%d"
        date_object = datetime.strptime(adate, format_string)
        time_string = atime+":00"
        format_code = "%H:%M:%S"
        time_object = datetime.strptime(time_string, format_code)
        
        now=time_object
        intime = now.replace(second=0, microsecond=0).time()
        date=date_object
        
        lot=ParkingLot.query.filter_by(lot_id=lotid).first()
        cost=lot.price
        
        reservation = ReserveParking(spot_id=spotid,user_id=userid,vehicle_no=vno,in_date=date,in_time=intime,cost_unit_time=cost)
        
        db.session.add(reservation)
        spot=ParkingSpot.query.get(spotid)
        spot.status="O"
        db.session.commit()
        
        return jsonify({"message":"Reservation Conformed"}),200
    
@user_bp.route('/release/<userid>/<resid>',methods=['GET'])
def UserRelease(userid,resid):
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if  userid != id:
        return jsonify({"error": "Unauthorized"}), 403
    
    redis_cach.delete(f"user:home:{userid}")
    redis_cach.delete("admin_homepage")
    redis_cach.delete("admin_users")
    
    res=ReserveParking.query.filter_by(res_id=resid).first()       
    spot=ParkingSpot.query.filter_by(spot_id=res.spot_id).first()
    lot=ParkingLot.query.filter_by(lot_id=spot.lot_id).first()
        
    redis_cach.delete(f"admin_lotdetails:{lot.lot_id}")
    return jsonify({
        "resid":resid,
        "spotid":spot.spot_id,
        "lotid":lot.lot_id,
        "userid":userid,
        "loc":lot.address,
        "vno":res.vehicle_no,
        "price":res.cost_unit_time,
    })
        
@user_bp.route('/payment/<userid>/<resid>',methods=['GET'])
def UserPayment(userid,resid):
    
    token = request.headers.get("Authorization")
    
    id = redis_auth.get(f"token:{token}")
    
    if not id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(userid=id).first()
    if  userid != id:
        return jsonify({"error": "Unauthorized"}), 403
    
    now = datetime.now()
    outtime=now.replace(second=0, microsecond=0).time()
    out_date=now.date()
    res=ReserveParking.query.get(resid)
    res.out_date=out_date
    res.out_time=outtime
    spot = ParkingSpot.query.get(res.spot_id)
    spot.status = "A"

    db.session.commit()
        
    lot=ParkingLot.query.filter_by(lot_id=spot.lot_id).first()

    in_datetime = datetime.combine(res.in_date, res.in_time)
    out_datetime = datetime.combine(out_date, outtime)
    hours = (out_datetime - in_datetime).total_seconds() / 3600
    cost = res.cost_unit_time * hours
        
    return jsonify({
        "resid":resid,
        "userid":userid,
        "loc":lot.address,
        "vno":res.vehicle_no,
        "in_date": res.in_date.strftime("%Y-%m-%d"),
        "in_time": res.in_time.strftime("%H:%M:%S") if res.in_time else None,
        "out_date": res.out_date.strftime("%Y-%m-%d"),
        "out_time": res.out_time.strftime("%H:%M:%S") if res.in_time else None,
        "dur":hours,
        "cost":cost
    })
