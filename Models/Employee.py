from typing import Optional

from pydantic import BaseModel


class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    email: Optional[str] = None
    address: Optional[str] = None
    organization_id: int = None
    organization: Optional["Organization"] = None
