FROM python:3.12
ADD . /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
