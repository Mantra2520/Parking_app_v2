from celery import Celery
from celery.schedules import crontab

def make_celery():
    # Import here to avoid circular import
    from backend.app import create_app

    flask_app = create_app()

    celery = Celery(
        flask_app.import_name,
        broker="redis://localhost:6379/2",
        backend="redis://localhost:6379/3",
        include=["backend.tasks"]   # <-- ADD THIS
    )



    celery.conf.update(
        timezone="Asia/Kolkata",
        enable_utc=False,
        beat_schedule={
            "daily-reminder": {
                "task": "backend.tasks.send_daily_reminders",
                "schedule": crontab(hour=19, minute=0),
            },
            "inactive-users-reminder": {
                "task": "backend.tasks.send_inactive_user_reminders",
                "schedule": crontab(day_of_month=1, hour=8, minute=0),  
            },
            "monthly-user-report": {
                "task": "backend.tasks.send_monthly_activity_report",
                "schedule": crontab(day_of_month=1, hour=8, minute=0),  
            }
        }
    )

    # Attach Flask context to all tasks
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery_app = make_celery()
