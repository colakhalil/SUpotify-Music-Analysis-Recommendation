# TERMINAL COMMAND:
# docker-compose up -d --build

FROM python:3.9

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

# Any additional file to be copied into the container should be stated here such as:
# COPY library1.py /app

COPY app.py /app

CMD python app.py