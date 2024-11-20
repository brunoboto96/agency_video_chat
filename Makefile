# Makefile

# =============================================================================
# Variables
# =============================================================================

# Google Cloud variables
GCLOUD_REGION ?= europe-west2
GCLOUD_PROJECT ?= your-gcloud-project-id

# Backend and Frontend image names
BACKEND_IMAGE_NAME ?= agency-video-chat-backend
FRONTEND_IMAGE_NAME ?= agency-video-chat-frontend

# Docker Registry
DOCKER_REGISTRY ?= europe-west2-docker.pkg.dev/agency-video-chat

# Repository URLs
BACKEND_REPO ?= $(DOCKER_REGISTRY)/repo-video-chat-backend/$(BACKEND_IMAGE_NAME)
FRONTEND_REPO ?= $(DOCKER_REGISTRY)/repo-video-chat-frontend/$(FRONTEND_IMAGE_NAME)

# Ports
FRONTEND_PORT ?= 3000
BACKEND_PORT ?= 8000


# Base URLs
BASE_URL ?= http://localhost
FRONTEND_BASE_URL ?= $(BASE_URL):$(FRONTEND_PORT)
BACKEND_BASE_URL ?= $(BASE_URL):$(BACKEND_PORT)


# =============================================================================
# Targets
# =============================================================================

.PHONY: all backend frontend backend-cloud frontend-cloud deploy-backend-cloud deploy-frontend-cloud up logs-backend logs-frontend clean build push help

# Default target to build both backend and frontend
all: build

# Build the backend Docker image locally
backend:
	docker build --platform linux/amd64 -t $(BACKEND_IMAGE_NAME) ./backend
	@echo "Backend Docker image has been built."

# Build the frontend Docker image locally
frontend:
	docker build -t $(FRONTEND_IMAGE_NAME) ./frontend
	@echo "Frontend Docker image has been built."

# Build and push the backend Docker image
backend-cloud:
	docker build --platform linux/amd64 -t $(BACKEND_IMAGE_NAME) ./backend
	docker tag $(BACKEND_IMAGE_NAME) $(BACKEND_REPO)
	docker push $(BACKEND_REPO)

# Build and push the frontend Docker image
frontend-cloud:
	docker build --platform linux/amd64 -t $(FRONTEND_IMAGE_NAME) ./frontend
	docker tag $(FRONTEND_IMAGE_NAME) $(FRONTEND_REPO)
	docker push $(FRONTEND_REPO)

# Deploy the backend to Google Cloud Run
deploy-backend-cloud: backend-cloud
	gcloud run deploy $(BACKEND_IMAGE_NAME) \
	  --image $(BACKEND_REPO) \
	  --platform managed \
	  --region $(GCLOUD_REGION) \
	  --project $(GCLOUD_PROJECT) \
	  --allow-unauthenticated

# Deploy the frontend to Google Cloud Run
deploy-frontend-cloud: frontend-cloud
	gcloud run deploy $(FRONTEND_IMAGE_NAME) \
	  --image $(FRONTEND_REPO) \
	  --platform managed \
	  --region $(GCLOUD_REGION) \
	  --project $(GCLOUD_PROJECT) \
	  --allow-unauthenticated

# Build both backend and frontend images
build: backend frontend

# Push both backend and frontend images to the registry
push: backend frontend

# Start services using Docker Compose
up:
	FRONTEND_IMAGE_NAME=${FRONTEND_IMAGE_NAME} BACKEND_IMAGE_NAME=${BACKEND_IMAGE_NAME} FRONTEND_PORT=${FRONTEND_PORT} BACKEND_PORT=${BACKEND_PORT} BASE_URL=${BASE_URL} docker-compose up -d
	@echo "Services are up and running."

# Follow logs for the backend service
logs-backend:
	docker-compose logs -f backend

# Follow logs for the frontend service
logs-frontend:
	docker-compose logs -f frontend

# Stop and remove services using Docker Compose
clean:
	docker-compose down --volumes
	@echo "Services have been stopped and removed."

# =============================================================================
# Help
# =============================================================================

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all              Build both backend and frontend Docker images."
	@echo "  backend          Build and push the backend Docker image."
	@echo "  frontend         Build and push the frontend Docker image."
	@echo "  deploy-backend   Deploy the backend to Google Cloud Run."
	@echo "  deploy-frontend  Deploy the frontend to Google Cloud Run."
	@echo "  build            Alias for 'all'."
	@echo "  push             Push both backend and frontend Docker images."
	@echo "  up               Start services using Docker Compose."
	@echo "  logs-backend     Follow logs for the backend service."
	@echo "  logs-frontend    Follow logs for the frontend service."
	@echo "  clean            Stop and remove services using Docker Compose."
	@echo "  help             Show this help message."

# =============================================================================