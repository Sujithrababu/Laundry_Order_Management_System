from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import uuid4
from datetime import datetime, timedelta

app = FastAPI()

# In-memory storage
orders_db: Dict[str, dict] = {}

# Allowed statuses
VALID_STATUSES = ["RECEIVED", "PROCESSING", "READY", "DELIVERED"]

# ------------------ MODELS ------------------

class Garment(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    price_per_item: float = Field(gt=0)

class OrderCreate(BaseModel):
    customer_name: str
    phone_number: str
    garments: List[Garment]

class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    phone_number: str
    garments: List[Garment]
    total_bill: float
    status: str
    created_at: datetime
    estimated_delivery: datetime

class StatusUpdate(BaseModel):
    status: str

# ------------------ ROUTES ------------------

# Create a new laundry order
@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate):
    order_id = str(uuid4())

    total_bill = sum(
        item.quantity * item.price_per_item for item in order.garments
    )

    created_at = datetime.utcnow()
    estimated_delivery = created_at + timedelta(days=3)

    new_order = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "phone_number": order.phone_number,
        "garments": order.garments,
        "total_bill": total_bill,
        "status": "RECEIVED",
        "created_at": created_at,
        "estimated_delivery": estimated_delivery,
    }

    orders_db[order_id] = new_order
    return new_order


# Update the status of an existing order
@app.patch("/orders/{order_id}/status")
def update_status(order_id: str, update: StatusUpdate):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    if update.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {VALID_STATUSES}"
        )

    orders_db[order_id]["status"] = update.status
    return {"message": "Status updated successfully"}


# Get all orders with optional filters
@app.get("/orders", response_model=List[OrderResponse])
def get_orders(
    status: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    phone_number: Optional[str] = Query(None)
):
    results = []

    for order in orders_db.values():
        if status and order["status"] != status:
            continue
        if customer_name and customer_name.lower() not in order["customer_name"].lower():
            continue
        if phone_number and order["phone_number"] != phone_number:
            continue

        results.append(order)

    return results


# Dashboard summary of orders and revenue
@app.get("/dashboard")
def dashboard():
    total_orders = len(orders_db)
    total_revenue = sum(order["total_bill"] for order in orders_db.values())

    status_count = {status: 0 for status in VALID_STATUSES}

    for order in orders_db.values():
        status_count[order["status"]] += 1

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "orders_per_status": status_count
    }