from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationCreate
from app.utils.hashing import hash_password  # Utility to hash passwords
from app.schemas.organization import OrganizationResponse

router = APIRouter()

@router.post("/create")
def create_organization(org_data: OrganizationCreate, db: Session = Depends(get_db)):
    # Check if organization already exists
    existing_org = db.query(Organization).filter(Organization.name == org_data.organization_name).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="Organization already exists")

    # Create new organization
    new_org = Organization(name=org_data.organization_name)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    # Create admin user
    hashed_password = hash_password(org_data.password)
    admin_user = User(email=org_data.email, password=hashed_password, organization_id=new_org.id, role="admin")
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return {"message": "Organization and admin created successfully!", "organization_id": new_org.id}
@router.get("/get", response_model=OrganizationResponse)
def get_organization(name: str, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.name == name).first()
    
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization