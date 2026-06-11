from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    reminder_type = Column(String(50), default="follow_up")
    remind_at = Column(DateTime(timezone=True), nullable=False)
    is_sent = Column(Boolean, default=False)
    note = Column(Text)

    application = relationship("Application", back_populates="reminders")