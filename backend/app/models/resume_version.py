from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label = Column(String(255), nullable=False)
    file_url = Column(String(500))
    target_role = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="resume_versions")
    applications = relationship("Application", back_populates="resume_version")