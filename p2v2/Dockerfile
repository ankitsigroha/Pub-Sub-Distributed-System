FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN mkdir /home/phase2
COPY . /home/phase2
WORKDIR /home/phase2
RUN ls
RUN chmod +x phase2.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["phase2.py"]