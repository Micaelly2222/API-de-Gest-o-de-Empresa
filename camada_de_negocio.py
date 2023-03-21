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
        raise ValueError("Token inválido")
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# recupera registros

def retrieve_all_organization(db: Session):
    return db.query(Organization).all()


def get_all_employees(db: Session):
    return db.query(Employee).all()
