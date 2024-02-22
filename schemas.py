from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, constr


class UserBase(BaseModel):
    tg_username: str
    tg_first_name: str
    tg_last_name: str
    phone_number: Optional[str]
    email: Optional[str]


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str
    permissions: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class ClientBase(UserBase):
    first_name: str
    last_name: str
    gender: str
    birth_date: date


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class EmployeeBase(UserBase):
    first_name: str
    last_name: str
    gender: str
    birth_date: date
    role_id: int
    organization_id: int


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    role_id: int
    organization_id: int

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    name: str
    address: Optional[str]


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    name: str
    description: str


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int]


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True