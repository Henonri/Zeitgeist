from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    account_type = Column(String)
    business_type = Column(String)
    location = Column(String)
    wants_notifications = Column(Boolean, default=True)

class Trend(Base):
    __tablename__ = "trends"
    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(String)
    platform = Column(String)
    description = Column(String)
    growth_rate = Column(Float)
    trend_category = Column(String)
    country = Column(String)
    date_detected = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trend_id = Column(Integer, ForeignKey("trends.id"))
    sent_at = Column(DateTime, default=datetime.utcnow)
    was_clicked = Column(Boolean, default=False)
