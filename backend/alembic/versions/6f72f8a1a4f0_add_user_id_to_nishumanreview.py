"""Add user_id to NISHumanReview

Revision ID: 6f72f8a1a4f0
Revises: 0bfa54c6abba
Create Date: 2026-06-07 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6f72f8a1a4f0'
down_revision: Union[str, None] = '0bfa54c6abba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('nis_human_reviews', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key('fk_nis_human_reviews_user_id', 'nis_human_reviews', 'nis_users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_nis_human_reviews_user_id', 'nis_human_reviews', type_='foreignkey')
    op.drop_column('nis_human_reviews', 'user_id')
