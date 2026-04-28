import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, Field, field_validator

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "laundry_management")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

mongo_client: Optional[AsyncIOMotorClient] = None
db = None
orders_collection = None
users_collection = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

VALID_STATUSES = ["RECEIVED", "PROCESSING", "READY", "DELIVERED"]


@app.on_event("startup")
async def startup_db_client():
    global mongo_client, db, orders_collection, users_collection

    if not MONGODB_URL:
        raise RuntimeError("MONGODB_URL environment variable is required")

    mongo_client = AsyncIOMotorClient(MONGODB_URL)
    db = mongo_client[DATABASE_NAME]
    orders_collection = db["orders"]
    users_collection = db["users"]

    await users_collection.create_index("username", unique=True)
    await orders_collection.create_index("order_id", unique=True)
    await orders_collection.create_index("status")
    await orders_collection.create_index("customer_name")
    await orders_collection.create_index("phone_number")
    await orders_collection.create_index("garments.name")


@app.on_event("shutdown")
async def shutdown_db_client():
    if mongo_client:
        mongo_client.close()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def clean_mongo_id(document: dict) -> dict:
    document.pop("_id", None)
    return document


def validate_letters_and_spaces(value: str, field_name: str, allow_empty: bool = False) -> str:
    stripped = value.strip()
    if not allow_empty and not stripped:
        raise ValueError(f"{field_name} cannot be empty")
    if any(not (char.isalpha() or char.isspace()) for char in stripped):
        raise ValueError(f"{field_name} must contain letters and spaces only")
    return stripped


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = utc_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = await users_collection.find_one({"username": username})
    if not user:
        raise credentials_exception

    return clean_mongo_id(user)


class Garment(BaseModel):
    name: str
    quantity: int
    price_per_item: float

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_letters_and_spaces(value, "Garment name")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

    @field_validator("price_per_item")
    @classmethod
    def validate_price_per_item(cls, value: float) -> float:
        if value < 1:
            raise ValueError("Price per item must be at least 1")
        return value


class OrderCreate(BaseModel):
    customer_name: str
    phone_number: str
    garments: List[Garment] = Field(..., min_length=1)

    @field_validator("customer_name")
    @classmethod
    def validate_customer_name(cls, value: str) -> str:
        stripped = validate_letters_and_spaces(value, "Customer name")
        if len(stripped) < 2:
            raise ValueError("Customer name must be at least 2 characters long")
        return stripped

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped.isdigit():
            raise ValueError("Phone number must contain numbers only")
        if len(stripped) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return stripped


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


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        stripped = value.strip()
        if len(stripped) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return stripped

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post("/auth/register", status_code=201)
async def register(user: UserCreate):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    await users_collection.insert_one(
        {
            "username": user.username,
            "hashed_password": hash_password(user.password),
            "created_at": utc_now(),
        }
    )

    return {"message": "User registered successfully"}


@app.post("/auth/login", response_model=TokenResponse)
async def login(user: UserCreate):
    stored_user = await users_collection.find_one({"username": user.username})
    if not stored_user or not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": stored_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    order_id = str(uuid4())
    total_bill = sum(item.quantity * item.price_per_item for item in order.garments)
    created_at = utc_now()
    estimated_delivery = created_at + timedelta(days=3)

    new_order = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "phone_number": order.phone_number,
        "garments": [item.model_dump() for item in order.garments],
        "total_bill": total_bill,
        "status": "RECEIVED",
        "created_at": created_at,
        "estimated_delivery": estimated_delivery,
    }

    await orders_collection.insert_one(new_order)
    return clean_mongo_id(new_order)


@app.patch("/orders/{order_id}/status")
async def update_status(
    order_id: str,
    update: StatusUpdate,
    current_user: dict = Depends(get_current_user),
):
    if update.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {VALID_STATUSES}",
        )

    result = await orders_collection.update_one(
        {"order_id": order_id},
        {"$set": {"status": update.status}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Status updated successfully"}


@app.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    status: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    phone_number: Optional[str] = Query(None),
    garment_name: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    query = {}

    if status:
        query["status"] = status
    if customer_name:
        query["customer_name"] = {"$regex": customer_name, "$options": "i"}
    if phone_number:
        query["phone_number"] = phone_number
    if garment_name:
        query["garments.name"] = {"$regex": garment_name, "$options": "i"}

    cursor = orders_collection.find(query).sort("created_at", -1)
    orders = [clean_mongo_id(order) async for order in cursor]
    return orders


@app.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    total_orders = await orders_collection.count_documents({})

    revenue_pipeline = [
        {"$group": {"_id": None, "total_revenue": {"$sum": "$total_bill"}}}
    ]
    revenue_result = await orders_collection.aggregate(revenue_pipeline).to_list(length=1)
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0

    status_count = {status_value: 0 for status_value in VALID_STATUSES}
    status_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
    ]
    async for item in orders_collection.aggregate(status_pipeline):
        if item["_id"] in status_count:
            status_count[item["_id"]] = item["count"]

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "orders_per_status": status_count,
    }
