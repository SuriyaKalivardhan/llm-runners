FROM python:3

RUN apt update -y; apt install vim -y
WORKDIR /usr/src/app

RUN git clone https://github.com/SuriyaKalivardhan/llm-runners.git .
RUN git fetch -p
RUN git pull
RUN pip install --no-cache-dir -r requirements.txt