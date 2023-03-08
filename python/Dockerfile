FROM python:3.9-alpine
WORKDIR /app
COPY api.py auth.py db.py model.py networking.py userservice.py requirements.txt ./
RUN pip install -r requirements.txt
# App must run on port 8000
ENTRYPOINT ["sh","-c", "gunicorn --bind=0.0.0.0:${APP_PORT} ${APP_MODULES}"]
