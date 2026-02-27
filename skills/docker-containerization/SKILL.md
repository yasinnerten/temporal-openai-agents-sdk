---
name: docker-containerization
description: Complete Docker and containerization patterns for microservices including multi-stage builds, optimization, and orchestration.
license: Apache-2.0
metadata:
  category: devops
  tags: [docker, containers, microservices, kubernetes]
---

# Docker Containerization

This skill provides comprehensive guidance for containerizing applications, optimizing images, and managing container orchestration.

## Multi-Stage Builds

### 1. Python Multi-Stage
```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir /tmp/pip -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Go Multi-Stage
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server ./cmd/server

# Runtime stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/
COPY --from=builder /app/server .
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
CMD ["./server"]
```

### 3. Node.js Multi-Stage
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "dist/main.js"]
```

## Image Optimization

### 1. Alpine Linux Base
```dockerfile
FROM python:3.11-alpine AS base

# Install only runtime dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    postgresql-client \
    ca-certificates

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir /tmp/pip -r requirements.txt

# Clean up
RUN apk del py3-pip && rm -rf /root/.cache
```

### 2. Layer Caching
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies separately (cached)
COPY package*.json ./
RUN npm ci --only=production

# Copy source code (frequent changes)
COPY . .
RUN npm run build

# Copy node_modules from previous stage
COPY --from=builder /app/node_modules ./node_modules
```

### 3. .dockerignore
```
# .dockerignore
.git
.gitignore
.env
.env.local
__pycache__
*.pyc
node_modules
dist
.DS_Store
tests/
*.test.ts
*.spec.ts
coverage/
```

## Docker Compose

### 1. Basic Service
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### 2. Multi-Service App
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - FRONTEND_URL=http://frontend:3000

  worker:
    build: ./worker
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
```

### 3. Development Environment
```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/app  # Live reload for development
    ports:
      - "8000:8000"
      - "5678:5678"  # Debugger
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
```

## Best Practices

### 1. Minimal Base Images
```dockerfile
# Bad: Too many packages
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
      python3 \
      python3-pip \
      npm \
      nodejs \
      # ... many more

# Good: Alpine for minimal footprint
FROM python:3.11-alpine
RUN apk add --no-cache python3 py3-pip
```

### 2. Non-Root User
```dockerfile
FROM node:20-alpine

# Create non-root user
RUN addgroup -g node -S -g 1000 && \
    adduser -u 1000 -G node -s /bin/bash -g node

WORKDIR /app

USER node

COPY --chown=node:node ./
```

### 3. Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### 4. Signal Handling
```dockerfile
STOPSIGNAL SIGTERM
STOPSIGNAL SIGINT

# Graceful shutdown
ENTRYPOINT ["/app/graceful-shutdown.sh"]
```

## Kubernetes

### 1. Deployment YAML
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry/myapp:v1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
```

### 2. Service YAML
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. ConfigMap
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgres://user:pass@postgres:5432/db"
  REDIS_URL: "redis://redis:6379"
  LOG_LEVEL: "info"
```

### 4. Secret Management
```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  API_KEY: base64encoded-api-key
  DB_PASSWORD: base64encoded-password
```

## Container Security

### 1. Scanning
```bash
# Scan image for vulnerabilities
trivy image myregistry/myapp:v1.0.0

# Scan build context
trivy fs .
```

### 2. Base Image Updates
```dockerfile
# Specify tag to prevent automatic latest updates
FROM python:3.11-alpine:3.11@20240101

# Or use digest for exact version
FROM python@sha256:abc123...
```

### 3. Resource Limits
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
```

## Docker Registry

### 1. Docker Hub Push
```bash
# Build and tag image
docker build -t myregistry/myapp:v1.0.0 .

# Push to registry
docker push myregistry/myapp:v1.0.0
```

### 2. Private Registry
```bash
# Login to private registry
docker login myregistry.com

# Tag for private registry
docker tag myapp:v1.0.0 myregistry.com/myapp:v1.0.0

# Push to private registry
docker push myregistry.com/myapp:v1.0.0
```

## Orchestration

### 1. Docker Swarm
```yaml
# docker-stack.yml
version: '3.8'

services:
  web:
    image: nginx:alpine
    deploy:
      mode: replicated
      replicas: 3
    ports:
      - "80:80"

  api:
    image: myregistry/api:v1.0.0
    deploy:
      mode: replicated
      replicas: 2
    networks:
      - backend
    environment:
      - DATABASE_URL=postgres://db:5432/app
```

### 2. Nomad
```hcl
# job.nomad
job "worker" {
  datacenters = ["dc1"]
  type = "batch"

  group "count" {
    count = 5
  }

  task "process" {
    driver = "docker"
    config {
      image = "myregistry/worker:v1.0.0"
    }
  }
}
```

## Optimization Strategies

### 1. BuildKit Caching
```dockerfile
# syntax=docker/dockerfile:1.2
# Use build cache mounts
RUN --mount=type=cache,target=/root/.cache go mod download

# Share cache between builds
FROM scratch
COPY --from=cache /root/.cache /cache
```

### 2. Parallel Builds
```bash
#!/bin/bash
# Build multiple architectures in parallel
docker buildx build --platform linux/amd64 -t myapp:amd64 .
docker buildx build --platform linux/arm64 -t myapp:arm64 .
```

### 3. Image Size Reduction
```dockerfile
FROM alpine:latest AS base

# Install and cleanup in one layer
RUN apk add --no-cache --virtual .build-deps \
      gcc \
      musl-dev && \
    apk add --no-cache python3 && \
    apk del .build-deps

# Use .dockerignore to exclude unnecessary files
```

## Troubleshooting

### 1. Debugging Containers
```bash
# Interactive shell in running container
docker exec -it mycontainer /bin/sh

# View logs
docker logs -f mycontainer

# Inspect container
docker inspect mycontainer
```

### 2. Networking Issues
```bash
# Check container DNS resolution
docker run --rm alpine nslookup google.com

# Test connectivity between containers
docker run --rm --link postgres:db --link app:web alpine ping postgres

# Port forwarding
docker run -p 8000:8000 myapp
```

### 3. Cleanup
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove all unused resources
docker system prune -a --volumes
```

## CI/CD Integration

### 1. GitHub Actions
```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Login to Docker Hub
        run: docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}

      - name: Build image
        run: docker build -t myregistry/myapp:${{ github.sha }} .

      - name: Push image
        run: docker push myregistry/myapp:${{ github.sha }}
```

### 2. GitLab CI
```yaml
# .gitlab-ci.yml
image: docker:20.10.16

services:
  - docker:dind

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## References
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Trivy Security Scanner](https://aquasecurity.github.io/trivy/)
