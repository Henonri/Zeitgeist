from fastapi import FastAPI
from pydantic import BaseModel
from backend.db import init_db, SessionLocal
from backend import models
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    print("✅ App startup: initializing DB")
    init_db()

@app.get("/")
def ping():
    return {"ping": "pong"}

# --------------------------
# USERS
# --------------------------

class UserCreate(BaseModel):
    email: str
    name: str
    account_type: str
    business_type: str
    location: str
    wants_notifications: bool = True

@app.post("/register")
def register_user(user: UserCreate):
    print("🚀 Received registration for:", user.email)
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == user.email).first()
        if existing:
            return {"error": "User already exists."}

        new_user = models.User(
            email=user.email,
            name=user.name,
            account_type=user.account_type,
            business_type=user.business_type,
            location=user.location,
            wants_notifications=user.wants_notifications,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered", "id": new_user.id}
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
        return {"error": "Internal server error"}
    finally:
        db.close()

@app.get("/users")
def list_users():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        return [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "account_type": u.account_type,
                "business_type": u.business_type,
                "location": u.location,
                "wants_notifications": u.wants_notifications,
            }
            for u in users
        ]
    finally:
        db.close()

# --------------------------
# TRENDS
# --------------------------

from fastapi import Request

@app.get("/trends/enhanced")
def get_enhanced_trends(request: Request):
    business_type = request.query_params.get("business_type", "").lower()

    all_trends = [
        {
            "title": "LaBubus TikTok Sound",
            "hashtags": ["#labubus", "#viral", "#sound"],
            "platform": "TikTok",
            "views_today": 1200000,
            "views_per_hour": 83000,
            "llm_summary": "A chaotic meme sound going viral for comedic timing.",
            "reuse_suggestion": "Use this to exaggerate your product’s ‘before and after’ transformation.",
            "audience": ["influencer", "brand", "content creator"]
        },
        {
            "title": "NYC Café Review Trend",
            "hashtags": ["#coffeereview", "#nyceats", "#aesthetic"],
            "platform": "Instagram",
            "views_today": 430000,
            "views_per_hour": 19000,
            "llm_summary": "Instagrammers reviewing coffee spots in a minimal, cozy style.",
            "reuse_suggestion": "Film a 10-second walkthrough of your café with aesthetic lighting and this audio.",
            "audience": ["coffee shop", "bakery", "restaurant", "café"]
        },
        {
            "title": "Before/After Reels",
            "hashtags": ["#beforeafter", "#reels", "#dayinmylife"],
            "platform": "Instagram",
            "views_today": 850000,
            "views_per_hour": 65000,
            "llm_summary": "This format compares moments: ‘before work vs after coffee’, etc.",
            "reuse_suggestion": "Show how your product/service improves someone’s day in a 2-part split.",
            "audience": ["brand", "influencer", "café", "fitness coach"]
        }
    ]

    personalized = [
        trend for trend in all_trends
        if business_type in trend["audience"]
    ]

    return personalized or all_trends

