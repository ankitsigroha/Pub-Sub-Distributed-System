FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN mkdir /home/app
COPY . /home/app
WORKDIR /home/app
RUN ls
RUN chmod +x run.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]