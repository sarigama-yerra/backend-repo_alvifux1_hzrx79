import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import db, create_document, get_documents

app = FastAPI(title="Transport SaaS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Transport SaaS API running"}

# Health and DB test
@app.get("/test")
def test_database():
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# ---------------- Public lead capture: Quote ----------------
class QuoteRequest(BaseModel):
    name: str
    email: str
    phone: str | None = None
    origin: str
    destination: str
    date: str | None = None
    cargo_details: str | None = None
    weight_kg: float | None = None
    volume_m3: float | None = None

@app.post("/api/quotes")
def create_quote(quote: QuoteRequest):
    try:
        quote_id = create_document("quote", quote)
        return {"ok": True, "id": quote_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quotes")
def list_quotes():
    try:
        docs = get_documents("quote", limit=50)
        # stringify ObjectIds for safety
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return {"ok": True, "items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple public shipment tracking lookup by tracking_code
@app.get("/api/track/{tracking_code}")
def track_shipment(tracking_code: str):
    try:
        results = get_documents("shipment", {"tracking_code": tracking_code}, limit=1)
        if not results:
            raise HTTPException(status_code=404, detail="Tracking code not found")
        doc = results[0]
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return {"ok": True, "shipment": doc}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
