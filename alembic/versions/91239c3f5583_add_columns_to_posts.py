"""add columns to posts

Revision ID: 91239c3f5583
Revises: 57ec023af639
Create Date: 2022-03-09 21:09:05.495543

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = '91239c3f5583'
down_revision = '57ec023af639'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
