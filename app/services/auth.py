from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import User
from app.utils.token import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.services.db import get_db
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Fetch user from DB
        user = db.query(User).filter(User.email == email).first()
        if user is None or user.role != "admin":
            raise HTTPException(status_code=401, detail="Admin not found or invalid role")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
