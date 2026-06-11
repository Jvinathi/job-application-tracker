from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ApplicationCreate(BaseModel):
    company_name: str
    role_title: str
    platform: Optional[str] = None
    jd_url: Optional[str] = None
    notes: Optional[str] = None
    contact_id: Optional[int] = None
    resume_version_id: Optional[int] = None
    status: str = "applied"

class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    platform: Optional[str] = None
    jd_url: Optional[str] = None
    notes: Optional[str] = None
    contact_id: Optional[int] = None
    resume_version_id: Optional[int] = None
    status: Optional[str] = None
    kanban_order: Optional[int] = None

class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    role_title: str
    status: str
    platform: Optional[str]
    jd_url: Optional[str]
    notes: Optional[str]
    applied_on: datetime
    kanban_order: int
    contact_id: Optional[int]
    resume_version_id: Optional[int]
    updated_at: datetime

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: str
    kanban_order: Optional[int] = None