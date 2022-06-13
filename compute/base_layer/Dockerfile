FROM amazonlinux:2

RUN yum install -y amazon-linux-extras
RUN amazon-linux-extras | grep -i python
RUN amazon-linux-extras enable python3.8

RUN yum install -y python3.8 && \
    yum install -y zip && \
    yum clean all

RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install virtualenv

RUN python3.8 -m venv base
RUN source base/bin/activate

COPY requirements.txt .
RUN pip install -r requirements.txt -t ./python

RUN zip -r layer.zip ./python/
