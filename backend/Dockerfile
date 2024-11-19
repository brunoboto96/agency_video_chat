FROM python:3.10

WORKDIR /backend

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000", "--workers=3"]