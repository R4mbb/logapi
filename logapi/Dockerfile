FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    uvicorn

RUN mkdir -p /logapi/logs
WORKDIR /logapi

COPY requirements.txt .
RUN pip install "fastapi[all]"
RUN pip install -r requirements.txt

COPY ./main.py /logapi
COPY ./log_etc/* /logapi/logs/

#ENTRYPOINT ["uvicorn", "main:app", "--reload"]

