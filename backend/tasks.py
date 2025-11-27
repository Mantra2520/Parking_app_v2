# backend/tasks.py
import csv
import os
from backend.utils.emailer import send_email,send_email_html
from backend.models.models import User,ReserveParking,ParkingLot,ParkingSpot  # if needed
from datetime import datetime, timedelta
from backend.redis_clients import redis_auth

from backend.celery_app import celery_app


# DAILY REMINDER TASK
@celery_app.task
def send_daily_reminders():
    print("Running daily reminder task...")

    users = User.query.all()
    now = datetime.now().date()
    two_days_later = now + timedelta(days=2)


    for user in users:

        # UPCOMING BOOKING REMINDER (in 2 days)
        upcoming = ReserveParking.query.filter(
            ReserveParking.user_id == user.userid,
            ReserveParking.in_date.between(now, two_days_later)
        ).first()


        if upcoming:
            body = (
                f"Hi {user.fullname},\n\n"
                f"You have a booking on {upcoming.in_date} at {upcoming.in_time}.\n"
                f"This is a reminder in advance.\n\n"
                "Parking App"
            )
            send_email(user.email, "Upcoming Booking Reminder", body)
            continue

    return {"status": "done"}

@celery_app.task
def notify_users_new_lot(lot_id,add,pl):
    from backend.models.models import User, ParkingLot
    from backend.utils.emailer import send_email

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return {"error": "Lot not found"}

    users = User.query.all()
    count = 0

    for user in users:
        body = (
            f"Hello {user.fullname},\n\n"
            f"A new parking lot has been added at {pl}.\n"
            f"Address: {add}.\n"
            "Book your spot now!"
        )
        send_email(user.email, "New Parking Lot Added!", body)
        count += 1

    return {"status": "done", "emails_sent": count}

@celery_app.task
def send_inactive_user_reminders():

    now = datetime.now().date()
    sixty_days_ago = now - timedelta(days=60)
    THROTTLE_DAYS = 30  # remind once every 30 days

    users = User.query.all()
    sent = 0

    for user in users:
        # 1. Get last booking
        last_booking = ReserveParking.query.filter_by(user_id=user.userid)\
                            .order_by(ReserveParking.in_date.desc()).first()

        # Determine inactivity
        if not last_booking:
            inactive = True
        else:
            inactive = last_booking.in_date < sixty_days_ago

        if not inactive:
            continue

        # 2. Check Redis throttle
        key = f"inactive:reminder:user:{user.userid}"
        last_sent = redis_auth.get(key)

        if last_sent:
            last_sent_date = datetime.strptime(last_sent, "%Y-%m-%d").date()
            if (now - last_sent_date).days < THROTTLE_DAYS:
                continue  # skip, reminder sent recently

        # 3. Send reminder email
        send_email(
            user.email,
            "We miss you at ParkingApp!",
            f"Hi {user.fullname},\n\n"
            "You haven't booked a spot in the last two months.\n"
            "Visit the app to make your next booking.\n\n"
            "Parking App"
        )

        # 4. Update Redis time
        redis_auth.set(key, now.strftime("%Y-%m-%d"))

        sent += 1

    return {"status": "done", "sent": sent}


