from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    resume_version_id = Column(Integer, ForeignKey("resume_versions.id"), nullable=True)

    company_name = Column(String(255), nullable=False)
    role_title = Column(String(255), nullable=False)
    status = Column(String(50), default="applied")
    platform = Column(String(100))
    jd_url = Column(String(500))
    notes = Column(Text)
    applied_on = Column(DateTime(timezone=True), server_default=func.now())
    kanban_order = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="applications")
    contact = relationship("Contact", back_populates="applications")
    resume_version = relationship("ResumeVersion", back_populates="applications")
    reminders = relationship("Reminder", back_populates="application", cascade="all, delete")