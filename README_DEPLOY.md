# Deploying Daily Mini Crossword to Render

This guide explains how to deploy the Daily Mini Crossword app to [Render](https://render.com) with a free PostgreSQL database and get a public HTTPS URL.

## Prerequisites

- A GitHub account with this repository pushed
- A [Render](https://render.com) account (free tier available)

## Deployment Options

### Option A: One-Click Blueprint Deploy (Recommended)

The repository includes a `render.yaml` file that automatically configures everything.

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub account if not already connected
   - Select your repository
   - Render will detect `render.yaml` and show the resources to create:
     - PostgreSQL database: `crossword-db`
     - Web service: `daily-mini-crossword`
   - Click **"Apply"**

3. **Wait for Deployment**
   - Database creation: ~1-2 minutes
   - Web service build: ~3-5 minutes
   - First request may take ~30 seconds (cold start on free tier)

4. **Access Your App**
   - Your app URL will be: `https://daily-mini-crossword.onrender.com`
   - (The exact URL depends on availability; Render may add random characters)

---

### Option B: Manual Setup

If you prefer manual control, follow these steps:

#### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `crossword-db`
   - **Database**: `crossword`
   - **User**: `crossword`
   - **Region**: Oregon (or closest to you)
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for creation, then copy the **Internal Database URL**

#### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

   | Field | Value |
   |-------|-------|
   | **Name** | `daily-mini-crossword` |
   | **Region** | Oregon (same as database) |
   | **Branch** | `main` |
   | **Root Directory** | (leave empty) |
   | **Runtime** | Python 3 |
   | **Build Command** | `cd backend && pip install -r requirements.txt` |
   | **Start Command** | `cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |
   | **Plan** | Free |

4. Add Environment Variables:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | (paste Internal Database URL from Step 1) |
   | `SECRET_KEY` | (click "Generate" or paste a random 32+ char string) |
   | `JWT_SECRET_KEY` | (click "Generate" or paste a random 32+ char string) |
   | `DEBUG` | `false` |
   | `PYTHON_VERSION` | `3.11.4` |

5. Click **"Create Web Service"**

---

## After Deployment

### Finding Your URL

1. Go to your web service in Render Dashboard
2. The URL is shown at the top of the page:
   ```
   https://daily-mini-crossword.onrender.com
   ```
   (or similar with random suffix if name was taken)

### Testing the Deployment

1. **Health Check**
   ```bash
   curl https://your-app-url.onrender.com/api/health
   ```
   Expected: `{"status":"healthy","app":"Daily Mini Crossword"}`

2. **Open in Browser**
   - Visit `https://your-app-url.onrender.com`
   - You should see the crossword game

3. **Test Registration**
   - Click "Register"
   - Create an account
   - Try solving a puzzle

### Default Test Users

The app auto-seeds with these test accounts:
| Username | Password |
|----------|----------|
| alice | password123 |
| bob | password123 |
| charlie | password123 |

---

## Database Migrations

For initial deployment, the app automatically creates tables on startup.

For future schema changes:

1. **SSH into Render** (paid plans only) or run locally:
   ```bash
   # Local with production database
   DATABASE_URL="postgresql://..." alembic upgrade head
   ```

2. **Or use Render's Shell** (paid plans):
   ```bash
   cd backend
   alembic upgrade head
   ```

---

## Troubleshooting

### App Shows "No puzzle available"

The database seeding may have failed. Check logs:
1. Go to your web service in Render
2. Click **"Logs"**
3. Look for seeding errors

To manually seed:
```bash
# If you have shell access
cd backend
python seed_data.py
```

### Build Fails

Check that `requirements.txt` has all dependencies:
```bash
cd backend && pip install -r requirements.txt
```

### Database Connection Errors

1. Verify `DATABASE_URL` is set correctly
2. Ensure database is in the same region as web service
3. Check that database is fully initialized (takes 1-2 min)

### Cold Starts

On Render's free tier, apps sleep after 15 minutes of inactivity.
First request after sleep takes ~30 seconds. This is normal.

### Static Files Not Loading

Check logs for:
```
Frontend directory: /opt/render/project/src/frontend
Mounted static files from ...
```

If missing, the path detection may have failed. The app should still work with API endpoints.

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SECRET_KEY` | Yes | App secret (32+ chars) |
| `JWT_SECRET_KEY` | Yes | JWT signing key (32+ chars) |
| `DEBUG` | No | Set to `false` for production |
| `PORT` | Auto | Render sets this automatically |

---

## Architecture on Render

```
┌─────────────────────────────────────────────────────┐
│                    Render                           │
│                                                     │
│  ┌─────────────────────┐    ┌──────────────────┐  │
│  │   Web Service       │    │   PostgreSQL     │  │
│  │   (Python/FastAPI)  │───▶│   Database       │  │
│  │                     │    │                  │  │
│  │ - Serves frontend   │    │ - Users          │  │
│  │ - API endpoints     │    │ - Puzzles        │  │
│  │ - Static files      │    │ - Solves         │  │
│  └─────────────────────┘    │ - Friends        │  │
│           │                 └──────────────────┘  │
│           │                                        │
│           ▼                                        │
│  https://your-app.onrender.com                     │
│  (Platform-provided HTTPS URL)                     │
└─────────────────────────────────────────────────────┘
```

---

## Costs

**Free Tier Includes:**
- 750 hours/month web service (enough for 1 always-on service)
- PostgreSQL with 1GB storage, 1 million rows
- Auto-sleep after 15 min inactivity
- HTTPS with platform subdomain

**Limitations:**
- Cold starts after sleep (~30 sec)
- No custom domains on free tier
- Database expires after 90 days (must recreate)

**Paid Options:**
- $7/month for always-on web service
- $7/month for persistent database
- Custom domains

---

## Updating the App

After pushing changes to GitHub:

1. Render automatically detects the push
2. Builds and deploys the new version
3. Zero-downtime deployment

To manually trigger:
1. Go to your web service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Support

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- GitHub Issues: (your repo)/issues
