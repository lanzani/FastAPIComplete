"""Add content column to posts table

Revision ID: 5b5d9aae474d
Revises: 2763983575ce
Create Date: 2022-03-09 20:44:21.170101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b5d9aae474d'
down_revision = '2763983575ce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade():
    op.drop_column("posts", "content")
