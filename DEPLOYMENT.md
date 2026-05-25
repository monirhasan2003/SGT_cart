# SGT Cart — Production Deployment

Step-by-step checklist for a single Linux server running PostgreSQL,
nginx, gunicorn + Flask-SocketIO, and the maintenance cron jobs.

A typical host: Ubuntu 22.04 LTS, 2 vCPU / 4 GB RAM, Postgres 18, nginx,
TLS via Let's Encrypt. Scale up by moving Postgres to a managed service
and adding more app workers with a shared Redis message queue.

---

## 1. Operating-system prep

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3.12 python3.12-venv python3-pip \
    postgresql-18 redis-server nginx certbot python3-certbot-nginx \
    build-essential libpq-dev
```

Skip `redis-server` if you don't need multi-worker scaling yet — the app
falls back to in-process SocketIO and an in-memory rate-limit store.

## 2. PostgreSQL database

```bash
sudo -u postgres psql <<'SQL'
CREATE USER sgt WITH PASSWORD 'a-strong-password';
CREATE DATABASE sgt_ecommerce OWNER sgt;
GRANT ALL PRIVILEGES ON DATABASE sgt_ecommerce TO sgt;
SQL
```

## 3. Clone, venv, install

```bash
sudo mkdir -p /opt/sgt && sudo chown $USER:$USER /opt/sgt
cd /opt/sgt
git clone <your-repo-url> SGT_Ecommerce
cd SGT_Ecommerce
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn eventlet     # production-only WSGI server + async worker
```

## 4. `.env` configuration

```bash
cp .env.example .env
# Generate strong secrets:
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

Edit `.env`:

| Key | Required? | Notes |
|---|---|---|
| `SECRET_KEY` | yes | `production` config refuses to boot with the dev placeholder. |
| `JWT_SECRET_KEY` | yes | Same scheme — random hex string. |
| `FLASK_CONFIG` | yes | Set to `production`. |
| `FLASK_DEBUG` | yes | `False`. |
| `DATABASE_URL` | yes | `postgresql://sgt:…@localhost:5432/sgt_ecommerce`. |
| `MAIL_*` | yes | SMTP credentials for OTP + transactional email. |
| `ADMIN_EMAIL` | yes | Used by the first-run `create-admin` CLI. |
| `SSLCOMMERZ_*` | optional | Cash on Delivery works without them. |
| `REDIS_URL` | optional | Switches the rate-limit + cache stores to Redis. |
| `SOCKETIO_MESSAGE_QUEUE` | optional | Required to run more than one gunicorn worker. |
| `FCM_CREDENTIALS_FILE` | optional | Path to a Firebase service-account JSON for app push. |

## 5. Database schema + bootstrap data

```bash
source venv/bin/activate
export FLASK_APP=run
flask db upgrade
flask create-admin              # interactive — sets the super-admin password
flask seed-catalog              # starter category tree (safe to re-run)
```

## 6. systemd service

```bash
sudo cp deploy/sgt-ecommerce.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sgt-ecommerce
sudo systemctl status sgt-ecommerce          # verify it is `active (running)`
```

Edit the unit file beforehand if your project lives somewhere other than
`/opt/sgt/SGT_Ecommerce` or your service user isn't `www-data`.

## 7. nginx + TLS

```bash
sudo cp deploy/nginx.conf.example /etc/nginx/sites-available/sgt-ecommerce
sudo ln -s /etc/nginx/sites-available/sgt-ecommerce /etc/nginx/sites-enabled/
# Edit server_name + static alias to match your install.
sudo nginx -t && sudo systemctl reload nginx

sudo certbot --nginx -d your-domain.com
```

## 8. Maintenance cron jobs

```bash
sudo mkdir -p /var/log/sgt && sudo chown www-data:www-data /var/log/sgt
sudo crontab -u www-data deploy/sgt-cron.example
```

This runs:

- `flask process-payouts` every 2 hours — auto-approves payouts older than
  the `auto_payout_min_hours` setting (default 24).
- `flask scan-abandoned-carts` hourly — emails a one-time recovery reminder
  to customers whose cart has gone idle.
- `flask embed-products` nightly — refreshes CLIP image embeddings (only
  needed if you use the image-search feature).

## 9. Smoke tests on the server

After the first deploy:

```bash
source venv/bin/activate
python tests/smoke_phase14_security.py     # CSP, CSRF, HSTS, rate limits
```

Then visit the live URL, sign in as admin, and try the full path: register
a customer → place an order → mark it delivered → run a payout.

---

## Scaling notes

- **Multi-worker SocketIO** — set `SOCKETIO_MESSAGE_QUEUE=redis://…` and
  bump `GUNICORN_WORKERS` in the environment.
- **Image search** — `flask embed-products` is the only place that loads
  the CLIP model. Run it as a one-off after seeding products, then on the
  nightly cron.
- **pgvector swap-out** — `app/services/image_search_service.py` keeps the
  cosine similarity in Python today. Switching to pgvector means changing
  `embedding` from `LargeBinary` to `Vector(512)` plus the search query;
  the service interface stays the same.
- **Celery** — `process-payouts`, `scan-abandoned-carts`, `embed-products`
  are all idempotent CLI commands today (cron-driven). Moving them under
  Celery beat is straightforward; the call sites in
  `app/services/payout_service.py` and `abandoned_cart_service.py` are the
  only things that need wrapping.
