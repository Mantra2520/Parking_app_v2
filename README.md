# parking_app_v2

How to Run the Project
1. Start Backend

Install dependencies:

    pip install -r requirements.txt


Run Flask server:

    python backend/app.py

2. Start Redis Server

    Make sure Redis is running on default port (6379).

3. Start Celery Worker

    celery -A backend.celery_app.celery_app worker --loglevel=info

4. Start Celery Beat

    celery -A backend.celery_app.celery_app beat --loglevel=info

5. Start Frontend

Inside the frontend folder:

    npm install
    npm run dev
