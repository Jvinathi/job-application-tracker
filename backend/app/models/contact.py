from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(255))
    email = Column(String(255))
    linkedin_url = Column(String(500))
    company = Column(String(255))

    user = relationship("User", back_populates="contacts")
    applications = relationship("Application", back_populates="contact")