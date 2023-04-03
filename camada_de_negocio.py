from sqlalchemy.orm import Session

from Models import Organization, Employee


def create_organization(db: Session, organization: Organization):
    new_organization = Organization(**organization.dict())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization


def create_employee(db: Session, employee: Employee):
    organization = db.query(Organization).filter(Organization.id == employee.organization_id).first()
    if not organization:
        raise HTTPException(status_code=401, detail="Organização não encontrada.")
    employee_dict = employee.dict(exclude={'organization_id'})
    new_employee = Employee(**employee_dict)
    new_employee.organization_id = employee.organization_id
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    new_employee.organization = organization
    return new_employee


# recupera registros

def retrieve_all_organizations(db: Session):
    return db.query(Organization).all()


def get_all_employees(db: Session):
    organizations = db.query(Organization).all()
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizações não encontradas.")
    employees = db.query(Employee).all()
    for employee in employees:
        employee.organization = next((org for org in organizations if org.id == employee.organization_id), None)
    return employees
