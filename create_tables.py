from app.services.db import engine
from app.models.base import Base
from app.models.organization import Organization
from app.models.user import User

# Create tables in the database
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
