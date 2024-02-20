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

    tg_first_name: Mapped[str] = mapped_column(String(200))
    tg_last_name: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))
    birth_date: Mapped[datetime.date] = mapped_column(DATE)

    client: Mapped['Client'] = relationship(back_populates='user', lazy='selection')
    employees: Mapped[List['Employee']] = relationship(
        secondary=users_employees, back_populates='users', lazy='selection'
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    permissions: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum))

    employees: Mapped[List['Employee']] = relationship(back_populates='role', lazy='selection')


class Client(User):
    __tablename__ = "clients"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='client', lazy='selection')

    __table_args__ = (UniqueConstraint("user_id"),)


class Employee(User):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role: Mapped[Role] = relationship(back_populates='employees', lazy='selection')
    users: Mapped[List['User']] = relationship(
        secondary=users_employees, back_populates='employees', lazy='selection'
    )
    #
    __mapper_args__ = {
        'inherit_condition': id == User.id
    }
