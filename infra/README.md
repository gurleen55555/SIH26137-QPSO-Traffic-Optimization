# 🐳 Infrastructure & Deployment (`infra/`)

> **Owner:** M4 (STACK Lead - Integration, Containers & Deployment)

The `infra` directory contains containerization templates, orchestration configuration, and deployment scripts for running the complete solution locally via **Docker Compose** or on lightweight cloud compute instances (AWS EC2 / GCP Compute Engine).

---

## 📂 Directory Layout

```
infra/
├── README.md               # This file - setup, networking, and deployment guide
├── docker-compose.yml      # 5-service orchestration definition
├── .env.example            # Sample environment variables template
├── Dockerfile.backend      # Container image for FastAPI & Algorithm engine
├── Dockerfile.frontend     # Multi-stage build container (Node build + Nginx Alpine)
└── deploy/                 # Cloud deployment automation
    ├── setup_ec2.sh        # Provisioning script for AWS EC2 t3.medium
    └── setup_gcp.sh        # Provisioning script for GCP e2-medium
```

---

## 🚢 Service Architecture (Docker Compose)

| Service | Image / Base | Internal Port | Host Port | Purpose |
|---|---|:---:|:---:|---|
| **`frontend`** | `nginx:alpine` | `80` | `3000` | Serves compiled React SPA + proxies API/WS |
| **`api-server`** | `python:3.11-slim` | `8000` | `8000` | FastAPI REST endpoints & WebSocket server |
| **`db`** | `postgis/postgis:16-3.4` | `5432` | `5432` | Stores spatial road network and trip logs |
| **`redis`** | `redis:7-alpine` | `6379` | `6379` | Fast pub/sub channel for live edge weights |

---

## 🚀 Quick Launch Instructions

### 1. Configure Environment
```bash
cp infra/.env.example infra/.env
```

### 2. Start Services
```bash
# From repository root
docker compose -f infra/docker-compose.yml up --build -d
```

### 3. Check Health & Logs
```bash
# View aggregated service logs
docker compose -f infra/docker-compose.yml logs -f

# Check container status
docker compose -f infra/docker-compose.yml ps
```

### 4. Stop Services
```bash
docker compose -f infra/docker-compose.yml down
```

---

## 🔒 Production Hardening & Cloud Notes
- **Resource Constraints**: Docker Compose specifies memory limits (`api-server`: 1.5GB RAM, `db`: 1GB RAM) to run comfortably on standard developer laptops and modest cloud VMs.
- **Volume Persistence**: PostGIS database records are mounted to `pgdata` named volume to preserve loaded city networks across container restarts.
- **Failover**: If the PostGIS container is stopped or fails health check, the backend automatically reads cached graph pickles from `data/backups/`.
