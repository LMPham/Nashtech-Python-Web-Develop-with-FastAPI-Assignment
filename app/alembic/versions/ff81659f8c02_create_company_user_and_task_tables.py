"""Create Company, User, and Task tables

Revision ID: ff81659f8c02
Revises: 
Create Date: 2024-09-05 20:02:21.257361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from entities.company import CompanyMode
from entities.task import TaskStatus


# revision identifiers, used by Alembic.
revision: str = 'ff81659f8c02'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('companies',
    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
    sa.Column('name', sa.String, nullable=True),
    sa.Column('description', sa.String, nullable=True),
    sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.PENDING),
    sa.Column('rating', sa.SmallInteger, nullable=False, default=0),
    sa.Column('created_at', sa.Time, nullable=False),
    sa.Column('updated_at', sa.Time, nullable=False),
    )
    op.create_table('users',
    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
    sa.Column('email', sa.String, nullable=True),
    sa.Column('username', sa.String, nullable=True),
    sa.Column('first_name', sa.String, nullable=False),
    sa.Column('last_name', sa.String, nullable=False),
    sa.Column('hashed_password', sa.String, nullable=False),
    sa.Column('is_active', sa.Boolean, nullable=True, default=True),
    sa.Column('is_admin', sa.Boolean, nullable=True, default=False),
    sa.Column('company_id', sa.UUID, nullable=False),
    sa.Column('created_at', sa.Time, nullable=False),
    sa.Column('updated_at', sa.Time, nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('tasks',
    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
    sa.Column('summary', sa.String, nullable=True),
    sa.Column('description', sa.String, nullable=True),
    sa.Column('status', sa.Enum(TaskStatus), nullable=True, default=TaskStatus.CREATED),
    sa.Column('priority', sa.SmallInteger, nullable=True),
    sa.Column('user_id', sa.UUID, nullable=False),
    sa.Column('created_at', sa.Time, nullable=False),
    sa.Column('updated_at', sa.Time, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('companies')
    op.execute("DROP TYPE taskstatus;")
    op.execute("DROP TYPE companymode;")
