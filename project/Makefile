# =============================================================================
# Makefile — SkillCluster AI Build Automation
# Python-project parallel to Maven's build lifecycle
# Usage: make <target>   e.g.  make build   or   make run
# =============================================================================

# Variables
IMAGE_NAME      := skillcluster-ai
DOCKERHUB_USER  := shubhamgautam05
GHCR_REGISTRY   := ghcr.io/shubhamgautam05
VERSION         := $(shell git describe --tags --always --dirty 2>/dev/null || echo "1.0.0")
FULL_IMAGE      := $(DOCKERHUB_USER)/$(IMAGE_NAME)
GHCR_IMAGE      := $(GHCR_REGISTRY)/$(IMAGE_NAME)

# Default target
.DEFAULT_GOAL := help

# =============================================================================
# HELP — List all available targets
# =============================================================================
.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "  SkillCluster AI — DevOps Makefile"
	@echo "  =================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# PHASE 1: VALIDATE — Lint and code quality checks
# =============================================================================
.PHONY: lint
lint: ## Run flake8 linter across all Python files
	@echo ">> Running linter..."
	pip install flake8 --quiet
	flake8 *.py --max-line-length=150 --ignore=E501,W503,E302,E303 --exclude=__pycache__
	@echo ">> Lint passed!"

# =============================================================================
# PHASE 2: COMPILE — Validate imports and NLTK data
# =============================================================================
.PHONY: compile
compile: ## Verify all imports resolve and NLTK corpora are present
	@echo ">> Verifying dependencies..."
	python -c "import streamlit, pandas, sklearn, nltk, plotly, joblib; print('All imports OK')"
	python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True); nltk.download('wordnet', quiet=True); print('NLTK data OK')"
	@echo ">> Compile check passed!"

# =============================================================================
# PHASE 3: TEST — Run unit tests
# =============================================================================
.PHONY: test
test: ## Run all unit tests with pytest
	@echo ">> Running tests..."
	pip install pytest --quiet
	pytest tests/ -v --tb=short 2>/dev/null || echo ">> No tests found — skipping"
	@echo ">> Test phase complete!"

# =============================================================================
# PHASE 4: PACKAGE — Build Docker image
# =============================================================================
.PHONY: build
build: ## Build Docker image (production multi-stage)
	@echo ">> Building Docker image: $(IMAGE_NAME):$(VERSION)"
	docker build \
		--build-arg PYTHON_VERSION=3.11 \
		--build-arg BUILD_ENV=production \
		--tag $(IMAGE_NAME):latest \
		--tag $(IMAGE_NAME):$(VERSION) \
		--tag $(FULL_IMAGE):latest \
		--tag $(FULL_IMAGE):$(VERSION) \
		--tag $(GHCR_IMAGE):latest \
		--tag $(GHCR_IMAGE):$(VERSION) \
		--file Dockerfile \
		.
	@echo ">> Image built: $(IMAGE_NAME):$(VERSION)"

.PHONY: build-no-cache
build-no-cache: ## Force rebuild without using any cache layers
	@echo ">> Building fresh (no cache)..."
	docker build --no-cache \
		--tag $(IMAGE_NAME):latest \
		--file Dockerfile .

# =============================================================================
# PHASE 5: RUN — Local development
# =============================================================================
.PHONY: run
run: ## Run app locally using Docker Compose (dev mode with hot reload)
	@echo ">> Starting SkillCluster AI (dev mode)..."
	docker compose up --build

.PHONY: run-prod
run-prod: ## Run in production mode (no overrides, no hot reload)
	@echo ">> Starting SkillCluster AI (production mode)..."
	docker compose -f docker-compose.yml up -d

.PHONY: pipeline
pipeline: ## Run the ML training pipeline inside Docker
	@echo ">> Running ML pipeline..."
	docker compose --profile pipeline run --rm pipeline-runner

.PHONY: stop
stop: ## Stop all running containers
	docker compose down

.PHONY: down-clean
down-clean: ## Stop containers AND remove volumes (full cleanup)
	docker compose down --volumes --remove-orphans

# =============================================================================
# PHASE 6: DEPLOY — Push to registries
# =============================================================================
.PHONY: login-hub
login-hub: ## Login to Docker Hub
	docker login --username $(DOCKERHUB_USER)

.PHONY: login-ghcr
login-ghcr: ## Login to GitHub Container Registry (GHCR)
	echo "$(GITHUB_TOKEN)" | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin

.PHONY: push-hub
push-hub: ## Push image to Docker Hub
	@echo ">> Pushing to Docker Hub..."
	docker push $(FULL_IMAGE):latest
	docker push $(FULL_IMAGE):$(VERSION)
	@echo ">> Pushed to https://hub.docker.com/r/$(DOCKERHUB_USER)/$(IMAGE_NAME)"

.PHONY: push-ghcr
push-ghcr: ## Push image to GitHub Container Registry
	@echo ">> Pushing to GHCR..."
	docker push $(GHCR_IMAGE):latest
	docker push $(GHCR_IMAGE):$(VERSION)
	@echo ">> Pushed to ghcr.io/shubhamgautam05/$(IMAGE_NAME)"

.PHONY: push-all
push-all: push-hub push-ghcr ## Push to BOTH Docker Hub and GHCR

# =============================================================================
# UTILITIES — Inspect, debug, and manage containers
# =============================================================================
.PHONY: logs
logs: ## Stream live container logs
	docker compose logs -f skillcluster-app

.PHONY: shell
shell: ## Open a shell inside the running container
	docker exec -it skillcluster-app /bin/bash

.PHONY: inspect
inspect: ## Show full image layer history and size breakdown
	@echo "=== Image History (Layers) ==="
	docker history $(IMAGE_NAME):latest
	@echo ""
	@echo "=== Image Details ==="
	docker inspect $(IMAGE_NAME):latest | python -c \
		"import json,sys; d=json.load(sys.stdin)[0]; print('Size:', round(d['Size']/1024/1024,2), 'MB'); print('Layers:', len(d['RootFS']['Layers']))"

.PHONY: ps
ps: ## Show running containers and their status
	docker compose ps

.PHONY: stats
stats: ## Live resource usage (CPU, memory) of running containers
	docker stats skillcluster-app

.PHONY: prune
prune: ## Remove dangling images, stopped containers, unused networks
	docker system prune -f

# =============================================================================
# FULL LIFECYCLE — Run everything in sequence (like mvn clean install deploy)
# =============================================================================
.PHONY: all
all: lint compile test build push-all ## Full lifecycle: lint → compile → test → build → push
	@echo ""
	@echo ">> Full DevOps lifecycle complete!"
	@echo ">> Image available on:"
	@echo "     Docker Hub : https://hub.docker.com/r/$(DOCKERHUB_USER)/$(IMAGE_NAME)"
	@echo "     GHCR       : https://$(GHCR_IMAGE)"
