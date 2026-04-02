FROM python:3.11

WORKDIR /app

COPY . .

# تثبيت FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# تثبيت المكتبات
RUN pip install -r requirements.txt

CMD ["python","Dowlod.py"]
