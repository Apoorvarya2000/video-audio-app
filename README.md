🎬 Video-to-Audio Microservices App on Kubernetes (Minikube + AWS S3)

A production-style DevOps project built using Python microservices, Docker, Kubernetes (Minikube), AWS S3, and WSL Ubuntu.
This project takes a video file, extracts its audio using FFmpeg, and uploads the audio file to Amazon S3.

🚀 Project Architecture
User → Video Service → Shared Volume → Audio Service → S3 Bucket

Components
Component	Tech	Description
Video Service	Python + Flask	Accepts video upload and stores it in shared directory
Audio Service	Python + Flask + FFmpeg	Extracts audio and uploads MP3 to S3
Storage	Kubernetes PVC	Used for sharing files between services
Docker	Containerization	Builds microservice images
Kubernetes	Deployments + Services	Runs and exposes microservices
AWS S3	Cloud Storage	Stores the extracted audio
WSL + Minikube	Local Kubernetes Cluster	Development/testing environment
🛠️ Tech Stack

Python (Flask)

FFmpeg

Docker

Kubernetes (Minikube)

AWS S3

WSL Ubuntu

NodePort / Minikube Service

PVC + PV (Kubernetes)

📁 Project Structure
video-audio-app/
│
├── video-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── audio-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── k8s/
│   ├── video-deployment.yaml
│   ├── audio-deployment.yaml
│   ├── video-service.yaml
│   ├── audio-service.yaml
│   └── shared-storage.yaml
│
└── README.md

🔧 How to Run Locally (Complete Steps)
1. Start Minikube
minikube start --driver=docker

2. Enable Docker inside Minikube
eval $(minikube docker-env)

3. Build Docker images
docker build -t video-service:1.0 ./video-service
docker build -t audio-service:1.0 ./audio-service

4. Apply Kubernetes manifests
kubectl apply -f k8s/shared-storage.yaml
kubectl apply -f k8s/video-deployment.yaml
kubectl apply -f k8s/audio-deployment.yaml
kubectl apply -f k8s/video-service.yaml
kubectl apply -f k8s/audio-service.yaml

5. Provide AWS Credentials
kubectl create secret generic aws-secret \
  --from-literal=AWS_ACCESS_KEY_ID=XXXX \
  --from-literal=AWS_SECRET_ACCESS_KEY=YYYY

6. Expose Video Service
minikube service video-service --url

7. Upload a Video File
curl -X POST <URL_FROM_MINIKUBE> \
  -F "file=@/path/to/video.mp4"


Response Example:

{
  "video_path": "/data/videos/sample.mp4",
  "audio_response": {
    "local_path": "/data/audio/sample.mp3",
    "s3_url": "https://my-bucket.s3.amazonaws.com/..."
  }
}

🎧 Output

✔ Audio extracted using FFmpeg
✔ MP3 saved in PVC shared storage
✔ File uploaded to AWS S3
✔ Public URL returned to the user
