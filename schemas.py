"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# ------------------ Core Transport SaaS Schemas ------------------

class Company(BaseModel):
    """
    Transport companies using the SaaS
    Collection name: "company"
    """
    name: str = Field(..., description="Company legal name")
    email: str = Field(..., description="Primary contact email")
    phone: Optional[str] = Field(None, description="Primary contact phone")
    address: Optional[str] = Field(None, description="Headquarters address")
    website: Optional[str] = Field(None, description="Company website")

class Driver(BaseModel):
    """
    Drivers employed by companies
    Collection name: "driver"
    """
    company_id: Optional[str] = Field(None, description="Owning company id")
    name: str = Field(..., description="Full name")
    email: Optional[str] = Field(None, description="Email")
    phone: Optional[str] = Field(None, description="Phone")
    license_number: Optional[str] = Field(None, description="Driver license number")
    is_active: bool = Field(True, description="Active/Inactive driver")

class Vehicle(BaseModel):
    """
    Fleet vehicles
    Collection name: "vehicle"
    """
    company_id: Optional[str] = Field(None, description="Owning company id")
    plate_number: str = Field(..., description="License plate")
    type: str = Field(..., description="Truck/Van/Bike/Ship/Air")
    capacity_kg: Optional[float] = Field(None, ge=0, description="Capacity in kilograms")
    volume_m3: Optional[float] = Field(None, ge=0, description="Capacity in cubic meters")
    status: str = Field("available", description="available|in_service|maintenance")

class Shipment(BaseModel):
    """
    Shipments being transported
    Collection name: "shipment"
    """
    company_id: Optional[str] = Field(None, description="Owning company id")
    customer_name: str = Field(..., description="Customer name")
    origin: str = Field(..., description="Pickup location")
    destination: str = Field(..., description="Drop-off location")
    cargo_details: Optional[str] = Field(None, description="Cargo description")
    weight_kg: Optional[float] = Field(None, ge=0, description="Weight in kg")
    volume_m3: Optional[float] = Field(None, ge=0, description="Volume in m3")
    tracking_code: str = Field(..., description="Public tracking code")
    status: str = Field("created", description="created|in_transit|delivered|cancelled")

class Quote(BaseModel):
    """
    Quote requests submitted by prospects
    Collection name: "quote"
    """
    name: str = Field(..., description="Requester name")
    email: str = Field(..., description="Requester email")
    phone: Optional[str] = Field(None, description="Requester phone")
    origin: str = Field(..., description="Pickup location")
    destination: str = Field(..., description="Drop-off location")
    date: Optional[str] = Field(None, description="Preferred pickup date (ISO date)")
    cargo_details: Optional[str] = Field(None, description="Cargo description")
    weight_kg: Optional[float] = Field(None, ge=0, description="Estimated weight in kg")
    volume_m3: Optional[float] = Field(None, ge=0, description="Estimated volume in m3")
    status: str = Field("new", description="new|reviewed|quoted|won|lost")

# ------------------ Example legacy schemas (kept) ------------------

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
