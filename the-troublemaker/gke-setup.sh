# Ativar APIs necessárias
gcloud services enable container.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# Criar repositório para a imagem
gcloud artifacts repositories create demo-repo --repository-format=docker --location=us-central1

gcloud container clusters create-auto demo-investigations \
    --location us-central1 \
    --project [SEU-PROJECT-ID]

# Obter as credenciais
gcloud container clusters get-credentials demo-investigations --location us-central1

# Build da imagem usando Cloud Build
gcloud builds submit --tag us-central1-docker.pkg.dev/[SEU-PROJECT-ID]/demo-repo/gke-troublemaker:v1 .

# Criar o deployment (usando a imagem acima)
kubectl create deployment gke-app --image=us-central1-docker.pkg.dev/[SEU-PROJECT-ID]/demo-repo/gke-troublemaker:v1
kubectl expose deployment gke-app --type=LoadBalancer --port=80 --target-port=8080