# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /app

# Variables d'environnement pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Copier uniquement les fichiers de dépendances pour profiter du cache Docker
COPY env/base.txt ./env/base.txt

# Installer les dépendances dans un virtualenv isolé
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r env/base.txt

# ── Runtime stage ───────────────────────────────────────────────────────────────
FROM python:3.10-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH" \
    VIRTUAL_ENV=/venv

# Copier uniquement le virtualenv depuis le builder (pas les outils de build)
COPY --from=builder /venv /venv

# Copier le code applicatif
COPY . .

# Least-privilege : permettre l'exécution par un utilisateur non-root (OpenShift compatible)
RUN chgrp -R 0 /app && chmod -R g=u /app

# Exposer le port applicatif
EXPOSE 5000

# Démarrer Gunicorn en production
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app.cli:app"]
