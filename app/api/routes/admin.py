from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import get_current_admin

from app.schemas.auth import AdminLogin
from app.utils.hashing import pwd_context
from app.utils.token import create_access_token


router = APIRouter()

@router.post("/login")
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    # Fetch user from DB
    user = db.query(User).filter(User.email == login_data.email, User.role == "admin").first()
    
    if not user or not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate token
    token = create_access_token({"sub": user.email, "role": "admin"})

    return {"access_token": token, "token_type": "bearer"}

@router.post("/user/create")
def create_user(user_data: UserCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    # Ensure the logged-in user is an admin
    # Here you should include authorization checks to make sure that the logged-in user is an admin.
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # Create new user
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        role=user_data.role,
        organization_id=1  # Use the appropriate organization ID (This is hardcoded for now)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": f"User {new_user.email} created successfully!"}

@router.get("/users")
def get_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    # Fetch all users for the logged-in admin's organization
    print(admin)
    users = db.query(User).filter(User.organization_id == admin.organization_id).all()
    return {"users": users}