from backend.celery_app import celery_app

# Celery uses this "app" variable as the worker application
app = celery_app

if __name__ == "__main__":
    app.start()
