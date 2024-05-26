"""first_migration

Revision ID: 60aef39934cd
Revises: 
Create Date: 2024-05-23 22:14:26.488780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60aef39934cd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('description', sa.Text, nullable=True)
    )

    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('description', sa.Text, nullable=True)
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('status.id'), nullable=False),
        sa.Column('description', sa.Text, nullable=True)
    )

    op.create_table(
        'executors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('surname', sa.String(30), nullable=False),
        sa.Column('email', sa.String(30), nullable=False),
        sa.Column('login', sa.String(30), nullable=False),
        sa.Column('password', sa.String(30), nullable=False)
    )

    op.create_table(
        'task_executors',
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id'), primary_key=True),
        sa.Column('executor_id', sa.Integer, sa.ForeignKey('executors.id'), primary_key=True)
    )

    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id'), nullable=False)
    )

    op.create_table(
        'files',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('path', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id'), nullable=False)
    )


def downgrade():
    op.drop_table('files')
    op.drop_table('comments')
    op.drop_table('task_executors')
    op.drop_table('executors')
    op.drop_table('tasks')
    op.drop_table('status')
    op.drop_table('projects')
