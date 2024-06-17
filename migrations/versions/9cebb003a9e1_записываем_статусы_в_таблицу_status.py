"""Записываем статусы в таблицу status

Revision ID: 9cebb003a9e1
Revises: 9ceae42b48f4
Create Date: 2024-06-17 21:23:18.858450

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session
from app.models import Status

# revision identifiers, used by Alembic.
revision: str = '9cebb003a9e1'
down_revision: Union[str, None] = '9ceae42b48f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    statuses = [
        Status(name='New', description='Task has just started'),
        Status(name='In progress', description='Task is being in progress'),
        Status(name='Done', description='Task is done')
    ]

    session.add_all(statuses)
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(Status).delete()
    session.commit()
