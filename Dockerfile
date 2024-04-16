FROM python:3

WORKDIR /usr/src/app

RUN git clone https://github.com/SuriyaKalivardhan/llm-runners.git .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "sleep", "infinity" ]