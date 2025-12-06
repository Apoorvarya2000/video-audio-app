FROM python:3.10-slim
WORKDIR /app

# install ffmpeg and dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
RUN mkdir -p /data/videos /data/audio
EXPOSE 5001
CMD ["python", "app.py"]
