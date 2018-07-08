# Pulls base image
FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Copy app data
COPY . /project
WORKDIR /project

# Install Python packages
RUN pip install -r requirements.txt

EXPOSE 5005

# Start server
CMD gunicorn --worker-class eventlet --access-logfile - --reload -b 0.0.0.0:5005 manage:app
