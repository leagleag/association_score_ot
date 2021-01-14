FROM ubuntu:18.04

RUN useradd -rm -d /home/ubuntu -g root -G sudo -u 1001 myuser

USER myuser

WORKDIR /home/ubuntu

COPY --chown=myuser . /home/ubuntu

USER root

RUN apt-get update \
  && yes | apt-get install python3-pip \
  && pip3 install -r /home/ubuntu/requirements.txt

USER myuser

ENV PYTHONPATH "${PYTHONPATH}:/home/ubuntu"

ENTRYPOINT ["/usr/bin/python3", "/home/ubuntu/association_analysis/interface.py"]

CMD ["-h"]
