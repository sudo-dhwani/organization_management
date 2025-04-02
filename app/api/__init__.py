from fastapi import APIRouter
from app.api.routes import org, admin,db_test,user

api_router = APIRouter()
api_router.include_router(org.router, prefix="/org", tags=["Organization"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(db_test.router, prefix="/test", tags=["Database"]) 
