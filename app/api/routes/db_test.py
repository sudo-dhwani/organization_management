from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db import get_db
from sqlalchemy.sql import text

router = APIRouter()
 
@router.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SHOW DATABASES;"))  # Ensure it's uppercase for MySQL
        databases = [row[0] for row in result.fetchall()]  # Extract database names
        return {"message": "Database connection is successful!", "databases": databases}
    except Exception as e:
        return {"error": str(e)}