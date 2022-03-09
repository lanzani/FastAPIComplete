"""create posts table

Revision ID: 2763983575ce
Revises: 
Create Date: 2022-03-09 20:16:14.191122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2763983575ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))


def downgrade():
    op.drop_table("posts")
