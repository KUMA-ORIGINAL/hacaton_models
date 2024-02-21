import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Enum, ForeignKey, Table, Column, UniqueConstraint, DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class PermissionEnum(enum.Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'


users_employees = Table(
    'users_employees',
    Base.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('employees_id', ForeignKey('employees.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_username: Mapped[str] = mapped_column(String(200), unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(200), unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True)

    client: Mapped['Client'] = relationship(back_populates='user')
    employees: Mapped[List['Employee']] = relationship(
        secondary=users_employees, back_populates='users'
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    permissions: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum))

    employees: Mapped[List['Employee']] = relationship(back_populates='role')


class Client(User):
    __tablename__ = "clients"

    tg_first_name: Mapped[str] = mapped_column(String(200))
    tg_last_name: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))
    birth_date: Mapped[datetime.date] = mapped_column(DATE)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='client')

    __table_args__ = (UniqueConstraint("user_id"),)


class Employee(User):
    __tablename__ = "employees"

    tg_first_name: Mapped[str] = mapped_column(String(200))
    tg_last_name: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))
    birth_date: Mapped[datetime.date] = mapped_column(DATE)

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role: Mapped[Role] = relationship(back_populates='employees')
    users: Mapped[List['User']] = relationship(
        secondary=users_employees, back_populates='employees'
    )
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    organization: Mapped['Organization'] = relationship(back_populates='employees')

    __mapper_args__ = {
        'inherit_condition': id == User.id
    }


organizations_services = Table(
    'organizations_services',
    Base.metadata,
    Column('organizations_id', ForeignKey('organizations.id'), primary_key=True),
    Column('services_id', ForeignKey('services.id'), primary_key=True)
)

services_categories = Table(
    'services_categories',
    Base.metadata,
    Column('services_id', ForeignKey('services.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True)
)


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[Optional[str]] = mapped_column(String(200))

    employees: Mapped[List['Employee']] = relationship(back_populates='organization')
    services: Mapped[List['Service']] = relationship(
        secondary=organizations_services, back_populates='organizations'
    )


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str]

    organizations: Mapped[List['Organization']] = relationship(
        secondary=organizations_services, back_populates='services'
    )
    categories: Mapped[List['Category']] = relationship(
        secondary=services_categories, back_populates='services'
    )


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    parent_id: Mapped[int] = relationship(ForeignKey('categories.id'))
    parent: Mapped['Category'] = relationship(
        'Category', remote_side=[id], backref='subcategories'
    )
    services: Mapped[List['Service']] = relationship(
        secondary=services_categories, back_populates='categories'
    )
