FROM tiangolo/uvicorn-gunicorn:python3.10

LABEL maintainer="Fat Plants MU <fatplantsmu@gmail.com>"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
# RUN apt install libgl1-mesa-glx
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Set environment variables
ENV place=docker
ENV CORS_ALLOW_ORIGINS="https://fatplants.net"

COPY . /app

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000","--ssl-certfile","auth_docker/fullchain.pem","--ssl-keyfile","auth_docker/privkey.pem"]