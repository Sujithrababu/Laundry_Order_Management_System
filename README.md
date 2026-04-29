# Laundry Order Management System

A FastAPI-based laundry order management system with JWT authentication, MongoDB Atlas integration, and a vanilla JavaScript frontend.

## Tech Stack

- **Python** + **FastAPI**
- **Pydantic** (validation)
- **Motor** (async MongoDB driver)
- **MongoDB Atlas** (cloud free tier)
- **Python-Jose** (JWT authentication)
- **Passlib** (password hashing)

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up MongoDB Atlas Free Tier

1. **Create an account** at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. **Create a new cluster** (choose the **M0 Free Tier**)
3. **Wait for the cluster to deploy** (this may take 1–3 minutes)
4. **Create a database user**:
   - Go to **Database Access** → **Add New Database User**
   - Choose **Password** authentication
   - Set a username and password (save these!)
5. **Whitelist your IP address**:
   - Go to **Network Access** → **Add IP Address**
   - Click **Allow Access from Anywhere** (`0.0.0.0/0`) for development, or add your specific IP
6. **Get the connection string**:
   - Go to **Clusters** → click **Connect** on your cluster
   - Choose **Drivers** → **Python** → **Motor**
   - Copy the connection string, which looks like:
     ```
     mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```
   - Replace `<username>` and `<password>` with your database user credentials
   - Optionally append your database name, e.g.:
     ```
     mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/laundry_management?retryWrites=true&w=majority
     ```

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and paste your MongoDB Atlas connection string into `MONGODB_URL`
3. Change `SECRET_KEY` to a strong random string

### 4. Run the Backend

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 5. Local Development

**Backend**:
```bash
uvicorn main:app --reload
```

**Frontend**:
```bash
cd frontend
python -m http.server 5500
```

Visit `http://localhost:5500` → **Login** → **Dashboard** (API at `http://127.0.0.1:8000`)

### 🌐 Deploy to Render (Free!)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Deploy laundry app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/laundry-app.git
git push -u origin main
```

2. **Backend** (render.com → New → Web Service):
   - **Repository**: Your GitHub repo
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     MONGODB_URL=your_atlas_connection_string
     SECRET_KEY=generate_random_string
     ```

3. **Frontend** (render.com → New → Static Site):
   - **Repository**: Same GitHub repo
   - **Root Directory**: `frontend`
   - **Environment Variable**: `API_URL=https://your-backend.onrender.com`

4. **URLs**:
   ```
   API: https://your-backend.onrender.com/docs
   Frontend: https://your-frontend.onrender.com
   ```

**render.yaml** (optional - auto multi-service):
```
services:
  - type: web
    name: laundry-api
    env: python
    buildCommand: pip install -r requirements.txt  
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
  - type: web
    name: laundry-frontend
    env: static
    dir: frontend
```

**Free tier limits**: Backend sleeps after 15min inactivity, wakes on first request (~30s cold start).


---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login and receive JWT token |
| POST | `/orders` | Yes | Create a new order |
| GET | `/orders` | Yes | List/search orders |
| PATCH | `/orders/{id}/status` | Yes | Update order status |
| GET | `/dashboard` | Yes | Get dashboard statistics |

---

## Validation Rules

| Field | Rule |
|-------|------|
| Customer name | Letters and spaces only, minimum 2 characters |
| Phone number | Exactly 10 digits, numbers only |
| Garment name | Letters and spaces only, cannot be empty |
| Quantity | Minimum 1 |
| Price per item | Minimum 1 |

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGODB_URL` | Yes | — | MongoDB Atlas connection string |
| `DATABASE_NAME` | No | `laundry_management` | MongoDB database name |
| `SECRET_KEY` | Yes | — | Secret key for JWT signing |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | JWT token expiry time |

