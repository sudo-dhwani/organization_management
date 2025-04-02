from pydantic import BaseModel, EmailStr
from typing import Optional

class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str

class OrganizationResponse(BaseModel):
    id: int
    name: str
    database_url: Optional[str] = None

    class Config:
        orm_mode = True
