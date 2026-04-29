# Laundry Order Management System

**Live**: https://laundry-order-management-system-opkq.onrender.com  
**API Docs**: https://laundry-order-management-system-opkq.onrender.com/docs  
**Repo**: https://github.com/Sujithrababu/Laundry_Order_Management_System

## Features Implemented

### Core Requirements
1. **Create Order**: Customer details, multiple garments, total bill, unique Order ID
2. **Status Management**: RECEIVED → PROCESSING → READY → DELIVERED (quick + manual)
3. **View Orders**: List + filters (status, name, phone, garment)
4. **Dashboard**: Total orders, revenue, status counts

### Bonus Features
- JWT authentication (register/login)
- MongoDB Atlas persistence
- Estimated delivery (3 days ahead)
- Real-time frontend validation
- Render deployment (single service)
- 3-page UI flow

## Tech Stack
```
Backend: FastAPI + Motor (MongoDB) + JWT + Pydantic
Frontend: Vanilla HTML/CSS/JS
Database: MongoDB Atlas
Deployment: Render
```

## Local Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Visit `http://localhost:8000`

**Required**:
```
MONGODB_URL=your_atlas_connection_string
SECRET_KEY=generate_secret
```

## AI Usage Report (~5-6 hours development)

### Tools
- **BLACKBOX AI**: Code generation (backend, frontend structure)
- **ChatGPT-4**: Debugging, validation logic

### Key Prompts Used
```
BLACKBOX: "FastAPI laundry system + MongoDB Atlas + JWT + frontend"
BLACKBOX: "3-page frontend: landing/auth/dashboard with localStorage"
ChatGPT: "Pydantic validators for customer name, phone (10 digits), garments"
BLACKBOX: "Fix Render 404 + serve static files from FastAPI"
```

### AI Limitations Fixed
1. **Pydantic syntax errors** → Manual field validators
2. **Incomplete frontend functions** → Added `updateStatusManual()`, `loadDashboard()`
3. **Relative path issues** → Fixed `href="./auth.html"`
4. **Deployment 404** → `@app.get("/")` route

### Development Breakdown
```
Backend API + DB: 3hrs
Frontend + Auth: 2hrs  
Deployment + Fixes: 1.5hrs
Total: ~6.5hrs (within 72hr window)
```

## Tradeoffs
| Decision | Why |
|----------|-----|
| Vanilla JS | Speed > Framework overhead |
| MongoDB | Persistence bonus |
| Render | Free + auto-deploy |
| Single service | Simpler deployment |

## Future Improvements
- Customer SMS notifications
- Multi-branch support
- Advanced reporting
- Payment gateway

**Built using BLACKBOX AI + ChatGPT as primary development tools.**


