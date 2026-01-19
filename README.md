# SMSFilter
A lightweight backend for filtering SMS messages based on safety constraints.

## Environment

```bash
# USER
UID=10001
GID=10001
# NETWORKING
ALLOWED_HOSTS='["http://localhost:5173", "http://127.0.0.1:5173", "http://10.0.0.119:5173"]'
# Application
APP_DIR=/app
# Quantization
QUANT=Q4_K_M
# Exclude
EXCL='[]'
# Include
INCL='[]'
```

NOTE: Exclusions and Inclusions are not currently supported.

## Build

```bash
mvnd clean install
```

## Deploy

```
docker compose up
```