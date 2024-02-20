"""init alembic

Revision ID: af10ab8fa78c
Revises: 
Create Date: 2024-02-21 04:36:27.958369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af10ab8fa78c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('permissions', sa.Enum('create', 'read', 'update', 'delete', name='permissionenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_username', sa.String(length=200), nullable=False),
    sa.Column('phone_number', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('tg_first_name', sa.String(length=200), nullable=False),
    sa.Column('tg_last_name', sa.String(length=200), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=200), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', 'other', name='genderenum'), nullable=False),
    sa.Column('birth_date', sa.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('tg_username')
    )
    op.create_table('clients',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_employees',
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('employees_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employees_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('users_id', 'employees_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_employees')
    op.drop_table('employees')
    op.drop_table('clients')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
