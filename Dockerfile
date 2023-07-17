# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /
ENV FLASK_APP=waiter.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
EXPOSE 80
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/JaidedAI/EasyOCR.git
COPY . .
CMD ["flask", "--app", "waiter", "run", "--host=0.0.0.0"]
