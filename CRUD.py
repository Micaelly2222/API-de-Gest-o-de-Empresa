from sqlalchemy.orm import Session

from Models import Organization, Employee


# Criando registros
def create_organization(db: Session, organization: Organization):
    new_organization = Organization(**organization.dict())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization


def create_employee(db: Session, employee: Employee):
    organization = db.query(Organization).filter(Organization.id == employee.organization_id).first()
    if not organization:
        raise ValueError("Organização não encontrada.")
    employee_dict = employee.dict(exclude={'organization_id'})
    new_employee = Employee(**employee_dict)
    new_employee.organization_id = employee.organization_id
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    new_employee.organization = organization
    return new_employee


# Recuperando registros

def retrieve_all_organizations(db: Session):
    return db.query(Organization).all()


def get_organization(db: Session, organization_id: int):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def update_organization_data(db: Session, organization: Organization):
    db_organization = db.query(Organization).filter(Organization.id == organization.id).first()
    db_organization.name = organization.name
    db_organization.address = organization.address
    db.commit()
    db.refresh(db_organization)
    return db_organization


def get_all_employees(db: Session):
    return db.query(Employee).all()
