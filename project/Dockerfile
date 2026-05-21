# =============================================================================
# SkillCluster AI — Production Dockerfile
# Multi-stage build: demonstrates image layering, caching & size optimization
# =============================================================================

# ── STAGE 1: Dependency Builder ───────────────────────────────────────────────
# ARG instruction — build-time variable (overridable via --build-arg)
ARG PYTHON_VERSION=3.11
ARG BUILD_ENV=production

# FROM instruction — base image (first layer)
FROM python:${PYTHON_VERSION}-slim AS builder

# LABEL instruction — image metadata / OCI annotations
LABEL maintainer="Shubham Gautam <shubhamgautam05@github.com>" \
      org.opencontainers.image.title="SkillCluster AI" \
      org.opencontainers.image.description="AI-powered resume clustering & skill gap detection" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.source="https://github.com/shubhamgautam05/SkillCluster_AI"

# ENV instruction — environment variables (persisted in image)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# WORKDIR instruction — sets working directory (creates if not exists)
WORKDIR /build

# COPY instruction — copy requirements FIRST (separate layer for cache efficiency)
# This layer is only rebuilt when requirements.txt changes — not on every code change
# COPY lean Docker requirements (excludes unused heavy packages like sentence-transformers)
COPY requirements-docker.txt .

# RUN instruction — install all dependencies to default Python site-packages
# --retries 5: retry on network drop  --timeout 120: wait longer per chunk
RUN pip install --upgrade pip --retries 5 --timeout 120 && \
    pip install --retries 5 --timeout 120 -r requirements-docker.txt

# RUN instruction — pre-download NLTK corpora at build time (baked into image layer)
# Works because packages are now in the default site-packages path
RUN python -c "\
import nltk; \
nltk.download('stopwords', download_dir='/usr/local/nltk_data', quiet=True); \
nltk.download('punkt', download_dir='/usr/local/nltk_data', quiet=True); \
nltk.download('punkt_tab', download_dir='/usr/local/nltk_data', quiet=True); \
nltk.download('wordnet', download_dir='/usr/local/nltk_data', quiet=True); \
print('NLTK data downloaded successfully')"


# ── STAGE 2: Production Runtime ───────────────────────────────────────────────
# Second FROM — starts a FRESH minimal image (multi-stage keeps final image lean)
FROM python:${PYTHON_VERSION}-slim AS production

# Re-declare ARG after FROM (ARGs don't persist across stages)
ARG BUILD_ENV

# ENV for runtime configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NLTK_DATA=/usr/local/nltk_data \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    BUILD_ENV=${BUILD_ENV}

# WORKDIR — application root
WORKDIR /app

# RUN — create non-root user for security (DevOps best practice)
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser && \
    mkdir -p /app/output /app/datasets && \
    chown -R appuser:appgroup /app

# RUN — pre-create Streamlit credentials to suppress interactive email prompt
# Without this, Streamlit blocks startup waiting for user input inside Docker
RUN mkdir -p /home/appuser/.streamlit && \
    printf '[general]\nemail = ""\n' > /home/appuser/.streamlit/credentials.toml && \
    chown -R appuser:appgroup /home/appuser/.streamlit

# COPY dependencies from builder stage (this is the multi-stage transfer)
# Only built artifacts are copied — not the full build environment
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/nltk_data /usr/local/nltk_data

# COPY application source code (this layer changes most often — keep it last)
COPY --chown=appuser:appgroup . .

# VOLUME instruction — declares mount points for persistent data
# output/ holds trained ML model artifacts (.pkl files)
VOLUME ["/app/output", "/app/datasets"]

# EXPOSE instruction — documents the port (does NOT publish it)
EXPOSE 8501

# Switch to non-root user
USER appuser

# HEALTHCHECK instruction — Docker monitors container health automatically
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ENTRYPOINT — fixed executable (cannot be overridden without --entrypoint flag)
ENTRYPOINT ["streamlit", "run"]

# CMD — default arguments to ENTRYPOINT (can be overridden at runtime)
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]
