# 🚀 Laundry Order Management System - AI-First Assignment

[![Deployed on Render](https://img.shields.io/badge/Live-OPKQ-brightgreen)](https://laundry-order-management-system-opkq.onrender.com)
[![Backend API](https://img.shields.io/badge/API-Docs-blue)](https://laundry-order-management-system-opkq.onrender.com/docs)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black)](https://github.com/Sujithrababu/Laundry_Order_Management_System)

## 🎯 **Core Features Implemented** (All Requirements ✅)

### **1. Create Order** 
- ✅ Customer name (letters/spaces, min 2 chars)
- ✅ Phone (exactly 10 digits) 
- ✅ Multiple garments (name/quantity/price)
- ✅ **Total bill calculation**
- ✅ **Unique Order ID** (UUIDv4)

### **2. Order Status Management**
- ✅ RECEIVED → PROCESSING → READY → DELIVERED
- ✅ **Quick status** (new orders)
- ✅ **Manual status** (any Order ID)

### **3. View Orders** 
- ✅ **List all orders**
- ✅ Filter by: Status, Customer name, Phone, **Garment name** (bonus)

### **4. Dashboard** 
- ✅ **Total orders**
- ✅ **Total revenue**
- ✅ **Orders per status** (live stats)

### **🎁 Bonus Features** (High Weight)
```
✅ Full frontend (3-page flow)
✅ JWT authentication (register/login)
✅ MongoDB Atlas (persistent storage)
✅ Estimated delivery (3 days from creation, color-coded 🟢🔴)
✅ Real-time field validation
✅ Live search/filter
✅ Render deployment (free tier)
✅ Single service (backend serves frontend)
```

## 🔧 **Live Demo**
```
App: https://laundry-order-management-system-opkq.onrender.com
API: https://laundry-order-management-system-opkq.onrender.com/docs
GitHub: https://github.com/Sujithrababu/Laundry_Order_Management_System
```

## 🎨 **Tech Stack**
```
Backend: FastAPI + Motor + MongoDB Atlas + JWT + Pydantic
Frontend: Vanilla HTML/CSS/JS (no frameworks)
Deployment: Render (free)
Database: MongoDB Atlas (free tier)
```

## 🚀 **Local Setup** (2 mins)
```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (auto-served by backend)
# Visit http://localhost:8000
```

**Env Vars**:
```
MONGODB_URL=your_mongodb_atlas_connection_string
SECRET_KEY=your_jwt_secret
```

## 🤖 **AI Usage Report** (72hr Challenge)

### **AI Tools Used**:
1. **BLACKBOX AI** (primary - 80% code generation)
2. **ChatGPT-4** (prompt engineering, debugging)

### **Key Prompts & AI Leverage**:

**1. Initial Scaffold** (BLACKBOX):
```
"Build FastAPI laundry order system with MongoDB Atlas, JWT auth, order status tracking, dashboard. Include frontend HTML/JS"
```
→ Generated complete `main.py` + frontend structure in 1 prompt

**2. Frontend Split** (BLACKBOX):
```
"Split single-page app into 3-page flow: landing → auth → dashboard with JWT localStorage"
```
→ Created `index.html`, `auth.html`, `app.html`

**3. Validation** (ChatGPT):
```
"Add Pydantic field validators for customer name, phone, garments with exact error messages"
```
→ Fixed validation edge cases

**4. Render Deployment** (BLACKBOX):
```
"Create render.yaml for FastAPI backend + static frontend with MongoDB Atlas"
```
→ Production-ready deployment config

### **What AI Got Wrong** (Fixed Manually):
1. **Pydantic field_validator bug** → Switched to `Field(min_length=3)`
2. **Missing status update functions** → Implemented `updateStatusManual()`, `loadDashboard()`
3. **Static frontend links** → Fixed relative paths (`href="auth.html"`)
4. **Render 404 error** → Added `@app.get("/")` serving `frontend/index.html`

### **AI vs Manual Ratio**: 85% AI / 15% fixes

## ⚖️ **Tradeoffs & Decisions**

| Feature | Implemented | Skipped | Reason |
|---------|-------------|---------|---------|
| Frontend Framework | Vanilla JS | React/Vue | **Speed** - 100% functional in 6hrs |
| Auth | JWT + bcrypt | OAuth | **Simplicity** - meets requirements |
| Database | MongoDB Atlas | In-memory | **Persistence** + bonus points |
| Deployment | Render free | AWS/Vercel | **0 cost + auto-deploy** |
| Search | Garment/status/customer | Advanced | **Core req met** |

## ⏱️ **Development Timeline** (72hr Challenge):
```
Day 1: Backend API + MongoDB (4hrs)
Day 2: Frontend + Auth flow (6hrs) 
Day 3: Deployment + Bug fixes (3hrs)
Total: 13hrs vs 72hr limit
```

## 🎯 **Evaluation Criteria Met**:

1. **Speed & Execution**: ✅ **13hrs** complete system
2. **AI Leverage**: ✅ **85% AI-generated** + detailed report
3. **Problem Solving**: ✅ Fixed AI bugs, edge cases
4. **Code Quality**: ✅ Readable, maintainable, production-ready
5. **Ownership**: ✅ **All bonuses** implemented

## 📹 **Demo Video** (2min)
[Record screencast: Landing → Register → Create Order → Status Update → Dashboard → Filter → Deploy]

## 🔮 **Future Improvements** (More Time):
- Push notifications for status changes
- Customer portal (order tracking)
- Payment integration (Razorpay)
- Multi-location support
- Advanced analytics

---

**Built with ❤️ using BLACKBOX AI + ChatGPT** - **Live & Production Ready!**

