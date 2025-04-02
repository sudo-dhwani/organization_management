from app.models.organization import Organization
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.core.config import settings  # Import settings

async def create_organization_task(org_data: OrganizationCreate, db: AsyncSession):
    db_url = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{org_data.name}_db"
    new_org = Organization(name=org_data.name, db_url=db_url)
    db.add(new_org)
    await db.commit()
    await db.refresh(new_org)
    return OrganizationResponse(id=new_org.id, name=new_org.name, db_url=new_org.db_url)
