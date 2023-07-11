from typing import Optional

from sqlalchemy.orm import Session

from Models.Employee import Employee
from Models.Organization import Organization


def create_organization(db: Session, organization: Organization):
    new_organization = Organization(**organization.dict())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization


def create_employee(db: Session, employee: Employee) -> Employee:
    organization = db.query(Organization).filter(Organization._id == employee.organization_id).first()
    if organization is None:
        raise ValueError("Organization not found")
    db_employee = EmployeeDB(**employee.dict())
    db_employee.organization = organization
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return Employee(**db_employee.dict())


def retrieve_all_organizations(db: Session):
    return db.query(Organization).all()


def get_organization(db: Session, organization_id: str) -> Optional[Organization]:
    return db.query(Organization).filter(Organization._id == organization_id).first()


def update_organization_data(db: Session, organization: Organization) -> Organization:
    db_organization = db.query(Organization).filter(Organization._id == organization._id).first()
    if db_organization:
        for key, value in organization.dict().items():
            setattr(db_organization, key, value)
        db.commit()
        db.refresh(db_organization)
        return Organization(**db_organization.dict())
    raise ValueError("Organization not found")


def get_all_employees(db: Session):
    return db.query(Employee).all()
