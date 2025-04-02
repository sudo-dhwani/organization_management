from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    role: str  # This can be 'admin' or 'user'
