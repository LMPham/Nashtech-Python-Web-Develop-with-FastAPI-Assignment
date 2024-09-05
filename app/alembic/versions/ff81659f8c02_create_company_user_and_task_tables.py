"""Create Company, User, and Task tables

Revision ID: ff81659f8c02
Revises: 
Create Date: 2024-09-05 20:02:21.257361

"""
import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from entities.company import CompanyMode
from entities.user import get_password_hash
from entities.task import TaskStatus


# revision identifiers, used by Alembic.
revision: str = 'ff81659f8c02'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    companies_table = op.create_table('companies',
    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
    sa.Column('name', sa.String, nullable=True),
    sa.Column('description', sa.String, nullable=True),
    sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.PENDING),
    sa.Column('rating', sa.SmallInteger, nullable=False, default=0),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    users_table = op.create_table('users',
    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
    sa.Column('email', sa.String, nullable=False),
    sa.Column('username', sa.String, nullable=False),
    sa.Column('first_name', sa.String, nullable=False),
    sa.Column('last_name', sa.String, nullable=False),
    sa.Column('hashed_password', sa.String, nullable=False),
    sa.Column('is_active', sa.Boolean, nullable=True, default=True),
    sa.Column('is_admin', sa.Boolean, nullable=True, default=False),
    sa.Column('company_id', sa.UUID, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    tasks_table = op.create_table('tasks',
    sa.Column('id', sa.UUID, nullable=False, primary_key=True),
    sa.Column('summary', sa.String, nullable=True),
    sa.Column('description', sa.String, nullable=True),
    sa.Column('status', sa.Enum(TaskStatus), nullable=True, default=TaskStatus.CREATED),
    sa.Column('priority', sa.SmallInteger, nullable=True),
    sa.Column('user_id', sa.UUID, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    
    # Seed data
    companies = [
        {'id': uuid.uuid4(), 'name': 'TechCorp', 'description': 'A leading technology company.', 'mode': CompanyMode.STARTUP, 'rating': 4, 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'name': 'Innovate Inc.', 'description': 'Innovating the future.', 'mode': CompanyMode.ESTABLISHED, 'rating': 5, 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'name': 'GreenSolutions', 'description': 'Eco-friendly solutions provider.', 'mode': CompanyMode.PENDING, 'rating': 3, 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'name': 'Fintech Ltd.', 'description': 'Financial technology experts.', 'mode': CompanyMode.CLOSED, 'rating': 2, 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'name': 'HealthPlus', 'description': 'Healthcare and wellness company.', 'mode': CompanyMode.ESTABLISHED, 'rating': 4, 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)}
    ]
    users = [
        {'id': uuid.uuid4(), 'email': 'alice.johnson@techcorp.com', 'username': 'alice.johnson', 'first_name': 'Alice', 'last_name': 'Johnson', 'hashed_password': get_password_hash("alice.johnson"), 'is_active': True, 'is_admin': False, 'company_id': companies[0]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'bob.smith@techcorp.com', 'username': 'bob.smith', 'first_name': 'Bob', 'last_name': 'Smith', 'hashed_password': get_password_hash("bob.smith"), 'is_active': True, 'is_admin': True, 'company_id': companies[0]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'carol.williams@innovate.com', 'username': 'carol.williams', 'first_name': 'Carol', 'last_name': 'Williams', 'hashed_password': get_password_hash("carol.williams"), 'is_active': True, 'is_admin': False, 'company_id': companies[1]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'dave.brown@innovate.com', 'username': 'dave.brown', 'first_name': 'Dave', 'last_name': 'Brown', 'hashed_password': get_password_hash("dave.brown"), 'is_active': True, 'is_admin': True, 'company_id': companies[1]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'eve.davis@greensolutions.com', 'username': 'eve.davis', 'first_name': 'Eve', 'last_name': 'Davis', 'hashed_password': get_password_hash("eve.davis"), 'is_active': True, 'is_admin': False, 'company_id': companies[2]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'frank.miller@greensolutions.com', 'username': 'frank.miller', 'first_name': 'Frank', 'last_name': 'Miller', 'hashed_password': get_password_hash("frank.miller"), 'is_active': True, 'is_admin': True, 'company_id': companies[2]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'grace.wilson@fintech.com', 'username': 'grace.wilson', 'first_name': 'Grace', 'last_name': 'Wilson', 'hashed_password': get_password_hash("grace.wilson"), 'is_active': True, 'is_admin': False, 'company_id': companies[3]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'heidi.moore@fintech.com', 'username': 'heidi.moore', 'first_name': 'Heidi', 'last_name': 'Moore', 'hashed_password': get_password_hash("heidi.moore"), 'is_active': True, 'is_admin': True, 'company_id': companies[3]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'ivan.taylor@healthplus.com', 'username': 'ivan.taylor', 'first_name': 'Ivan', 'last_name': 'Taylor', 'hashed_password': get_password_hash("ivan.taylor"), 'is_active': True, 'is_admin': False, 'company_id': companies[4]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'email': 'judy.anderson@healthplus.com', 'username': 'judy.anderson', 'first_name': 'Judy', 'last_name': 'Anderson', 'hashed_password': get_password_hash("judy.anderson"), 'is_active': True, 'is_admin': True, 'company_id': companies[4]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)}
    ]
    tasks = [
        {'id': uuid.uuid4(), 'summary': 'Complete tech setup', 'description': 'Set up the new tech equipment.', 'status': TaskStatus.CREATED, 'priority': 1, 'user_id': users[0]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Prepare demo', 'description': 'Prepare for the upcoming product demo.', 'status': TaskStatus.CANCELLED, 'priority': 2, 'user_id': users[0]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Code review', 'description': 'Review the latest code submissions.', 'status': TaskStatus.STARTED, 'priority': 3, 'user_id': users[1]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Market analysis', 'description': 'Conduct market analysis for the new product.', 'status': TaskStatus.COMPLETED, 'priority': 2, 'user_id': users[2]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Update website', 'description': 'Update the company website with new features.', 'status': TaskStatus.CREATED, 'priority': 1, 'user_id': users[2]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Submit report', 'description': 'Submit the quarterly financial report.', 'status': TaskStatus.CANCELLED, 'priority': 2, 'user_id': users[4]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Plan event', 'description': 'Plan the annual company event.', 'status': TaskStatus.STARTED, 'priority': 3, 'user_id': users[4]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'HR meeting', 'description': 'Attend the HR department meeting.', 'status': TaskStatus.COMPLETED, 'priority': 1, 'user_id': users[6]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Client presentation', 'description': 'Prepare and deliver client presentation.', 'status': TaskStatus.CANCELLED, 'priority': 3, 'user_id': users[6]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)},
        {'id': uuid.uuid4(), 'summary': 'Data analysis', 'description': 'Analyze the customer feedback data.', 'status': TaskStatus.CREATED, 'priority': 2, 'user_id': users[7]['id'], 'created_at': datetime.now(timezone.utc), 'updated_at': datetime.now(timezone.utc)}
    ]
    op.bulk_insert(companies_table, companies)
    op.bulk_insert(users_table, users)
    op.bulk_insert(tasks_table, tasks)


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('companies')
    op.execute("DROP TYPE taskstatus;")
    op.execute("DROP TYPE companymode;")
    