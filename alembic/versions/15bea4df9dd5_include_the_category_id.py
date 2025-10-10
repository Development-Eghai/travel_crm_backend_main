"""include the category_id

Revision ID: 15bea4df9dd5
Revises: 2be649dcd6f4
Create Date: 2025-10-09 18:09:32.903323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '15bea4df9dd5'
down_revision: Union[str, None] = '2be649dcd6f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new column
    op.add_column('trips', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_trips_category', 'trips', 'categories', ['category_id'], ['id']
    )

    # Drop old column safely if exists
    with op.batch_alter_table('trips') as batch_op:
        batch_op.drop_column('categories')

def downgrade():
    with op.batch_alter_table('trips') as batch_op:
        batch_op.add_column(sa.Column('categories', sa.Text()))
    op.drop_constraint('fk_trips_category', 'trips', type_='foreignkey')
    op.drop_column('trips', 'category_id')
