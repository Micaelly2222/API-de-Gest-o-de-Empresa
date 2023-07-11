from fastapi import HTTPException
from sqlalchemy.orm import Session

from Models.Employee import Employee
from Models.Organization import Organization


def retrieve_all_organizations(db: Session):
    return db.query(Organization).all()


def get_all_employees(db: Session):
    organizations = retrieve_all_organizations(db)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizações não encontradas.")

    employees = db.query(Employee).all()

    for employee in employees:
        employee.organization = next((org for org in organizations if org.id == employee.organization_id), None)

    return employees