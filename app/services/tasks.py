from app.models.organization import Organization
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.organization import OrganizationCreate, OrganizationResponse

async def create_organization_task(org_data: OrganizationCreate, db: AsyncSession):
    new_org = Organization(name=org_data.name, db_url=f"mysql://root:password@localhost/{org_data.name}_db")
    db.add(new_org)
    await db.commit()
    await db.refresh(new_org)
    return OrganizationResponse(id=new_org.id, name=new_org.name, db_url=new_org.db_url)
