FROM python:3.11
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
