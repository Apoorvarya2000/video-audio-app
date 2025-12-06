🎬 Video-to-Audio Microservices App (Docker + Kubernetes + AWS S3)

Convert any uploaded video file into MP3 audio using a fully containerized microservices architecture deployed on Kubernetes (Minikube) and storing output on AWS S3.

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


🚀 Architecture Overview
🧩 Microservices
Service	Purpose
video-service	Accepts video upload → saves it → calls audio-service
audio-service	Extracts MP3 using FFmpeg → uploads to S3
🔗 Communication
Client → video-service → audio-service → AWS S3

📦 Storage

Shared Persistent Volume (PV + PVC) between both services

Used to share uploaded video files

☁️ Cloud

Output MP3 uploaded to AWS S3 Bucket

🛠️ Tech Stack
Component	Technology
Backend	Python + Flask
Audio Extraction	FFmpeg
Containers	Docker
Orchestration	Kubernetes (Minikube)
Cloud Storage	AWS S3
OS	WSL Ubuntu
🔧 How to Run Locally
1️⃣ Start Minikube
minikube start --driver=docker

2️⃣ Build Docker images inside Minikube
eval $(minikube docker-env)

cd video-service
docker build -t video-service:1.0 .

cd ../audio-service
docker build -t audio-service:1.0 .

3️⃣ Apply Kubernetes manifests
cd ~/video-audio-app/k8s
kubectl apply -f shared-storage.yaml
kubectl apply -f video-deployment.yaml
kubectl apply -f audio-deployment.yaml
kubectl apply -f video-service.yaml
kubectl apply -f audio-service.yaml


Check pods:

kubectl get pods

🌩️ AWS S3 Setup

Create bucket:

aws s3 mb s3://my-video-audio-bucket --region ap-south-1


Create secret:

kubectl create secret generic aws-secret \
  --from-literal=AWS_ACCESS_KEY_ID=xxxxx \
  --from-literal=AWS_SECRET_ACCESS_KEY=yyyyy


Link secret to audio-service:

kubectl set env deployment/audio-deployment --from=secret/aws-secret


Restart:

kubectl rollout restart deployment audio-deployment

🎯 Using the App

Get the URL of video-service:

minikube service video-service --url


Example (your output may differ):

http://127.0.0.1:36891


Upload a video:

curl -X POST http://127.0.0.1:36891/upload \
  -F "file=@/mnt/c/Users/apurv/Videos/Captures/sample.mp4.mp4"


Sample Response:

{
  "audio_response": {
    "local_path": "/data/audio/sample.mp3",
    "s3_url": "https://my-video-audio-bucket.s3.amazonaws.com/audio/.../sample.mp3"
  },
  "video_path": "/data/videos/sample.mp4"
}

📤 Public S3 Access (Optional)

To allow public audio download:

Open AWS S3 Console

Select your bucket → Permissions

Add Bucket Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-video-audio-bucket/*"
    }
  ]
}

👨‍💻 What I Learned (Interview Summary)

✔ Dockerizing Python microservices
✔ Sharing PV/PVC between services
✔ Exposing services using NodePort
✔ Using Minikube's internal Docker daemon
✔ Calling microservices from each other
✔ Using FFmpeg to process media
✔ Using AWS S3 for cloud storage
✔ Debugging pods using logs & rollout restart

📎 Useful Commands
View logs
kubectl logs <pod-name>

Restart deployments
kubectl rollout restart deployment <name>

Delete all (cleanup)
kubectl delete all --all
