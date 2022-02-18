FROM python:3.9-slim

RUN mkdir opt/wigeon
COPY wigeon opt/wigeon
COPY setup.py opt/setup.py
COPY requirements.txt opt/requirements.txt
COPY README.md opt/README.md
WORKDIR opt
RUN ls
RUN python setup.py install
