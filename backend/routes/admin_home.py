from flask import Blueprint,request,jsonify
from models.models import db,ParkingLot,ParkingSpot,ReserveParking

admin_home_bp = Blueprint('admin_home_bp',__name__)

@admin_home_bp.route("/home")
def admin_home():
    PL=[]
    lots=ParkingLot.query.all()
    for lot in lots:
        os=ParkingSpot.query.filter_by(lot_id=lot.lot_id,status='O').count()
        PL.append({"id":lot.lot_id,"os":os,"ms":lot.max_spots})
    return jsonify(PL),200

@admin_home_bp.route("/lot_details/<lotid>",methods=['GET'])
def lot_details(lotid):
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
    return jsonify({
        "lot_id": lot.lot_id,
        "prime_location_name": lot.prime_location_name,
        "price": lot.price,
        "address": lot.address,
        "pin_code": lot.pin_code,
        "max_spots": lot.max_spots,
        "occupidespot": os,
        "spots":s
    }), 200    

@admin_home_bp.route("/edit_parking/<lotid>",methods=['PUT'])
def edit_Parkinglot(lotid):
    data = request.get_json()
    lot = ParkingLot.query.filter_by(lot_id=lotid).first()
    if not lot:
        return jsonify({"error": "Lot not found"}), 404

    lot.address = data.get('address', lot.address)
    lot.price = data.get('price', lot.price)
    lot.prime_location_name = data.get('primelocation', lot.prime_location_name)
    lot.pin_code = data.get('pincode', lot.pin_code)
    lot.max_spots = data.get('maxspots', lot.max_spots)

    db.session.commit()
    return jsonify({"message": "Parking lot updated successfully"}), 200

@admin_home_bp.route('delete_parking/<lotid>', methods=['DELETE'])
def delete_parking(lotid):
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

@admin_home_bp.route('/add_parkinglot',methods=['POST'])
def add_parkinglot():
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
    
    return jsonify({"message": "Parking lot added successfully", "lot_id": lotid}), 201