# MONTHLY REPORT TASK
@celery_app.task
def send_monthly_activity_report():
    from backend.models.models import User, ReserveParking
    from backend.utils.emailer import send_email
    from datetime import datetime

    now = datetime.now()

    current_month_start = now.replace(day=1)
    pmonth_end = current_month_start - timedelta(days=1)
    pmonth_start = pmonth_end.replace(day=1)

    month_name = pmonth_start.strftime("%B %Y")

    users = User.query.all()
    sent = 0

    for user in users:
        bookings = ReserveParking.query.filter(
            ReserveParking.user_id == user.userid,
            ReserveParking.in_date >= pmonth_start.date(),
            ReserveParking.out_time.isnot(None)
        ).all()
        if not bookings:
            continue
        
        total_booking=len(bookings)
        total_money=0
        total_minutes=0
        lot_names=[]
        rows_html = ""
        
        for res in bookings:
            spot = ParkingSpot.query.get(res.spot_id)
            lot = ParkingLot.query.get(spot.lot_id)
            lot_names.append(lot.prime_location_name)
            
            in_dt = datetime.combine(res.in_date, res.in_time)
            out_dt = datetime.combine(res.out_date, res.out_time)

            duration = out_dt - in_dt
            minutes = duration.total_seconds() / 60
            total_minutes += minutes

            time_units = minutes / 60
            cost = time_units * res.cost_unit_time
            total_money += cost
            rows_html += f"""
            <tr>
                <td style="padding:8px; border:1px solid #ddd;">{res.res_id}</td>
                <td style="padding:8px; border:1px solid #ddd;">{lot.address}</td>
                <td style="padding:8px; border:1px solid #ddd;">{res.vehicle_no}</td>
                <td style="padding:8px; border:1px solid #ddd;">{res.in_date}</td>
                <td style="padding:8px; border:1px solid #ddd;">{res.in_time}</td>
                <td style="padding:8px; border:1px solid #ddd;">{res.out_date}</td>
                <td style="padding:8px; border:1px solid #ddd;">{res.out_time}</td>
                <td style="padding:8px; border:1px solid #ddd;">₹{int(cost)}</td>
            </tr>
            """
        
        total_hours = int(total_minutes / 60)
        most_used_lot = max(set(lot_names), key=lot_names.count) if lot_names else None
        
        table_html = f"""
        <table style="width:100%; border-collapse: collapse; font-family: Arial, sans-serif;">
            <thead>
                <tr style="background:#f2f2f2; text-align:left;">
                    <th style="padding:8px; border:1px solid #ddd;">ID</th>
                    <th style="padding:8px; border:1px solid #ddd;">Location</th>
                    <th style="padding:8px; border:1px solid #ddd;">Vehicle No.</th>
                    <th style="padding:8px; border:1px solid #ddd;">Entry Date</th>
                    <th style="padding:8px; border:1px solid #ddd;">Entry Time</th>
                    <th style="padding:8px; border:1px solid #ddd;">Exit Date</th>
                    <th style="padding:8px; border:1px solid #ddd;">Exit Time</th>
                    <th style="padding:8px; border:1px solid #ddd;">Cost</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
        
        html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    .container {{
                        font-family: Arial, sans-serif;
                        background: #f7f7f7;
                        padding: 20px;
                        border-radius: 10px;
                    }}
                    h2 {{
                        color: #4a4a4a;
                    }}
                    .box {{
                        background: white;
                        padding: 15px;
                        margin-top: 10px;
                        border-left: 4px solid #4CAF50;
                        border-radius: 5px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #333;
                    }}
                    .value {{
                        color: #555;
                    }}
                    .footer {{
                        margin-top: 25px;
                        font-size: 12px;
                        color: #777;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Your Monthly Parking Report — {month_name}</h2>

                    <div class="box">
                        <p><span class="label">Total Bookings:</span>
                        <span class="value">{total_booking}</span></p>
                        <p><span class="label">Most Used Parking Lot:</span>
                        <span class="value">{most_used_lot}</span></p>
                        <p><span class="label">Total Amount Spent:</span>
                        <span class="value">₹{round(total_money,2)}</span></p>
                        <p><span class="label">Total Time Spent:</span>
                        <span class="value">{total_hours}</span></p>
                    </div>

                    <h3>Bookings</h3>
                    <div>
                        <p>{table_html}</p>
                    </div>

                    <p class="footer">
                        This is an automated monthly summary generated by Parking App.
                    </p>
                </div>
            </body>
            </html>
            """

        send_email_html(
            user.email,
            f"Your Monthly Parking Report – {month_name}",
            html_content
        )

        sent += 1

    return {"status": "done", "reports_sent": sent}


# CSV EXPORT TASK (ASYNC)
@celery_app.task
def export_bookings_csv(user_id):
    EXPORT_DIR = "exports"
    os.makedirs(EXPORT_DIR, exist_ok=True)

    filename = os.path.join(
        EXPORT_DIR,
        f"user_{user_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    bookings = ReserveParking.query.filter_by(user_id=user_id).all()

    if not bookings:
        return {"status": "error", "message": "No bookings found."}

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "reservation_id", "user_id", "lot_name", "spot_id",
            "in_date", "in_time", "out_date", "out_time",
            "duration_minutes", "cost"
        ])

        for b in bookings:
            if b.out_date:
                spot = ParkingSpot.query.get(b.spot_id)
                lot = ParkingLot.query.get(spot.lot_id)

                in_dt = datetime.combine(b.in_date, b.in_time)
                out_dt = datetime.combine(b.out_date, b.out_time)

                duration = (out_dt - in_dt).total_seconds() / 60
                cost = (duration / 60) * b.cost_unit_time

            writer.writerow([
                b.res_id,
                b.user_id,
                lot.prime_location_name,
                b.spot_id,
                b.in_date.isoformat() if b.in_date else "N/A",
                b.in_time.strftime("%H:%M:%S") if b.in_time else "N/A",
                b.out_date.isoformat() if b.out_date else "N/A",
                b.out_time.strftime("%H:%M:%S") if b.out_time else "N/A",
                int(duration),
                round(cost, 2) if b.out_date else "N/A",
            ])

    return {
        "status": "success",
        "file_path": filename
    }